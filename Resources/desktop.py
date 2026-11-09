"""Register Cecilia in the current user's Linux application menu."""

from pathlib import Path
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


def register_desktop():
    """Create or refresh ~/.local/share/applications/cecilia.desktop."""
    if not sys.platform.startswith('linux'):
        raise RuntimeError('Desktop registration is currently supported only on Linux.')

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
