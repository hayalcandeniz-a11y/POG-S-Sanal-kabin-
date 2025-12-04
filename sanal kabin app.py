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
st.write("Aşağıdaki adımları takip ederek sanal deneme yapabilirsin.")

# --- 1. ADIM: Kendi Fotoğrafını Yükle ---
st.subheader("1. Adım: Kendi Fotoğrafın")
human_file = st.file_uploader("Boydan çekilmiş bir fotoğrafını yükle", type=['png', 'jpg', 'jpeg'])

if human_file is not None:
    st.image(human_file, caption="Senin Fotoğrafın", width=200)
    st.success("Fotoğrafın hazır!")

# --- 2. ADIM: Ürün Linki Alma ---
st.markdown("---")
st.subheader("2. Adım: Denenecek Ürün")
urun_linki = st.text_input("Ürün Resminin Linkini Buraya Yapıştır")

garm_img = None # Başlangıçta boş olsun

if urun_linki:
    try:
        # Linkteki resmi indirip hafızaya alıyoruz
        response = requests.get(urun_linki)
        garm_img = Image.open(BytesIO(response.content))
        
        # Ekranda kullanıcıya doğru resmi seçtiğini gösterelim
        st.image(garm_img, caption="Seçilen Ürün", width=300)
        st.success("Ürün fotoğrafı başarıyla alındı!")
    except:
        st.error("Bu linkte bir resim bulamadım. Linkin .jpg veya .png ile bittiğinden emin ol.")

# --- 3. ADIM: Deneme Butonu ---
st.markdown("---")

if st.button("SANAL DENEMEYİ BAŞLAT", type="primary"):
    # KONTROL: Hem insan fotosu hem ürün fotosu var mı?
    if human_file is not None and garm_img is not None:
        st.balloons()
        st.success("Yapay zeka motoru çalışıyor... (Sistem şu an tam hazır!)")
        
        # Buraya ileride Replicate API kodu gelecek
        # human_file -> Müşteri fotosu
        # urun_linki -> Kıyafet linki
        
    else:
        if human_file is None:
            st.error("Lütfen önce kendi fotoğrafınızı yükleyin (1. Adım).")
        elif garm_img is None:
            st.error("Lütfen bir ürün linki yapıştırın (2. Adım).")