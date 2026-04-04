import streamlit as st
from utils.helpers import get_image_base64
import os

def get_avatar_html(image_name, initials):
    """Helper to render avatar from assets or show initials if not found."""
    # Check common extensions
    for ext in ["png", "jpg", "jpeg"]:
        path = f"assets/{image_name}.{ext}"
        if os.path.exists(path):
            img_b64 = get_image_base64(path)
            if img_b64:
                return f'<img src="data:image/{ext};base64,{img_b64}" style="width:64px; height:64px; border-radius:50%; object-fit:cover; margin-bottom:8px; border:2px solid #38bdf8; box-shadow:0 4px 6px -1px rgba(0,0,0,0.5);">'
    
    # Fallback to initials
    return f'<div style="width:64px; height:64px; border-radius:50%; background:#1e293b; color:#94a3b8; display:flex; align-items:center; justify-content:center; margin:0 auto 8px auto; font-size:22px; font-weight:700; border:2px solid #334155;">{initials}</div>'

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
        st.markdown("**🕷️ Bonus**")
        st.page_link(label="🕷️ Data Crawling", page="pages/data_crawling.py")

        st.divider()
        
        avatar_phuong = get_avatar_html("phuong", "P")
        avatar_quang = get_avatar_html("quang", "Q")
        avatar_quan = get_avatar_html("quan", "Q")
        
        st.markdown(
            '<div style="text-align:center; padding:8px 0;">'
            # ── GVHD ──
            '<p style="font-size:10px; font-weight:600; color:#94a3b8 !important; margin:0 0 6px 0; letter-spacing:0.06em;">GIẢNG VIÊN HƯỚNG DẪN</p>'
            f'{avatar_phuong}'
            '<p style="font-size:13px; font-weight:700; color:#f8fafc !important; margin:0;">ThS. Khuất Thùy Phương</p>'
            '<div style="border-top:1px solid rgba(148,163,184,0.15); margin:16px 16px;"></div>'
            # ── Team ──
            '<p style="font-size:10px; font-weight:700; color:#38bdf8 !important; margin:0 0 10px 0; letter-spacing:0.1em; text-transform:uppercase;">Team 9 — DL07 · K311</p>'
            # ── Quang ──
            f'{avatar_quang}'
            '<p style="font-size:12px; font-weight:600; color:#e2e8f0 !important; margin:0;">Đoàn Nhật Quang</p>'
            '<p style="font-size:10px; color:#64748b !important; margin:2px 0 0 0;">Technical Architect at Cyberlogitec VN</p>'
            '<p style="font-size:10px; margin:1px 0 0 0;"><a href="https://www.linkedin.com/in/dnq-httt/" target="_blank" style="color:#38bdf8 !important; text-decoration:none;">linkedin.com/in/dnq-httt</a></p>'
            '<div style="border-top:1px solid rgba(148,163,184,0.12); margin:12px 20px;"></div>'
            # ── Quân ──
            f'{avatar_quan}'
            '<p style="font-size:12px; font-weight:600; color:#e2e8f0 !important; margin:0;">Phan Ngọc Minh Quân</p>'
            '<p style="font-size:10px; color:#64748b !important; margin:2px 0 0 0;">Technical Architect at Cyberlogitec VN</p>'
            '<p style="font-size:10px; color:#64748b !important; margin:1px 0 0 0;">Giảng viên · ĐH Huflit</p>'
            '<p style="font-size:10px; margin:1px 0 0 0;"><a href="https://www.linkedin.com/in/phanquan111" target="_blank" style="color:#38bdf8 !important; text-decoration:none;">linkedin.com/in/phanquan111</a></p>'
            '<div style="border-top:1px solid rgba(148,163,184,0.12); margin:12px 20px;"></div>'
            # ── School ──
            '<p style="font-size:10px; color:#475569 !important; margin:0;">ĐH Khoa Học Tự Nhiên TP.HCM</p>'
            '<p style="font-size:10px; color:#475569 !important; margin:2px 0 0 0;">Trung Tâm Tin Học · 2026</p>'
            '</div>',
            unsafe_allow_html=True
        )
