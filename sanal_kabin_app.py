import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO

# --- 1. AYARLAR ---
# Sayfa yapılandırması (Bu komut her zaman en başta olmalıdır)
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="🍌", layout="wide")

# --- 2. DOKTOR MODU (KONTROLLER) ---

# ADIM A: requirements.txt kontrolü
if not os.path.exists("requirements.txt"):
    st.error("🚨 HATA 1: 'requirements.txt' dosyası bulunamadı!")
    st.info("ÇÖZÜM: Sol menüden 'New File' diyerek bu isimde bir dosya oluşturmalısın.")
    st.stop()

# ADIM B: requirements.txt içeriği kontrolü
with open("requirements.txt", "r") as f:
    dosya_icerigi = f.read()
    if "gradio_client" not in dosya_icerigi:
        st.error("🚨 HATA 2: 'requirements.txt' dosyasında 'gradio_client' eksik!")
        st.warning(f"Mevcut içerik:\n{dosya_icerigi}")
        st.info("ÇÖZÜM: Dosyaya 'gradio_client' satırını eklemelisin.")
        st.stop()

# ADIM C: Motor (Gradio Client) Yükleme
try:
    from gradio_client import Client, handle_file
    st.success("✅ Motor başarıyla yüklendi! Sistem hazır.")
except ImportError:
    st.error("🚨 HATA 3: Kütüphaneler yüklü değil veya motor başlatılamadı.")
    st.info("ÇÖZÜM: Sağ alt köşedeki 'Manage App' menüsünden 'Reboot App' butonuna basarak uygulamayı yeniden başlat.")
    st.stop()

# --- 3. SAYFA DÜZENİ ---
col1, col2 = st.columns(2)

garm_img_path = None
human_img_path = None

# --- SOL SÜTUN: MÜŞTERİ FOTOĞRAFI ---
with col1:
    st.subheader("1. Adım: Senin Fotoğrafın")
    human_file = st.file_uploader("Boydan bir fotoğrafını yükle", type=['png', 'jpg', 'jpeg'])
    
    if human_file:
        st.image(human_file, caption="Müşteri Fotoğrafı", width=300)
        # Dosyayı geçici olarak kaydet
        with open("temp_human.jpg", "wb") as f:
            f.write(human_file.getbuffer())
        human_img_path = "temp_human.jpg"
        st.info("✅ Fotoğraf alındı.")

# --- SAĞ SÜTUN: ÜRÜN LİNKİ ---
with col2:
    st.subheader("2. Adım: Ürün Linki")
    st.info("💡 İpucu: Ürün resminin linkini yapıştır (.jpg veya .png ile biten).")
    girilen_link = st.text_input("Ürün Resim Linki")

    if girilen_link:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(girilen_link, headers=headers)
            if response.status_code == 200:
                garm_img_display = Image.open(BytesIO(response.content))
                garm_img_display.save("temp_garm.jpg")
                garm_img_path = "temp_garm.jpg"
                st.image(garm_img_display, caption="Seçilen Ürün", width=300)
                st.info("✅ Ürün alındı.")
            else:
                st.error("Resim indirilemedi. Bağlantıyı kontrol et.")
        except Exception as e:
            st.error(f"Resim yüklenirken hata oluştu: {e}")

# --- 4. BAŞLATMA BUTONU ---
st.markdown("---")
if st.button("ÜCRETSİZ DENE (BAŞLAT)", type="primary", use_container_width=True):
    
    if not human_img_path or not garm_img_path:
        st.error("❌ Lütfen önce hem kendi fotoğrafını yükle hem de geçerli bir ürün linki gir.")
        st.stop()

    st.warning("🍌 Nano Banana Motoru çalışıyor... (40-60 saniye sürebilir, lütfen bekle...)")
    
    try:
        # Hugging Face üzerindeki ücretsiz motoru kullanıyoruz
        client = Client("yisol/IDM-VTON")
        
        # API çağrısı
        # Not: 'dict' parametresi isimlendirilmiş argüman olarak gönderiliyor.
        # Python keyword ile çakışsa da gradio_client bunu bekliyor olabilir.
        result = client.predict(
            dict={"background": handle_file(human_img_path), "layers": [], "composite": None},
            garm_img=handle_file(garm_img_path),
            garment_des="clothing",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )
        
        # Sonuç genellikle bir liste veya tuple döner, ilk elemanı dosya yoludur
        sonuc_resim_yolu = result[0]
        
        st.balloons()
        st.success("🎉 İŞTE SONUÇ!")
        st.image(sonuc_resim_yolu, caption="Sanal Deneme Sonucu", use_column_width=True)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        st.info("Sunucu şu an çok yoğun olabilir veya API yanıt vermiyor olabilir. Lütfen 1-2 dakika sonra tekrar dene.")