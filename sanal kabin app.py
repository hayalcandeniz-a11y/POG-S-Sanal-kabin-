import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

# --- Sayfa Ayarları ---
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="👕")

# --- SOL MENÜ (API ANAHTARI) ---
with st.sidebar:
    st.header("🔑 Anahtar Girişi")
    st.info("Sistemin çalışması için Replicate API anahtarınızı girin.")
    api_key = st.text_input("Replicate API Token", type="password", placeholder="r8_... ile başlayan kod")

    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key
        st.success("Anahtar kaydedildi! ✅")

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
    # 1. Kontrol: API Anahtarı girilmiş mi?
    if not api_key:
        st.error("Lütfen önce sol menüden API anahtarınızı girin!")
        st.stop()
        
    # 2. Kontrol: Dosyalar tamam mı?
    if human_file is not None and garm_img is not None and urun_linki:
        st.info("⏳ Yapay zeka motoru çalışıyor... Bu işlem 15-30 saniye sürebilir. Lütfen bekleyin.")
        
        try:
            # Replicate kütüphanesini burada çağırıyoruz
            import replicate
            
            # --- MOTOR BURADA ÇALIŞIYOR ---
            output = replicate.run(
                "cuuupid/idm-vton:c871bb9b046607400f7e0472a2441966250652885738466665097774130204c8",
                input={
                    "human_img": human_file, # Senin yüklediğin dosya
                    "garm_img": urun_linki,  # Senin yapıştırdığın link
                    "category": "upper_body", # Varsayılan olarak üst giyim
                    "garment_des": "clothing item"
                }
            )
            
            # --- SONUÇ GELDİ ---
            st.balloons()
            st.success("İşlem Başarılı! 🎉")
            
            # Yeni oluşan fotoğrafı göster
            st.image(output, caption="Sanal Deneme Sonucu", use_column_width=True)
            
        except ImportError:
            st.error("HATA: 'replicate' kütüphanesi yüklü değil. Terminale 'pip install replicate' yazmalısın.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
        
    else:
        if human_file is None:
            st.error("Lütfen önce kendi fotoğrafınızı yükleyin (1. Adım).")
        elif garm_img is None:
            st.error("Lütfen bir ürün linki yapıştırın (2. Adım).")