import streamlit as st

def display():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 8px 0 4px 0;">
            <p style="font-size: 22px; margin: 0; color: #f8fafc !important;">🏠</p>
            <p style="font-size: 14px; font-weight: 700; margin: 4px 0 2px 0; color: #f8fafc !important; letter-spacing: 0.02em;">
                Dự đoán giá nhà
            </p>
            <p style="font-size: 11px; margin: 0; color: #64748b !important;">
                & Phát hiện bất thường
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size: 11px; text-align: center; color: #64748b !important; margin: 2px 0 0 0;">
            GVHD: ThS. Khuất Thùy Phương
        </p>
        """, unsafe_allow_html=True)

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
        st.page_link(label="📁 Data & EDA", page="pages/data_understanding.py")
        st.page_link(label="📊 So sánh Models", page="pages/model_comparison.py")
        st.page_link(label="🔍 Kết quả bất thường", page="pages/anomaly_results.py")

        st.divider()
        st.markdown(
            "<div style='text-align:center; padding: 12px 0;'>"
            "<p style='font-size: 11px; font-weight: 600; color: #64748b !important; margin: 0 0 6px 0; letter-spacing: 0.05em;'>TEAM 9</p>"
            "<p style='font-size: 12px; color: #94a3b8 !important; margin: 2px 0;'>Đoàn Nhật Quang</p>"
            "<p style='font-size: 10px; color: #64748b !important; margin: 0 0 4px 0;'>dnq.httt@gmail.com</p>"
            "<p style='font-size: 12px; color: #94a3b8 !important; margin: 2px 0;'>Phan Ngọc Minh Quân</p>"
            "<p style='font-size: 10px; color: #64748b !important; margin: 0 0 8px 0;'>quan.phanngocminh.111@gmail.com</p>"
            "<p style='font-size: 10px; color: #475569 !important; margin: 0;'>DL07 — K311</p>"
            "<p style='font-size: 10px; color: #475569 !important; margin: 0;'>ĐH Khoa Học Tự Nhiên TP.HCM</p>"
            "</div>",
            unsafe_allow_html=True
        )
