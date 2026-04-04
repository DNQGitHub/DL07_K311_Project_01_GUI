import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()

    st.markdown("# 📊 Business Problem")
    st.divider()

    # Context
    st.markdown("### 🏢 Bối cảnh")
    st.markdown("""
    **Nhà Tốt (nhatot.com)** là nền tảng đăng tin bất động sản hàng đầu Việt Nam.
    Với hàng ngàn tin đăng mỗi ngày, việc **định giá hợp lý** và **phát hiện tin đăng bất thường**
    (giá quá cao hoặc quá thấp so với thị trường) là bài toán thiết thực.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card info-card-blue">
            <h4 style="color: #1d4ed8; margin-top: 0;">🎯 Bài toán 1: Dự đoán giá nhà</h4>
            <p style="color: #334155;">Xây dựng mô hình <strong>Regression</strong> dự đoán giá bán hợp lý dựa trên các đặc trưng
            của căn nhà: diện tích, vị trí, số phòng, loại hình, tiện ích...</p>
            <p style="color: #334155;"><strong>Mục tiêu:</strong> Gợi ý giá đăng bán hợp lý cho người bán,
            giúp người mua đánh giá mức giá.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card info-card-red">
            <h4 style="color: #dc2626; margin-top: 0;">🔍 Bài toán 2: Phát hiện bất thường</h4>
            <p style="color: #334155;">Xây dựng hệ thống phát hiện tin đăng có <strong>giá quá rẻ hoặc quá đắt</strong>
            so với dự đoán và thị trường khu vực.</p>
            <p style="color: #334155;"><strong>Mục tiêu:</strong> Cảnh báo tin đăng bất thường,
            hỗ trợ nền tảng kiểm duyệt chất lượng tin.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Data overview
    st.markdown("### 📁 Dữ liệu")
    st.markdown("""
    Dữ liệu được thu thập từ Nhà Tốt, bao gồm tin đăng bán nhà ở **3 quận TP.HCM**:
    """)

    data_cols = st.columns(3)
    districts = [
        ("Bình Thạnh", "2,665", "32.2%", "#3b82f6"),
        ("Gò Vấp", "4,374", "52.9%", "#22c55e"),
        ("Phú Nhuận", "1,234", "14.9%", "#f59e0b"),
    ]
    for col, (name, count, pct, color) in zip(data_cols, districts):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">{name}</div>
                <div class="stat-value" style="color: {color};">{count}</div>
                <div class="stat-detail">{pct} tổng dữ liệu (raw)</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Methodology
    st.markdown("### ⚙️ Phương pháp")

    st.markdown("#### Bài toán 1 — Prediction Models")
    pred_data = {
        "Môi trường": ["Sklearn", "Sklearn", "Sklearn", "Sklearn", "PySpark", "PySpark", "PySpark", "PySpark"],
        "Model": ["Linear Regression", "Ridge Regression", "Random Forest", "Gradient Boosting",
                   "Linear Regression", "Decision Tree", "Random Forest", "GBT"],
        "Vai trò": ["Baseline (R²=0.734)", "Regularized baseline (R²=0.734)",
                     "🏆 Best model (R²=0.846)", "Ensemble (R²=0.826)",
                     "Baseline (R²=0.685)", "Tree model (R²=0.765)",
                     "🏆 Best PySpark (R²=0.820)", "Ensemble (R²=0.805)"],
    }
    st.dataframe(pred_data, use_container_width=True, hide_index=True)

    st.markdown("#### Bài toán 2 — Anomaly Detection (Composite Score)")
    anom_data = {
        "Phương pháp": ["Residual-z", "Vi phạm Min/Max", "Ngoài P10–P90", "Isolation Forest"],
        "Trọng số": ["w₁ = 0.40", "w₂ = 0.10", "w₃ = 0.20", "w₄ = 0.30"],
        "Ý nghĩa": [
            "Sai số dự đoán chuẩn hóa theo khu vực",
            "Vượt giá tối thiểu / tối đa hợp lý",
            "Giá nằm ngoài khoảng phân vị P10–P90",
            "Phát hiện bất thường đa chiều (unsupervised)",
        ],
    }
    st.dataframe(anom_data, use_container_width=True, hide_index=True)

    st.latex(r"\text{Anomaly Score} = w_1 \times S_{resid} + w_2 \times S_{minmax} + w_3 \times S_{percentile} + w_4 \times S_{ML}")

    st.divider()

    # Data pipeline summary
    st.markdown("### 🔄 Data Pipeline")
    st.markdown("""
    | Giai đoạn | Input | Output | Ghi chú |
    |-----------|-------|--------|---------|
    | **Thu thập** | 3 quận | 8,273 rows × 24 cols | Crawl từ nhatot.com |
    | **Làm sạch** | 8,273 rows | 7,961 rows × 9 cols | Loại 312 dòng lỗi |
    | **Feature Engineering** | 7,961 rows | 6,979 rows × 29 cols | Thêm 20 features mới |
    | **Modeling** | 6,979 rows | 8 models | 80/20 train/test split |
    """)

main()
