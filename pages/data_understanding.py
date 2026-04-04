import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import components.sidebar as sidebar
from utils.helpers import get_data_pipeline_info, load_data

def render():
    sidebar.display()

    st.markdown("## 📁 Dữ liệu & Khám phá (EDA)")
    st.markdown("Phân tích dữ liệu tin đăng bất động sản TP.HCM (Nhà Tốt) qua các bước thu thập, tiền xử lý và feature engineering.")

    pipeline = get_data_pipeline_info()
    df = load_data()

    # --- Section: Data Pipeline ---
    st.markdown("### 🔄 1. Quá trình xử lý dữ liệu (Data Pipeline)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="info-card info-card-blue">
            <h4 style="color: #1d4ed8; margin-top: 0;">📥 Dữ liệu thô (Raw)</h4>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['raw_data']['rows']:,}</strong> tin đăng</p>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['raw_data']['cols']}</strong> thuộc tính</p>
            <p style="color: #64748b; margin: 4px 0; font-size: 13px;">Nguồn: {pipeline['raw_data']['sources']} quận trung tâm</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-card info-card-amber">
            <h4 style="color: #d97706; margin-top: 0;">🧹 Sau khi làm sạch</h4>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['after_cleaning']['rows']:,}</strong> tin đăng</p>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['after_cleaning']['cols']}</strong> thuộc tính</p>
            <p style="color: #64748b; margin: 4px 0; font-size: 13px;">Loại bỏ: {pipeline['after_cleaning']['dropped_rows']} dòng lỗi</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="info-card info-card-green">
            <h4 style="color: #16a34a; margin-top: 0;">⚙️ Sau Feature Engineering</h4>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['after_feature_eng']['rows']:,}</strong> tin đăng</p>
            <p style="color: #334155; margin: 4px 0;"><strong>{pipeline['after_feature_eng']['cols']}</strong> thuộc tính</p>
            <p style="color: #64748b; margin: 4px 0; font-size: 13px;">Thêm mới: {pipeline['after_feature_eng']['new_features']} features</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- Section: Features List ---
    st.markdown("### 🛠️ 2. Các nhóm thuộc tính (Features)")

    tabs = st.tabs(list(pipeline["feature_groups"].keys()))
    for i, (group_name, features) in enumerate(pipeline["feature_groups"].items()):
        with tabs[i]:
            st.markdown(f"Danh sách các features thuộc nhóm **{group_name}**:")
            for f in features:
                st.markdown(f"- `{f}`")

    st.divider()

    # --- Section: EDA ---
    st.markdown("### 📊 3. Exploratory Data Analysis (EDA)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Phân bố giá bán (tỷ VNĐ)")
        fig_hist = px.histogram(df, x="gia_ban", nbins=50,
                                color_discrete_sequence=["#3b82f6"],
                                title="Histogram phân bố Giá bán")
        fig_hist.update_layout(
            xaxis_title="Giá bán (tỷ VNĐ)", yaxis_title="Số lượng",
            plot_bgcolor="#fafafa", paper_bgcolor="#ffffff",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c2:
        st.markdown("#### Phân bố theo Quận")
        quan_counts = df["quan"].value_counts().reset_index()
        quan_counts.columns = ["Quận", "Số lượng"]
        fig_pie = px.pie(quan_counts, values="Số lượng", names="Quận",
                         title="Tỷ trọng tin đăng theo Quận",
                         color_discrete_sequence=["#3b82f6", "#22c55e", "#f59e0b"])
        fig_pie.update_layout(
            plot_bgcolor="#fafafa", paper_bgcolor="#ffffff",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("#### Top tương quan (Correlation) với Giá bán")
    corr_df = pd.DataFrame(pipeline["top_correlations"], columns=["Feature", "Hệ số tương quan (r)"])
    fig_bar = px.bar(corr_df, x="Hệ số tương quan (r)", y="Feature", orientation="h",
                     title="Mức độ ảnh hưởng đến giá bán (Linear Correlation)",
                     color="Hệ số tương quan (r)", color_continuous_scale="Blues")
    fig_bar.update_layout(
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor="#fafafa", paper_bgcolor="#ffffff",
        font=dict(family="Inter"),
        height=350,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Thống kê mô tả Giá bán")
    stats = pipeline["price_stats"]
    st.dataframe(pd.DataFrame([
        {"Trung bình (Mean)": f"{stats['mean']} tỷ",
         "Trung vị (Median)": f"{stats['median']} tỷ",
         "Độ lệch chuẩn (Std)": f"{stats['std']}",
         "Giá Min": f"{stats['min']} tỷ",
         "Giá Max": f"{stats['max']} tỷ"}
    ]), use_container_width=True, hide_index=True)

    st.divider()

    # --- Section: Key Insights ---
    st.markdown("### 💡 4. Insights chính từ EDA")
    st.markdown("""
    | Insight | Chi tiết |
    |---------|----------|
    | **Phân bố giá lệch phải** | Skewness = 6.49, Kurtosis = 104.9 → sử dụng log transform |
    | **Log transform hiệu quả** | Skewness giảm còn 0.26, Kurtosis = 1.59 |
    | **Diện tích là yếu tố chính** | Correlation r = 0.69 với giá bán |
    | **Phú Nhuận đắt nhất** | Median 7.85 tỷ vs Gò Vấp 5.95 tỷ |
    | **Multicollinearity** | gia_kv_hien_tai ↔ gia_kv_mean: r = 0.903 |
    """)

render()
