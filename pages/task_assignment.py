import streamlit as st
import components.sidebar as sidebar

def main():
    sidebar.display()
    
    st.markdown("# 👥 Task Assignment")
    st.markdown("---")
    
    st.markdown("### Phân công nhiệm vụ — Team 9")
    st.markdown("""
    > **Lớp:** DL07 — K311  
    > **Môn học:** Đồ án AI tốt nghiệp  
    > **Trường:** ĐH Khoa Học Tự Nhiên TP.HCM

    > **Thành viên:** Phan Ngọc Minh Quân, Đoàn Nhật Quang
    """)
       
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
            "✅ Hoàn thành",
            "🔄 Đang làm",
        ],
        "Thành viên": [
            "Phan Ngọc Minh Quân, Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân, Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân, Đoàn Nhật Quang", 
            "Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân", 
            "Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân", 
            "Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân, Đoàn Nhật Quang", 
            "Phan Ngọc Minh Quân, Đoàn Nhật Quang"
        ],
    }
    
    st.dataframe(tasks, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📅 Timeline")
    st.markdown("""
    | Ngày  | Nội dung | Trạng thái |
    |------|----------|-----------|
    | 1 | Thu thập dữ liệu, Data Loading, Cleaning | ✅ |
    | 2 | Feature Engineering, EDA | ✅ |
    | 3–4 | Modeling (Sklearn + PySpark) | ✅ |
    | 5-6 | Anomaly Detection | ✅ |
    | 7 | GUI Streamlit + Báo cáo | 🔄 |
    """)

main()
