from html.parser import HTMLParser
import requests

# URL del prodotto per il test (attualmente il CD disponibile)
PRODUCT_URL = "https://shopeu.madonna.com/products/premium-cd-16-track"
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
        r = requests.post(url, json=payload, timeout=10)
        print(f"Esito invio Telegram: {r.status_code}")
    except Exception as e:
        print(f"Errore invio Telegram: {e}")


class ShopifyFormParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_cart_form = False
        self.form_html = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "form" and "/cart/add" in attr_dict.get("action", ""):
            self.in_cart_form = True

        if self.in_cart_form:
            # Ricostruisce i tag principali per l'analisi
            attrs_str = " ".join([f'{k}="{v}"' for k, v in attrs])
            self.form_html.append(f"<{tag} {attrs_str}>")

    def handle_endtag(self, tag):
        if self.in_cart_form:
            self.form_html.append(f"</{tag}>")
            if tag == "form":
                self.in_cart_form = False

    def handle_data(self, data):
        if self.in_cart_form:
            self.form_html.append(data)


def check_stock():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=10)
        print(f"Codice risposta HTTP: {response.status_code}")

        if response.status_code == 200:
            parser = ShopifyFormParser()
            parser.feed(response.text)
            form_content = "".join(parser.form_html).lower()

            if not form_content:
                print(
                    "AVVISO: Modulo /cart/add non trovato, analizzo i pulsanti"
                    " di acquisto principali."
                )
                form_content = response.text.lower()

            # Verifichiamo lo stato del pulsante nel modulo specifico
            is_disabled = (
                "disabled" in form_content or "sold-out" in form_content
            )
            has_buy_button = (
                "add to cart" in form_content
                or 'name="add"' in form_content
                or "aggiungi" in form_content
            )

            print(
                f"Modulo Prodotto -> Pulsante presente: {has_buy_button} |"
                f" Disabilitato/SoldOut: {is_disabled}"
            )

            if has_buy_button and not is_disabled:
                print("ESITO: Prodotto DISPONIBILE! Invio notifica...")
                msg = (
                    "🚨 *PRODOTTO DISPONIBILE!* 🚨\n\nIl prodotto è"
                    f" acquistabile!\n\nLink: {PRODUCT_URL}"
                )
                send_telegram_message(msg)
            else:
                print("ESITO: Il prodotto risulta attualmente esaurito.")
        else:
            print(f"Errore risposta server: {response.status_code}")
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")


if __name__ == "__main__":
    check_stock()
