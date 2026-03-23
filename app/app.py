import streamlit as st
from PIL import Image
import os
import sys
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.roboflow_utils import DroughtDetector
from config import (
    STREAMLIT_PAGE_TITLE,
    STREAMLIT_PAGE_ICON,
    STREAMLIT_LAYOUT,
    MAX_FILE_SIZE
)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .severity-high {
        color: #ff4444;
        font-weight: bold;
        font-size: 24px;
    }
    .severity-medium {
        color: #ff9500;
        font-weight: bold;
        font-size: 24px;
    }
    .severity-low {
        color: #44b700;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'detector' not in st.session_state:
    st.session_state.detector = DroughtDetector()

# ==================== HEADER ====================
st.markdown("# 🌾 Sorgum Drought Detector")
st.markdown("*Sistem deteksi kekeringan pada daun sorgum menggunakan AI*")
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Konfigurasi")
    st.info("""
    **Sorgum Drought Detector** menggunakan teknologi 
    **Computer Vision** dan **Machine Learning** untuk 
    mendeteksi tingkat kekeringan pada daun sorgum.
    
    **Model**: Roboflow Drought Detection v4
    """)

# ==================== MAIN CONTENT ====================
tab1, tab2, tab3 = st.tabs(["📸 Analisis Gambar", "📚 Panduan", "ℹ️ Tentang"])

# ==================== TAB 1: IMAGE ANALYSIS ====================
with tab1:
    st.markdown("### Pilih Sumber Gambar")
    upload_option = st.radio(
        "Pilih metode input:",
        ["Upload File", "URL Gambar"],
        label_visibility="collapsed"
    )
    
    uploaded_file = None
    image_url = None
    
    if upload_option == "Upload File":
        uploaded_file = st.file_uploader(
            "Unggah gambar daun sorgum",
            type=["jpg", "jpeg", "png", "bmp"],
            help=f"Ukuran maksimal: {MAX_FILE_SIZE}MB"
        )
    else:
        image_url = st.text_input(
            "Masukkan URL gambar:",
            placeholder="https://example.com/image.jpg"
        )
    
    # Process image
    if uploaded_file is not None or image_url:
        try:
            # Load and display image
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.markdown("### 📷 Gambar Original")
                st.image(image, use_column_width=True)
            else:
                try:
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    st.markdown("### 📷 Gambar Original")
                    st.image(image, use_column_width=True)
                except:
                    st.error("❌ Tidak bisa load gambar dari URL")
                    st.stop()
            
            # Run detection
            with st.spinner("🔍 Menganalisis gambar..."):
                if isinstance(image_url, str) and image_url:
                    results = st.session_state.detector.predict(image_url)
                elif uploaded_file is not None:
                    # Save temporarily
                    temp_path = f"/tmp/{uploaded_file.name}"
                    os.makedirs("/tmp", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    results = st.session_state.detector.predict(temp_path)
                    try:
                        os.remove(temp_path)
                    except:
                        pass
            
            # Display results
            if results['success']:
                st.success("✅ Analisis selesai!")
                
                severity_data = st.session_state.detector.detect_drought_severity(results)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 📊 Tingkat Keparahan")
                    severity = severity_data['severity']
                    if severity == "Parah":
                        st.markdown(f"<p class='severity-high'>{severity}</p>", unsafe_allow_html=True)
                    elif severity == "Sedang":
                        st.markdown(f"<p class='severity-medium'>{severity}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='severity-low'>{severity}</p>", unsafe_allow_html=True)
                
                with col2:
                    st.metric("Confidence Score", f"{severity_data['confidence']:.1f}%")
                
                with col3:
                    st.metric("Deteksi Area", severity_data['detection_count'])
                
                st.markdown("### 📈 Detail Hasil")
                st.info(severity_data['message'])
                
                with st.expander("🔬 Detail Teknis"):
                    st.json(results['predictions'])
            else:
                st.error(f"❌ Error: {results['error']}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ==================== TAB 2: PANDUAN ====================
with tab2:
    st.markdown("## 📚 Panduan Penggunaan")
    st.markdown("""
    ### 1️⃣ Persiapan Gambar
    - Ambil foto daun sorgum dengan pencahayaan baik
    - Gunakan background yang kontras
    - Pastikan fokus pada area yang ingin dianalisis
    
    ### 2️⃣ Upload Gambar
    - Pilih metode: Upload File atau URL Gambar
    - Klik tombol "Browse Files" untuk upload
    - Atau masukkan URL gambar
    
    ### 3️⃣ Analisis
    - Aplikasi akan menganalisis gambar secara otomatis
    - Proses 10-30 detik
    - Hasil akan ditampilkan dengan visualisasi
    
    ### 4️⃣ Interpretasi Hasil
    - **Tingkat Keparahan**: Ringan, Sedang, atau Parah
    - **Confidence Score**: Kepercayaan deteksi (0-100%)
    - **Deteksi Area**: Jumlah area dengan potensi kekeringan
    """)
    
    st.markdown("### 🔍 Interpretasi Hasil")
    st.table({
        "Tingkat": ["Sehat", "Ringan", "Sedang", "Parah"],
        "Deskripsi": [
            "Tidak ada tanda kekeringan",
            "Awal tanda kekeringan",
            "Kekeringan terlihat jelas",
            "Kekeringan serius"
        ],
        "Aksi": [
            "Monitor berkala",
            "Perhatikan irigasi",
            "Tingkatkan irigasi",
            "Tindakan mendesak"
        ]
    })

# ==================== TAB 3: TENTANG ====================
with tab3:
    st.markdown("## ℹ️ Tentang Aplikasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Teknologi
        - **Frontend**: Streamlit
        - **Backend**: Python
        - **ML Model**: Roboflow
        - **Computer Vision**: OpenCV
        
        ### 📚 Library Utama
        - streamlit
        - roboflow
        - opencv-python-headless
        - numpy
        - pillow
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍💻 Developer
        - **Author**: Lisha Nur Cahyani
        - **GitHub**: [@lishanurcahyani-sketch](https://github.com/lishanurcahyani-sketch)
        
        ### 🔗 Link Penting
        - [Repository GitHub](https://github.com/lishanurcahyani-sketch/Sorgum-Drought-Detector)
        - [Roboflow](https://roboflow.com)
        - [Streamlit Docs](https://docs.streamlit.io)
        """)
    
    st.info("**Versi**: 1.0.0 | **Update**: 2026")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌾 Sorgum Drought Detector © 2026 | Powered by Roboflow & Streamlit</p>
</div>
""", unsafe_allow_html=True)
