"""Desktop registration checks without GUI/audio dependencies."""

import base64
import json
import os
from pathlib import Path
import plistlib
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from Resources import desktop


def macos_tool(command, **kwargs):
    """Stand in for the macOS compiler/signing tools on other platforms."""
    if command[0] == '/usr/bin/osacompile':
        contents = Path(command[2]) / 'Contents'
        (contents / 'MacOS').mkdir(parents=True)
        (contents / 'Resources').mkdir()
        (contents / 'MacOS/applet').write_bytes(b'native applet placeholder')
        (contents / 'Info.plist').write_bytes(plistlib.dumps({
            'CFBundleExecutable': 'applet', 'CFBundlePackageType': 'APPL',
        }))
    return subprocess.CompletedProcess(command, 0, '', '')


class DesktopTests(unittest.TestCase):
    def test_registration_creates_and_refreshes_entry(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'linux'), \
                patch.object(desktop.sys, 'executable', '/tmp/my venv/bin/python'), \
                patch.object(Path, 'home', return_value=Path(directory)):
            destination = desktop.register_desktop()
            self.assertEqual(destination, Path(directory) / '.local/share/applications/cecilia.desktop')
            content = destination.read_text(encoding='utf-8')
            self.assertIn('Type=Application\n', content)
            self.assertIn('Exec="/tmp/my venv/bin/python" "-c" "from Cecilia5 import main; main()" %f\n', content)
            self.assertIn('Terminal=false\n', content)
            icon = next(line[5:] for line in content.splitlines() if line.startswith('Icon='))
            self.assertTrue(Path(icon).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
            destination.write_text('outdated')
            desktop.register_desktop()
            self.assertEqual(destination.read_text(), content)

    def test_exec_argument_escaping(self):
        self.assertEqual(desktop._quote_argument('/a b/%f'), '"/a b/%%f"')
        self.assertEqual(desktop._quote_argument('$`"\\'), '"\\\\$\\\\`\\\\"\\\\\\\\"')

    def test_windows_registration_uses_environment_and_ico(self):
        with tempfile.TemporaryDirectory(prefix="Cecilia's ") as directory:
            interpreter = Path(directory) / 'python.exe'
            pythonw = interpreter.with_name('pythonw.exe')
            pythonw.touch()
            destination = Path(directory) / 'Programs' / 'Cecilia5.lnk'
            completed = subprocess.CompletedProcess([], 0, str(destination) + '\n', '')
            with patch.object(desktop.sys, 'platform', 'win32'), \
                    patch.object(desktop.sys, 'executable', str(interpreter)), \
                    patch.object(Path, 'home', return_value=Path(directory)), \
                    patch.object(desktop.subprocess, 'run', return_value=completed) as run:
                self.assertEqual(desktop.register_desktop(), destination)
                command = run.call_args.args[0]
                self.assertEqual(command[:4], [
                    'powershell.exe', '-NoProfile', '-NonInteractive', '-EncodedCommand'])
                script = base64.b64decode(command[4]).decode('utf-16-le')
                self.assertIn("[Environment]::GetFolderPath('Programs')", script)
                self.assertIn("Join-Path $programs 'Cecilia5.lnk'", script)
                self.assertIn('$shortcut.TargetPath = ' + desktop._powershell_string(pythonw), script)
                self.assertIn("$shortcut.Arguments = '-c \"from Cecilia5 import main; main()\"'", script)
                self.assertIn('$shortcut.WorkingDirectory = ' + desktop._powershell_string(directory), script)
                icon = Path(desktop.__file__).resolve().with_name('Cecilia5.ico')
                self.assertTrue(icon.is_file())
                self.assertIn('$shortcut.IconLocation = ' + desktop._powershell_string(str(icon) + ',0'), script)
                self.assertIn('$shortcut.Save()', script)

    def test_powershell_literal_escaping(self):
        self.assertEqual(desktop._powershell_string("C:/O'Brien/$home`/é"),
                         "'C:/O''Brien/$home`/é'")

    def test_windows_missing_interpreter_returns_error_without_creating_shortcut(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'win32'), \
                patch.object(desktop.sys, 'executable', str(Path(directory) / 'python.exe')), \
                patch.object(desktop.subprocess, 'run') as run:
            self.assertEqual(desktop.main(), 1)
            run.assert_not_called()

    def test_windows_powershell_failures_return_error(self):
        failures = [FileNotFoundError('powershell.exe'),
                    subprocess.CalledProcessError(1, 'powershell.exe', stderr='access denied')]
        for failure in failures:
            with self.subTest(failure=failure), \
                    patch.object(desktop.sys, 'platform', 'win32'), \
                    patch.object(Path, 'is_file', return_value=True), \
                    patch.object(desktop.subprocess, 'run', side_effect=failure):
                self.assertEqual(desktop.main(), 1)

    def test_macos_registration_creates_and_refreshes_bundle(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(desktop, '_application_version', return_value='9.8.7'), \
                patch.object(Path, 'home', return_value=Path(directory)), \
                patch.object(desktop.subprocess, 'run', side_effect=macos_tool):
            destination = desktop.register_desktop()
            self.assertEqual(destination, Path(directory) / 'Applications/Cecilia5.app')
            contents = destination / 'Contents'
            plist_path = contents / 'Info.plist'
            info = plistlib.loads(plist_path.read_bytes())
            self.assertEqual(info['CFBundlePackageType'], 'APPL')
            self.assertEqual(info['CFBundleIdentifier'], 'org.cecilia5.launcher')
            self.assertEqual(info['CFBundleShortVersionString'], '9.8.7')
            self.assertEqual(info['CFBundleVersion'], '9.8.7')
            self.assertTrue(info['NSMicrophoneUsageDescription'])
            self.assertEqual(info['CFBundleExecutable'], 'applet')
            launcher = contents / 'Resources/launch'
            original = launcher.read_text()
            self.assertEqual(launcher.stat().st_mode & 0o777, 0o755)
            icon = contents / 'Resources' / info['CFBundleIconFile']
            self.assertEqual(icon.read_bytes(),
                             Path(desktop.__file__).with_name('Cecilia5.icns').read_bytes())
            launcher.write_text('outdated')
            launcher.chmod(0o644)
            icon.write_bytes(b'outdated')
            self.assertEqual(desktop.register_desktop(), destination)
            self.assertEqual(launcher.read_text(), original)
            self.assertEqual(launcher.stat().st_mode & 0o777, 0o755)
            self.assertTrue(icon.read_bytes().startswith(b'icns'))
            with patch.object(desktop.sys, 'executable', __file__):
                desktop.register_desktop()
            command = launcher.read_text().splitlines()[-1]
            self.assertEqual(shlex.split(command)[1], __file__)

    @unittest.skipIf(os.name == 'nt', 'The macOS launcher uses a POSIX shell.')
    def test_macos_launcher_preserves_interpreter_paths_and_arguments(self):
        with tempfile.TemporaryDirectory(prefix="Cecilia's é $` ") as directory:
            home = Path(directory).resolve()
            interpreter = home / 'venv with spaces/bin/python3'
            interpreter.parent.mkdir(parents=True)
            interpreter.symlink_to(sys.executable)
            # Exercise the launcher without importing GUI or audio dependencies.
            (home / 'Cecilia5.py').write_text(
                'import json, os, sys\n'
                'def main():\n'
                '    print(json.dumps([sys.executable, os.getcwd(), sys.argv[1:]]))\n')
            with patch.object(desktop.sys, 'platform', 'darwin'), \
                    patch.object(desktop.sys, 'executable', str(interpreter)), \
                    patch.object(Path, 'home', return_value=home), \
                    patch.object(desktop.subprocess, 'run', side_effect=macos_tool):
                destination = desktop.register_desktop()
            arguments = ["/tmp/a file's $`é.c5", 'another argument']
            result = subprocess.run(
                [str(destination / 'Contents/Resources/launch'), *arguments],
                cwd='/', check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(result.stdout),
                             [str(interpreter), str(home.resolve()), arguments])

    def test_macos_registration_refuses_existing_application(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(Path, 'home', return_value=Path(directory)):
            contents = Path(directory) / 'Applications/Cecilia5.app/Contents'
            contents.mkdir(parents=True)
            for content in (b'invalid plist', b'<?xml version="1.0"?><plist><dict>',
                            plistlib.dumps({'CFBundleName': 'Cecilia5'})):
                with self.subTest(content=content):
                    plist_path = contents / 'Info.plist'
                    plist_path.write_bytes(content)
                    self.assertEqual(desktop.main(), 1)
                    self.assertEqual(plist_path.read_bytes(), content)
                    self.assertFalse((contents / 'MacOS').exists())

    def test_macos_missing_launcher_files_do_not_create_bundle(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(Path, 'home', return_value=Path(directory)):
            with patch.object(desktop.sys, 'executable', str(Path(directory) / 'missing-python')):
                self.assertEqual(desktop.main(), 1)
            with patch.object(desktop, '__file__', str(Path(directory) / 'desktop.py')):
                self.assertEqual(desktop.main(), 1)
            self.assertFalse((Path(directory) / 'Applications').exists())

    def test_macos_tool_failure_preserves_existing_launcher(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(Path, 'home', return_value=Path(directory)):
            with patch.object(desktop.subprocess, 'run', side_effect=macos_tool):
                destination = desktop.register_desktop()
            launcher = destination / 'Contents/Resources/launch'
            launcher.write_text('previous launcher')

            def failed_signing(command, **kwargs):
                if command[0] == '/usr/bin/codesign':
                    raise subprocess.CalledProcessError(1, command, stderr='signing failed')
                return macos_tool(command, **kwargs)

            for failure in (FileNotFoundError('osacompile'), failed_signing):
                with self.subTest(failure=failure), \
                        patch.object(desktop.subprocess, 'run', side_effect=failure):
                    self.assertEqual(desktop.main(), 1)
                    self.assertEqual(launcher.read_text(), 'previous launcher')
                    self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_unsupported_platform_does_not_create_entry(self):
        with patch.object(desktop.sys, 'platform', 'freebsd'), \
                patch.object(Path, 'home') as home:
            self.assertEqual(desktop.main(), 1)
            home.assert_not_called()

    def test_write_failure_returns_error(self):
        with patch.object(desktop.sys, 'platform', 'linux'), \
                patch.object(Path, 'mkdir', side_effect=PermissionError('denied')):
            self.assertEqual(desktop.main(), 1)
