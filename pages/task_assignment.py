import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()

    st.markdown("# 👥 Task Assignment")
    st.divider()

    st.markdown("""
    <div class="info-card info-card-blue">
        <p style="color: #334155; margin: 0;">
            <strong>Lớp:</strong> DL07 — K311 &nbsp;|&nbsp;
            <strong>Môn:</strong> Đồ án AI tốt nghiệp &nbsp;|&nbsp;
            <strong>Trường:</strong> ĐH Khoa Học Tự Nhiên TP.HCM
        </p>
        <p style="color: #334155; margin: 4px 0 0 0;">
            <strong>Thành viên:</strong> Phan Ngọc Minh Quân &nbsp;&&nbsp; Đoàn Nhật Quang
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Phân công nhiệm vụ")

    tasks = {
        "Giai đoạn": [
            "Data Collection & Loading",
            "Data Cleaning",
            "Feature Engineering",
            "EDA",
            "Modeling — Sklearn",
            "Modeling — PySpark",
            "Anomaly Detection — Sklearn",
            "Anomaly Detection — PySpark",
            "GUI (Streamlit)",
            "Báo cáo & Presentation",
        ],
        "Notebook": [
            "00_crawl + 01_data_loading",
            "02_data_cleaning",
            "03_feature_engineering",
            "04_eda",
            "05_model_sklearn",
            "06_model_pyspark",
            "07_anomaly_sklearn",
            "08_anomaly_pyspark",
            "Streamlit App",
            "PPTX + Report",
        ],
        "Trạng thái": [
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "✅ Hoàn thành",
            "🔄 Đang làm",
        ],
        "Thành viên": [
            "Quân, Quang",
            "Quân, Quang",
            "Quân, Quang",
            "Quân, Quang",
            "Đoàn Nhật Quang",
            "Phan Ngọc Minh Quân",
            "Đoàn Nhật Quang",
            "Phan Ngọc Minh Quân",
            "Quân, Quang",
            "Quân, Quang",
        ],
    }

    st.dataframe(tasks, use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("### 📅 Timeline")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        | Ngày  | Nội dung | Trạng thái |
        |------|----------|-----------|
        | 1 | Thu thập dữ liệu, Data Loading, Cleaning | ✅ |
        | 2 | Feature Engineering, EDA | ✅ |
        | 3–4 | Modeling (Sklearn + PySpark) | ✅ |
        | 5–6 | Anomaly Detection | ✅ |
        | 7 | GUI Streamlit + Báo cáo | 🔄 |
        """)

    with col2:
        completed = 9
        total = 10
        pct = completed / total * 100
        st.markdown(f"""
        <div class="stat-box" style="margin-top: 8px;">
            <div class="stat-label">Tiến độ tổng thể</div>
            <div class="stat-value" style="color: #16a34a;">{pct:.0f}%</div>
            <div class="stat-detail">{completed}/{total} giai đoạn hoàn thành</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top: 16px;">
            <div style="background: #e2e8f0; border-radius: 10px; height: 12px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #16a34a, #22c55e); width: {pct}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

main()
