import requests
import os

def telegram_asistani_yonet(cekilen_notlar):
    TOKEN = os.environ.get("TG_TOKEN", "")
    CHAT_ID = os.environ.get("TG_ID", "")
    HAFIZA_DOSYASI = "notlar_hafiza.txt"

    if not cekilen_notlar:
        print("⚠️ Çekilen not listesi boş, işlem iptal.")
        return

    # Hafızayı oku
    eski_notlar = set()
    if os.path.exists(HAFIZA_DOSYASI):
        with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
            eski_notlar = set(line.strip() for line in f if line.strip())

    yeni_notlar_set = set(n.strip() for n in cekilen_notlar if n.strip())
    yeni_aciklananlar = yeni_notlar_set - eski_notlar

    print(f"📂 Hafızadaki: {len(eski_notlar)} | Siteden: {len(yeni_notlar_set)} | Yeni: {len(yeni_aciklananlar)}")

    if yeni_aciklananlar:
        print(f"🔔 {len(yeni_aciklananlar)} yeni not, mesaj gönderiliyor...")
        mesaj = "🚀 *YENİ NOT AÇIKLANDI!*\n\n" + "\n".join(sorted(yeni_aciklananlar))
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("✅ Telegram mesajı gönderildi.")
                with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                    f.write("\n".join(sorted(yeni_notlar_set)))
            else:
                print(f"❌ Telegram hatası: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"⚠️ Bağlantı hatası: {e}")
    else:
        print("😴 Yeni not yok, mesaj gönderilmedi.")
        if not os.path.exists(HAFIZA_DOSYASI):
            with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(yeni_notlar_set)))
