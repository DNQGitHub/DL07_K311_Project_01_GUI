"""
🔍 Anomaly Detection Results — Bài toán 2: Phát hiện bất thường

Displays anomaly detection methodology, results, and conclusions
for identifying overpriced/underpriced real estate listings.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import components.sidebar as sidebar

from utils.helpers import load_data, train_models, score_all_posts


def render():
    sidebar.display()
    st.markdown("## 🔍 Kết quả phát hiện bất thường — Bài toán 2")
    st.markdown("""
    > **Mục tiêu**: Xác định các tin đăng BĐS có giá **quá rẻ** hoặc **quá đắt** so với thị trường,
    > hỗ trợ Nhà Tốt kiểm duyệt nội dung và bảo vệ người dùng.
    """)

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "📋 Phương pháp",
        "📊 Kết quả phân tích",
        "🏆 Kết luận & Đề xuất",
    ])

    with tab1:
        render_methodology_tab()

    with tab2:
        render_results_tab()

    with tab3:
        render_conclusion_tab()


def render_methodology_tab():
    st.markdown("### 📋 Phương pháp phát hiện bất thường")

    st.markdown("""
    Hệ thống sử dụng **4 phương pháp kết hợp** để tính **Anomaly Score** (0-100) cho mỗi tin đăng:
    """)

    # Method cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 1️⃣ Residual Z-Score (Trọng số: 35%)
        
        Đo **khoảng cách** giữa giá thực và giá dự đoán:
        
        ```
        z = (giá_thực - giá_dự_đoán - μ) / σ
        ```
        
        - Tính **theo phân khúc** (quận × loại hình)
        - |z| > 2 → nghi ngờ bất thường
        - |z| > 3 → rất bất thường
        """)

        st.markdown("""
        #### 2️⃣ Min/Max Violation (Trọng số: 15%)
        
        Kiểm tra giá có **nằm ngoài biên** cực trị:
        
        - Giá < P1 (percentile 1%) → quá rẻ
        - Giá > P99 (percentile 99%) → quá đắt
        - Tính riêng cho từng **phân khúc thị trường**
        """)

    with col2:
        st.markdown("""
        #### 3️⃣ Percentile Check — P10/P90 (Trọng số: 20%)
        
        Kiểm tra giá trong **khoảng hợp lý**:
        
        - Giá < P10 → giá thấp hơn 90% phân khúc
        - Giá > P90 → giá cao hơn 90% phân khúc
        - Mức độ bất thường tỷ lệ với **khoảng cách vượt biên**
        """)

        st.markdown("""
        #### 4️⃣ Isolation Forest (Trọng số: 30%)
        
        Mô hình **unsupervised** phát hiện outlier:
        
        - Dựa trên **24 features** (vị trí, diện tích, tiện nghi...)
        - Xác định các mẫu **khác biệt** so với đa số
        - `contamination = 5%` (kỳ vọng ~5% bất thường)
        """)

    st.markdown("---")

    # Composite formula
    st.markdown("#### 📐 Công thức Composite Score")
    st.code("""
    Anomaly_Score = 0.35 × S_residual + 0.15 × S_minmax + 0.20 × S_percentile + 0.30 × S_isolation_forest

    Trong đó: mỗi S ∈ [0, 1], Anomaly_Score ∈ [0, 100]
    """, language="text")

    st.markdown("""
    | Anomaly Score | Nhãn | Ý nghĩa |
    |:---:|:---:|:---|
    | **≥ 70** | 🔴 Rất bất thường | Cần kiểm duyệt ngay — khả năng cao lừa đảo / sai thông tin |
    | **50-69** | 🟠 Bất thường | Giá chênh lệch đáng kể so với thị trường |
    | **30-49** | 🟡 Cần xem xét | Có dấu hiệu bất thường nhẹ |
    | **< 30** | 🟢 Bình thường | Giá hợp lý so với phân khúc |
    """)

    # Segment-based approach
    st.markdown("---")
    st.markdown("#### 🎯 Cải tiến: Phân tích theo phân khúc (Segment-based)")
    st.info("""
    **Thay vì so sánh toàn bộ dữ liệu**, hệ thống phân tích theo từng phân khúc:
    
    - **Quận** × **Loại hình** (VD: "Nhà mặt tiền tại Bình Thạnh")
    - Tính riêng thống kê (P10, P90, μ, σ) cho mỗi phân khúc
    - Giúp tránh **false positive**: nhà rẻ ở Gò Vấp không bị đánh là bất thường khi so với Phú Nhuận
    """)


def render_results_tab():
    st.markdown("### 📊 Kết quả phân tích bất thường")

    # Load and score data
    df = load_data()
    models = train_models()
    df_scored = score_all_posts(df, models)

    # Summary stats
    n_total = len(df_scored)
    n_critical = (df_scored["anomaly_score"] >= 70).sum()
    n_warning = ((df_scored["anomaly_score"] >= 50) & (df_scored["anomaly_score"] < 70)).sum()
    n_review = ((df_scored["anomaly_score"] >= 30) & (df_scored["anomaly_score"] < 50)).sum()
    n_normal = (df_scored["anomaly_score"] < 30).sum()

    # Metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🟢 Bình thường", f"{n_normal}", f"{n_normal/n_total*100:.1f}%")
    with col2:
        st.metric("🟡 Cần xem xét", f"{n_review}", f"{n_review/n_total*100:.1f}%")
    with col3:
        st.metric("🟠 Bất thường", f"{n_warning}", f"{n_warning/n_total*100:.1f}%")
    with col4:
        st.metric("🔴 Rất bất thường", f"{n_critical}", f"{n_critical/n_total*100:.1f}%")

    st.markdown("---")

    # Distribution charts
    col_a, col_b = st.columns(2)

    with col_a:
        # Histogram of anomaly scores
        fig_hist = px.histogram(
            df_scored, x="anomaly_score", nbins=50,
            title="📊 Phân phối Anomaly Score",
            labels={"anomaly_score": "Anomaly Score"},
            color_discrete_sequence=["#3498db"],
        )
        fig_hist.add_vline(x=30, line_dash="dash", line_color="#f1c40f", annotation_text="Ngưỡng xem xét")
        fig_hist.add_vline(x=50, line_dash="dash", line_color="#e67e22", annotation_text="Ngưỡng bất thường")
        fig_hist.add_vline(x=70, line_dash="dash", line_color="#e74c3c", annotation_text="Ngưỡng nguy hiểm")
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        # Pie chart
        pie_data = pd.DataFrame([
            {"Nhãn": "🟢 Bình thường", "Số lượng": int(n_normal), "Color": "#2ecc71"},
            {"Nhãn": "🟡 Cần xem xét", "Số lượng": int(n_review), "Color": "#f1c40f"},
            {"Nhãn": "🟠 Bất thường", "Số lượng": int(n_warning), "Color": "#e67e22"},
            {"Nhãn": "🔴 Rất bất thường", "Số lượng": int(n_critical), "Color": "#e74c3c"},
        ])
        fig_pie = px.pie(
            pie_data, values="Số lượng", names="Nhãn",
            title="📊 Tỷ lệ phân loại",
            color="Nhãn",
            color_discrete_map={
                "🟢 Bình thường": "#2ecc71",
                "🟡 Cần xem xét": "#f1c40f",
                "🟠 Bất thường": "#e67e22",
                "🔴 Rất bất thường": "#e74c3c",
            },
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Scatter: Actual vs Predicted with anomaly coloring
    st.markdown("#### 🎯 Giá thực vs Giá dự đoán (màu theo mức bất thường)")

    fig_scatter = px.scatter(
        df_scored, x="gia_du_bao", y="gia_ban",
        color="anomaly_score",
        color_continuous_scale=["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"],
        hover_data=["tieu_de", "quan", "dien_tich", "anomaly_score", "label"],
        labels={"gia_du_bao": "Giá dự đoán (tỷ VNĐ)", "gia_ban": "Giá thực (tỷ VNĐ)"},
        title="Actual vs Predicted — phát hiện giá bất thường",
    )

    # Add y=x line
    max_price = max(df_scored["gia_ban"].max(), df_scored["gia_du_bao"].max())
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_price], y=[0, max_price],
        mode="lines", line=dict(color="rgba(255,255,255,0.5)", dash="dash"),
        name="Giá thực = Dự đoán",
    ))
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # By district
    st.markdown("#### 📍 Phân tích theo Quận")
    col1, col2 = st.columns(2)

    with col1:
        avg_by_district = df_scored.groupby("quan").agg(
            Score_TB=("anomaly_score", "mean"),
            Số_lượng=("anomaly_score", "count"),
            Bất_thường=("anomaly_score", lambda x: (x >= 50).sum()),
        ).reset_index()

        fig_district = px.bar(
            avg_by_district, x="quan", y="Score_TB",
            color="Score_TB", color_continuous_scale="RdYlGn_r",
            title="Anomaly Score trung bình theo Quận",
            text="Score_TB",
        )
        fig_district.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_district.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_district, use_container_width=True)

    with col2:
        avg_by_type = df_scored.groupby("loai_hinh").agg(
            Score_TB=("anomaly_score", "mean"),
            Số_lượng=("anomaly_score", "count"),
            Bất_thường=("anomaly_score", lambda x: (x >= 50).sum()),
        ).reset_index()

        fig_type = px.bar(
            avg_by_type, x="loai_hinh", y="Score_TB",
            color="Score_TB", color_continuous_scale="RdYlGn_r",
            title="Anomaly Score trung bình theo Loại hình",
            text="Score_TB",
        )
        fig_type.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_type.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_type, use_container_width=True)

    st.markdown("---")

    # Top anomalous listings
    st.markdown("#### 🚨 Top tin đăng bất thường nhất")

    filter_level = st.selectbox(
        "Lọc theo mức độ:",
        ["Tất cả bất thường (score ≥ 30)", "🟠 Bất thường (score ≥ 50)", "🔴 Rất bất thường (score ≥ 70)"]
    )

    if "30" in filter_level:
        mask = df_scored["anomaly_score"] >= 30
    elif "50" in filter_level:
        mask = df_scored["anomaly_score"] >= 50
    else:
        mask = df_scored["anomaly_score"] >= 70

    df_filtered = df_scored[mask].sort_values("anomaly_score", ascending=False)

    if len(df_filtered) > 0:
        display_cols = ["tieu_de", "quan", "loai_hinh", "dien_tich", "gia_ban", "gia_du_bao", "anomaly_score", "label", "anomaly_type"]
        display_df = df_filtered[display_cols].copy()
        display_df.columns = ["Tiêu đề", "Quận", "Loại hình", "Diện tích (m²)", "Giá bán (tỷ)", "Giá dự đoán (tỷ)", "Score", "Nhãn", "Loại bất thường"]

        st.dataframe(
            display_df.head(20).style.background_gradient(subset=["Score"], cmap="RdYlGn_r"),
            use_container_width=True,
            hide_index=True,
            height=500,
        )
        st.caption(f"Hiển thị {min(20, len(df_filtered))} / {len(df_filtered)} tin đăng bất thường")
    else:
        st.info("Không có tin đăng nào ở mức độ bất thường đã chọn.")

    # Score breakdown for top item
    if len(df_filtered) > 0:
        st.markdown("---")
        st.markdown("#### 🔎 Chi tiết điểm bất thường — tin đăng bất thường nhất")
        top = df_filtered.iloc[0]
        cols = st.columns(4)
        with cols[0]:
            st.metric("S_residual", f"{top.get('s_resid', 0):.3f}", "Trọng số: 35%")
        with cols[1]:
            st.metric("S_minmax", f"{top.get('s_minmax', 0):.3f}", "Trọng số: 15%")
        with cols[2]:
            st.metric("S_percentile", f"{top.get('s_percentile', 0):.3f}", "Trọng số: 20%")
        with cols[3]:
            st.metric("S_isolation_forest", f"{top.get('s_ml', 0):.3f}", "Trọng số: 30%")

        st.markdown(f"""
        **Tin đăng**: {top['tieu_de']}  
        **Giá bán**: {top['gia_ban']:.2f} tỷ | **Giá dự đoán**: {top['gia_du_bao']:.2f} tỷ  
        **Z-Score**: {top.get('z_score', 0):.2f} | **Anomaly Score**: {top['anomaly_score']}  
        **Kết luận**: {top['label']} — {top.get('anomaly_type', '')}
        """)


def render_conclusion_tab():
    st.markdown("### 🏆 Kết luận & Đề xuất — Bài toán 2")

    st.success("""
    #### ✅ Kết quả đạt được
    
    1. **Xây dựng thành công** hệ thống phát hiện bất thường đa phương pháp:
       - Residual Z-Score (rule-based, 35%)
       - Min/Max Violation Check (rule-based, 15%)
       - Percentile Range P10-P90 (statistical, 20%)
       - Isolation Forest (ML-based, 30%)
    
    2. **Phân tích theo phân khúc** (Quận × Loại hình) → giảm false positive
    
    3. **Anomaly Score 0-100** → dễ hiểu, dễ ứng dụng cho đội kiểm duyệt
    """)

    st.markdown("---")

    # Types of anomalies detected
    st.markdown("#### 🎯 Các loại bất thường được phát hiện")

    col1, col2 = st.columns(2)
    with col1:
        st.error("""
        **🔻 Giá THẤP bất thường:**
        - Giá bán < P10 phân khúc tương ứng
        - Residual z-score âm lớn (< -2)
        - **Rủi ro**: Lừa đảo, thông tin sai, nhà có vấn đề pháp lý
        """)

    with col2:
        st.warning("""
        **🔺 Giá CAO bất thường:**
        - Giá bán > P90 phân khúc tương ứng
        - Residual z-score dương lớn (> 2)
        - **Rủi ro**: Đẩy giá, thông tin phóng đại, thổi giá BĐS
        """)

    st.markdown("---")

    # Extra signals from notebook
    st.markdown("#### 📌 Dấu hiệu bất thường bổ sung")
    st.markdown("""
    Ngoài Anomaly Score, hệ thống còn theo dõi các **tín hiệu văn bản** từ tin đăng:
    
    | Tín hiệu | Ý nghĩa | Ảnh hưởng |
    |-----------|----------|-----------|
    | `is_ban_gap` = 1 | Tin đăng "BÁN GẤP" | Có thể giá thấp hơn bình thường |
    | `is_ngop_bank` = 1 | "Ngộp bank" / cần tiền gấp | Giá thấp bất thường có thể hợp lý |
    | `is_no_hau` = 1 | Nhà nở hậu (diện tích tăng) | Giá cao hơn bình thường |
    | `is_nha_nat` = 1 | Nhà nát / cần sửa | Giá thấp có thể hợp lý |
    | `has_quy_hoach` = 1 | Có quy hoạch | Giá có thể bị ảnh hưởng |
    """)

    st.markdown("---")

    # Recommendations
    st.markdown("#### 🚀 Đề xuất ứng dụng")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        **Cho đội kiểm duyệt Nhà Tốt:**
        1. 🔴 Score ≥ 70 → **Auto-flag**, review bắt buộc
        2. 🟠 Score 50-69 → **Soft warning**, ưu tiên review
        3. 🟡 Score 30-49 → **Monitor**, xem xét nếu có thêm báo cáo
        4. 🟢 Score < 30 → **Approve**, tự động duyệt
        """)

    with col_b:
        st.markdown("""
        **Cải thiện trong tương lai:**
        1. 📱 **Real-time scoring** khi tin đăng mới
        2. 📊 **Dashboard monitoring** cho quản lý
        3. 🔄 **Feedback loop** — cập nhật model từ kết quả kiểm duyệt
        4. 🧠 **NLP** — phân tích nội dung mô tả để phát hiện bất thường
        """)

    st.markdown("---")

    # Final box
    st.info("""
    **📝 Tóm tắt**: Hệ thống phát hiện bất thường kết hợp **quy luật thống kê** (Residual, Percentile, Min/Max)
    với **Machine Learning** (Isolation Forest) để đánh giá từng tin đăng. Việc phân tích theo **phân khúc thị trường**
    giúp hệ thống chính xác hơn, tránh đánh giá sai khi so sánh giữa các khu vực có mức giá khác nhau.
    
    Kết quả: ngưỡng **top 5%** (95th percentile) được đề xuất làm mức "bất thường" — phù hợp với
    thực tế thị trường BĐS (khoảng 5-10% tin đăng có thể cần kiểm tra thêm).
    """)

render()
