import json
from pathlib import Path

from check_i18n import validate

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = Path(__file__).parent / "translations.json"
LOCALES_DIR = BASE_DIR / "bot" / "locales"


def fix() -> None:
    """Automatically appends missing translation keys into .ftl files from JSON database."""
    # 1. Retrieve the list of keys actually missing in the files
    missing_keys_report = validate()

    if not missing_keys_report:
        print("✅ All locales are synchronized. Nothing to do.")
        return

    # 2. Read the translation database
    if not JSON_PATH.exists():
        print(f"❌ CRITICAL ERROR: File {JSON_PATH} not found.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            db = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON ERROR: Invalid format in translations.json: {e}")
            return

    # 3. Append only existing translations
    for lang, keys in missing_keys_report.items():
        ftl_path = LOCALES_DIR / lang / "LC_MESSAGES" / "messages.ftl"
        new_entries: list[str] = []

        for key in keys:
            # Extract ONLY the specific language. No fallback to 'en'.
            translation = db.get(key, {}).get(lang)

            if translation:
                # Formatting for Fluent (indentation for multiline values)
                formatted_val = translation.replace("\n", "\n    ")
                new_entries.append(f"{key} = {formatted_val}")
            else:
                print(
                    f"⚠️ [SKIPPED] No translation found in JSON for '{key}' in language '{lang}'."
                )

        if new_entries:
            # Append entries to the file
            ftl_path.parent.mkdir(parents=True, exist_ok=True)
            with open(ftl_path, "a", encoding="utf-8") as f:
                f.write("\n" + "\n".join(new_entries) + "\n")
            print(f"✅ Added {len(new_entries)} keys for '{lang}'.")


if __name__ == "__main__":
    fix()
