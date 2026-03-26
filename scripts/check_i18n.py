import os
import re
from pathlib import Path

# Path configuration relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "bot"
LOCALES_DIR = APP_DIR / "locales"


def get_keys_from_code():
    """Finds translation keys, ignoring arguments after them."""
    keys = set()
    # Pattern: search for the beginning of the call and extract only the content of quotes
    pattern = re.compile(
        r'(?:(?:i18n|safe_get)\.get|_get)\(\s*[\'"]([a-zA-Z0-9_-]+)[\'"]'
    )

    for file in APP_DIR.rglob("*.py"):
        try:
            content = file.read_text(encoding="utf-8")
            found = pattern.findall(content)
            keys.update(found)
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")
    return keys


def get_keys_from_ftl(locale):
    """Extracts keys defined in the fluent translation file."""
    path = LOCALES_DIR / locale / "LC_MESSAGES" / "messages.ftl"
    if not path.exists():
        return set()
    content = path.read_text(encoding="utf-8")
    # Search for keys at the beginning of the line
    return set(re.findall(r"^([a-zA-Z0-9_-]+)\s*=", content, re.MULTILINE))


def validate():
    """Validates missing translations across all available locales."""
    code_keys = get_keys_from_code()
    if not LOCALES_DIR.exists():
        print(f"❌ Locales directory not found: {LOCALES_DIR}")
        exit(1)

    locales = [d.name for d in LOCALES_DIR.iterdir() if d.is_dir()]
    missing_report = {}

    for loc in locales:
        ftl_keys = get_keys_from_ftl(loc)
        missing = code_keys - ftl_keys
        if missing:
            missing_report[loc] = missing

    return missing_report


if __name__ == "__main__":
    report = validate()
    if report:
        print("❌ Missing translation keys found:")
        for lang, keys in report.items():
            print(f"[{lang}]: {', '.join(keys)}")
    else:
        print("✅ All translation keys are valid.")
