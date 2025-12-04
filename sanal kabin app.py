import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import re  # Linklerin içinden resim bulmak için dedektif kütüphanesi

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

# --- 2. ADIM: Ürün Linki Alma (AKILLI MOD) ---
st.markdown("---")
st.subheader("2. Adım: Denenecek Ürün")
st.info("İpucu: Doğrudan ürün sayfasının linkini (Örn: trendyol.com/urun...) veya resim linkini yapıştırabilirsin.")
girilen_link = st.text_input("Ürün Sayfası veya Resim Linki")

garm_img = None         # Ekranda göstereceğimiz resim
apiye_gidecek_link = "" # Yapay zekaya göndereceğimiz temiz resim linki

if girilen_link:
    try:
        # Linke istek atıyoruz
        headers = {'User-Agent': 'Mozilla/5.0'} # Kendimizi tarayıcı gibi tanıtıyoruz
        response = requests.get(girilen_link, headers=headers)
        
        # 1. Durum: Link zaten bir resim dosyasıysa (jpg, png vb.)
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            garm_img = Image.open(BytesIO(response.content))
            apiye_gidecek_link = girilen_link
            st.success("Doğrudan resim bağlantısı algılandı.")

        # 2. Durum: Link bir web sitesi sayfasıysa (html)
        else:
            st.info("Web sayfası algılandı, içindeki ürün görseli aranıyor... 🔍")
            html_icerigi = response.text
            
            # Sayfa kodları içinde 'og:image' etiketini arıyoruz (Genelde ana ürün fotosu budur)
            # Regex ile <meta property="og:image" content="..."> yapısını yakalıyoruz
            bulunan = re.search(r'<meta property="og:image" content="(.*?)"', html_icerigi)
            
            if bulunan:
                bulunan_resim_linki = bulunan.group(1)
                
                # Bazen linkler // ile başlar, başına https: ekleyelim
                if bulunan_resim_linki.startswith("//"):
                    bulunan_resim_linki = "https:" + bulunan_resim_linki
                
                # Bulduğumuz resmi indirelim
                resim_response = requests.get(bulunan_resim_linki, headers=headers)
                garm_img = Image.open(BytesIO(resim_response.content))
                apiye_gidecek_link = bulunan_resim_linki # AI'ya bu linki göndereceğiz
                
                st.success(f"Sayfadaki ana görsel bulundu!")
            else:
                st.warning("Sayfada uygun bir ürün görseli (og:image) bulunamadı. Lütfen doğrudan resim linki deneyin.")

        # Resmi Ekrana Bas
        if garm_img:
            st.image(garm_img, caption="Algılanan Ürün", width=300)

    except Exception as e:
        st.error(f"Link işlenirken bir hata oluştu: {e}")

# --- 3. ADIM: Deneme Butonu ---
st.markdown("---")

if st.button("SANAL DENEMEYİ BAŞLAT", type="primary"):
    # 1. Kontrol: API Anahtarı girilmiş mi?
    if not api_key:
        st.error("Lütfen önce sol menüden API anahtarınızı girin!")
        st.stop()
        
    # 2. Kontrol: Dosyalar tamam mı?
    if human_file is not None and garm_img is not None and apiye_gidecek_link:
        st.info("⏳ Yapay zeka motoru çalışıyor... Bu işlem 15-30 saniye sürebilir. Lütfen bekleyin.")
        
        try:
            import replicate
            
            # --- MOTOR BURADA ÇALIŞIYOR ---
            output = replicate.run(
                "cuuupid/idm-vton:c871bb9b046607400f7e0472a2441966250652885738466665097774130204c8",
                input={
                    "human_img": human_file,      # Senin yüklediğin dosya
                    "garm_img": apiye_gidecek_link, # Sayfadan ayıkladığımız TEMİZ resim linki
                    "category": "upper_body",
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
            st.error("Lütfen geçerli bir ürün sayfası linki yapıştırın (2. Adım).")