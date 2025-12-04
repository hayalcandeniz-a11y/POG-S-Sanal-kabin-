import streamlit as st
import os
import sys

# 1. AYARLAR (En üstte olmalı)
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="🍌", layout="wide")

st.title("Sanal Kabin (Nano Modu 🍌)")

# 2. HATA YAKALAYICI (Ekran boş kalmasın diye)
try:
    import requests
    from PIL import Image
    from io import BytesIO
    from gradio_client import Client, handle_file
except ImportError as e:
    st.error("🚨 KRİTİK HATA: Bir kütüphane eksik!")
    st.code(f"Hata detayı: {e}")
    st.warning("""
    ÇÖZÜM:
    1. 'requirements.txt' dosyasını kontrol et.
    2. Sağ alttan 'Manage App' -> 'Reboot App' yap.
    """)
    st.stop()

# --- Logo Kısmı ---
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S")

st.write("Bu sürüm ücretsiz HuggingFace altyapısını kullanır.")

# --- İKİ SÜTUNLU YAPI ---
col1, col2 = st.columns(2)

garm_img_path = None
human_img_path = None
human_file = None

# SOL SÜTUN
with col1:
    st.subheader("1. Adım: Fotoğrafın")
    human_file = st.file_uploader("Fotoğrafını Yükle", type=['png', 'jpg', 'jpeg'])
    if human_file:
        st.image(human_file, width=300)
        with open("temp_human.jpg", "wb") as f:
            f.write(human_file.getbuffer())
        human_img_path = "temp_human.jpg"

# SAĞ SÜTUN
with col2:
    st.subheader("2. Adım: Ürün Linki")
    girilen_link = st.text_input("Link Yapıştır")
    if girilen_link:
        try:
            resp = requests.get(girilen_link, headers={'User-Agent': 'Mozilla/5.0'})
            img = Image.open(BytesIO(resp.content))
            img.save("temp_garm.jpg")
            garm_img_path = "temp_garm.jpg"
            st.image(img, width=300)
        except:
            st.error("Resim açılmadı. Linkin doğruluğunu kontrol et.")

# BAŞLAT BUTONU
st.markdown("---")
if st.button("DENEMEYİ BAŞLAT", type="primary"):
    if not human_img_path or not garm_img_path:
        st.error("Lütfen önce fotoğraf ve ürün yükle.")
    else:
        st.info("🍌 İşlem başlıyor... (40-60 sn sürebilir)")
        try:
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
            st.success("İşlem Başarılı!")
            st.image(result[0], caption="Sonuç", use_column_width=True)
        except Exception as hata:
            st.error(f"Motor Hatası: {hata}")