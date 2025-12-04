<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>POG's Sanal Kabin</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <!-- AYARLAR VE YAPILANDIRMA -->
    <script>
        const APP_CONFIG = {
            // 1. Google AI Studio API Anahtarınızı Buraya Yapıştırın:
            apiKey: "", 
            
            // 2. Marka Bilgileri:
            brandName: "POG's",
            brandSubtitle: "SANAL KABİN",
            
            // 3. Renk Teması (Hex Kodları):
            colors: {
                primary: "#ec4899", // Ana Renk (Pembe)
                secondary: "#fbcfe8", // İkincil Renk (Açık Pembe)
                background: "#0a0a0a" // Arka Plan Rengi
            }
        };
    </script>

    <style>
        /* Dinamik CSS Değişkenleri */
        :root {
            --color-theme-primary: #ec4899; 
            --color-theme-secondary: #fbcfe8; 
            --color-theme-dark: #000000; 
            --color-theme-bg-dark: #0a0a0a; 
        }

        .color-accent { color: var(--color-theme-primary); }
        .bg-accent { background-color: var(--color-theme-primary); }
        .border-accent { border-color: var(--color-theme-primary); }
        .text-accent-light { color: var(--color-theme-secondary); }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--color-theme-bg-dark);
            background-image: radial-gradient(circle at 50% 0%, #1a0510 0%, var(--color-theme-bg-dark) 80%);
            height: 100dvh; 
            overflow: hidden;
            color: #d1d1d1;
        }
        
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); }
        ::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--color-theme-primary); }
        
        .loader {
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-left-color: var(--color-theme-primary); 
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .btn-neon {
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(236, 72, 153, 0.3); 
            border: 1px solid var(--color-theme-primary);
            color: white; 
            opacity: 0.9;
        }
        .btn-neon:hover {
            opacity: 1;
            box-shadow: 0 0 25px rgba(236, 72, 153, 0.6);
            filter: brightness(1.1);
        }
        .btn-neon:active { transform: scale(0.98); }
        
        .image-frame {
            border: 1px solid rgba(255, 255, 255, 0.1); 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
            padding: 0;
            background-color: #111; 
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .image-frame:hover { border-color: var(--color-theme-primary); }
        
        .brand-logo {
            font-family: 'Inter', sans-serif;
            font-weight: 900; 
            color: var(--color-theme-primary);
            font-size: 1.8rem; 
            letter-spacing: -0.02em; 
            text-transform: uppercase;
            background: linear-gradient(to right, var(--color-theme-primary), #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-studio-text {
            font-size: 0.7rem;
            font-weight: 400;
            color: var(--color-theme-secondary);
            margin-left: 0.5rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
        }

        .product-radio:checked + div {
            background-color: var(--color-theme-primary);
            border-color: var(--color-theme-primary);
            color: white;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(236, 72, 153, 0.3);
        }
        
        select:focus, textarea:focus, input:focus {
            border-color: var(--color-theme-primary) !important;
            box-shadow: 0 0 0 1px var(--color-theme-primary) !important;
            outline: none;
        }
        option { background-color: #111; color: #d1d1d1; }
        
        /* Mobil Panel */
        #controlsContent { transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out; }
        .panel-collapsed { max-height: 0; opacity: 0; overflow: hidden; padding: 0 !important; }
        .panel-expanded { max-height: 600px; opacity: 1; }
        
        #errorMessage {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(20, 20, 20, 0.95); color: #fff; padding: 20px 30px;
            border-radius: 4px; box-shadow: 0 4px 30px rgba(0,0,0,0.8);
            max-width: 90%; z-index: 50; text-align: center; border: 1px solid #333;
            font-family: monospace; display: none; animation: fadeIn 0.3s ease-in-out;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        .nav-btn {
            position: absolute; top: 50%; transform: translateY(-50%); z-index: 110;
            background: rgba(0, 0, 0, 0.5); color: white; border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem; cursor: pointer; transition: all 0.3s; opacity: 0.7; backdrop-filter: blur(5px);
        }
        .nav-btn:hover { opacity: 1; background: var(--color-theme-primary); }
        #prevImageBtn { left: 1rem; border-radius: 50%; }
        #nextImageBtn { right: 1rem; border-radius: 50%; }

        .glass-panel {
            background: rgba(20, 10, 15, 0.6);
            backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

    </style>
</head>
<body class="text-gray-300 text-sm flex flex-col overflow-hidden">
    
    <div id="errorMessage"></div>

    <!-- MODAL --><div id="imageModal" class="fixed inset-0 z-[100] hidden bg-black/98 flex flex-col items-center justify-center p-4 opacity-0 transition-opacity duration-300">
        <button id="prevImageBtn" class="nav-btn p-3 md:p-4 hidden"><i class="fas fa-chevron-left text-xl"></i></button>
        <button id="closeModal" class="absolute top-4 right-4 text-gray-400 hover:text-white p-3 hover:bg-white/10 rounded-full transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        <img id="modalImage" class="max-h-[80dvh] max-w-full shadow-2xl border border-[#333] object-contain transition-opacity duration-300" src="" alt="Büyük Görünüm">
        <button id="nextImageBtn" class="nav-btn p-3 md:p-4 hidden"><i class="fas fa-chevron-right text-xl"></i></button>
        <div class="mt-6 w-full px-4 max-w-sm">
            <button id="modalDownloadBtn" class="w-full py-3 bg-accent hover:bg-white hover:text-black text-white rounded-sm font-bold shadow-lg text-xs uppercase tracking-[0.2em] transition-colors">GÖRSELİ İNDİR</button>
        </div>
    </div>

    <!-- HEADER --><header class="w-full bg-[#0a0a0a]/90 backdrop-blur border-b border-[#222] py-2 px-6 shrink-0 z-20 flex justify-between items-center h-16">
        <div class="flex items-center gap-4">
            <!-- LOGO ALANI (TIKLANABİLİR & KAYDEDİLEBİLİR) -->
            <div class="relative group cursor-pointer" id="brandLogoWrapper">
                <input type="file" id="logoInput" accept="image/*" class="hidden">
                <div id="brandLogoContainer" class="flex items-center select-none h-10">
                    <span class="brand-logo" id="headerBrandName">POG's</span>
                    <span class="brand-studio-text ml-2" id="headerBrandSub">SANAL KABİN</span>
                </div>
                <!-- Hover İpucu (Logo Yüklendikten Sonra Gizlenecek) -->
                <div id="logoHint" class="absolute -bottom-4 left-0 text-[8px] text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    Logo yüklemek için tıkla (Kalıcıdır)
                </div>
            </div>
            
            <div class="hidden md:block h-4 w-[1px] bg-[#333]"></div>
            <p class="hidden md:block text-[10px] text-gray-500 tracking-[0.2em] uppercase font-medium">Sanal Deneme Teknolojisi</p>
        </div>
        <div class="flex items-center space-x-4 text-[10px] md:text-xs font-mono text-gray-600">
            <span class="text-gray-500 font-medium">AI Powered</span>
            <span class="text-[#333]">|</span>
            <span>v10.2 Final</span>
        </div>
    </header>

    <!-- ANA İÇERİK --><div class="flex-grow flex flex-col p-2 md:p-6 gap-4 overflow-hidden w-full max-w-[1920px] mx-auto">

        <!-- KONTROL PANELİ --><div class="w-full glass-panel rounded-lg shadow-2xl shrink-0 flex flex-col overflow-hidden">
            
            <div id="panelHeader" class="flex justify-between items-center p-4 cursor-pointer md:cursor-default bg-[#111]/40 md:bg-transparent border-b md:border-b-0 border-[#222]" onclick="toggleMobilePanel()">
                <div class="flex items-center gap-3 color-accent font-bold text-xs uppercase tracking-widest">
                    <i class="fas fa-magic"></i> POG's Studio
                </div>
                <div class="md:hidden text-gray-400"><i id="panelChevron" class="fas fa-chevron-up transition-transform duration-300"></i></div>
            </div>

            <div id="controlsContent" class="panel-expanded grid grid-cols-1 lg:grid-cols-12 gap-0 lg:divide-x divide-[#222]">
                
                <!-- BÖLÜM 1: ÇİFT YÜKLEME (YÜZ + ÜRÜN) --><div class="lg:col-span-4 p-4 grid grid-cols-2 gap-3 border-b md:border-b-0 border-[#222]">
                    
                    <!-- 1. Kutu: YÜZ -->
                    <div class="flex flex-col gap-2">
                        <span class="text-[9px] font-bold text-gray-500 uppercase tracking-wider text-center">1. MÜŞTERİ YÜZÜ</span>
                        <input type="file" id="faceUpload" accept="image/*" class="hidden">
                        
                        <label id="faceUploadBox" class="flex flex-col items-center justify-center w-full h-32 border border-dashed border-[#444] hover:border-accent rounded-sm cursor-pointer bg-[#111] transition-colors group relative">
                            <div class="text-center group-hover:scale-105 transition-transform z-10">
                                <i class="fas fa-user-circle text-gray-500 mb-2 text-2xl group-hover:text-accent-light"></i>
                                <p class="text-[8px] text-gray-500 font-bold uppercase group-hover:text-accent-light">Yüz Yükle</p>
                            </div>
                        </label>

                        <div id="facePreviewContainer" class="hidden relative h-32 group">
                            <img id="facePreview" src="#" class="w-full h-full object-cover rounded-sm border border-[#333] opacity-80">
                            <button id="changeFaceBtn" class="absolute inset-0 bg-black/70 text-white text-[9px] font-bold flex items-center justify-center uppercase opacity-0 group-hover:opacity-100 transition-opacity">Değiştir</button>
                        </div>
                    </div>

                    <!-- 2. Kutu: ÜRÜN/SS YÜKLEME -->
                    <div class="flex flex-col gap-2">
                        <span class="text-[9px] font-bold text-gray-500 uppercase tracking-wider text-center">2. ÜRÜN GÖRSELİ (SS)</span>
                        <input type="file" id="productUpload" accept="image/*" class="hidden">
                        
                        <label id="productUploadBox" class="flex flex-col items-center justify-center w-full h-32 border border-dashed border-[#444] hover:border-accent rounded-sm cursor-pointer bg-[#111] transition-colors group relative">
                            <div class="text-center group-hover:scale-105 transition-transform z-10">
                                <i class="fas fa-tshirt text-gray-500 mb-2 text-2xl group-hover:text-accent-light"></i>
                                <p class="text-[8px] text-gray-500 font-bold uppercase group-hover:text-accent-light">SS / Foto Yükle</p>
                            </div>
                        </label>

                        <div id="productPreviewContainer" class="hidden relative h-32 group">
                            <img id="productPreview" src="#" class="w-full h-full object-cover rounded-sm border border-[#333] opacity-80">
                            <button id="changeProductBtn" class="absolute inset-0 bg-black/70 text-white text-[9px] font-bold flex items-center justify-center uppercase opacity-0 group-hover:opacity-100 transition-opacity">Değiştir</button>
                        </div>
                    </div>
                </div>

                <!-- BÖLÜM 2: AYARLAR --><div class="lg:col-span-6 p-4 flex flex-col gap-3 border-b md:border-b-0 border-[#222]">
                    
                    <div class="grid grid-cols-1 gap-4">
                        <div class="flex bg-[#111] rounded-sm p-1 border border-[#222] h-9">
                            <label class="flex-1 cursor-pointer">
                                <input type="radio" name="modelGender" value="woman" class="product-radio hidden" checked>
                                <div class="h-full flex items-center justify-center rounded-sm text-sm text-gray-400 gap-2">
                                    <i class="fas fa-venus"></i> <span class="text-[10px] font-bold">KADIN</span>
                                </div>
                            </label>
                            <label class="flex-1 cursor-pointer">
                                <input type="radio" name="modelGender" value="man" class="product-radio hidden">
                                <div class="h-full flex items-center justify-center rounded-sm text-sm text-gray-400 gap-2">
                                    <i class="fas fa-mars"></i> <span class="text-[10px] font-bold">ERKEK</span>
                                </div>
                            </label>
                        </div>
                        <input type="hidden" id="modelAgeInput" value="adult">
                    </div>

                    <div class="grid grid-cols-3 gap-2 bg-[#151515] p-2 rounded-sm border border-[#222]">
                        <div class="flex flex-col gap-1">
                            <label class="text-[9px] text-gray-500 font-bold uppercase">Boy (cm)</label>
                            <input type="number" id="heightInput" value="170" min="100" max="220" class="w-full bg-[#0a0a0a] border border-[#333] text-white text-xs p-1 rounded-sm text-center font-mono">
                        </div>
                        <div class="flex flex-col gap-1">
                            <label class="text-[9px] text-gray-500 font-bold uppercase">Kilo (kg)</label>
                            <input type="number" id="weightInput" value="60" min="30" max="150" class="w-full bg-[#0a0a0a] border border-[#333] text-white text-xs p-1 rounded-sm text-center font-mono">
                        </div>
                        <div class="flex flex-col gap-1">
                            <label class="text-[9px] text-gray-500 font-bold uppercase">Vücut Tipi</label>
                            <select id="bodyTypeSelect" class="w-full bg-[#0a0a0a] border border-[#333] text-white text-[10px] p-1 rounded-sm h-[26px]">
                                <option value="slim">İnce / Slim</option>
                                <option value="average" selected>Normal / Average</option>
                                <option value="athletic">Atletik / Fit</option>
                                <option value="curvy">Kıvrımlı / Curvy</option>
                                <option value="plus_size">Balık Etli / Plus Size</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 flex-grow">
                        <div class="col-span-2 relative">
                            <select id="styleSelect" class="w-full h-9 bg-[#111] border border-[#333] text-gray-300 text-xs rounded-sm px-3 appearance-none hover:border-accent transition-colors">
                                <option value="minimalist_studio">Studio (Clean White)</option>
                                <option value="streetwear_urban">Urban Casual (Günlük)</option>
                                <option value="vintage_moody">Cozy Home (Ev Hali)</option>
                                <option value="luxury_editorial">High-Fashion Editorial</option>
                                <option value="outdoor_natural">Natural Garden (Dış Çekim)</option>
                            </select>
                            <i class="fas fa-chevron-down absolute right-3 top-2.5 text-[10px] text-gray-500 pointer-events-none"></i>
                        </div>
                        
                        <div class="col-span-2">
                            <textarea id="customRequestInput" placeholder="Ek talepleriniz? (Örn: Saçlar toplu olsun, güneş gözlüğü ekle...)" class="w-full h-16 bg-[#0a0a0a] border border-[#333] text-gray-300 text-xs p-2 rounded-sm resize-none focus:border-accent transition-colors"></textarea>
                        </div>
                    </div>
                </div>

                <!-- BÖLÜM 3: BUTON --><div class="lg:col-span-2 p-4 flex flex-col gap-2 justify-center bg-[#151515]">
                    <button id="startButton" class="w-full h-12 md:h-full min-h-[48px] bg-accent text-white rounded-sm font-bold text-xs tracking-[0.15em] btn-neon flex items-center justify-center gap-2 uppercase">
                        <span id="startBtnText">GİYDİR</span>
                        <i id="startBtnIcon" class="fas fa-magic text-sm"></i>
                    </button>
                    
                    <button id="stopButton" class="hidden w-full h-12 md:h-full min-h-[48px] bg-red-900/80 text-white rounded-sm font-bold text-xs border border-red-800 flex items-center justify-center gap-2 hover:bg-red-800 transition-colors">
                        <span class="loader w-3 h-3 border-2"></span> İptal
                    </button>
                    
                    <button id="clearGalleryBtn" class="hidden mt-1 text-[9px] text-gray-500 hover:text-red-400 transition-colors uppercase tracking-widest flex items-center justify-center w-full py-1 opacity-70 hover:opacity-100">
                        <i class="fas fa-trash-alt mr-2"></i> Temizle
                    </button>
                </div>
            </div>
        </div>

        <!-- GALERİ ALANI --><div id="outputContainer" class="flex-grow rounded-lg bg-[#0f0f0f] border border-[#222] relative overflow-y-auto custom-scrollbar p-4 shadow-inner min-h-0">
            
            <div id="messageBox" class="absolute inset-0 flex flex-col items-center justify-center text-gray-600 select-none pointer-events-none p-4 text-center">
                <div class="flex gap-4 mb-4 opacity-50">
                    <div class="w-12 h-12 rounded-full border border-[#333] flex items-center justify-center bg-[#111]"><i class="fas fa-user text-xl text-accent-light"></i></div>
                    <div class="flex items-center text-[#333]"><i class="fas fa-plus"></i></div>
                    <div class="w-12 h-12 rounded-full border border-[#333] flex items-center justify-center bg-[#111]"><i class="fas fa-camera text-xl text-accent-light"></i></div>
                </div>
                <p class="text-sm font-bold tracking-[0.3em] text-accent-light uppercase">POG's SANAL KABİN</p>
                <p class="text-[10px] text-gray-500 mt-2 font-mono">1. Yüzünü Yükle &nbsp;|&nbsp; 2. Ürün Görselini (SS) Yükle</p>
            </div>

            <div id="loadingIndicator" class="hidden absolute inset-x-0 top-0 z-10 flex flex-col items-center justify-center pt-12 pb-12 pointer-events-none bg-gradient-to-b from-[#0f0f0f] to-transparent">
                <div class="loader mb-4 border-t-accent-light"></div>
                <p class="text-accent-light text-[10px] font-mono tracking-widest uppercase">POG's Modelleri Hazırlanıyor... (<span id="progressCount">0</span>/3)</p>
            </div>

            <div id="galleryContainer" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 pb-20"></div>
        </div>
    </div>

    <script>
        // Sayfa Yüklenince Yapılandırmayı Uygula
        document.addEventListener('DOMContentLoaded', () => {
            
            // 1. Ayarları Uygula
            if (typeof APP_CONFIG !== 'undefined') {
                const root = document.documentElement;
                root.style.setProperty('--color-theme-primary', APP_CONFIG.colors.primary);
                root.style.setProperty('--color-theme-secondary', APP_CONFIG.colors.secondary);
                root.style.setProperty('--color-theme-bg-dark', APP_CONFIG.colors.background);
                
                const brandNameEl = document.getElementById('headerBrandName');
                const brandSubEl = document.getElementById('headerBrandSub');
                if(brandNameEl) brandNameEl.textContent = APP_CONFIG.brandName;
                if(brandSubEl) brandSubEl.textContent = APP_CONFIG.brandSubtitle;
            }

            // DOM Elementleri
            const faceUpload = document.getElementById('faceUpload');
            const facePreview = document.getElementById('facePreview');
            const faceUploadBox = document.getElementById('faceUploadBox');
            const facePreviewContainer = document.getElementById('facePreviewContainer');
            const changeFaceBtn = document.getElementById('changeFaceBtn');

            // Ürün (SS) Elementleri
            const productUpload = document.getElementById('productUpload');
            const productPreview = document.getElementById('productPreview');
            const productUploadBox = document.getElementById('productUploadBox');
            const productPreviewContainer = document.getElementById('productPreviewContainer');
            const changeProductBtn = document.getElementById('changeProductBtn');

            const heightInput = document.getElementById('heightInput');
            const weightInput = document.getElementById('weightInput');
            const bodyTypeSelect = document.getElementById('bodyTypeSelect');
            const styleSelect = document.getElementById('styleSelect');
            const customRequestInput = document.getElementById('customRequestInput'); 
            
            const startButton = document.getElementById('startButton');
            const stopButton = document.getElementById('stopButton');
            const outputContainer = document.getElementById('outputContainer');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const messageBox = document.getElementById('messageBox');
            const galleryContainer = document.getElementById('galleryContainer');
            const progressCountSpan = document.getElementById('progressCount');
            const imageModal = document.getElementById('imageModal');
            const modalImage = document.getElementById('modalImage');
            const closeModal = document.getElementById('closeModal');
            const modalDownloadBtn = document.getElementById('modalDownloadBtn');
            const controlsContent = document.getElementById('controlsContent');
            const panelChevron = document.getElementById('panelChevron');
            const mobileStopBtn = document.getElementById('mobileStopBtn');
            const errorMessageDiv = document.getElementById('errorMessage');
            const prevImageBtn = document.getElementById('prevImageBtn');
            const nextImageBtn = document.getElementById('nextImageBtn');
            const clearGalleryBtn = document.getElementById('clearGalleryBtn');

            // Logo İşlemleri
            const logoInput = document.getElementById('logoInput');
            const brandLogoContainer = document.getElementById('brandLogoContainer');
            const brandLogoWrapper = document.getElementById('brandLogoWrapper');
            const logoHint = document.getElementById('logoHint');

            // Global Değişkenler
            let faceBase64 = null;
            let productBase64 = null; 
            let isGenerating = false;
            let generationQueue = [];
            let currentModalImageIndex = -1;
            let currentGalleryImages;
            let isPanelOpen = true;

            // --- LOGO YÖNETİMİ ---
            function loadSavedLogo() {
                const savedLogo = localStorage.getItem('customBrandLogo');
                if (savedLogo) {
                    // Logo varsa: Yükle ve KİLİTLE
                    brandLogoContainer.innerHTML = `
                        <img src="${savedLogo}" class="h-8 md:h-10 object-contain mr-2"> 
                        <span class="brand-studio-text self-center">${APP_CONFIG.brandSubtitle}</span>
                    `;
                    // Tıklamayı ve ipucunu devre dışı bırak
                    brandLogoWrapper.style.cursor = 'default';
                    if(logoHint) logoHint.style.display = 'none';
                    return true; // Kilitli
                }
                return false; // Kilitli değil
            }
            
            // Başlangıçta kontrol et
            const isLogoLocked = loadSavedLogo();

            if(!isLogoLocked && logoInput && brandLogoWrapper) {
                // Sadece kilitli değilse (henüz logo yüklenmediyse) event listener ekle
                
                // Dosya seçilince çalışacak kod
                logoInput.addEventListener('change', (e) => {
                    const file = e.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = (event) => {
                            const result = event.target.result;
                            try {
                                // 1. Kaydet
                                localStorage.setItem('customBrandLogo', result);
                                
                                // 2. Görseli Güncelle
                                brandLogoContainer.innerHTML = `
                                    <img src="${result}" class="h-8 md:h-10 object-contain mr-2"> 
                                    <span class="brand-studio-text self-center">${APP_CONFIG.brandSubtitle}</span>
                                `;
                                
                                // 3. KİLİTLE: Event listener'ları kaldır ve UI'ı güncelle
                                brandLogoWrapper.onclick = null;
                                brandLogoWrapper.ondblclick = null;
                                brandLogoWrapper.style.cursor = 'default';
                                if(logoHint) logoHint.style.display = 'none';
                                
                                showCustomError("Logo başarıyla kaydedildi ve kilitlendi!");
                            } catch (err) { 
                                showCustomError("Logo görseli çok büyük, kaydedilemedi. Daha küçük bir dosya deneyin."); 
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                });

                // Tıklama ile dosya seçiciyi aç
                brandLogoWrapper.onclick = () => logoInput.click();
            }

            // --- GÖRSEL YÜKLEME ---
            function setupImageUpload(inputId, previewId, boxId, containerId, changeBtnId, type) {
                const input = document.getElementById(inputId);
                const preview = document.getElementById(previewId);
                const box = document.getElementById(boxId);
                const container = document.getElementById(containerId);
                const changeBtn = document.getElementById(changeBtnId);

                if(box) box.addEventListener('click', () => input.click());
                
                if(input) {
                    input.addEventListener('change', (e) => {
                        const file = e.target.files[0];
                        if (file) {
                            const reader = new FileReader();
                            reader.onload = (event) => {
                                const dataUrl = event.target.result;
                                preview.src = dataUrl;
                                if(type === 'face') faceBase64 = dataUrl.split(',')[1];
                                if(type === 'product') productBase64 = dataUrl.split(',')[1];
                                box.classList.add('hidden');
                                container.classList.remove('hidden');
                            };
                            reader.readAsDataURL(file);
                        }
                    });
                }

                if(changeBtn) {
                    changeBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        box.classList.remove('hidden');
                        container.classList.add('hidden');
                        input.value = null;
                        if(type === 'face') faceBase64 = null;
                        if(type === 'product') productBase64 = null;
                    });
                }
            }

            // Yükleyicileri Başlat
            setupImageUpload('faceUpload', 'facePreview', 'faceUploadBox', 'facePreviewContainer', 'changeFaceBtn', 'face');
            setupImageUpload('productUpload', 'productPreview', 'productUploadBox', 'productPreviewContainer', 'changeProductBtn', 'product');

            // --- ANA İŞLEM ---
            if(startButton) {
                startButton.addEventListener('click', () => {
                    // API KEY KONTROLÜ
                    if(!APP_CONFIG.apiKey) {
                        showCustomError("Lütfen 'index.html' dosyasını açıp 'APP_CONFIG' bölümüne API anahtarınızı girin.");
                        return;
                    }

                    if (!faceBase64) { showCustomError("Lütfen bir yüz fotoğrafı yükleyin!"); return; }
                    if (!productBase64) { showCustomError("Lütfen bir ürün görseli (SS) yükleyin!"); return; }
                    
                    generationQueue = buildPromptsForTryOn();
                    
                    messageBox.classList.add('hidden');
                    if (loadingIndicator) loadingIndicator.classList.remove('hidden'); 
                    progressCountSpan.textContent = '0';

                    if (window.innerWidth < 1024) {
                        if(isPanelOpen) toggleMobilePanel();
                        if (mobileStopBtn) {
                            mobileStopBtn.classList.remove('hidden');
                            setTimeout(() => mobileStopBtn.classList.remove('translate-y-32', 'opacity-0'), 50);
                        }
                    }

                    isGenerating = true;
                    startButton.classList.add('hidden');
                    if (stopButton) stopButton.classList.remove('hidden');
                    startGenerationLoop();
                });
            }

            function stopAllGeneration() {
                isGenerating = false;
                generationQueue = [];
                
                if(startButton) startButton.classList.remove('hidden');
                if(stopButton) stopButton.classList.add('hidden');
                if(loadingIndicator) loadingIndicator.classList.add('hidden');
                
                if(mobileStopBtn) {
                    mobileStopBtn.classList.add('translate-y-32', 'opacity-0');
                    setTimeout(() => {
                        if(mobileStopBtn) mobileStopBtn.classList.add('hidden');
                    }, 300);
                }
            }

            if(stopButton) stopButton.addEventListener('click', stopAllGeneration);
            if(mobileStopBtn) mobileStopBtn.addEventListener('click', stopAllGeneration);

            async function startGenerationLoop() {
                if (!isGenerating || generationQueue.length === 0) {
                    stopAllGeneration();
                    return;
                }

                const promptToGenerate = generationQueue.shift(); 
                progressCountSpan.textContent = 3 - generationQueue.length;

                try {
                    const generatedImageBase64 = await generateImage(promptToGenerate);
                    
                    if (generatedImageBase64 && isGenerating) {
                        const imageWrapper = document.createElement('div');
                        const imageIndex = 3 - generationQueue.length - 1; 
                        imageWrapper.className = 'group relative rounded-lg image-frame overflow-hidden bg-gray-900 aspect-[2/3] cursor-pointer'; 
                        const imgSrc = `data:image/png;base64,${generatedImageBase64}`;
                        const newImage = document.createElement('img');
                        newImage.src = imgSrc;
                        newImage.className = 'w-full h-full object-cover transition-transform duration-700 md:group-hover:scale-110'; 
                        imageWrapper.onclick = () => openModal(imgSrc, imageIndex); 

                        imageWrapper.appendChild(newImage);
                        galleryContainer.insertBefore(imageWrapper, galleryContainer.firstChild);
                        if (clearGalleryBtn) clearGalleryBtn.classList.remove('hidden');

                        if (generationQueue.length > 0) await new Promise(resolve => setTimeout(resolve, 1000)); 
                        requestAnimationFrame(startGenerationLoop); 
                    }
                } catch (error) {
                    console.error("Hata:", error);
                    showCustomError(error.message);
                    stopAllGeneration();
                }
            }

            // --- YARDIMCI ---
            window.toggleMobilePanel = function() {
                if (window.innerWidth >= 1024) return;
                if (isPanelOpen) {
                    if (controlsContent) {
                        controlsContent.classList.remove('panel-expanded');
                        controlsContent.classList.add('panel-collapsed');
                    }
                    if(panelChevron) panelChevron.style.transform = 'rotate(180deg)';
                } else {
                    if (controlsContent) {
                        controlsContent.classList.remove('panel-collapsed');
                        controlsContent.classList.add('panel-expanded');
                    }
                    if(panelChevron) panelChevron.style.transform = 'rotate(0deg)';
                }
                isPanelOpen = !isPanelOpen;
            }

            function showCustomError(message) {
                if(errorMessageDiv) {
                    errorMessageDiv.innerHTML = message;
                    errorMessageDiv.style.display = 'block';
                    setTimeout(() => errorMessageDiv.style.display = 'none', 5000);
                } else {
                    alert(message);
                }
            }

            function downloadImage(dataUrl) {
                const link = document.createElement('a');
                link.href = dataUrl;
                link.download = `pogs_tryon_${new Date().getTime()}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }

            // --- API ---
            const stylePrompts = {
                'minimalist_studio': "High-key clean studio shot. White backdrop. Soft, bright lighting. Cheerful and confident vibe.",
                'streetwear_urban': "Casual daily wear setting. City street or cafe background. Natural daylight.",
                'vintage_moody': "Cozy home setting. Sofa, window light, warm tones. Relaxed atmosphere.",
                'luxury_editorial': "High-end fashion editorial. Dramatic lighting, architectural background.",
                'outdoor_natural': "Outdoor garden setting. Greenery, sunlight, organic vibe."
            };

            const shotPlans = [
                "Full body shot showing the complete outfit and how it fits the body type.",
                "Medium shot (waist up) focusing on how the upper part of the garment looks.",
                "Dynamic pose shot showing movement and fit."
            ];

            async function generateImage(prompt) {
                const apiKey = APP_CONFIG.apiKey; 
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key=${apiKey}`;
                
                const payload = {
                    contents: [{ 
                        parts: [
                            { text: prompt }, 
                            { inlineData: { mimeType: "image/png", data: faceBase64 } }, 
                            { inlineData: { mimeType: "image/png", data: productBase64 } } 
                        ] 
                    }],
                    generationConfig: { responseModalities: ['IMAGE'] },
                    safetySettings: [
                        { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_ONLY_LOW" },
                        { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_ONLY_LOW" },
                        { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_ONLY_LOW" },
                        { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_ONLY_LOW" }
                    ]
                };

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    if (response.status === 401) throw new Error("Yetkilendirme Hatası (401). API Anahtarınızı kontrol edin.");
                    throw new Error(`API Hatası: ${response.status}`);
                }

                const result = await response.json();
                const base64Data = result?.candidates?.[0]?.content?.parts?.find(p => p.inlineData)?.inlineData?.data;
                if (!base64Data) {
                    if (result?.promptFeedback?.blockReason) throw new Error("Görsel Güvenlik Politikası nedeniyle engellendi.");
                    throw new Error("Görsel üretilemedi.");
                }
                return base64Data;
            }

            function buildPromptsForTryOn() {
                const modelGender = document.querySelector('input[name="modelGender"]:checked').value;
                const modelAge = 'adult';
                const height = heightInput.value;
                const weight = weightInput.value;
                const bodyType = bodyTypeSelect.options[bodyTypeSelect.selectedIndex].text;
                const selectedBodyTypeVal = bodyTypeSelect.value;
                const style = styleSelect.value;
                const customRequest = customRequestInput.value.trim(); 
                
                let bodyAdjectives = "";
                const bmi = weight / ((height/100) * (height/100));

                if (selectedBodyTypeVal === 'athletic') {
                    bodyAdjectives += "athletic build under clothes, broad shoulders, strong physique, fit, ";
                    if (bmi > 26) bodyAdjectives += "solid build, powerful physique, ";
                    else bodyAdjectives += "lean build, definition, ";
                } else if (selectedBodyTypeVal === 'slim') {
                    bodyAdjectives += "slim, slender, lean, model-like figure, ";
                } else if (selectedBodyTypeVal === 'plus_size') {
                    bodyAdjectives += "plus-size, full-figured, curvy, ";
                } else if (selectedBodyTypeVal === 'curvy') {
                    bodyAdjectives += "curvy, hourglass figure, voluptuous, ";
                } else {
                    if (bmi < 18.5) bodyAdjectives += "slim, slender, ";
                    else if (bmi >= 18.5 && bmi < 25) bodyAdjectives += "average build, fit, standard body, ";
                    else if (bmi >= 25 && bmi < 29) { 
                        if (modelGender === 'man') bodyAdjectives += "broad build, standard male physique, solid, "; 
                        else bodyAdjectives += "standard build, healthy weight, ";
                    }
                    else if (bmi >= 29) bodyAdjectives += "full-figured, plus-size, ";
                }

                let modelType = `${modelAge} ${modelGender}`;
                const baseStylePrompt = stylePrompts[style] || stylePrompts['minimalist_studio'];

                // "SS" (Screenshot) ve Genel Ürün Modu İçin Mantık
                const clothingLogic = `
                CLOTHING RULES (SS / PRODUCT PHOTO MODE):
                1. SOURCE: Image 2 is a user-uploaded image. It might be a direct product photo, a ghost mannequin shot, OR a screenshot of a product page.
                2. TASK: Identify the main garment in Image 2. Ignore text, UI elements, or white backgrounds common in screenshots.
                3. WARPING: "Warp" and "Drape" this garment onto the model defined by Image 1 (Face) and Body Specs.
                4. REALISM: Create natural fabric folds, shadows, and fit based on the body type (${selectedBodyTypeVal}).
                5. CONSISTENCY: Keep the pattern, logo, and color IDENTICAL to the product in Image 2.
                6. MODESTY RULE: The model MUST BE FULLY DRESSED. No exposed skin/nudity unless the item is swimwear.
                `;

                return shotPlans.map(shot => {
                    let finalPrompt = `VIRTUAL TRY-ON TASK (POG's Studio Mode).
                    
                    INPUTS:
                    - Image 1: Reference Face (USER).
                    - Image 2: Reference Clothing (UPLOADED IMAGE/SS).
                    
                    CRITICAL INSTRUCTIONS:
                    1. FACE FIDELITY (PRIORITY #1): The generated model's face MUST BE AN EXACT REPLICA of the face in Image 1. Preserve facial structure, nose shape, eye shape, and expression.
                    2. ${clothingLogic}
                    3. BODY SPECS: ${height}cm, ${weight}kg. Appearance: ${bodyAdjectives} ${modelType}.
                    
                    SCENE DETAILS:
                    Shot: ${shot}
                    Style: ${baseStylePrompt}
                    `;

                    if (customRequest) finalPrompt += `USER CUSTOM REQUEST: ${customRequest}`;

                    finalPrompt += `Negative Prompt: different face, plastic skin, distorted face, mismatched face, changing clothing pattern, wrong logo, nudity, ugly, blurry, low resolution, bad anatomy, topless, open shirt, exposed chest, exposed abs, text, watermark, ui elements.`;
                    
                    return finalPrompt;
                });
            }

            // Modal Events
            function hideModal() {
                if(imageModal) {
                    imageModal.classList.add('opacity-0');
                    setTimeout(() => { imageModal.classList.add('hidden'); modalImage.src = ''; }, 300);
                }
            }
            if(closeModal) closeModal.addEventListener('click', hideModal);
            if(imageModal) imageModal.addEventListener('click', (e) => { if (e.target === imageModal) hideModal(); });
            if(prevImageBtn) prevImageBtn.addEventListener('click', (e) => { e.stopPropagation(); navigateImage(-1); });
            if(nextImageBtn) nextImageBtn.addEventListener('click', (e) => { e.stopPropagation(); navigateImage(1); });

            function navigateImage(direction) {
                const newIndex = currentModalImageIndex + direction;
                if (newIndex >= 0 && newIndex < currentGalleryImages.length) {
                    const newImageWrapper = currentGalleryImages[newIndex];
                    const newImageElement = newImageWrapper.querySelector('img');
                    if (newImageElement) {
                        currentModalImageIndex = newIndex;
                        modalImage.classList.add('opacity-0');
                        setTimeout(() => {
                            modalImage.src = newImageElement.src;
                            modalDownloadBtn.onclick = () => downloadImage(newImageElement.src);
                            modalImage.classList.remove('opacity-0');
                            updateModalNavButtons();
                        }, 300);
                    }
                }
            }
            function updateModalNavButtons() {
                if (currentGalleryImages.length <= 1) {
                    prevImageBtn.classList.add('hidden');
                    nextImageBtn.classList.add('hidden');
                    return;
                }
                prevImageBtn.classList.remove('hidden');
                nextImageBtn.classList.remove('hidden');
                if (currentModalImageIndex === 0) prevImageBtn.classList.add('hidden');
                if (currentModalImageIndex === currentGalleryImages.length - 1) nextImageBtn.classList.add('hidden');
            }
            window.openModal = function(imageSrc, index) {
                currentGalleryImages = Array.from(galleryContainer.querySelectorAll('.group')).reverse();
                currentModalImageIndex = index;
                modalImage.src = imageSrc;
                modalDownloadBtn.onclick = () => downloadImage(imageSrc);
                imageModal.classList.remove('hidden');
                requestAnimationFrame(() => imageModal.classList.remove('opacity-0'));
                updateModalNavButtons();
            }
            
            if(clearGalleryBtn) {
                clearGalleryBtn.addEventListener('click', () => {
                    if(confirm('Galerideki tüm sonuçları silinecek. Emin misiniz?')) {
                        galleryContainer.innerHTML = '';
                        clearGalleryBtn.classList.add('hidden');
                        if (!isGenerating) messageBox.classList.remove('hidden');
                    }
                });
            }

            isPanelOpen = true; 
            if(controlsContent) controlsContent.classList.add('panel-expanded');
        });
    </script>
</body>
</html>