import streamlit as st
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, get_notebook_sklearn_results

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
            DL07 · K311 · Team 9 — ĐH Khoa Học Tự Nhiên TP.HCM
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats overview - use actual notebook results
    df = load_data()
    models = train_models()
    notebook_results = get_notebook_sklearn_results()
    best_r2 = max(r["R²"] for r in notebook_results)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Tổng tin đăng (thực tế)", "6,979")
    with col2:
        st.metric("🏘️ Số quận", "3")
    with col3:
        st.metric("🤖 Models đã train", "8", "4 Sklearn + 4 PySpark")
    with col4:
        st.metric("🎯 Best R² (Sklearn)", f"{best_r2:.4f}")
    with col5:
        st.metric("🎯 Best R² (PySpark)", "0.8201")
    
    st.divider()
    
    # Two columns: project overview + features
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📋 Tổng quan dự án")
        st.markdown("""
        Dự án xây dựng hệ thống **dự đoán giá nhà** và **phát hiện bất thường** 
        từ dữ liệu tin đăng bất động sản trên nền tảng Nhà Tốt (nhatot.com).
        
        **Hai bài toán chính:**
        """)

        st.markdown("""
        #### 📌 Bài toán 1: Dự đoán giá nhà
        - **Sklearn (4 models):** Random Forest, Gradient Boosting, Linear Regression, Ridge
        - **PySpark (4 models):** Random Forest, GBT, Decision Tree, Linear Regression
        - **Metrics:** MAE, RMSE, R² — đánh giá trên tập test (20%)
        - **Best Model:** Random Forest Sklearn (R² = 0.846, MAE = 0.140)
        """)
        
        st.markdown("""
        #### 📌 Bài toán 2: Phát hiện bất thường
        - **4 phương pháp kết hợp:** Residual Z-Score (35%), Isolation Forest (30%), 
          Percentile P10-P90 (20%), Min/Max (15%)
        - **Phân tích theo phân khúc** (Quận × Loại hình)
        - **Anomaly Score** 0-100 → phân loại 4 mức
        """)
        
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
            .highlight_max(subset=["R²"], color="#2ecc71", props="font-weight: bold")
            .highlight_min(subset=["MAE (log)"], color="#2ecc71", props="font-weight: bold")
            .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ)": "{:.3f}", "RMSE (tỷ)": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

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

    # Quick navigation
    st.markdown("### 🚀 Bắt đầu sử dụng")
    n1, n2, n3, n4, n5 = st.columns(5)
    with n1:
        st.info("📁 **Data & EDA**\n\nData pipeline, thống kê, feature engineering.")
        st.page_link("pages/data_understanding.py", label="→ Data & EDA", icon="📁")
    with n2:
        st.info("📝 **Dự đoán giá**\n\nNhập thông tin nhà, nhận giá từ models.")
        st.page_link("pages/price_prediction.py", label="→ Dự đoán", icon="🔮")
    with n3:
        st.success("📈 **So sánh Models**\n\nKết quả 8 models trên 2 nền tảng.")
        st.page_link("pages/model_comparison.py", label="→ Models", icon="📊")
    with n4:
        st.warning("🔍 **Bất thường**\n\nXem phương pháp và kết quả phát hiện giá bất thường.")
        st.page_link("pages/anomaly_results.py", label="→ Anomaly", icon="🔍")
    with n5:
        st.info("📋 **Tin đăng**\n\nDuyệt, lọc tin và xem chi tiết.")
        st.page_link("pages/posts.py", label="→ Tin đăng", icon="📰")

if __name__ == "__main__":
    main()
