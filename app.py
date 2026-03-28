import streamlit as st

st.set_page_config(
    page_title="Dự đoán giá nhà & Phát hiện bất thường",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a2a4a 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #e0e0e0 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }
    
    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #1a73e8;
        margin-bottom: 12px;
    }
    .metric-card h3 { margin: 0 0 8px 0; font-size: 14px; color: #666; }
    .metric-card .value { font-size: 28px; font-weight: 700; color: #1a2a4a; }
    
    /* Anomaly badges */
    .badge-normal { background: #d4edda; color: #155724; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-warning { background: #fff3cd; color: #856404; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-danger { background: #f8d7da; color: #721c24; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-critical { background: #721c24; color: #fff; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

import pages.home
