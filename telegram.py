import requests
import os

def telegram_asistani_yonet(cekilen_notlar):
    TOKEN = "8020410344:AAEtyi4uHJHoAksIbi5s1r3KQy-SoiEHQxM"
    CHAT_ID = "6567829934"
    HAFIZA_DOSYASI = "notlar_hafiza.txt"

    if not cekilen_notlar:
        print("⚠️ Çekilen not listesi boş, işlem iptal.")
        return

    # 1. Hafızayı oku
    eski_notlar = set()
    if os.path.exists(HAFIZA_DOSYASI):
        with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
            eski_notlar = set(line.strip() for line in f if line.strip())

    # 2. Gelen notları da set'e çevir (boş satırları temizle)
    yeni_notlar_set = set(n.strip() for n in cekilen_notlar if n.strip())

    # 3. Farkı bul
    yeni_aciklananlar = yeni_notlar_set - eski_notlar

    print(f"📂 Hafızadaki not sayısı: {len(eski_notlar)}")
    print(f"📡 Siteden çekilen not sayısı: {len(yeni_notlar_set)}")
    print(f"🆕 Yeni not sayısı: {len(yeni_aciklananlar)}")

    # 4. Aksiyon al
    if yeni_aciklananlar:
        print(f"🔔 {len(yeni_aciklananlar)} yeni not bulundu, mesaj gönderiliyor...")
        duyuru_metni = "🚀 *SİSTEMDEN YENİ BİLDİRİM!*\n\n"
        duyuru_metni += "\n".join(sorted(yeni_aciklananlar))

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": duyuru_metni, "parse_mode": "Markdown"}

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("✅ Telegram bildirimi iletildi.")
                # Hafızayı sadece başarıda güncelle — TÜM notları yaz
                with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                    f.write("\n".join(sorted(yeni_notlar_set)))
            else:
                print(f"❌ Telegram hatası: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"⚠️ Telegram bağlantı hatası: {e}")
    else:
        print("😴 Yeni not yok, bildirim gönderilmedi.")
        # Hafıza dosyası yoksa oluştur (ilk çalışma)
        if not os.path.exists(HAFIZA_DOSYASI):
            with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(yeni_notlar_set)))        payload = {
            "chat_id": CHAT_ID,
            "text": duyuru_metni,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print("✅ Telegram bildirimi başarıyla iletildi.")
                
                # Sadece mesaj başarıyla giderse hafızayı güncelle
                with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                    f.write("\n".join(cekilen_notlar))
            else:
                print(f"❌ Telegram hatası: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Telegram servisine bağlanılamadı: {e}")
            
    else:
        # Eğer çekilen veriler eskilerle tamamen aynıysa bildirim gitmez.
        print("😴 Yeni açıklanan bir not yok. Sessizliğe devam...")

# --- DİĞER KODUNUN SONUNDA ŞÖYLE KULLANACAKSIN ---
# final_liste = ["Ders A -> Vize: 70", "Ders B -> Final: 85"] # Bu liste diğer koddan gelecek
# telegram_asistani_yonet(final_liste)
