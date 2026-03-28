import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()
    
    st.markdown("# 👥 Task Assignment")
    st.markdown("---")
    
    st.markdown("### Phân công nhiệm vụ — Team 2")
    st.markdown("""
    > **Lớp:** DL07 — K311  
    > **Môn học:** LDS0 (Capstone Project)  
    > **Trường:** ĐH Khoa Học Tự Nhiên TP.HCM
    """)
    
    st.info("⚠️ Vui lòng cập nhật thông tin thành viên và phân công cụ thể tại đây.")
    
    # Placeholder task table
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
            "01_data_loading",
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
            "🔄 Đang làm",
            "🔄 Đang làm",
        ],
        "Thành viên": [
            "—", "—", "—", "—", "—", "—", "—", "—", "—", "—"
        ],
    }
    
    st.dataframe(tasks, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📅 Timeline")
    st.markdown("""
    | Tuần | Nội dung | Trạng thái |
    |------|----------|-----------|
    | 1–2 | Thu thập dữ liệu, Data Loading, Cleaning | ✅ |
    | 3–4 | Feature Engineering, EDA | ✅ |
    | 5–6 | Modeling (Sklearn + PySpark) | ✅ |
    | 7–8 | Anomaly Detection | ✅ |
    | 9–10 | GUI Streamlit + Báo cáo | 🔄 |
    """)

main()
