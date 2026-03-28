import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()
    
    st.markdown("# 📊 Business Problem")
    st.markdown("---")
    
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
        <div style="background: #e3f2fd; padding: 20px; border-radius: 12px; border-left: 4px solid #1a73e8;">
            <h4 style="color: #1a73e8; margin-top:0;">🎯 Bài toán 1: Dự đoán giá nhà</h4>
            <p>Xây dựng mô hình <strong>Regression</strong> dự đoán giá bán hợp lý dựa trên các đặc trưng 
            của căn nhà: diện tích, vị trí, số phòng, loại hình, tiện ích...</p>
            <p><strong>Mục tiêu:</strong> Gợi ý giá đăng bán hợp lý cho người bán, 
            giúp người mua đánh giá mức giá.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #fce4ec; padding: 20px; border-radius: 12px; border-left: 4px solid #e53935;">
            <h4 style="color: #e53935; margin-top:0;">🔍 Bài toán 2: Phát hiện bất thường</h4>
            <p>Xây dựng hệ thống phát hiện tin đăng có <strong>giá quá rẻ hoặc quá đắt</strong> 
            so với dự đoán và thị trường khu vực.</p>
            <p><strong>Mục tiêu:</strong> Cảnh báo tin đăng bất thường, 
            hỗ trợ nền tảng kiểm duyệt chất lượng tin.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data overview
    st.markdown("### 📁 Dữ liệu")
    st.markdown("""
    Dữ liệu được thu thập từ Nhà Tốt, bao gồm tin đăng bán nhà ở **3 quận TP.HCM**:
    """)
    
    data_cols = st.columns(3)
    districts = [
        ("Bình Thạnh", "~2,665 tin", "32.2%"),
        ("Gò Vấp", "~4,374 tin", "52.9%"),
        ("Phú Nhuận", "~1,234 tin", "14.9%"),
    ]
    for col, (name, count, pct) in zip(data_cols, districts):
        with col:
            st.markdown(f"""
            <div style="background: #f5f5f5; padding: 16px; border-radius: 10px; text-align: center;">
                <h3 style="margin:0; color:#1a2a4a;">{name}</h3>
                <p style="font-size: 24px; font-weight: 700; color: #1a73e8; margin: 8px 0;">{count}</p>
                <p style="color: #666; margin: 0;">{pct} tổng dữ liệu</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Methodology
    st.markdown("### ⚙️ Phương pháp")
    
    st.markdown("#### Bài toán 1 — Prediction Models")
    pred_data = {
        "Môi trường": ["Sklearn", "Sklearn", "Sklearn", "Sklearn", "PySpark", "PySpark", "PySpark", "PySpark"],
        "Model": ["Linear Regression", "Random Forest", "XGBoost", "SVR", 
                   "Linear Regression", "Random Forest", "GBT", "Decision Tree"],
        "Vai trò": ["Baseline", "🏆 Best model", "Ensemble mạnh", "Nonlinear",
                     "Baseline", "🏆 Best model", "Ensemble mạnh", "Bổ sung"],
    }
    st.dataframe(pred_data, use_container_width=True, hide_index=True)
    
    st.markdown("#### Bài toán 2 — Anomaly Detection (Composite Score)")
    anom_data = {
        "Phương pháp": ["Residual-z", "Vi phạm Min/Max", "Ngoài P10–P90", "Isolation Forest"],
        "Trọng số": ["w₁ = 0.35", "w₂ = 0.15", "w₃ = 0.20", "w₄ = 0.30"],
        "Ý nghĩa": [
            "Sai số dự đoán chuẩn hóa theo khu vực",
            "Vượt giá tối thiểu / tối đa hợp lý",
            "Giá nằm ngoài khoảng phân vị P10–P90",
            "Phát hiện bất thường đa chiều (unsupervised)",
        ],
    }
    st.dataframe(anom_data, use_container_width=True, hide_index=True)
    
    st.latex(r"\text{Anomaly Score} = w_1 \times S_{resid} + w_2 \times S_{minmax} + w_3 \times S_{percentile} + w_4 \times S_{ML}")

main()
