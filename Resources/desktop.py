"""Register Cecilia in the current user's Linux or Windows application menu."""

import base64
from pathlib import Path
import subprocess
import sys


def _escape_value(value):
    """Escape a desktop-entry string value."""
    return (str(value).replace('\\', '\\\\').replace('\n', '\\n')
            .replace('\r', '\\r').replace('\t', '\\t'))


def _quote_argument(value):
    """Apply Exec quoting, then desktop-entry string escaping."""
    value = str(value).replace('%', '%%')
    for character in ('\\', '"', '`', '$'):
        value = value.replace(character, '\\' + character)
    return _escape_value('"' + value + '"')


def _powershell_string(value):
    """Quote a literal PowerShell string, including paths with apostrophes."""
    return "'" + str(value).replace("'", "''") + "'"


def _register_windows():
    """Create or refresh Cecilia5.lnk in the current user's Programs folder."""
    # Keep the environment's interpreter path; resolving it can escape a venv.
    interpreter = Path(sys.executable).with_name('pythonw.exe')
    icon = Path(__file__).resolve().with_name('Cecilia5.ico')
    for path in (interpreter, icon):
        if not path.is_file():
            raise FileNotFoundError(f'Required shortcut file not found: {path}')

    # Ask Windows for the Programs folder to support redirected Start menus.
    # WScript.Shell is built in, so registration needs no extra Python packages.
    script = f"""
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$programs = [Environment]::GetFolderPath('Programs')
if (-not $programs) {{ throw 'Windows Programs folder could not be located.' }}
[System.IO.Directory]::CreateDirectory($programs) | Out-Null
$destination = Join-Path $programs 'Cecilia5.lnk'
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($destination)
$shortcut.TargetPath = {_powershell_string(interpreter)}
$shortcut.Arguments = '-c "from Cecilia5 import main; main()"'
$shortcut.WorkingDirectory = {_powershell_string(Path.home())}
$shortcut.IconLocation = {_powershell_string(str(icon) + ',0')}
$shortcut.Description = 'Create and process sound with Cecilia'
$shortcut.Save()
[Console]::WriteLine($destination)
"""
    # EncodedCommand preserves Unicode paths and avoids command-line quoting.
    encoded = base64.b64encode(script.encode('utf-16-le')).decode('ascii')
    try:
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded],
            check=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f'Windows shortcut creation failed: {error.stderr.strip()}') from error
    return Path(result.stdout.strip())


def register_desktop():
    """Create or refresh a per-user application menu entry."""
    if sys.platform == 'win32':
        return _register_windows()
    if not sys.platform.startswith('linux'):
        raise RuntimeError('Desktop registration is supported only on Linux and Windows.')

    icon = Path(__file__).resolve().with_name('Cecilia5.png')
    if not icon.is_file():
        raise FileNotFoundError(f'Application icon not found: {icon}')

    # Keep the virtual environment's interpreter path (do not resolve symlinks).
    # This also avoids relying on the desktop session's PATH.
    command = ' '.join(_quote_argument(arg) for arg in (
        sys.executable, '-c', 'from Cecilia5 import main; main()'))
    entry = (
        '[Desktop Entry]\n'
        'Version=1.0\n'
        'Type=Application\n'
        'Name=Cecilia5\n'
        'GenericName=Audio Processing Toolbox\n'
        'Comment=Create and process sound with Cecilia\n'
        f'Exec={command} %f\n'
        f'Icon={_escape_value(icon)}\n'
        'Terminal=false\n'
        'Categories=AudioVideo;Audio;\n'
        'Keywords=audio;sound;music;processing;synthesis;\n'
    )
    destination = Path.home() / '.local/share/applications/cecilia.desktop'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(entry, encoding='utf-8')
    return destination


def main():
    """Console entry point, independent of GUI and audio imports."""
    try:
        destination = register_desktop()
    except (OSError, RuntimeError) as error:
        print(f'Could not register Cecilia: {error}', file=sys.stderr)
        return 1
    print(f'Registered Cecilia: {destination}')
    return 0
