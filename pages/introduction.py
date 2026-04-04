import streamlit as st
import textwrap
import components.sidebar as sidebar
from utils.helpers import get_image_base64
import os


def render_profile_card(name, role, details, initials, image_name=""):
    """Render a professional profile card."""
    img_tag = ""
    found_img = False
    if image_name:
        for ext in ["png", "jpg", "jpeg"]:
            path = f"assets/{image_name}.{ext}"
            if os.path.exists(path):
                img_b64 = get_image_base64(path)
                if img_b64:
                    img_tag = (
                        f'<img src="data:image/{ext};base64,{img_b64}" '
                        f'style="width:110px; height:110px; border-radius:50%; object-fit:cover; '
                        f'border:3px solid #38bdf8; box-shadow:0 6px 20px rgba(56,189,248,0.25);">'
                    )
                    found_img = True
                    break

    if not found_img:
        img_tag = (
            f'<div style="width:110px; height:110px; border-radius:50%; '
            f'background:linear-gradient(135deg, #1e40af, #0ea5e9); color:#fff; '
            f'display:flex; align-items:center; justify-content:center; '
            f'font-size:40px; font-weight:700; border:3px solid #38bdf8; '
            f'box-shadow:0 6px 20px rgba(56,189,248,0.25);">{initials}</div>'
        )

    details = textwrap.dedent(details)
    html = textwrap.dedent(f"""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 32px 24px;
        height: 100%;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
    ">
        <div style="display:flex; justify-content:center; margin-bottom:20px;">
            {img_tag}
        </div>
        <h3 style="color:#f8fafc; margin:0 0 6px 0; font-size:20px; font-weight:700;">{name}</h3>
        <p style="
            color:#38bdf8; font-size:13px; font-weight:600;
            margin:0 0 20px 0;
            background: rgba(56,189,248,0.1);
            display:inline-block;
            padding: 4px 14px;
            border-radius: 20px;
        ">{role}</p>
        <div style="color:#cbd5e1; font-size:14px; line-height:1.7; text-align:left;">
            {details}
        </div>
    </div>
    """)
    return html


def render_reason_card(icon, title, description, color):
    """Render a styled reason/experience card."""
    description = textwrap.dedent(description)
    return textwrap.dedent(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30,41,59,0.7) 0%, rgba(15,23,42,0.9) 100%);
        padding: 24px;
        border-radius: 14px;
        border-left: 4px solid {color};
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    ">
        <div style="display:flex; align-items:flex-start; gap:16px;">
            <div style="
                font-size:28px;
                width:48px; height:48px;
                min-width:48px;
                background: rgba(255,255,255,0.05);
                border-radius:12px;
                display:flex; align-items:center; justify-content:center;
            ">{icon}</div>
            <div>
                <h4 style="color:#f8fafc; margin:0 0 10px 0; font-size:16px; font-weight:600;">{title}</h4>
                <p style="color:#cbd5e1; font-size:14px; line-height:1.7; margin:0;">{description}</p>
            </div>
        </div>
    </div>
    """)


def main():
    sidebar.display()

    # ── Custom page CSS ──
    st.markdown("""
    <style>
        .intro-hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
            padding: 48px 44px;
            border-radius: 20px;
            margin-bottom: 36px;
            position: relative;
            overflow: hidden;
        }
        .intro-hero::before {
            content: '';
            position: absolute;
            top: -60%;
            right: -8%;
            width: 420px;
            height: 420px;
            background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
            border-radius: 50%;
        }
        .intro-hero::after {
            content: '';
            position: absolute;
            bottom: -40%;
            left: -5%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        .intro-section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        .intro-section-title .icon-box {
            width: 40px; height: 40px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
        }
        .intro-section-title h3 {
            margin: 0;
            color: #f8fafc;
            font-size: 22px;
            font-weight: 700;
        }
    </style>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # HERO BANNER
    # ══════════════════════════════════════════════
    st.markdown("""
    <div class="intro-hero">
        <p style="
            color:#38bdf8; font-size:13px; font-weight:600;
            text-transform:uppercase; letter-spacing:2px;
            margin:0 0 12px 0;
        ">DL07 - K311 - Team 9</p>
        <h1 style="
            color:#fff; margin:0 0 12px 0;
            font-size:2.4rem; font-weight:800;
            letter-spacing:-0.02em; line-height:1.2;
        ">Dự đoán giá nhà & Phát hiện bất thường</h1>
        <p style="color:#94a3b8; font-size:16px; margin:0; line-height:1.6; max-width:700px;">
            Đồ án tốt nghiệp khóa học <strong style="color:#cbd5e1;">Data Science and Machine Learning Certificate</strong>
            <br>Trung tâm Tin học - Đại học Khoa học Tự nhiên TP.HCM
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # GIẢNG VIÊN HƯỚNG DẪN
    # ══════════════════════════════════════════════
    phuong_img_b64 = get_image_base64("assets/phuong.png")
    if phuong_img_b64:
        phuong_img_tag = f'<img src="data:image/png;base64,{phuong_img_b64}" style="width:60px; height:60px; min-width:60px; border-radius:14px; object-fit:cover; border:2px solid #f59e0b; box-shadow:0 4px 10px rgba(245,158,11,0.2);">'
    else:
        phuong_img_tag = '<div style="width:52px; height:52px; min-width:52px; background: rgba(245,158,11,0.12); border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:26px;">👩‍🏫</div>'

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px 28px;
        border-radius: 14px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 36px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    ">
        {phuong_img_tag}
        <div>
            <p style="color:#94a3b8; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; margin:0 0 4px 0;">Giảng viên hướng dẫn</p>
            <h3 style="color:#f8fafc; margin:0; font-size:20px; font-weight:700;">Thạc sỹ Khuất Thùy Phương</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # ĐỘI NGŨ THỰC HIỆN
    # ══════════════════════════════════════════════
    st.markdown("""
    <div class="intro-section-title">
        <div class="icon-box" style="background:rgba(56,189,248,0.12);">👥</div>
        <h3>Đội ngũ thực hiện</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        details_quang = """
        <ul style="padding-left:18px; margin:0 0 20px 0; list-style:none;">
            <li style="margin-bottom:10px; padding-left:20px; position:relative;">
                <span style="position:absolute; left:0; color:#38bdf8;">&#9656;</span>
                <strong style="color:#e2e8f0;">Ngành học:</strong>
                <span style="color:#94a3b8;">Công nghệ thông tin</span>
            </li>
            <li style="margin-bottom:10px; padding-left:20px; position:relative;">
                <span style="position:absolute; left:0; color:#38bdf8;">&#9656;</span>
                <strong style="color:#e2e8f0;">Công việc:</strong>
                <span style="color:#94a3b8;">Technical Architect @ Cyberlogitec Vietnam</span>
            </li>
        </ul>
        <div style="text-align:center;">
            <a href="https://www.linkedin.com/in/dnq-httt/" target="_blank" style="
                background: linear-gradient(135deg, #0ea5e9, #0284c7);
                color:white; padding:10px 24px; border-radius:8px;
                text-decoration:none; font-size:13px; font-weight:600;
                display:inline-block; transition:opacity 0.2s;
                box-shadow: 0 4px 12px rgba(14,165,233,0.3);
            ">LinkedIn Profile</a>
        </div>"""
        st.markdown(render_profile_card(
            name="Đoàn Nhật Quang",
            role="Data Science Student",
            details=details_quang,
            initials="Q",
            image_name="quang"
        ), unsafe_allow_html=True)

    with col2:
        details_quan = """
        <ul style="padding-left:18px; margin:0 0 20px 0; list-style:none;">
            <li style="margin-bottom:10px; padding-left:20px; position:relative;">
                <span style="position:absolute; left:0; color:#38bdf8;">&#9656;</span>
                <strong style="color:#e2e8f0;">Ngành học:</strong>
                <span style="color:#94a3b8;">Khoa học máy tính</span>
            </li>
            <li style="margin-bottom:10px; padding-left:20px; position:relative;">
                <span style="position:absolute; left:0; color:#38bdf8;">&#9656;</span>
                <strong style="color:#e2e8f0;">Công việc:</strong>
                <span style="color:#94a3b8;">Technical Architect @ Cyberlogitec Vietnam</span>
            </li>
         </ul>
        <div style="text-align:center;">
            <a href="https://www.linkedin.com/in/phanquan111" target="_blank" style="
                background: linear-gradient(135deg, #0ea5e9, #0284c7);
                color:white; padding:10px 24px; border-radius:8px;
                text-decoration:none; font-size:13px; font-weight:600;
                display:inline-block; transition:opacity 0.2s;
                box-shadow: 0 4px 12px rgba(14,165,233,0.3);
            ">LinkedIn Profile</a>
        </div>"""
        st.markdown(render_profile_card(
            name="Phan Ngọc Minh Quân",
            role="Data Science Student",
            details=details_quan,
            initials="Q",
            image_name="quan"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:48px;'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # LÝ DO CHỌN KHÓA HỌC
    # ══════════════════════════════════════════════
    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.markdown("""
        <div class="intro-section-title">
            <div class="icon-box" style="background:rgba(16,185,129,0.12);">💡</div>
            <h3>Lý do chọn khóa học</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(render_reason_card(
            icon="🔭",
            title="Mở rộng tầm nhìn kiến trúc",
            description=(
                "Trong kỷ nguyên dẫn dắt bởi dữ liệu, việc chỉ nắm vững các thiết kế hệ thống "
                "hay xây dựng backend hiệu năng cao là chưa đủ. Chúng em chọn khóa học này để "
                "<strong>xóa mờ ranh giới giữa Software Architecture truyền thống và Data Engineering</strong>, "
                "từ đó thiết kế ra những hệ thống thông minh hơn."
            ),
            color="#10b981"
        ), unsafe_allow_html=True)

        st.markdown(render_reason_card(
            icon="🧩",
            title="Hoàn thiện hệ sinh thái công nghệ",
            description=(
                "Chương trình có học phần <strong>Dữ liệu lớn với PySpark</strong> cực kỳ phù hợp "
                "với định hướng của nhóm. Khóa học là mảnh ghép giúp hoàn thiện bức tranh toàn cảnh: "
                "từ việc thiết kế luồng dữ liệu thô trên môi trường cloud, đến việc nhúng trực tiếp "
                "các mô hình phân tích dự báo vào sâu bên trong lõi kiến trúc của sản phẩm công nghệ."
            ),
            color="#3b82f6"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="intro-section-title">
            <div class="icon-box" style="background:rgba(139,92,246,0.12);">🎓</div>
            <h3>Kinh nghiệm rút ra</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(render_reason_card(
            icon="🔄",
            title="Chuyển dịch tư duy luồng dữ liệu",
            description=(
                "Khóa học đã giúp chúng em có sự thay đổi lớn về tư duy, hiểu sâu sắc hơn về "
                "<strong>vòng đời dữ liệu (Data Pipeline)</strong> — cách làm sạch, chuẩn hóa và "
                "xử lý dữ liệu phân tán để các mô hình Machine Learning có thể hoạt động trơn tru "
                "và chính xác nhất."
            ),
            color="#8b5cf6"
        ), unsafe_allow_html=True)

        st.markdown(render_reason_card(
            icon="⚙️",
            title="Chuẩn hóa quy trình MLOps",
            description=(
                "Kinh nghiệm quý giá nhất là việc nhìn nhận các mô hình AI không phải là những "
                "thành phần rời rạc. Khóa học giúp hoạch định chiến lược <strong>tích hợp mô hình "
                "học máy vào quy trình CI/CD</strong> hiện tại của doanh nghiệp, đảm bảo sự đồng bộ "
                "giữa khối phát triển phần mềm và Data Science."
            ),
            color="#ec4899"
        ), unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="
        text-align:center;
        padding:32px 0 16px 0;
        margin-top:48px;
        border-top:1px solid rgba(148,163,184,0.15);
    ">
        <p style="color:#64748b; font-size:13px; margin:0;">
            DL07 - K311 - Team 9 &nbsp;&bull;&nbsp; Data Science & Machine Learning Certificate
            &nbsp;&bull;&nbsp; TTTH - ĐHKHTN TP.HCM
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
