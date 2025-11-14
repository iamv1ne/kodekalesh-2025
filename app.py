# app.py - FINAL ADVANCED CANNY + PRO UI
import streamlit as st
import cv2
import numpy as np

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Kuch Toota?",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS — BLACK BG + WHITE TEXT + INTER FONT ===
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
<style>
    html, body, .main, .stApp {background: #000000 !important; color: #ffffff !important;}
    * {font-family: 'Inter', sans-serif !important; color: #ffffff !important;}
    
    .header {padding: 3rem 0; text-align: center;}
    .logo {font-size: 3.5rem; font-weight: 900; letter-spacing: -2px; color: #ffffff;}
    .logo span {color: #00d4ff;}
    .tagline {font-size: 1.3rem; color: #aaaaaa; margin-top: 0.8rem; max-width: 700px; margin-left: auto; margin-right: auto; line-height: 1.6;}
    
    .upload-container {margin: 3rem 0; text-align: center;}
    .upload-box {background: #111111; border: 2px dashed #333; border-radius: 16px; padding: 3.5rem; transition: all 0.3s;}
    .upload-box:hover {border-color: #00d4ff; background: #0a1a2a;}
    
    .result-container {margin: 4rem 0;}
    .result-image {border-radius: 16px; box-shadow: 0 15px 40px rgba(0,0,0,0.6);}
    .result-text {font-size: 2.2rem; font-weight: 800; margin: 2rem 0; text-align: center;}
    .defect {color: #ff4757;}
    .good {color: #2ed573;}
    
    .footer {text-align: center; padding: 4rem 0; color: #666; font-size: 0.95rem;}
    .footer a {color: #00d4ff; text-decoration: none;}
    
    .stFileUploader > div > div {background-color: #111111 !important;}
    .stFileUploader label, .stFileUploader div {color: white !important;}
    .stMarkdown, .stText {color: white !important;}
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown("""
<div class="header">
    <h1 class="logo">KUCH <span>TOOTA?</span></h1>
    <p class="tagline">Advanced Canny edge detection — detects even the smallest cracks.</p>
</div>
""", unsafe_allow_html=True)

# === UPLOAD ===
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("**Drag and drop your image here**", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Read image
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    annotated = img.copy()
    h, w = img.shape[:2]

    # === ADVANCED CANNY EDGE DETECTION ===
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive noise reduction
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Adaptive Canny thresholds
    v = np.median(blurred)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    
    edges = cv2.Canny(blurred, lower, upper)
    
    # Morphological closing to connect broken edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    edge_density = np.sum(edges > 0) / edges.size

    # Central ROI
    x1, y1 = w//4, h//4
    x2, y2 = 3*w//4, 3*h//4

    # Result logic
    if edge_density > 0.008:  # Lowered for sensitivity
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 12)
        cv2.putText(annotated, "DEFECT", (x1, y1-60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 7)
        result_text = '<p class="result-text defect">DEFECT DETECTED</p>'
    else:
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 100, 255), 12)
        cv2.putText(annotated, "GOOD", (x1, y1-60), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 100, 255), 7)
        result_text = '<p class="result-text good">GOOD — NO DEFECT</p>'

    # Display result
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.image(img, width="stretch", caption="Original Image")
    
    with col2:
        st.image(edges, width="stretch", caption="Edge Map")

    with col3:
        st.image(annotated, channels="BGR", width="stretch", caption="AI Analysis")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(result_text, unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class="footer">
    <p>© 2025 Kuch Toota? | Advanced Canny Edge Detection</p>
    <p>Made for <a href="#">KodeKalesh 2025</a></p>
</div>
""", unsafe_allow_html=True)
