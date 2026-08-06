import os
import requests

URL = "https://shopeu.madonna.com/products/premium-cd-16-track.js"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            is_available = data.get("available", False)
            
            if is_available:
                product_title = data.get("title", "Premium CD 16 Track")
                msg = (
                    f"🚨 **PRODOTTO DISPONIBILE!** 🚨\n\n"
                    f"Il prodotto **{product_title}** è tornato disponibile su Madonna Store EU!\n\n"
                    f"👉 Link acquisto: https://shopeu.madonna.com/products/premium-cd-16-track"
                )
                
                telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(telegram_url, json={
                    "chat_id": CHAT_ID,
                    "text": msg,
                    "parse_mode": "Markdown"
                })
                print("Notifica inviata con successo su Telegram!")
            else:
                print("Prodotto ancora esaurito.")
        else:
            print(f"Errore nella richiesta HTTP: Stato {response.status_code}")
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    check_stock()
