"""Desktop registration checks without GUI/audio dependencies."""

from pathlib import Path
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

    def test_unsupported_platform_does_not_create_entry(self):
        with patch.object(desktop.sys, 'platform', 'darwin'), \
                patch.object(Path, 'home') as home:
            self.assertEqual(desktop.main(), 1)
            home.assert_not_called()

    def test_write_failure_returns_error(self):
        with patch.object(desktop.sys, 'platform', 'linux'), \
                patch.object(Path, 'mkdir', side_effect=PermissionError('denied')):
            self.assertEqual(desktop.main(), 1)
