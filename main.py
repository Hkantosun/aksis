from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

def telegram_asistani_yonet(cekilen_notlar):
    # --- AYARLAR ---
    TOKEN = "8020410344:AAEtyi4uHJHoAksIbi5s1r3KQy-SoiEHQxM" # @BotFather'dan aldığın kod
    CHAT_ID = "6567829934" # getUpdates linkinden aldığın numara
    HAFIZA_DOSYASI = "notlar_hafiza.txt"
    
    if not cekilen_notlar:
        print("⚠️ Liste boş olduğu için Telegram işlemi iptal edildi.")
        return

    # 1. Hafızayı Oku
    eski_notlar = []
    if os.path.exists(HAFIZA_DOSYASI):
        with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
            eski_notlar = f.read().splitlines()
    
    # 2. Yeni Notları Bul
    yeni_aciklananlar = [n for n in cekilen_notlar if n not in eski_notlar]
    
    # 3. Aksiyon Al
    if yeni_aciklananlar:
        print(f"🔔 {len(yeni_aciklananlar)} yeni not bulundu! Mesaj gönderiliyor...")
        mesaj = "🚀 **YENİ NOTUN AÇIKLANDI!**\n\n" + "\n".join(yeni_aciklananlar)
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
        
        try:
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                print("✅ Mesaj başarıyla iletildi.")
                # Hafızayı güncelle
                with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
                    f.write("\n".join(cekilen_notlar))
        except Exception as e:
            print(f"❌ Telegram hatası: {e}")
    else:
        print("😴 Yeni açıklanan not yok.")


# 1. Tarayıcı Ayarları
chrome_options = Options()
# chrome_options.add_argument("--headless") # Şimdilik bunu açma, botu izle.
chrome_options.add_argument("--window-size=1920,1080")

# 2. Sürücü Başlatma
print("🚀 Tarayıcı başlatılıyor...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 3. Sayfaya Git
    print("🌐 Aksis giriş sayfasına gidiliyor...")
    driver.get("https://aksis.istanbul.edu.tr/")

    # 4. Giriş Elemanlarının Yüklenmesini Bekle (Max 10 saniye)
    wait = WebDriverWait(driver, 10)
    
    # Kullanıcı adı ve Şifre alanlarını bul
    # Aksis için genellikle ID'ler 'UserName' ve 'Password' şeklindedir
    user_input = wait.until(EC.presence_of_element_located((By.ID, "UserName")))
    pass_input = driver.find_element(By.ID, "Password")
    # 5. Bilgileri Yaz
    print("⌨️ Giriş bilgileri dolduruluyor...")
    user_input.send_keys("10724709066") 
    pass_input.send_keys("hakan5678")

    # 6. Giriş Yap
    try:
        # 1. Yöntem: Butonun tipine göre bul (En sağlamı genelde budur)
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except:
        # 2. Yöntem: Eğer üstteki yemezse, ID'si 'btnLogOn' olabilir (Aksis'in bazı sürümlerinde böyledir)
        login_btn = driver.find_element(By.ID, "btnLogOn")

    print("🖱️ Buton bulundu, tıklanıyor...")
    login_btn.click()

    # 7. Giriş Başarılı mı Kontrol Et
    # Giriş yaptıktan sonra sayfanın değişmesini bekleyelim
    time.sleep(5)
    
    if "Giriş" not in driver.title:
        print(f"✅ Giriş Başarılı! Şu anki sayfa: {driver.title}")
        
        # Buraya notların olduğu linke gitme kodunu ekleyeceğiz
        # Örnek: driver.get("https://aksis.istanbul.edu.tr/Ogrenci/NotBilgileri")
        
        # Başarıyı kanıtlamak için ekran görüntüsü alalım
        driver.save_screenshot("giris_sonrasi.png")
        print("📸 Ekran görüntüsü alındı: giris_sonrasi.png")
    else:
        print("❌ Giriş başarısız gibi görünüyor. Lütfen bilgileri veya ID'leri kontrol et.")

except Exception as e:
    print(f"⚠️ Bir hata oluştu: {e}")
    driver.save_screenshot("hata_aninda_ekran.png")

finally:
    print("🏁 İşlem tamamlandı. Tarayıcıyı manuel kapatabilirsin veya buraya driver.quit() ekleyebilirsin.")
    # driver.quit()


# ... (Giriş başarılı olduktan hemen sonra) ...
# --- GİRİŞ SONRASI AKIŞ ---
    print("🏠 Giriş yapıldı, ana sayfanın oturması bekleniyor...")
    time.sleep(7) 

    try:
        # 1. OBS Butonuna Tıkla
        print("🖱️ OBS butonu aranıyor...")
        obs_xpath = "//*[contains(text(), 'OBS')] | //*[contains(text(), 'Öğrenci Bilgi Sistemi')]"
        obs_btn = wait.until(EC.element_to_be_clickable((By.XPATH, obs_xpath)))
        obs_btn.click()
        print("✅ OBS tıklandı.")
        
        # 2. Yeni Sekme Kontrolü (AOS genellikle yeni sekme açar)
        time.sleep(5)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            print(f"🌐 Yeni sekmeye geçildi: {driver.title}")

        # 3. Menü Navigasyonu
        print("🖱️ Sınav İşlemleri -> Sınav Sonuçları yolu izleniyor...")
        # Sınav İşlemleri Menüsü
        sinav_islem = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sınav İşlemleri')]")))
        driver.execute_script("arguments[0].click();", sinav_islem)
        time.sleep(2)
        
        # Sınav Sonuçları Sekmesi
        sinav_sonuc = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sınav Sonuçları')]")))
        driver.execute_script("arguments[0].click();", sinav_sonuc)

        # 4. Sayfanın Verileri Yüklemesi İçin Bekleme
        print("⏳ Notlar yükleniyor... (15 saniye sabır)")
        time.sleep(15)

        # 5. JS İLE "GÖRDÜĞÜNÜ AL" MODU
        print("🧠 Tarayıcı hafızasından metinler süzülüyor...")
        
        # Sayfadaki tüm metni (scriptler hariç) çeken JS komutu
        sayfa_metni = driver.execute_script("return document.body.innerText;")
        
        # Metni satır satır parçala
        # 5. Hafızalı Tarama Başlıyor
        print("🧠 Ders başlıkları ve notlar eşleştiriliyor...")
        
        # Sayfadaki tüm anlamlı metin elemanlarını (Başlıklar ve Tablo Satırları) sırayla çekelim
        # AOS'ta ders başlıkları genellikle <h4>, <h5>, <strong> veya belirli bir class içindedir.
        # Bu XPath hem başlık olabilecek metinleri hem de tablo satırlarını sırayla bulur.
        elemanlar = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //strong | //tr | //div[contains(@class, 'title')]")
        
        cekilen_notlar = []
        aktif_ders_adi = "Bilinmeyen Ders"

        for el in elemanlar:
            metin = el.text.strip()
            if not metin: continue

            # 1. DERS ADINI GÜNCELLE
            # Eğer metin kısa değilse ve içinde 'Vize/Final' geçmiyorsa bu bir ders adıdır
            if len(metin) > 5 and not any(k in metin for k in ["Vize", "Final", "Ara Sınav", "Notu"]):
                aktif_ders_adi = metin
                # print(f"📍 Ders Tespit Edildi: {aktif_ders_adi}")

            # 2. NOTU YAKALA VE AKTİF DERSLE BİRLEŞTİR
            if any(k in metin for k in ["Vize", "Final", "Ara Sınav"]):
                # Eğer bu bir tablo satırıysa içindeki hücreleri ayıkla ki temiz veri gelsin
                cells = el.find_elements(By.TAG_NAME, "td")
                if cells:
                    not_verisi = " | ".join([c.text.strip() for c in cells if c.text.strip()])
                else:
                    not_verisi = metin
                
                final_bilgi = f"📘 {aktif_ders_adi} -> {not_verisi}"
                if final_bilgi not in cekilen_notlar:
                    print(f"✅ Eşleşti: {final_bilgi}")
                    cekilen_notlar.append(final_bilgi)

        if not cekilen_notlar:
            print("⚠️ Eşleşme yapılamadı. Lütfen 'hata_aninda_goruntu.png' dosyasında ders adının tipine bak.")
    except Exception as e:
        print(f"❌ Akış hatası: {e}")
        driver.save_screenshot("hata_detayi.png")
    finally:
        driver.quit()
        # VERİ ÇEKME BİTTİ, ŞİMDİ TELEGRAM'I TETİKLE
        telegram_asistani_yonet(cekilen_notlar)


