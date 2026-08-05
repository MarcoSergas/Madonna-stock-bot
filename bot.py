import requests

# URL corretto della pagina web del prodotto
PRODUCT_URL = "https://shopeu.madonna.com/products/premium-cd-16-track"
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
        print(f"Esito invio Telegram: {r.status_code}")
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        print(f"Codice risposta HTTP: {response.status_code}")

        if response.status_code == 200:
            html = response.text.lower()

            # Verifichiamo le parole chiave presenti nel codice sorgente della pagina
            has_add_to_cart = "add to cart" in html or "aggiungi al carrello" in html
            is_sold_out = "sold out" in html or "esaurito" in html

            print(f"Trovato 'Add to Cart': {has_add_to_cart}")
            print(f"Trovato 'Sold Out': {is_sold_out}")

            # Se è presente il pulsante e non la dicitura sold out
            if has_add_to_cart and not is_sold_out:
                print("ESITO: Prodotto DISPONIBILE! Invio notifica...")
                msg = f"🚨 *TEST PRODOTTO DISPONIBILE!* 🚨\n\nIl prodotto è acquistabile nello store!\n\nLink: {PRODUCT_URL}"
                send_telegram_message(msg)
            else:
                print("ESITO: Prodotto esaurito.")
        else:
            print(f"Errore risposta server: {response.status_code}")
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")

if __name__ == "__main__":
    check_stock()
