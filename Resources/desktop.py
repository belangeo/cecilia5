"""Register Cecilia in the current user's application menu."""

import ast
import base64
from pathlib import Path
import plistlib
import shlex
import shutil
import subprocess
import sys
import tempfile
from xml.parsers.expat import ExpatError


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


def _application_version():
    """Read APP_VERSION without importing constants and its GUI dependencies."""
    constants = Path(__file__).resolve().with_name('constants.py')
    for node in ast.parse(constants.read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == 'APP_VERSION'
                for target in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError(f'APP_VERSION not found in {constants}')


def _register_macos():
    """Create or refresh a local applet that launches the installed Python."""
    # Do not resolve symlinks: the selected interpreter may belong to a venv.
    interpreter = Path(sys.executable)
    icon = Path(__file__).resolve().with_name('Cecilia5.icns')
    for path in (interpreter, icon):
        if not path.is_file():
            raise FileNotFoundError(f'Required launcher file not found: {path}')
    version = _application_version()

    destination = Path.home() / 'Applications/Cecilia5.app'
    contents = destination / 'Contents'
    plist_path = contents / 'Info.plist'
    # Never replace a standalone app or another application at this location.
    if destination.exists() or destination.is_symlink():
        try:
            info = plistlib.loads(plist_path.read_bytes())
        except (OSError, ValueError, ExpatError):
            info = {}
        if (destination.is_symlink() or not isinstance(info, dict)
                or info.get('CeciliaDesktopLauncher') is not True):
            raise RuntimeError(
                f'Refusing to overwrite an existing application: {destination}. '
                'Move it before registering the launcher.')

    destination.parent.mkdir(parents=True, exist_ok=True)
    # A native applet avoids LaunchServices rejecting a shell-script main
    # executable. Both tools ship with macOS; no compiler or py2app is needed.
    script = ('do shell script quoted form of ((POSIX path of (path to me)) '
              '& "Contents/Resources/launch")')
    with tempfile.TemporaryDirectory(prefix='.cecilia-launcher-', dir=destination.parent) as directory:
        staged = Path(directory) / 'Cecilia5.app'
        try:
            subprocess.run(['/usr/bin/osacompile', '-o', str(staged), '-e', script],
                           check=True, capture_output=True, text=True)
            resources = staged / 'Contents/Resources'
            launcher = resources / 'launch'
            command = shlex.join((str(interpreter), '-c', 'from Cecilia5 import main; main()'))
            launcher.write_text(
                '#!/bin/sh\n'
                f'cd {shlex.quote(str(Path.home()))} || exit 1\n'
                f'exec {command} "$@"\n', encoding='utf-8')
            launcher.chmod(0o755)
            shutil.copyfile(icon, resources / icon.name)
            plist_path = staged / 'Contents/Info.plist'
            info = plistlib.loads(plist_path.read_bytes())
            info.update({
                'CFBundleName': 'Cecilia5',
                'CFBundleDisplayName': 'Cecilia5',
                'CFBundleIdentifier': 'org.cecilia5.launcher',
                'CFBundleShortVersionString': version,
                'CFBundleVersion': version,
                'CFBundleIconFile': icon.name,
                # The applet waits for Python; only Cecilia needs a Dock icon.
                'LSUIElement': True,
                'NSMicrophoneUsageDescription': 'Cecilia uses audio input to process live sound.',
                'CeciliaDesktopLauncher': True,
            })
            plist_path.write_bytes(plistlib.dumps(info))
            # Editing the generated bundle invalidates osacompile's signature.
            # Re-sign locally without Developer ID, hardened runtime or entitlements.
            subprocess.run(['/usr/bin/codesign', '--force', '--sign', '-', str(staged)],
                           check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f'macOS launcher creation failed: {error.stderr.strip()}') from error

        # Build and sign completely before replacing an older launcher.
        backup = Path(directory) / 'previous.app'
        if destination.exists():
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise
    return destination


def register_desktop():
    """Create or refresh a per-user application menu entry."""
    if sys.platform == 'win32':
        return _register_windows()
    if sys.platform == 'darwin':
        return _register_macos()
    if not sys.platform.startswith('linux'):
        raise RuntimeError('Desktop registration is supported only on Linux, Windows and macOS.')

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
