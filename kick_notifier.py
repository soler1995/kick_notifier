import requests
import time

# ── Configuración ──────────────────────────────────────────
STREAMER      = "forg1"   # usuario en Kick
BOT_TOKEN     = "8783397085:AAFdV_i9fRZeaCWr9lPQiHZMEttoczSgam8"
CHAT_ID       = "5659754687"
INTERVALO_SEG = 60                      # chequea cada 60 segundos
# ───────────────────────────────────────────────────────────

def esta_en_vivo(streamer):
    try:
        url = f"https://kick.com/api/v1/channels/{streamer}"
        r = requests.get(url, timeout=10).json()
        return r.get("is_live", False)
    except:
        return False

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})

def main():
    print(f"👀 Monitoreando a {STREAMER} en Kick...")
    estaba_en_vivo = esta_en_vivo(STREAMER)  # estado inicial
    print(f"Estado actual: {'EN VIVO' if en_vivo else 'offline'}")
    while True:
        time.sleep(INTERVALO_SEG)
        en_vivo = esta_en_vivo(STREAMER)

        if en_vivo and not estaba_en_vivo:
            enviar_telegram(f"🔴 ¡{STREAMER} acaba de prender stream en Kick!\nhttps://kick.com/{STREAMER}")
            print("✅ Notificación enviada")

        elif not en_vivo and estaba_en_vivo:
            enviar_telegram(f"⚫ {STREAMER} terminó el stream.")
            print("✅ Notificación de fin enviada")

        estaba_en_vivo = en_vivo

if __name__ == "__main__":
    main()
