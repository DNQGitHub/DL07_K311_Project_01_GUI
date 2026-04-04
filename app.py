import streamlit as st

st.set_page_config(
    page_title="Dự đoán giá nhà & Phát hiện bất thường",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — Professional Data Science Dashboard Theme
st.markdown("""
<style>
    /* ── Fix Expander Arrow Leak ── */
    details summary > span > span:first-child {
        display: none !important;
    }

    /* ── Global Typography ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"] p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavSeparator"] span,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
    }
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span,
    section[data-testid="stSidebar"] a p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p {
        color: #94a3b8 !important;
        transition: color 0.2s ease;
    }
    section[data-testid="stSidebar"] a:hover span,
    section[data-testid="stSidebar"] a:hover p,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover span {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] [aria-current="page"] span,
    section[data-testid="stSidebar"] [aria-current="page"] p,
    section[data-testid="stSidebar"] .stPageLink-active span {
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #94a3b8 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(148,163,184,0.15);
        margin: 0.8rem 0;
    }

    /* ── Main Content Area ── */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    /* ── Custom Metric Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .metric-card h3 { margin: 0 0 8px 0; font-size: 13px; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-card .value { font-size: 28px; font-weight: 700; color: #0f172a; }

    /* ── Section Cards ── */
    .section-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 16px;
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1a4d2e 100%);
        padding: 48px 40px;
        border-radius: 16px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner h1 { color: #fff; margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; }
    .hero-banner .subtitle { color: #93c5fd; font-size: 1.1rem; margin-top: 10px; font-weight: 400; }
    .hero-banner .meta { color: #94a3b8; font-size: 0.85rem; margin-top: 6px; }

    /* ── Stat Boxes ── */
    .stat-box {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: transform 0.15s ease;
    }
    .stat-box:hover { transform: translateY(-2px); }
    .stat-box .stat-icon { font-size: 24px; margin-bottom: 6px; }
    .stat-box .stat-label { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500; }
    .stat-box .stat-value { font-size: 24px; font-weight: 700; color: #0f172a; margin: 4px 0; }
    .stat-box .stat-detail { font-size: 12px; color: #94a3b8; }

    /* ── Info Cards (for Bài toán 1 & 2) ── */
    .info-card {
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 16px;
        border-left: 4px solid;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .info-card-blue { background: #eff6ff; border-left-color: #3b82f6; }
    .info-card-red { background: #fef2f2; border-left-color: #ef4444; }
    .info-card-green { background: #f0fdf4; border-left-color: #22c55e; }
    .info-card-amber { background: #fffbeb; border-left-color: #f59e0b; }
    .info-card h4 { margin-top: 0; font-weight: 600; }

    /* ── Nav Cards ── */
    .nav-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        height: 100%;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .nav-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59,130,246,0.15);
    }
    .nav-card .nav-icon { font-size: 28px; margin-bottom: 8px; }
    .nav-card h4 { margin: 0 0 6px 0; font-weight: 600; color: #0f172a; font-size: 15px; }
    .nav-card p { margin: 0; font-size: 13px; color: #64748b; line-height: 1.5; }

    /* ── Anomaly Badges ── */
    .badge-normal { background: #dcfce7; color: #166534; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-warning { background: #fef3c7; color: #92400e; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-danger { background: #fecaca; color: #991b1b; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }
    .badge-critical { background: #991b1b; color: #fff; padding: 4px 14px; border-radius: 20px; font-weight: 600; font-size: 13px; }

    /* ── Streamlit Metric Override ── */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #64748b !important;
    }
    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 500;
        padding: 8px 20px;
    }

    /* ── DataFrames ── */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* ── Divider ── */
    hr {
        border-color: #e2e8f0;
    }

    /* ── Footer ── */
    .footer-text {
        text-align: center;
        font-size: 12px;
        color: #94a3b8;
        padding: 20px 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
    }
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
crawl_page = st.Page("pages/data_crawling.py", title="Data Crawling", icon="🕷️")
pg = st.navigation({
    "📋 Tổng quan": [home_page, business_page, task_page],
    "🔮 Dự đoán & Phát hiện": [prediction_page],
    "📰 Dữ liệu": [posts_page, detail_page],
    "📈 Kết quả & Báo cáo": [data_page, model_page, anomaly_page],
    "🕷️ Bonus": [crawl_page],
})

pg.run()
