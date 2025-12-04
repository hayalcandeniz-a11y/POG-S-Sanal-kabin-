import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO

# --- 1. AYARLAR (EN BAŞTA OLMALI) ---
st.set_page_config(page_title="POG'S Sanal Kabin (Ücretsiz)", page_icon="🍌", layout="wide")

# --- 2. MOTOR KONTROLÜ VE KURTARMA ---
try:
    from gradio_client import Client, handle_file
except ImportError:
    st.error("🚨 HATA: Motor parçaları eksik!")
    
    # Kullanıcıya ne yapması gerektiğini kutu içinde gösterelim
    st.info("🛠️ TAMİR ETMEK İÇİN ŞUNU YAP:")
    st.code("requirements.txt", language="text")
    st.markdown("""
    1. Soldaki dosya listesinde **'requirements.txt'** diye bir dosya var mı?
       - **YOKSA:** Hemen '+' butonuna basıp bu isimde bir dosya oluştur.
       - **VARSA:** İçini aç ve kontrol et.
    
    2. O dosyanın içine şu 4 kelimeyi alt alta yazıp kaydet:
    """)
    st.code("""streamlit
requests
Pillow
gradio_client""", language="text")
    
    st.markdown("""
    3. Son olarak sağ alttan **'Manage App' -> 'Reboot App'** yap.
    """)
    st.stop() # Kodun geri kalanını çalıştırma

# --- Logo Kısmı ---
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S")

st.title("Sanal Kabin (Nano Modu 🍌)")
st.success("Sistem şu an sorunsuz çalışıyor! ✅")
st.write("Bu sürüm tamamen ücretsizdir! HuggingFace altyapısını kullanır.")

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
            # Linkten resmi indir
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(girilen_link, headers=headers)
            garm_img_display = Image.open(BytesIO(response.content))
            
            # Dosyayı geçici olarak kaydet
            garm_img_display.save("temp_garm.jpg")
            garm_img_path = "temp_garm.jpg"
            
            st.image(garm_img_display, caption="Seçilen Ürün", width=300)
            st.info("✅ Ürün alındı.")

        except Exception as e:
            st.error("Resim yüklenemedi. Linkin doğrudan bir resim dosyası olduğundan emin ol.")

# --- 4. BAŞLATMA BUTONU ---
st.markdown("---")
if st.button("ÜCRETSİZ DENE (BAŞLAT)", type="primary", use_container_width=True):
    
    # Dosya Kontrolü
    if not human_img_path or not garm_img_path:
        st.error("❌ Lütfen önce fotoğrafını yükle ve geçerli bir ürün linki gir.")
        st.stop()

    st.warning("🍌 Nano Banana Motoru çalışıyor... (Ücretsiz sunucu olduğu için 40-60 saniye sürebilir, lütfen bekle...)")
    
    try:
        # ÜCRETSİZ API BAĞLANTISI
        client = Client("yisol/IDM-VTON")
        
        # İşlemi Başlat
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
        
        # Sonuç gösterimi
        sonuc_resim_yolu = result[0]
        st.balloons()
        st.success("🎉 İŞTE SONUÇ!")
        st.image(sonuc_resim_yolu, caption="Sanal Deneme Sonucu", use_column_width=True)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        st.info("Sunucu yoğun olabilir, birazdan tekrar dene.")