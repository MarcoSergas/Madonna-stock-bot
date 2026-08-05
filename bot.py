import json
import requests

PRODUCT_URL = "https://shopeu.madonna.com/products/premium-cd-16-track.json"
TELEGRAM_TOKEN = "8468230379:AAF5Aan9RBe2f2MjnsUSf6KkR6Wet6VP9lI"
TELEGRAM_CHAT_ID = "1285907094"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"Esito invio Telegram: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        print(f"Codice risposta HTTP: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            product = data.get("product", {})
            title = product.get("title", "Prodotto sconosciuto")
            variants = product.get("variants", [])

            print(f"Titolo prodotto trovato: {title}")
            print(f"Numero varianti trovate: {len(variants)}")

            any_available = False
            for v in variants:
                var_title = v.get("title", "Standard")
                avail = v.get("available", False)
                price = v.get("price", "0.00")
                print(f"-> Variante: '{var_title}' | Available: {avail} | Prezzo: {price}")
                if avail:
                    any_available = True

            if any_available:
                print("ESITO: Almeno una variante risulta DISPONIBILE!")
                send_telegram_message(f"🚨 *TEST DISPONIBILE!*\n\nProdotto: *{title}*")
            else:
                print("ESITO: Tutte le varianti risultano NON DISPONIBILI nel JSON.")
        else:
            print(f"Errore: Il server risponde con status {response.status_code}")
    except Exception as e:
        print(f"Errore di rete/connessione: {e}")

if __name__ == "__main__":
    check_stock()
