import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO

# --- 1. AYARLAR ---
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="🍌", layout="wide")

st.title("Sanal Kabin (Final Sürüm 🍌)")
st.markdown("Eğer bu yazı görünüyorsa uygulama başlamış demektir.")

# --- 2. KÜTÜPHANE KONTROLÜ (Otomatik Kontrol) ---
try:
    from gradio_client import Client, handle_file
    st.success("✅ Motor (Gradio Client) başarıyla yüklendi!")
except ImportError:
    st.error("🚨 HATA: 'gradio_client' kütüphanesi bulunamadı!")
    st.warning("Lütfen sol menüde 'requirements.txt' adında bir dosya oluşturduğundan ve içine 'gradio_client' yazdığından emin ol.")
    st.stop()

# --- 3. SAYFA DÜZENİ ---
col1, col2 = st.columns(2)
human_img_path = None
garm_img_path = None

with col1:
    st.subheader("1. Senin Fotoğrafın")
    human_file = st.file_uploader("Fotoğrafını Yükle", type=['png', 'jpg', 'jpeg'])
    if human_file:
        st.image(human_file, width=250)
        with open("temp_human.jpg", "wb") as f:
            f.write(human_file.getbuffer())
        human_img_path = "temp_human.jpg"

with col2:
    st.subheader("2. Kıyafet Linki")
    link = st.text_input("Ürün görsel linkini yapıştır")
    if link:
        try:
            resp = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content))
                st.image(img, width=250)
                img.save("temp_garm.jpg")
                garm_img_path = "temp_garm.jpg"
            else:
                st.error("Resim indirilemedi.")
        except:
            st.error("Link hatası.")

# --- 4. ÇALIŞTIRMA ---
st.markdown("---")
if st.button("DENEMEYİ BAŞLAT", type="primary"):
    if not human_img_path or not garm_img_path:
        st.error("Lütfen önce iki resmi de yükle!")
    else:
        st.info("⏳ İşlem başladı... Lütfen 40-60 saniye bekleyin, sayfayı kapatmayın.")
        try:
            # HuggingFace API Bağlantısı
            client = Client("yisol/IDM-VTON")
            
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
            
            st.success("İşlem Tamamlandı!")
            st.image(result[0], caption="Sonuç", use_column_width=True)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")
            st.info("Sunucu yoğun olabilir. Lütfen 1 dakika sonra tekrar dene.")