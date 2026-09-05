import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN o TELEGRAM_CHAT_ID non configurati.")

# Inserisci qui tutti i prodotti che vuoi monitorare
PRODUCTS = [
    {
        "name": "Cassette",
        "url": "https://shopeu.madonna.com/products/cassette.js",
        "link": "https://shopeu.madonna.com/products/cassette"
    },
    {
        "name": "Deluxe 2LP Set",
        "url": "https://shopeu.madonna.com/products/luxe-expanded-2lpe-epink.js",
        "link": "https://shopeu.madonna.com/products/luxe-expanded-2lpe-epink"
    },
    {
        "name": "LP Pride Edition",
        "url": "https://shopeu.madonna.com/products/confessions-ii-d-12-track-vinyl-lp-pride-edition.js",
        "link": "https://shopeu.madonna.com/products/confessions-ii-d-12-track-vinyl-lp-pride-edition"
    },
    {
        "name": "Bass Persuades Neon",
        "url": "https://store.mileyofficial.com/en-eu/products/bass-persuades-neon-coral-vinyl-store-exclusive.js",
        "link": "https://store.mileyofficial.com/en-eu/products/bass-persuades-neon-coral-vinyl-store-exclusive"
    },
    {
        "name": "Bass Persuades Signed",
        "url": "https://store.mileyofficial.com/products/bass-persuades-signed-black-vinyl.js",
        "link": "https://store.mileyofficial.com/products/bass-persuades-signed-black-vinyl"
    },
    {
        "name": "Bass Persuades Ruby",
        "url": "https://store.mileyofficial.com/en-eu/products/bass-persuades-ruby-vinyl-store-exclusive.js",
        "link": "https://store.mileyofficial.com/en-eu/products/bass-persuades-ruby-vinyl-store-exclusive"
    }
]

def send_telegram(msg):
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(
            telegram_url,
            json={
                "chat_id": CHAT_ID,
                "text": msg,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("Notifica Telegram inviata con successo!")
        else:
            print(f"Errore Telegram ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"Errore durante l'invio del messaggio Telegram: {e}")

def check_stock():
    print("==========================================")
    print("Monitor Madonna Store")
    print("Avvio controllo disponibilità...")
    print("==========================================")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for item in PRODUCTS:
        print(f"Controllo prodotto: {item['name']}")
        try:
            response = requests.get(item["url"], headers=headers, timeout=10)
            print(f"[{item['name']}] Risposta HTTP: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                is_available = data.get("available", False)
                
                if is_available:
                    product_title = data.get("title", item["name"])
                    msg = (
                        f"🚨 **PRODOTTO DISPONIBILE!** 🚨\n\n"
                        f"Il prodotto **{product_title}** è disponibile!\n\n"
                        f"👉 Link acquisto: {item['link']}"
                    )
                    send_telegram(msg)
                else:
                    print(f"[{item['name']}] Prodotto ancora esaurito.")
            else:
                print(f"[{item['name']}] Errore HTTP: Stato {response.status_code}")
        except Exception as e:
            print(f"[{item['name']}] Errore durante l'esecuzione: {e}")
            
        time.sleep(1)

    print("==========================================")
    print("Controllo completato.")
    print("==========================================")

if __name__ == "__main__":
    check_stock()
