import requests

# URL del CD (Disponibile) per fare il test
PRODUCT_URL = (
    "https://shopeu.madonna.com/products/premium-cd-16-track.json"
)
TELEGRAM_TOKEN = "8468230379:AAF5Aan9RBe2f2MjnsUSf6KkR6Wet6VP9lI"
TELEGRAM_CHAT_ID = "1285907094"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")


def check_stock():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            product = data.get("product", {})
            title = product.get("title", "Premium CD 16-Track")
            variants = product.get("variants", [])

            is_available = any(
                variant.get("available", False) for variant in variants
            )

            if is_available:
                link = "https://shopeu.madonna.com/products/premium-cd-16-track"
                msg = f"🚨 *TEST PRODOTTO DISPONIBILE!* 🚨\n\n*{title}* risulta disponibile nello store!\n\nLink: {link}"
                send_telegram_message(msg)
                print("DISPONIBILE! Notifica inviata su Telegram.")
            else:
                print("Prodotto non disponibile.")
        else:
            print(f"Errore risposta server: {response.status_code}")
    except Exception as e:
        print(f"Errore richiesta: {e}")


if __name__ == "__main__":
    check_stock()
