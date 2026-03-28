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
        st.info(f"**Dữ liệu thô (Raw)**\n\n"
                f"- **{pipeline['raw_data']['rows']:,}** tin đăng\n"
                f"- **{pipeline['raw_data']['cols']}** thuộc tính\n"
                f"- Nguồn: {pipeline['raw_data']['sources']} quận trung tâm")
    
    with col2:
        st.warning(f"**Sau khi làm sạch (Cleaning)**\n\n"
                   f"- **{pipeline['after_cleaning']['rows']:,}** tin đăng\n"
                   f"- **{pipeline['after_cleaning']['cols']}** thuộc tính\n"
                   f"- Loại bỏ: {pipeline['after_cleaning']['dropped_rows']} dòng lỗi")
        
    with col3:
        st.success(f"**Sau Feature Engineering**\n\n"
                   f"- **{pipeline['after_feature_eng']['rows']:,}** tin đăng\n"
                   f"- **{pipeline['after_feature_eng']['cols']}** thuộc tính\n"
                   f"- Thêm mới: {pipeline['after_feature_eng']['new_features']} features")

    st.markdown("---")

    # --- Section: Features List ---
    st.markdown("### 🛠️ 2. Các nhóm thuộc tính (Features)")
    
    tabs = st.tabs(list(pipeline["feature_groups"].keys()))
    for i, (group_name, features) in enumerate(pipeline["feature_groups"].items()):
        with tabs[i]:
            st.markdown(f"Danh sách các features thuộc nhóm **{group_name}**:")
            for f in features:
                st.markdown(f"- `{f}`")

    st.markdown("---")

    # --- Section: EDA ---
    st.markdown("### 📊 3. Exploratory Data Analysis (EDA)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Phân bố giá bán (tỷ VNĐ)")
        fig_hist = px.histogram(df, x="gia_ban", nbins=50, 
                                color_discrete_sequence=["#3498db"],
                                title="Histogram phân bố Giá bán")
        fig_hist.update_layout(xaxis_title="Giá bán (tỷ VNĐ)", yaxis_title="Số lượng")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with c2:
        st.markdown("#### Phân bố theo Quận")
        quan_counts = df["quan"].value_counts().reset_index()
        quan_counts.columns = ["Quận", "Số lượng"]
        fig_pie = px.pie(quan_counts, values="Số lượng", names="Quận", 
                         title="Tỷ trọng tin đăng theo Quận",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("#### Top tương quan (Correlation) với Giá bán")
    corr_df = pd.DataFrame(pipeline["top_correlations"], columns=["Feature", "Hệ số tương quan (r)"])
    fig_bar = px.bar(corr_df, x="Hệ số tương quan (r)", y="Feature", orientation="h",
                     title="Mức độ ảnh hưởng đến giá bán (Linear Correlation)",
                     color="Hệ số tương quan (r)", color_continuous_scale="Blues")
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
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


render()
