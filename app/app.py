import streamlit as st
from PIL import Image
import requests
import io
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Sorghum Leaf Drought Detector",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .navbar-brand {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .navbar-nav {
        display: flex;
        gap: 2rem;
    }
    
    .navbar-nav a {
        text-decoration: none;
        color: #34495e;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        padding-bottom: 0.5rem;
    }
    
    .navbar-nav a.active {
        color: #27ae60;
        border-bottom: 2px solid #27ae60;
    }
    
    .btn-login {
        background: #27ae60;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 600;
    }
    
    .upload-box {
        border: 2px dashed #bdc3c7;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: white;
        transition: all 0.3s;
    }
    
    .upload-box:hover {
        border-color: #27ae60;
        background: #f0f9f4;
    }
    
    .btn-browse {
        background: #27ae60;
        color: white;
        padding: 0.7rem 2rem;
        border-radius: 5px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    .btn-browse:hover {
        background: #229954;
    }
    
    .results-table {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .legend {
        display: flex;
        gap: 2rem;
        margin-top: 1.5rem;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .legend-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
    }
    
    .healthy { background: #27ae60; }
    .moderate { background: #f39c12; }
    .severe { background: #e74c3c; }
</style>
""", unsafe_allow_html=True)

# Navbar
col1, col2, col3 = st.columns([3, 4, 1])
with col1:
    st.markdown("### 🌾 Sorghum Leaf Drought Detector")

with col2:
    tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)
    with tab_col1:
        st.markdown("[**Home**](#)")
    with tab_col2:
        st.markdown("[**Upload Image**](#)")
    with tab_col3:
        st.markdown("[**Results**](#)")
    with tab_col4:
        st.markdown("[**About**](#)")

with col3:
    if st.button("🔐 Login", key="login_btn"):
        st.info("Login feature coming soon!")

st.markdown("---")

# Main content
col_left, col_right = st.columns([1, 1], gap="large")

# LEFT COLUMN - Upload
with col_left:
    st.markdown("### Sorghum Leaf Drought Detector")
    st.write("Upload an image of sorghum leaves to detect drought symptoms using AI.")
    st.markdown("⚡ **AI Model:** YOLOV8")
    
    st.markdown("")
    
    # Upload area
    uploaded_file = st.file_uploader(
        "Drag & Drop or Click to Upload Image",
        type=["jpg", "jpeg", "png", "bmp"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Detection section
        st.markdown("### Detection Results")
        
        # Simulated results (replace dengan Roboflow API call)
        results_data = {
            "Healthy Leaf": {"confidence": 0.92, "count": 2, "color": "🟢"},
            "Moderate Drought": {"confidence": 0.85, "count": 2, "color": "🟡"},
            "Severe Drought": {"confidence": 0.79, "count": 1, "color": "🔴"}
        }
        
        # Results table
        st.markdown('<div class="results-table">', unsafe_allow_html=True)
        
        result_cols = st.columns([2, 2, 2])
        with result_cols[0]:
            st.markdown("**Class**")
        with result_cols[1]:
            st.markdown("**Confidence**")
        with result_cols[2]:
            st.markdown("**Count**")
        
        st.markdown("---")
        
        for class_name, data in results_data.items():
            r_col1, r_col2, r_col3 = st.columns([2, 2, 2])
            with r_col1:
                st.write(f"{data['color']} {class_name}")
            with r_col2:
                st.write(f"✓ {data['confidence']}")
            with r_col3:
                st.write(f"{data['count']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN - Example result
with col_right:
    st.markdown("### 👤 Example Result")
    
    # Example image (placeholder)
    st.markdown("""
    <div style="
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    ">
        <p style="color: #7f8c8d; font-size: 3rem;">📸</p>
        <p style="color: #7f8c8d;">Hasil deteksi akan muncul di sini</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Legend")
    st.markdown("""
    <div class="legend">
        <div class="legend-item">
            <div class="legend-dot healthy"></div>
            <span>Healthy</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot moderate"></div>
            <span>Moderate Drought</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot severe"></div>
            <span>Severe Drought</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Note:** Bounding boxes matter for precise detection.
    """)
