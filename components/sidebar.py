import streamlit as st

def display():
    with st.sidebar:
        st.markdown("### 🏠 Dự đoán giá nhà")
        st.markdown("##### & Phát hiện bất thường")
        st.markdown("*Nhà Tốt — TP.HCM*")
        st.divider()

        st.markdown("**📋 Tổng quan**")
        st.page_link(label="🏠 Home", page="pages/home.py")
        st.page_link(label="📊 Business Problem", page="pages/business_problem.py")
        st.page_link(label="👥 Task Assignment", page="pages/task_assignment.py")
        
        st.divider()
        st.markdown("**🔮 Dự đoán & Phát hiện**")
        st.page_link(label="📝 Nhập thông tin nhà", page="pages/price_prediction.py")
        
        st.divider()
        st.markdown("**📰 Dữ liệu tin đăng**")
        st.page_link(label="📋 Danh sách tin đăng", page="pages/posts.py")
        st.page_link(label="🔍 Chi tiết tin đăng", page="pages/post_detail.py")

        st.divider()
        st.markdown("**📈 Kết quả & Báo cáo**")
        st.page_link(label="📊 So sánh Models", page="pages/model_comparison.py")
        st.page_link(label="🔍 Kết quả bất thường", page="pages/anomaly_results.py")
        
        st.divider()
        st.markdown(
            "<div style='text-align:center; font-size:12px; color:#888; margin-top:20px;'>"
            "DL07 — K311 — Team 2<br>"
            "ĐH Khoa Học Tự Nhiên TP.HCM"
            "</div>",
            unsafe_allow_html=True
        )
