import requests
import time

TELEGRAM_BOT_TOKEN = "8958167208:AAFqfL1Gv..."
TELEGRAM_CHAT_ID = "7747286464"

def enviar_alerta(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

def consultar_binance(trade_type):
    target_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    body = {
        "asset": "USDT",
        "fiat": "VES", 
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 3,
        "tradeType": trade_type
    }

    try:
        response = requests.post(target_url, json=body, headers=headers, timeout=15)
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return float(data["data"][0]["adv"]["unitPrice"])
    except Exception as e:
        print(f"Error Binance {trade_type}: {e}")
    return None

def verificar_arbitraje():
    print("Consultando mercado P2P...")
    precio_compra = consultar_binance("BUY")
    precio_venta = consultar_binance("SELL")

    if precio_compra and precio_venta:
        margen = ((precio_venta - precio_compra) / precio_compra) * 100
        print(f"Compra: {precio_compra} | Venta: {precio_venta} | Margen: {margen:.2f}%")

        if margen > 0.5:
            mensaje = (
                f"🚨 **¡Oportunidad de Arbitraje Detectada!** 🚨\n\n"
                f"🟢 **Compra barato a:** {precio_compra} VES\n"
                f"🔴 **Vende caro a:** {precio_venta} VES\n"
                f"📊 **Margen estimado:** `{margen:.2f}%`\n\n"
                f"[🔗 Abrir Binance P2P](https://p2p.binance.com)"
            )
            enviar_alerta(mensaje)

while True:
    verificar_arbitraje()
    time.sleep(60)
