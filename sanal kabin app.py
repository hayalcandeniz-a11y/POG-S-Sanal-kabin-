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
uploaded_file = st.file_uploader("Boydan fotoğrafınızı yükleyin:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklediğiniz Fotoğraf", width=300)
    st.success("Fotoğraf yüklendi! Şimdi aşağıdan bir ürün seçin.")

# 3. Ürün Seçimi (3 Sütun Halinde)
st.subheader("Denemek İstediğin Ürünü Seç")
col1, col2, col3 = st.columns(3)

# Not: tisort1.png, tisort2.png isimli dosyaların GitHub'da yüklü olması lazım.
# Eğer yoksa hata vermesin diye basit butonlar koydum.

with col1:
    st.info("Tişört Modeli 1")
    if st.button("Seç", key="t1"):
        st.session_state['secilen'] = "Model 1"

with col2:
    st.info("Tişört Modeli 2")
    if st.button("Seç", key="t2"):
        st.session_state['secilen'] = "Model 2"

with col3:
    st.info("Sweatshirt")
    if st.button("Seç", key="t3"):
        st.session_state['secilen'] = "Model 3"

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