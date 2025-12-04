import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import re
from gradio_client import Client, handle_file

# --- Sayfa Ayarları ---
st.set_page_config(page_title="POG'S Sanal Kabin (Ücretsiz)", page_icon="🍌", layout="wide")

# --- Logo Kısmı ---
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S")

st.title("Sanal Kabin (Nano Modu 🍌)")
st.write("Bu sürüm tamamen ücretsizdir! Google Nano/HuggingFace altyapısını kullanır.")

# --- İKİ SÜTUNLU YAPI ---
col1, col2 = st.columns(2)

garm_img_path = None    # Dosya yolu (Gradio için)
human_img_path = None   # Dosya yolu (Gradio için)
garm_img_display = None # Ekranda göstermek için

# --- SOL SÜTUN: MÜŞTERİ FOTOĞRAFI ---
with col1:
    st.subheader("1. Adım: Senin Fotoğrafın")
    human_file = st.file_uploader("Boydan bir fotoğrafını yükle", type=['png', 'jpg', 'jpeg'])
    
    if human_file:
        st.image(human_file, caption="Müşteri Fotoğrafı", width=300)
        # Gradio'ya göndermek için dosyayı geçici olarak kaydedelim
        with open("temp_human.jpg", "wb") as f:
            f.write(human_file.getbuffer())
        human_img_path = "temp_human.jpg"
        st.success("✅ Fotoğraf hazır.")

# --- SAĞ SÜTUN: ÜRÜN LİNKİ ---
with col2:
    st.subheader("2. Adım: Ürün Linki")
    st.info("💡 İpucu: Ürün resminin linkini yapıştır.")
    girilen_link = st.text_input("Ürün Resim Linki")

    if girilen_link:
        try:
            # Linkten resmi indir
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(girilen_link, headers=headers)
            garm_img_display = Image.open(BytesIO(response.content))
            
            # Resmi diske kaydet (API'ye göndermek için)
            garm_img_display.save("temp_garm.jpg")
            garm_img_path = "temp_garm.jpg"
            
            st.image(garm_img_display, caption="Seçilen Ürün", width=300)
            st.success("✅ Ürün hazır.")

        except Exception as e:
            st.error("Resim yüklenemedi. Direkt resim linki olduğundan emin ol (.jpg/.png).")

# --- 3. ADIM: BAŞLATMA BUTONU ---
st.markdown("---")
if st.button("ÜCRETSİZ DENE (BAŞLAT)", type="primary", use_container_width=True):
    
    if not human_img_path or not garm_img_path:
        st.error("❌ Lütfen önce fotoğrafını yükle ve ürün linkini gir.")
        st.stop()

    st.info("🍌 Nano Motor çalışıyor... (Ücretsiz sunucu olduğu için 30-60 saniye sürebilir, lütfen bekle...)")
    
    try:
        # ÜCRETSİZ API BAĞLANTISI (Hugging Face Spaces)
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
        
        # Sonuç (result) genellikle bir dosya yolu döner
        sonuc_resim_yolu = result[0]
        
        st.balloons()
        st.success("🎉 İŞTE SONUÇ!")
        st.image(sonuc_resim_yolu, caption="Sanal Deneme Sonucu", use_column_width=True)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        st.warning("Eğer 'Queue' hatası alırsan sunucu çok yoğundur, 1 dakika sonra tekrar dene.")