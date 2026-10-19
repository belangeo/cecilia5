"""Launcher and installed-resource checks without GUI/audio dependencies."""

import importlib.util
from collections import defaultdict
import os
from pathlib import Path
import runpy
import sys
import tempfile
import types
import unittest
import xmlrpc.client
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = os.getcwd()
        self.addCleanup(os.chdir, self.cwd)
        os.chdir(self.temp.name)
        package = types.ModuleType('Resources')
        package.__path__ = [str(ROOT / 'Resources')]
        images = types.ModuleType('Resources.images')
        images.catalog = defaultdict(lambda: None)
        self.modules = {'Resources': package, 'Resources.images': images}
        self.module_patch = patch.dict(sys.modules, self.modules)
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)
        home_patch = patch('os.path.expanduser', return_value=self.temp.name)
        home_patch.start()
        self.addCleanup(home_patch.stop)

    def constants(self):
        spec = importlib.util.spec_from_file_location(
            'Resources.constants', ROOT / 'Resources/constants.py')
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_resources_are_independent_of_working_directory(self):
        constants = self.constants()
        self.assertEqual(Path(constants.RESOURCES_PATH), ROOT / 'Resources')
        self.assertTrue(Path(constants.SPLASH_FILE_PATH).is_file())
        self.assertTrue((Path(constants.MODULES_PATH) / 'Dynamics/Degrade.c5').is_file())
        self.assertEqual(os.getcwd(), self.temp.name)

    def test_mac_bundle_resources_follow_executable(self):
        with patch.object(sys, 'platform', 'darwin'), \
                patch.object(sys, 'frozen', 'macosx_app', create=True), \
                patch.object(sys, 'executable', '/Applications/Cecilia5.app/Contents/MacOS/Cecilia5'), \
                patch.dict(os.environ), patch('shutil.copytree'):
            constants = self.constants()
        self.assertEqual(constants.RESOURCES_PATH, '/Applications/Cecilia5.app/Contents/Resources')
        self.assertEqual(constants.AUDIO_DRIVERS, ['portaudio'])

    def test_main_launches_and_preserves_relative_file_argument(self):
        self.constants()
        wx = types.ModuleType('wx')
        app = Mock()

        class App:
            def __init__(self, **kwargs):
                self.SetTopWindow = app.SetTopWindow
                self.MainLoop = app.MainLoop

        wx.App = App
        wx.Log = Mock()
        wx.Display = Mock(side_effect=RuntimeError('No display'))
        variables = types.ModuleType('Resources.Variables')
        variables.loadBitmaps = Mock()
        audio = types.ModuleType('Resources.audio')
        audio.AudioServer = Mock()
        mainframe = types.ModuleType('Resources.CeciliaMainFrame')
        mainframe.CeciliaMainFrame = Mock()
        lib = types.ModuleType('Resources.CeciliaLib')
        lib.setVar = Mock()
        lib.getVar = Mock(return_value=False)
        lib.queryAudioMidiDrivers = Mock()
        lib.ensureNFD = lambda path: path
        splash = types.ModuleType('Resources.splash')
        splash.CeciliaSplashScreen = Mock(side_effect=lambda *args, **kwargs: kwargs['callback']())
        Path('example.c5').touch()
        with patch.dict(sys.modules, {
            'wx': wx, 'Resources.Variables': variables, 'Resources.audio': audio,
            'Resources.CeciliaMainFrame': mainframe, 'Resources.CeciliaLib': lib,
            'Resources.splash': splash,
        }), patch.object(sys, 'argv', ['cecilia', 'example.c5']):
            launcher = runpy.run_path(str(ROOT / 'Cecilia5.py'))
            audio.AudioServer.assert_not_called()
            launcher['main']()
        frame = mainframe.CeciliaMainFrame.return_value
        frame.onOpen.assert_called_once_with('example.c5')
        app.SetTopWindow.assert_called_once_with(frame)
        app.MainLoop.assert_called_once_with()
        variables.loadBitmaps.assert_called_once_with()
        self.assertEqual(os.getcwd(), self.temp.name)

    def test_windows_bundle_resources_follow_executable(self):
        with patch.object(sys, 'platform', 'win32'), \
                patch.object(sys, 'frozen', True, create=True), \
                patch.object(sys, 'executable', '/standalone/Cecilia5.exe'), \
                patch('shutil.copytree'):
            constants = self.constants()
        self.assertEqual(constants.RESOURCES_PATH, '/standalone/Resources')

    def test_factory_presets_are_installed_once(self):
        constants = self.constants()
        factory = ROOT / 'presets'
        installed = Path(constants.PRESETS_PATH)
        self.assertEqual(Path(constants.PRESETS_VERSION_FILE).read_text().strip(), constants.APP_VERSION)
        originals = sorted(path.relative_to(factory) for path in factory.glob('*/*'))
        self.assertEqual(len(originals), 105)
        self.assertEqual(sorted(path.relative_to(installed) for path in installed.glob('*/*')), originals)
        for relative in originals:
            self.assertEqual((installed / relative).read_bytes(), (factory / relative).read_bytes())
            data = xmlrpc.client.loads((installed / relative).read_bytes())[0][0]
            self.assertTrue(all(isinstance(key, str) for key in data['plugins']))

        edited = installed / originals[0]
        edited.write_text('user-edited preset')
        deleted = installed / originals[1]
        deleted.unlink()
        custom = installed / 'custom module'
        custom.mkdir()
        (custom / 'my preset').write_text('custom')
        with patch('shutil.copytree') as copy:
            self.constants()
        copy.assert_not_called()
        self.assertEqual(edited.read_text(), 'user-edited preset')
        self.assertFalse(deleted.exists())
        self.assertEqual((custom / 'my preset').read_text(), 'custom')

    def test_factory_presets_refresh_when_version_is_missing_or_outdated(self):
        constants = self.constants()
        installed = Path(constants.PRESETS_PATH)
        version = Path(constants.PRESETS_VERSION_FILE)
        factory = next((ROOT / 'presets').glob('*/*'))
        target = installed / factory.relative_to(ROOT / 'presets')
        custom = target.parent / 'my custom preset'
        custom.write_text('custom')
        for old_version in (None, '5.4.0'):
            with self.subTest(version=old_version):
                if old_version is None:
                    version.unlink()
                else:
                    version.write_text(old_version)
                target.write_text('old preset')
                self.constants()
                self.assertEqual(target.read_bytes(), factory.read_bytes())
                self.assertEqual(custom.read_text(), 'custom')
                self.assertEqual(version.read_text().strip(), constants.APP_VERSION)

    def test_failed_preset_refresh_does_not_update_version(self):
        constants = self.constants()
        version = Path(constants.PRESETS_VERSION_FILE)
        version.write_text('5.4.0')
        with patch('shutil.copytree', side_effect=OSError('copy failed')):
            with self.assertRaises(OSError):
                self.constants()
        self.assertEqual(version.read_text(), '5.4.0')
