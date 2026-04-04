import streamlit as st
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, get_notebook_sklearn_results, get_pyspark_results

def main():
    sidebar.display()

    # ── Hero Banner ──
    st.markdown("""
    <div class="hero-banner">
        <h1>Du doan gia nha & Phat hien bat thuong</h1>
        <p class="subtitle">
            Nen tang Nha Tot — Du lieu 3 quan TP.HCM: Binh Thanh, Go Vap, Phu Nhuan
        </p>
        <p class="meta">DL07 · K311 · Team 9 — DH Khoa Hoc Tu Nhien TP.HCM</p>
        <p class="meta">GVHD: Thac sy Khuat Thuy Phuong </p>
        <p class="meta">Thực hiện: Doan Nhat Quang — Phan Ngoc Minh Quan</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Metrics Row ──
    notebook_results = get_notebook_sklearn_results()
    pyspark_results = get_pyspark_results()
    best_sklearn_r2 = max(r["R²"] for r in notebook_results)
    best_pyspark_r2 = max(r["R²"] for r in pyspark_results)

    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 28px;">
        <div class="stat-box">
            <div class="stat-icon">📊</div>
            <div class="stat-label">Tong tin dang</div>
            <div class="stat-value">6,979</div>
            <div class="stat-detail">Du lieu thuc te</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">🏘️</div>
            <div class="stat-label">So quan</div>
            <div class="stat-value">3</div>
            <div class="stat-detail">Binh Thanh · Go Vap · Phu Nhuan</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">🤖</div>
            <div class="stat-label">Models da train</div>
            <div class="stat-value">8</div>
            <div class="stat-detail">4 Sklearn + 4 PySpark</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">🎯</div>
            <div class="stat-label">Best R² Sklearn</div>
            <div class="stat-value" style="color: #16a34a;">""" + f"{best_sklearn_r2:.4f}" + """</div>
            <div class="stat-detail">Random Forest</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">⚡</div>
            <div class="stat-label">Best R² PySpark</div>
            <div class="stat-value" style="color: #2563eb;">""" + f"{best_pyspark_r2:.4f}" + """</div>
            <div class="stat-detail">Random Forest</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Two columns: Project overview + Results ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📋 Tổng quan dự án")
        st.markdown("""
        Dự án xây dựng hệ thống **dự đoán giá nhà** và **phát hiện bất thường**
        từ dữ liệu tin đăng bất động sản trên nền tảng Nhà Tốt (nhatot.com).
        """)

        st.markdown("""
        <div class="info-card info-card-blue">
            <h4 style="color: #1d4ed8;">📌 Bài toán 1: Dự đoán giá nhà</h4>
            <ul style="margin: 8px 0; padding-left: 20px; color: #334155;">
                <li><strong>Sklearn (4 models):</strong> Random Forest, Gradient Boosting, Linear Regression, Ridge</li>
                <li><strong>PySpark (4 models):</strong> Random Forest, GBT, Decision Tree, Linear Regression</li>
                <li><strong>Metrics:</strong> MAE, RMSE, R² — đánh giá trên tập test (20%)</li>
                <li><strong>Best Model:</strong> Random Forest Sklearn (R² = 0.846, MAE = 0.140)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card info-card-red">
            <h4 style="color: #dc2626;">📌 Bài toán 2: Phát hiện bất thường</h4>
            <ul style="margin: 8px 0; padding-left: 20px; color: #334155;">
                <li><strong>4 phương pháp kết hợp:</strong> Residual Z-Score (40%), Isolation Forest (30%),
                  Percentile P10-P90 (20%), Min/Max (10%)</li>
                <li><strong>Phân tích theo phân khúc</strong> (Quận × Loại hình)</li>
                <li><strong>Anomaly Score</strong> 0-100 → phân loại 4 mức</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔧 Công nghệ sử dụng")
        st.markdown("""
        | Thành phần | Công nghệ |
        |-----------|-----------|
        | **ML Framework** | Scikit-learn, PySpark MLlib |
        | **Best Model** | Random Forest (R² = 0.846) |
        | **Anomaly** | Composite Score (4 phương pháp) |
        | **Visualization** | Plotly, Matplotlib |
        | **GUI** | Streamlit |
        | **Data** | 6,979 BĐS, 29 features |
        """)

    with col_right:
        st.markdown("### 📊 Bảng tổng hợp kết quả Sklearn")

        import pandas as pd
        df_results = pd.DataFrame(notebook_results)
        df_results.columns = ["Mô hình", "MAE (log)", "RMSE (log)", "R²", "MAE (tỷ)", "RMSE (tỷ)"]
        st.dataframe(
            df_results.style
            .highlight_max(subset=["R²"], color="#bbf7d0", props="font-weight: bold")
            .highlight_min(subset=["MAE (log)"], color="#bbf7d0", props="font-weight: bold")
            .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ)": "{:.3f}", "RMSE (tỷ)": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### ⚡ Bảng tổng hợp kết quả PySpark")
        df_pyspark = pd.DataFrame(pyspark_results)
        df_pyspark_display = df_pyspark[["Model", "R²", "MAE_log", "RMSE_log", "MAE_tỷ", "RMSE_tỷ"]].copy()
        df_pyspark_display.columns = ["Mô hình", "R²", "MAE (log)", "RMSE (log)", "MAE (tỷ)", "RMSE (tỷ)"]
        st.dataframe(
            df_pyspark_display.style
            .highlight_max(subset=["R²"], color="#bfdbfe", props="font-weight: bold")
            .highlight_min(subset=["MAE (log)"], color="#bfdbfe", props="font-weight: bold")
            .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ)": "{:.3f}", "RMSE (tỷ)": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

        df = load_data()
        st.markdown("### 📊 Phân bố dữ liệu (Demo)")
        quan_counts = df["quan"].value_counts()
        st.bar_chart(quan_counts, color="#1a73e8")
        
        st.markdown("### 💰 Phân bố giá bán (Demo, tỷ VNĐ)")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(df["gia_ban"], bins=30, color="#2d6a4f", edgecolor="white", alpha=0.85)
        ax.set_xlabel("Giá bán (tỷ VNĐ)")
        ax.set_ylabel("Số lượng")
        ax.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig)
    
    st.divider()

    # ── Quick Navigation ──
    st.markdown("### 🚀 Bắt đầu sử dụng")

    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 16px;">
        <div class="nav-card">
            <div class="nav-icon">📁</div>
            <h4>Data & EDA</h4>
            <p>Data pipeline, thống kê, feature engineering</p>
        </div>
        <div class="nav-card">
            <div class="nav-icon">🔮</div>
            <h4>Dự đoán giá</h4>
            <p>Nhập thông tin nhà, nhận giá từ 4 models</p>
        </div>
        <div class="nav-card">
            <div class="nav-icon">📈</div>
            <h4>So sánh Models</h4>
            <p>Kết quả 8 models trên 2 nền tảng</p>
        </div>
        <div class="nav-card">
            <div class="nav-icon">🔍</div>
            <h4>Bất thường</h4>
            <p>Phương pháp & kết quả phát hiện giá bất thường</p>
        </div>
        <div class="nav-card">
            <div class="nav-icon">📋</div>
            <h4>Tin đăng</h4>
            <p>Duyệt, lọc tin và xem chi tiết</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    n1, n2, n3, n4, n5 = st.columns(5)
    with n1:
        st.page_link("pages/data_understanding.py", label="→ Data & EDA", icon="📁")
    with n2:
        st.page_link("pages/price_prediction.py", label="→ Dự đoán", icon="🔮")
    with n3:
        st.page_link("pages/model_comparison.py", label="→ Models", icon="📊")
    with n4:
        st.page_link("pages/anomaly_results.py", label="→ Anomaly", icon="🔍")
    with n5:
        st.page_link("pages/posts.py", label="→ Tin đăng", icon="📰")

    # ── Footer ──
    st.markdown("""
    <div class="footer-text">
        DL07 — K311 — Team 9 &nbsp;|&nbsp; ĐH Khoa Học Tự Nhiên TP.HCM &nbsp;|&nbsp;
        GVHD: ThS. Khuất Thùy Phương
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
