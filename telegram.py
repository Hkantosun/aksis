import requests
import os

def telegram_asistani_yonet(cekilen_notlar):
    """
    Bu fonksiyon sadece bildirim ve hafıza işlerine bakar.
    Veri çekme işlemi (Scraping) burada yapılmaz, dışarıdan liste olarak gelir.
    """
    
    # --- AYARLAR ---
    TOKEN = "8020410344:AAEtyi4uHJHoAksIbi5s1r3KQy-SoiEHQxM"
    CHAT_ID = "6567829934"
    HAFIZA_DOSYASI = "notlar_hafiza.txt"
    
    # 1. HAFIZAYI KONTROL ET
    # Daha önce kaydedilmiş notlar var mı diye bakıyoruz.
    eski_notlar = []
    if os.path.exists(HAFIZA_DOSYASI):
        with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
            eski_notlar = f.read().splitlines()
    
    # 2. KIYASLAMA YAP
    # Yeni gelen listede olup, eski listede olmayan (yeni açıklanan) notları bulur.
    yeni_aciklananlar = [not_satiri for not_satiri in cekilen_notlar if not_satiri not in eski_notlar]
    
    # 3. AKSİYON AL
    if yeni_aciklananlar:
        print(f"🔔 Yeni notlar tespit edildi: {len(yeni_aciklananlar)} adet.")
        
        # Telegram Mesajını Hazırla
        duyuru_metni = "🚀 **SİSTEMDEN YENİ BİLDİRİM!**\n\n"
        duyuru_metni += "Aşağıdaki notların sisteme girildi:\n"
        duyuru_metni += "\n".join(yeni_aciklananlar)
        
        # Telegram API'sine Gönder
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
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