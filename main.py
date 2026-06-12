from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import telegram_asistani_yonet  # ← EKLENDİ
import time

cekilen_notlar = []  # ← SCOPE SORUNU GİDERİLDİ, en üstte tanımla

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

print("🚀 Tarayıcı başlatılıyor...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    wait = WebDriverWait(driver, 10)  # ← wait burada tanımlanırsa her iki try'da da erişilebilir

    print("🌐 Aksis giriş sayfasına gidiliyor...")
    driver.get("https://aksis.istanbul.edu.tr/")

    user_input = wait.until(EC.presence_of_element_located((By.ID, "UserName")))
    pass_input = driver.find_element(By.ID, "Password")

    user_input.send_keys("10724709066")
    pass_input.send_keys("hakan5678")

    try:
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except:
        login_btn = driver.find_element(By.ID, "btnLogOn")

    login_btn.click()
    time.sleep(5)

    if "Giriş" not in driver.title:
        print(f"✅ Giriş Başarılı! Sayfa: {driver.title}")
    else:
        print("❌ Giriş başarısız.")

    # --- GİRİŞ SONRASI AKIŞ ---
    time.sleep(7)

    obs_xpath = "//*[contains(text(), 'OBS')] | //*[contains(text(), 'Öğrenci Bilgi Sistemi')]"
    obs_btn = wait.until(EC.element_to_be_clickable((By.XPATH, obs_xpath)))
    obs_btn.click()

    time.sleep(5)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])

    sinav_islem = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sınav İşlemleri')]")))
    driver.execute_script("arguments[0].click();", sinav_islem)
    time.sleep(2)

    sinav_sonuc = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sınav Sonuçları')]")))
    driver.execute_script("arguments[0].click();", sinav_sonuc)
    time.sleep(15)

    elemanlar = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //strong | //tr | //div[contains(@class, 'title')]")

    aktif_ders_adi = "Bilinmeyen Ders"
    for el in elemanlar:
        metin = el.text.strip()
        if not metin:
            continue
        if len(metin) > 5 and not any(k in metin for k in ["Vize", "Final", "Ara Sınav", "Notu"]):
            aktif_ders_adi = metin
        if any(k in metin for k in ["Vize", "Final", "Ara Sınav"]):
            cells = el.find_elements(By.TAG_NAME, "td")
            not_verisi = " | ".join([c.text.strip() for c in cells if c.text.strip()]) if cells else metin
            final_bilgi = f"📘 {aktif_ders_adi} -> {not_verisi}"
            if final_bilgi not in cekilen_notlar:
                cekilen_notlar.append(final_bilgi)

except Exception as e:
    print(f"❌ Hata: {e}")
    driver.save_screenshot("hata_aninda_ekran.png")

finally:
    driver.quit()  # ← YORUM SATIRINDAN ÇIKARILDI

# Telegram'ı telegram.py'deki doğru versiyonla tetikle
telegram_asistani_yonet(cekilen_notlar)
