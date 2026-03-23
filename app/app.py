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

# PAGE CONFIG
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# HEADER
st.markdown("# 🌾 Sorgum Drought Detector")
st.markdown("*Sistem deteksi kekeringan pada daun sorgum menggunakan AI*")
st.markdown("---")

# SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Konfigurasi")
    st.info("""
    **Sorgum Drought Detector** menggunakan teknologi 
    **Computer Vision** dan **Machine Learning** untuk 
    mendeteksi tingkat kekeringan pada daun sorgum.
    """)

# INITIALIZE
if 'detector' not in st.session_state:
    st.session_state.detector = DroughtDetector()

# TABS
tab1, tab2, tab3 = st.tabs(["📸 Analisis Gambar", "📚 Panduan", "ℹ️ Tentang"])

# TAB 1: IMAGE ANALYSIS
with tab1:
    st.markdown("### Pilih Sumber Gambar")
    upload_option = st.radio(
        "Pilih metode input:",
        ["Upload File", "URL Gambar"],
        label_visibility="collapsed"
    )
    
    if upload_option == "Upload File":
        uploaded_file = st.file_uploader(
            "Unggah gambar daun sorgum",
            type=["jpg", "jpeg", "png", "bmp"]
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar Original", use_column_width=True)
            
            if st.button("🔍 Analisis Gambar"):
                with st.spinner("Menganalisis..."):
                    temp_path = f"/tmp/{uploaded_file.name}"
                    os.makedirs("/tmp", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    results = st.session_state.detector.predict(temp_path)
                    
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                
                if results['success']:
                    st.success("✅ Analisis selesai!")
                    severity_data = st.session_state.detector.detect_drought_severity(results)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tingkat Keparahan", severity_data['severity'])
                    with col2:
                        st.metric("Confidence", f"{severity_data['confidence']:.1f}%")
                    with col3:
                        st.metric("Deteksi Area", severity_data['detection_count'])
                    
                    st.info(severity_data['message'])
                else:
                    st.error(f"Error: {results['error']}")
    
    else:
        image_url = st.text_input("Masukkan URL gambar:")
        
        if image_url:
            try:
                image = Image.open(requests.get(image_url, stream=True).raw)
                st.image(image, caption="Gambar Original", use_column_width=True)
                
                if st.button("🔍 Analisis Gambar"):
                    with st.spinner("Menganalisis..."):
                        results = st.session_state.detector.predict(image_url)
                    
                    if results['success']:
                        st.success("✅ Analisis selesai!")
                        severity_data = st.session_state.detector.detect_drought_severity(results)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Tingkat Keparahan", severity_data['severity'])
                        with col2:
                            st.metric("Confidence", f"{severity_data['confidence']:.1f}%")
                        with col3:
                            st.metric("Deteksi Area", severity_data['detection_count'])
                        
                        st.info(severity_data['message'])
                    else:
                        st.error(f"Error: {results['error']}")
            except:
                st.error("❌ Tidak bisa load gambar dari URL")

# TAB 2: PANDUAN
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
    - Klik tombol "Analisis Gambar"
    - Tunggu hasil analisis
    - Hasil akan ditampilkan dengan visualisasi
    """)
    
    st.markdown("### 🔍 Interpretasi Hasil")
    st.table({
        "Tingkat": ["Sehat", "Ringan", "Sedang", "Parah"],
        "Deskripsi": [
            "Tidak ada tanda kekeringan",
            "Awal tanda kekeringan",
            "Kekeringan terlihat jelas",
            "Kekeringan serius"
        ]
    })

# TAB 3: TENTANG
with tab3:
    st.markdown("## ℹ️ Tentang Aplikasi")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🏗️ Teknologi
        - Frontend: Streamlit
        - Backend: Python
        - ML Model: Roboflow
        - Computer Vision: OpenCV
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍💻 Developer
        - Author: Lisha Nur Cahyani
        - GitHub: [@lishanurcahyani-sketch](https://github.com/lishanurcahyani-sketch)
        """)
    
    st.info("**Versi**: 1.0.0 | **Update**: 2026")

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌾 Sorgum Drought Detector © 2026</p>
</div>
""", unsafe_allow_html=True)
