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
    /* All sidebar text: headings, paragraphs, labels */
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #e0e0e0 !important;
    }
    /* Navigation section headers (📋 Tổng quan, etc.) */
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"] p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"] span,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    /* Navigation page links */
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span,
    section[data-testid="stSidebar"] a p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p {
        color: #c8d6e5 !important;
    }
    section[data-testid="stSidebar"] a:hover span,
    section[data-testid="stSidebar"] a:hover p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover span {
        color: #ffffff !important;
    }
    /* Active page link */
    section[data-testid="stSidebar"] [aria-current="page"] span,
    section[data-testid="stSidebar"] [aria-current="page"] p,
    section[data-testid="stSidebar"] .stPageLink-active span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    /* Catch-all for any remaining text inside sidebar */
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #c8d6e5 !important;
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

# ─── Navigation Setup ───
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
business_page = st.Page("pages/business_problem.py", title="Business Problem", icon="📊")
task_page = st.Page("pages/task_assignment.py", title="Task Assignment", icon="👥")
prediction_page = st.Page("pages/price_prediction.py", title="Dự đoán giá", icon="📝")
model_page = st.Page("pages/model_comparison.py", title="So sánh Models", icon="📈")
anomaly_page = st.Page("pages/anomaly_results.py", title="Kết quả bất thường", icon="🔍")
posts_page = st.Page("pages/posts.py", title="Danh sách tin đăng", icon="📋")
detail_page = st.Page("pages/post_detail.py", title="Chi tiết tin đăng", icon="🔎")
data_page = st.Page("pages/data_understanding.py", title="Data & EDA", icon="📁")
pg = st.navigation({
    "📋 Tổng quan": [home_page, business_page, task_page],
    "🔮 Dự đoán & Phát hiện": [prediction_page],
    "📰 Dữ liệu": [posts_page, detail_page],
    "📈 Kết quả & Báo cáo": [data_page, model_page, anomaly_page],
})

pg.run()
