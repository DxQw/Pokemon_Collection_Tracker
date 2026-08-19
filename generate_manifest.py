import json
import os
import requests

OUTPUT_MANIFEST = os.path.join(".", "manifest.js")

# Target set or local list of IDs you own
CARD_IDS = [
    # Add your card IDs here or read them from your local directory filenames
]

unique_cards = {}
session = requests.Session()

# Fetch metadata and use direct CDN URLs
for card_id in CARD_IDS:
    try:
        resp = session.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            
            # Direct remote CDN URL
            image_url = f"{data.get('image')}/high.webp" if data.get("image") else ""
            
            unique_cards[card_id] = {
                "id": card_id,
                "name": data.get("name", "Unknown"),
                "filePath": image_url
            }
    except Exception:
        pass

card_data_list = list(unique_cards.values())

with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
    f.write(f"window.LOCAL_IMAGE_FILES = {json.dumps(card_data_list, indent=2)};")

print(f"✓ Created CDN-backed manifest with {len(card_data_list)} cards.")