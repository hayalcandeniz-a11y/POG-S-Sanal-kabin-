import streamlit as st

# Sayfa Başlığı ve Ayarları
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="👕")

# --- TASARIM KISMI ---

# 1. Logo (Eğer logo.png yüklediysen çalışır, yoksa hata vermemesi için try-except koydum)
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S") # Logo yoksa yazı yazar

st.title("Sanal Kabin'e Hoşgeldiniz")
st.write("Kendi fotoğrafını yükle ve ürünlerimizi üzerinde dene!")

# 2. Fotoğraf Yükleme Alanı
# YENİ KOD (Bunu yapıştır)
import requests # Eğer sayfanın en tepesinde bu yoksa ekle
from PIL import Image
from io import BytesIO

# 1. Kullanıcıdan link isteyen kutucuk
urun_linki = st.text_input("Ürün Resminin Linkini Buraya Yapıştır")

garm_img = None # Başlangıçta boş olsun

# 2. Eğer kutuya bir şey yazıldıysa
if urun_linki:
    try:
        # Linkteki resmi indirip hafızaya alıyoruz
        response = requests.get(urun_linki)
        garm_img = Image.open(BytesIO(response.content))
        
        # Ekranda kullanıcıya doğru resmi seçtiğini gösterelim
        st.image(garm_img, caption="Seçilen Ürün", width=300)
    except:
        st.error("Bu linkte bir resim bulamadım. Linkin .jpg veya .png ile bittiğinden emin ol.")
if garm_img is not None:
st.image(garm_img, ...)    st.success("Fotoğraf yüklendi! Şimdi aşağıdan bir ürün seçin.")

# 3. Ürün Seçimi (3 Sütun Halinde)
st.subheader("Denemek İstediğin Ürünü Seç")
col1, col2, col3 = st.columns(3)


# Seçim Bilgisi
if 'secilen' in st.session_state:
    st.write(f"Seçilen Ürün: **{st.session_state['secilen']}**")

# 4. Dev Buton
st.markdown("---")
if st.button("SANAL DENEMEYİ BAŞLAT", type="primary"):
    if uploaded_file is not None:
        st.balloons()
        st.success("Yapay zeka motoru çalışıyor... (Bu özellik bir sonraki adımda eklenecek!)")
    else:
        st.error("Lütfen önce kendi fotoğrafınızı yükleyin.")