import os
import sys
import json
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://shopeu.madonna.com/products/premium-cd-16-track"
JSON_ENDPOINT = "https://shopeu.madonna.com/products/premium-cd-16-track.js"
TARGET_VARIANT_ID = 47678287184098

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Credenziali Telegram non trovate nelle variabili d'ambiente.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[ERROR] Impossibile inviare la notifica Telegram: {e}")

def check_via_js_endpoint():
    """Metodo 1: Interroga l'endpoint .js nativo di Shopify per verificare la variante specifica."""
    try:
        res = requests.get(JSON_ENDPOINT, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            variants = data.get("variants", [])
            for v in variants:
                if v.get("id") == TARGET_VARIANT_ID or len(variants) == 1:
                    is_available = v.get("available", False)
                    print(f"[DEBUG API .js] Variant ID: {v.get('id')} | Available: {is_available}")
                    return is_available, data.get("title", "CONFESSIONS II Deluxe CD")
    except Exception as e:
        print(f"[DEBUG API] Fallimento chiamata endpoint .js: {e}")
    return None, None

def check_via_html_parsing():
    """Metodo 2: Analizza l'HTML cercando il bottone di acquisto e i dati JSON-LD."""
    try:
        res = requests.get(PRODUCT_URL, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"[DEBUG HTML] Status HTTP non valido: {res.status_code}")
            return False

        soup = BeautifulSoup(res.text, "html.parser")
        
        # 1. Verifica presenza di 'InStock' nei tag Schema JSON-LD
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            if script.string and "InStock" in script.string:
                print("[DEBUG HTML] Trovato stato Schema: InStock")
                return True

        # 2. Controllo analitico del bottone di aggiunta al carrello
        add_button = soup.find("button", {"name": "add"}) or soup.find("button", {"id": lambda x: x and "add" in x.lower()})
        if add_button:
            is_disabled = add_button.has_attr("disabled") or "disabled" in add_button.get("class", [])
            button_text = add_button.get_text(strip=True).lower()
            print(f"[DEBUG HTML] Bottone trovato: '{button_text}' | Disabled: {is_disabled}")
            
            if not is_disabled and "sold out" not in button_text and "esaurito" not in button_text:
                return True

    except Exception as e:
        print(f"[DEBUG HTML] Errore durante il parsing dell'HTML: {e}")
    return False

def main():
    print(f"--- Controllo Stock: {PRODUCT_URL} ---")
    
    # Primo controllo via API .js
    is_available, title = check_via_js_endpoint()
    
    # Secondo controllo (Fallback HTML) se l'API non risponde o dà incertezze
    if is_available is None:
        print("[INFO] Fallback su analisi HTML diretta...")
        is_available = check_via_html_parsing()
        title = "CONFESSIONS II – 16-track Deluxe CD"

    if is_available:
        print("🟢 RISULTATO: Prodotto DISPONIBILE!")
        msg = (
            f"🚨 **PRODOTTO DISPONIBILE!** 🚨\n\n"
            f"**{title}** è di nuovo in stock!\n"
            f"🛒 Link: {PRODUCT_URL}"
        )
        send_telegram(msg)
    else:
        print("🔴 RISULTATO: Prodotto attualmente NON disponibile (Sold Out).")

if __name__ == "__main__":
    main()
