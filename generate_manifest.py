import json
import os
import requests

EN_DIR = os.path.join(".", "pokemon_art_rarities", "en")
OUTPUT_MANIFEST = os.path.join(".", "manifest.js")
VALID_EXTS = (".png", ".jpg", ".jpeg", ".webp")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

if os.path.exists(EN_DIR):
    files = [f for f in os.listdir(EN_DIR) if f.lower().endswith(VALID_EXTS)]
    
    # Dictionary used to prevent duplicate card entries by Card ID
    unique_cards = {}

    print(f"Indexing {len(files)} English files and removing duplicates...")

    for filename in files:
        raw_id = os.path.splitext(filename)[0]
        card_id = raw_id.replace("_", "/")

        # Skip if this card ID has already been added
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

        unique_cards[card_id] = {
            "filename": filename,
            "id": card_id,
            "name": pokemon_name
        }

    # Convert unique dictionary values to list
    card_data_list = list(unique_cards.values())

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        f.write(f"window.LOCAL_IMAGE_FILES = {json.dumps(card_data_list, indent=2)};")

    print(f"✓ Successfully indexed {len(card_data_list)} unique cards to root manifest.js.")
else:
    print(f"✗ Directory missing: {EN_DIR}")