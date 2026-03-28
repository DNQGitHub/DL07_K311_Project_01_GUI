import streamlit as st
import components.sidebar as sidebar
from utils.helpers import load_data, train_models

def main():
    sidebar.display()
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 50%, #2d6a4f 100%); 
                padding: 40px; border-radius: 16px; margin-bottom: 24px;">
        <h1 style="color: #fff; margin: 0; font-size: 36px;">🏠 Dự đoán giá nhà & Phát hiện bất thường</h1>
        <p style="color: #a0c4ff; font-size: 18px; margin-top: 8px;">
            Nền tảng Nhà Tốt — Dữ liệu 3 quận TP.HCM: Bình Thạnh, Gò Vấp, Phú Nhuận
        </p>
        <p style="color: #ccc; font-size: 14px; margin-top: 4px;">
            DL07 · K311 · Team 2 — ĐH Khoa Học Tự Nhiên TP.HCM
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats overview
    df = load_data()
    models = train_models()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Tổng tin đăng", f"{len(df):,}")
    with col2:
        st.metric("🏘️ Số quận", df["quan"].nunique())
    with col3:
        st.metric("💰 Giá trung vị", f"{df['gia_ban'].median():.2f} tỷ")
    with col4:
        st.metric("🎯 Model R²", f"{models['test_score']:.3f}")
    
    st.divider()
    
    # Two columns: project overview + features
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📋 Tổng quan dự án")
        st.markdown("""
        Dự án xây dựng hệ thống **dự đoán giá nhà** và **phát hiện bất thường** 
        từ dữ liệu tin đăng bất động sản trên nền tảng Nhà Tốt (nhatot.com).
        
        **Hai bài toán chính:**
        1. **Dự đoán giá** — Regression với Random Forest, XGBoost, Linear Regression, SVR 
           trên cả Sklearn và PySpark
        2. **Phát hiện bất thường** — Composite Score kết hợp Residual-z, Isolation Forest, 
           Percentile range, Min/Max violation
        """)
        
        st.markdown("### 🔧 Công nghệ sử dụng")
        st.markdown("""
        - **ML Framework**: Scikit-learn, PySpark MLlib
        - **Best Model**: Random Forest (Sklearn R²≈0.84, PySpark R²≈0.82)
        - **Anomaly Detection**: Composite Score (4 phương pháp × trọng số)
        - **GUI**: Streamlit
        """)
    
    with col_right:
        st.markdown("### 📊 Phân bố dữ liệu theo quận")
        quan_counts = df["quan"].value_counts()
        st.bar_chart(quan_counts, color="#1a73e8")
        
        st.markdown("### 💰 Phân bố giá bán (tỷ VNĐ)")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(df["gia_ban"], bins=30, color="#2d6a4f", edgecolor="white", alpha=0.85)
        ax.set_xlabel("Giá bán (tỷ VNĐ)")
        ax.set_ylabel("Số lượng")
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig)
    
    st.divider()
    
    # Quick navigation
    st.markdown("### 🚀 Bắt đầu sử dụng")
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.info("📝 **Nhập thông tin nhà**\n\nNhập thông số căn nhà để nhận giá dự báo và kiểm tra bất thường.")
        st.page_link("pages/price_prediction.py", label="→ Dự đoán giá", icon="🔮")
    with nav2:
        st.info("📋 **Xem danh sách tin đăng**\n\nDuyệt, lọc và tìm kiếm trong bộ dữ liệu tin đăng.")
        st.page_link("pages/posts.py", label="→ Danh sách tin đăng", icon="📰")
    with nav3:
        st.info("🔍 **Chi tiết tin đăng**\n\nXem chi tiết từng tin đăng kèm phân tích bất thường.")
        st.page_link("pages/post_detail.py", label="→ Chi tiết & Anomaly", icon="🔍")

main()
