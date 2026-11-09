"""Desktop registration checks without GUI/audio dependencies."""

import base64
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from Resources import desktop


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

    def test_unsupported_platform_does_not_create_entry(self):
        with patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(Path, 'home') as home:
            self.assertEqual(desktop.main(), 1)
            home.assert_not_called()

    def test_write_failure_returns_error(self):
        with patch.object(desktop.sys, 'platform', 'linux'), \
                patch.object(Path, 'mkdir', side_effect=PermissionError('denied')):
            self.assertEqual(desktop.main(), 1)
