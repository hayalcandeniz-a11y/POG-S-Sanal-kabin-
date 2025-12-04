import streamlit as st  # Web sitesini oluşturan araç (Biz ona 'st' diyeceğiz)
import os               # Bilgisayarın dosya sistemine erişen araç
import sys              # Sistem ayarları için araç

# --- 1. AYARLAR (Sitenin Kimliği) ---
# Sayfanın sekme adını ve ikonunu (muz) ayarlıyoruz.
st.set_page_config(page_title="POG'S Sanal Kabin", page_icon="🍌", layout="wide")

st.title("Sanal Kabin (Nano Modu 🍌)")

# --- 2. MOTOR KONTROLÜ (Güvenlik Önlemi) ---
# Burada "Arabanın motoru (gradio_client) takılı mı?" diye bakıyoruz.
try:
    import requests                           # İnternetten resim indirmek için
    from PIL import Image                     # Resimleri işlemek (açmak/kaydetmek) için
    from io import BytesIO                    # Resim verisini hafızada tutmak için
    from gradio_client import Client, handle_file # Yapay zeka ile konuşacak olan asıl motor
except ImportError as hata_mesaji:
    # Eğer motor yoksa, çalışmayı durdur ve kullanıcıya ne yapması gerektiğini söyle.
    st.error("🚨 KRİTİK HATA: Bir kütüphane eksik!")
    st.code(f"Hata detayı: {hata_mesaji}")
    st.warning("""
    ÇÖZÜM:
    1. 'requirements.txt' dosyasını kontrol et (içinde gradio_client var mı?).
    2. Sağ alttan 'Manage App' -> 'Reboot App' yaparak sistemi yeniden başlat.
    """)
    st.stop() # Kodun geri kalanını çalıştırma, burada dur.

# --- Logo Kısmı ---
# Logo varsa göster, yoksa sadece yazı yaz.
try:
    st.image("logo.svg", width=200)
except:
    st.header("POG'S")

st.write("Bu sürüm ücretsiz HuggingFace altyapısını kullanır.")

# --- 3. SAYFA DÜZENİ (İki Sütun) ---
# Sayfayı ikiye bölüyoruz: Sol Sütun (col1) ve Sağ Sütun (col2)
col1, col2 = st.columns(2)

# Bu değişkenler (kutular) başlangıçta boş, içlerini aşağıda dolduracağız.
kiyafet_resim_yolu = None
insan_resim_yolu = None
yuklenen_insan_dosyasi = None

# --- SOL SÜTUN: İnsan Fotoğrafı ---
with col1:
    st.subheader("1. Adım: Fotoğrafın")
    # Kullanıcıdan dosya yüklemesini iste
    yuklenen_insan_dosyasi = st.file_uploader("Fotoğrafını Yükle", type=['png', 'jpg', 'jpeg'])
    
    if yuklenen_insan_dosyasi:
        # Fotoğraf yüklendiyse ekranda göster
        st.image(yuklenen_insan_dosyasi, width=300)
        
        # Bu dosyayı yapay zekaya gönderebilmek için geçici olarak kaydediyoruz
        with open("gecici_insan.jpg", "wb") as dosya:
            dosya.write(yuklenen_insan_dosyasi.getbuffer())
        insan_resim_yolu = "gecici_insan.jpg"

# --- SAĞ SÜTUN: Kıyafet Linki ---
with col2:
    st.subheader("2. Adım: Ürün Linki")
    # Kullanıcıdan link iste
    girilen_link = st.text_input("Link Yapıştır")
    
    if girilen_link:
        try:
            # İnternetten (requests) o linkteki resmi çekmeye çalış
            cevap = requests.get(girilen_link, headers={'User-Agent': 'Mozilla/5.0'})
            resim = Image.open(BytesIO(cevap.content))
            
            # Resmi yine geçici olarak kaydediyoruz
            resim.save("gecici_kiyafet.jpg")
            kiyafet_resim_yolu = "gecici_kiyafet.jpg"
            
            # Resmi ekranda göster
            st.image(resim, width=300)
        except:
            st.error("Resim açılmadı. Linkin doğruluğunu kontrol et.")

# --- 4. İŞLEM BUTONU ---
st.markdown("---") # Araya bir çizgi çek

if st.button("DENEMEYİ BAŞLAT", type="primary"):
    # Önce kontrol: İki resim de elimizde mi?
    if not insan_resim_yolu or not kiyafet_resim_yolu:
        st.error("Lütfen önce fotoğrafını yükle ve bir ürün linki yapıştır.")
    else:
        st.info("🍌 İşlem başlıyor... (Sunucu yoğunluğuna göre 40-60 saniye sürebilir)")
        
        try:
            # --- YAPAY ZEKA BAĞLANTISI ---
            # HuggingFace üzerindeki 'yisol/IDM-VTON' adlı motora bağlanıyoruz
            istemci = Client("yisol/IDM-VTON")
            
            # Motora emri veriyoruz (Predict = Tahmin Et / Yap)
            sonuc = istemci.predict(
                dict={"background": handle_file(insan_resim_yolu), "layers": [], "composite": None},
                garm_img=handle_file(kiyafet_resim_yolu), # Kıyafet resmi
                garment_des="clothing",                   # Kıyafet tanımı
                is_checked=True,                          # Otomatik kırpma var mı?
                is_checked_crop=False,                    # Kırpma ayarı
                denoise_steps=30,                         # Kalite adımı (30 iyidir)
                seed=42,                                  # Rastgelelik tohumu (hep aynı sonuç için)
                api_name="/tryon"                         # Fonksiyon adı
            )
            
            # --- SONUÇ GELDİ ---
            st.success("İşlem Başarılı! 🎉")
            # Gelen sonucu (result[0]) ekrana basıyoruz
            st.image(sonuc[0], caption="Sonuç", use_column_width=True)
            
        except Exception as hata:
            st.error(f"Motor Hatası: {hata}")