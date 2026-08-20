<<<<<<< HEAD
import json
import os
import requests

EN_DIR = os.path.join(".", "pokemon_art_rarities", "en")
OUTPUT_MANIFEST = os.path.join(".", "manifest.js")

# Make sure .webp is listed first or included
VALID_EXTS = (".webp", ".png", ".jpg", ".jpeg")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

if os.path.exists(EN_DIR):
    files = [f for f in os.listdir(EN_DIR) if f.lower().endswith(VALID_EXTS)]
    unique_cards = {}

    print(f"Indexing {len(files)} English files...")

    for filename in files:
        raw_id = os.path.splitext(filename)[0]
        card_id = raw_id.replace("_", "/")

        if card_id in unique_cards:
            continue

        pokemon_name = "Unknown"

        try:
            resp = session.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                pokemon_name = data.get("name", "Unknown")
        except Exception:
            pass

        # Uses the exact .webp filename on disk
        unique_cards[card_id] = {
            "filename": filename,
            "id": card_id,
            "name": pokemon_name
        }

    card_data_list = list(unique_cards.values())

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        f.write(f"window.LOCAL_IMAGE_FILES = {json.dumps(card_data_list, indent=2)};")

=======
import json
import os
import requests

EN_DIR = os.path.join(".", "pokemon_art_rarities", "en")
OUTPUT_MANIFEST = os.path.join(".", "manifest.js")

# Make sure .webp is listed first or included
VALID_EXTS = (".webp", ".png", ".jpg", ".jpeg")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

if os.path.exists(EN_DIR):
    files = [f for f in os.listdir(EN_DIR) if f.lower().endswith(VALID_EXTS)]
    unique_cards = {}

    print(f"Indexing {len(files)} English files...")

    for filename in files:
        raw_id = os.path.splitext(filename)[0]
        card_id = raw_id.replace("_", "/")

        if card_id in unique_cards:
            continue

        pokemon_name = "Unknown"

        try:
            resp = session.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                pokemon_name = data.get("name", "Unknown")
        except Exception:
            pass

        # Uses the exact .webp filename on disk
        unique_cards[card_id] = {
            "filename": filename,
            "id": card_id,
            "name": pokemon_name
        }

    card_data_list = list(unique_cards.values())

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        f.write(f"window.LOCAL_IMAGE_FILES = {json.dumps(card_data_list, indent=2)};")

>>>>>>> 0777306 (Update website content)
    print(f"✓ Indexed {len(card_data_list)} unique cards to root manifest.js.")