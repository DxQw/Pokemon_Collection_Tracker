import os
import requests
import time

# Directory to save the images
SAVE_DIR = os.path.join(".", "pokemon_art_rarities", "en")
os.makedirs(SAVE_DIR, exist_ok=True)

# TCGdex specific classifications for all "hits" (excluding basics/standard holos)
TARGET_RARITIES = [
    "Double Rare",               # ex cards
    "Rare Holo V",               # V cards
    "Rare Holo VMAX",            # VMAX cards
    "Rare Holo VSTAR",           # VSTAR cards
    "Ultra Rare",                # UR / Full Arts
    "Hyper Rare",                # HR / Gold cards
    "Illustration Rare",         # IR / Art Rares
    "Special Illustration Rare", # SIR / SAR
    "Rare Secret",               # Older Secret Rares
    "Rare Ultra",                # Older Ultra Rares
    "Radiant Rare",              # Radiant cards
    "Amazing Rare"               # Amazing Rares
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

def fetch_special_cards():
    total_downloaded = 0
    
    for rarity in TARGET_RARITIES:
        print(f"\nSearching for {rarity} cards...")
        
        # Query TCGdex API filtered strictly by rarity
        url = f"https://api.tcgdex.net/v2/en/cards?rarity={rarity.replace(' ', '%20')}"
        
        try:
            response = session.get(url, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch {rarity}. API returned {response.status_code}")
                continue
                
            cards = response.json()
            print(f"Found {len(cards)} cards for {rarity}.")
            
            for card in cards:
                if not card.get("image"):
                    continue
                    
                # Format ID and filepath
                card_id = card["id"]
                safe_filename = f"{card_id.replace('/', '_')}.png"
                filepath = os.path.join(SAVE_DIR, safe_filename)
                
                # Skip if already downloaded
                if os.path.exists(filepath):
                    continue 
                    
                # Download High-Res version of the card
                image_url = f"{card['image']}/high.png"
                img_resp = session.get(image_url, timeout=15)
                
                if img_resp.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    print(f"✓ Downloaded: {card.get('name')} ({card_id})")
                    total_downloaded += 1
                    
                    # Short pause to prevent overwhelming the API
                    time.sleep(0.15) 
                    
        except Exception as e:
            print(f"Error processing {rarity}: {e}")
            
    print(f"\nFinished! Downloaded {total_downloaded} new special cards.")

if __name__ == "__main__":
    fetch_special_cards()