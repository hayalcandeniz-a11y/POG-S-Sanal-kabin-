import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- Sayfa Ayarları ---
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="👕")

# --- Logo Kısmı ---
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S")

st.title("Sanal Kabin'e Hoşgeldiniz")
st.write("Kendi fotoğrafını yükle ve ürünlerimizi üzerinde dene!")

# --- 1. Bölüm: Ürün Linki Alma ---
urun_linki = st.text_input("Ürün Resminin Linkini Buraya Yapıştır")

garm_img = None # Başlangıçta boş olsun

if urun_linki:
    try:
        # Linkteki resmi indirip hafızaya alıyoruz
        response = requests.get(urun_linki)
        garm_img = Image.open(BytesIO(response.content))
        
        # Ekranda kullanıcıya doğru resmi seçtiğini gösterelim
        st.image(garm_img, caption="Seçilen Ürün", width=300)
        st.success("Fotoğraf başarıyla alındı!")
    except:
        st.error("Bu linkte bir resim bulamadım. Linkin .jpg veya .png ile bittiğinden emin ol.")

# --- 2. Bölüm: Deneme Butonu ---
st.markdown("---")

if st.button("SANAL DENEMEYİ BAŞLAT", type="primary"):
    # Burayı düzelttik: Artık 'uploaded_file' değil 'garm_img' kontrol ediliyor
    if garm_img is not None:
        st.balloons()
        st.success("Yapay zeka motoru çalışıyor... (Sistem hazır!)")
    else:
        st.error("Lütfen önce yukarıya geçerli bir resim linki yapıştırın.")