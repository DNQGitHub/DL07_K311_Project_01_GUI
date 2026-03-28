import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, score_all_posts

def main():
    sidebar.display()
    
    st.markdown("# 🔍 Chi tiết tin đăng & Phân tích bất thường")
    st.markdown("---")
    
    df = load_data()
    models = train_models()
    
    # Score all posts if not cached
    if "scored_df" not in st.session_state:
        with st.spinner("Đang phân tích..."):
            st.session_state.scored_df = score_all_posts(df, models)
    
    scored = st.session_state.scored_df.copy()
    
    # ── POST SELECTOR ──
    col_sel1, col_sel2 = st.columns([1, 2])
    
    with col_sel1:
        post_id = st.number_input("Nhập ID tin đăng", min_value=1, max_value=int(scored["id"].max()), value=1, step=1)
    
    with col_sel2:
        # Quick filter: show anomalous posts
        show_anomalous = st.checkbox("Chỉ hiện tin bất thường (Score ≥ 50)")
        if show_anomalous:
            anomalous_ids = scored[scored["anomaly_score"] >= 50]["id"].tolist()
            if anomalous_ids:
                post_id = st.selectbox("Chọn tin bất thường", anomalous_ids, 
                                       format_func=lambda x: f"ID {x} — Score {scored[scored['id']==x]['anomaly_score'].values[0]}")
            else:
                st.info("Không có tin đăng nào có Score ≥ 50.")
    
    # Get post data
    post = scored[scored["id"] == post_id]
    if post.empty:
        st.warning(f"Không tìm thấy tin đăng ID {post_id}")
        return
    
    post = post.iloc[0]
    
    st.markdown("---")
    
    # ── POST HEADER ──
    badge_html = f'<span class="{post["badge_class"]}">{post["label"]}</span>'
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 24px; border-radius: 12px; margin-bottom: 16px;
                border-left: 5px solid {'#e53935' if post['anomaly_score'] >= 50 else '#4caf50'};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h2 style="margin: 0 0 8px 0; color: #1a2a4a;">{post['tieu_de']}</h2>
                <p style="color: #666; margin: 0;">📍 {post['dia_chi']}</p>
            </div>
            <div style="text-align: right;">
                {badge_html}
                <p style="font-size: 12px; color: #888; margin-top: 4px;">Score: {post['anomaly_score']}/100</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── KEY METRICS ──
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("💰 Giá đăng", f"{post['gia_ban']:.2f} tỷ")
    with m2:
        st.metric("🔮 Giá dự báo", f"{post['gia_du_bao']:.2f} tỷ")
    with m3:
        diff = post['gia_ban'] - post['gia_du_bao']
        st.metric("📊 Chênh lệch", f"{diff:+.2f} tỷ")
    with m4:
        st.metric("📐 Diện tích", f"{post['dien_tich']:.1f} m²")
    with m5:
        st.metric("🛏️ Phòng ngủ", f"{post['so_phong_ngu']}")
    
    st.markdown("---")
    
    # ── TWO COLUMNS: INFO + ANOMALY ──
    info_col, anomaly_col = st.columns([1, 1])
    
    with info_col:
        st.markdown("### 📋 Thông tin chi tiết")
        
        st.markdown(f"**Mô tả:** {post['mo_ta']}")
        st.markdown("")
        
        info_data = {
            "Thuộc tính": [
                "Quận", "Loại hình", "Giấy tờ pháp lý", 
                "Diện tích", "Số phòng ngủ", "Điểm tiện nghi",
                "Giá khu vực TB", "Giá khu vực hiện tại",
            ],
            "Giá trị": [
                post["quan"], post["loai_hinh"], post["giay_to_phap_ly"],
                f"{post['dien_tich']:.1f} m²", str(post["so_phong_ngu"]), str(post["tien_nghi_score"]),
                f"{post['gia_kv_mean']:.1f} triệu/m²", f"{post['gia_kv_hien_tai']:.1f} triệu/m²",
            ]
        }
        st.dataframe(info_data, use_container_width=True, hide_index=True)
        
        # Text features
        st.markdown("**Đặc điểm nhà (từ mô tả):**")
        text_feats = {
            "Mặt tiền": post["is_mat_tien"], "Hẻm xe hơi": post["is_hxh"],
            "Lô góc": post["is_lo_goc"], "Kinh doanh": post["is_kinh_doanh"],
            "Thang máy": post["has_thang_may"], "Nhà mới": post["is_nha_moi"],
            "Nhà nát": post["is_nha_nat"], "Sân thượng": post["has_san_thuong"],
            "Gara": post["has_gara"], "Chính chủ": post["is_chinh_chu"],
            "Ở ngay": post["o_ngay"], "Nở hậu": post["is_no_hau"],
            "Quy hoạch": post["has_quy_hoach"], "Ngộp bank": post["is_ngop_bank"],
            "Bán gấp": post["is_ban_gap"], "Dòng tiền": post["is_dong_tien"],
        }
        
        tags_on = [k for k, v in text_feats.items() if v == 1]
        tags_off = [k for k, v in text_feats.items() if v == 0]
        
        if tags_on:
            tags_html = " ".join([
                f'<span style="background:{"#ffebee" if t in ["Quy hoạch","Ngộp bank","Bán gấp","Nhà nát"] else "#e3f2fd"}; '
                f'padding: 3px 10px; border-radius: 12px; font-size: 12px; margin: 2px; display: inline-block;">'
                f'{"⚠️" if t in ["Quy hoạch","Ngộp bank","Bán gấp","Nhà nát"] else "✅"} {t}</span>'
                for t in tags_on
            ])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.caption("Không có đặc điểm nổi bật.")
    
    with anomaly_col:
        st.markdown("### 🔍 Phân tích bất thường")
        
        # Anomaly score gauge
        score = post["anomaly_score"]
        fig_gauge, ax_gauge = plt.subplots(figsize=(6, 1.2))
        
        # Background bar
        ax_gauge.barh(0, 100, height=0.5, color="#e0e0e0", edgecolor="none")
        # Score bar
        score_color = "#e53935" if score >= 70 else ("#ff9800" if score >= 50 else ("#ffc107" if score >= 30 else "#4caf50"))
        ax_gauge.barh(0, score, height=0.5, color=score_color, edgecolor="none")
        # Threshold lines
        for threshold in [30, 50, 70]:
            ax_gauge.axvline(x=threshold, color="#666", linestyle=":", linewidth=0.8, alpha=0.6)
        ax_gauge.text(score + 1, 0, f" {score}", va="center", fontweight="bold", fontsize=14, color=score_color)
        ax_gauge.set_xlim(0, 105)
        ax_gauge.set_yticks([])
        ax_gauge.spines[["top", "right", "left", "bottom"]].set_visible(False)
        ax_gauge.set_xlabel("Anomaly Score (0–100)")
        plt.tight_layout()
        st.pyplot(fig_gauge)
        
        # Component scores
        st.markdown("**Đóng góp từng phương pháp:**")
        
        components_data = {
            "Phương pháp": ["Residual-z (w=0.35)", "Min/Max (w=0.15)", "Percentile (w=0.20)", "Isolation Forest (w=0.30)"],
            "Score (0–1)": [post["s_resid"], post["s_minmax"], post["s_percentile"], post["s_ml"]],
            "Đóng góp": [
                f"{post['s_resid'] * 0.35 * 100:.1f}",
                f"{post['s_minmax'] * 0.15 * 100:.1f}",
                f"{post['s_percentile'] * 0.20 * 100:.1f}",
                f"{post['s_ml'] * 0.30 * 100:.1f}",
            ]
        }
        st.dataframe(components_data, use_container_width=True, hide_index=True)
        
        # Interpretation
        st.markdown(f"**Z-score:** {post['z_score']} → {post['anomaly_type']}")
        
        if post["anomaly_score"] >= 50:
            st.error(f"""
            **Kết luận:** Tin đăng này được phân loại **{post['label']}**.
            
            Giá đăng **{post['gia_ban']:.2f} tỷ** chênh lệch **{diff:+.2f} tỷ** so với giá dự báo 
            **{post['gia_du_bao']:.2f} tỷ**. 
            
            {"Giá đăng quá CAO — có thể do diện tích/vị trí đặc biệt hoặc sai thông tin." if post['z_score'] > 0 else "Giá đăng quá THẤP — có thể là deal tốt hoặc cần kiểm tra kỹ thông tin."}
            """)
        elif post["anomaly_score"] >= 30:
            st.warning(f"""
            **Kết luận:** Tin đăng **{post['label']}**. 
            Chênh lệch giá ở mức vừa phải, nên so sánh thêm với các tin tương tự.
            """)
        else:
            st.success(f"""
            **Kết luận:** Tin đăng **{post['label']}**. 
            Giá đăng phù hợp với đặc điểm căn nhà và mặt bằng giá khu vực.
            """)
    
    st.markdown("---")
    
    # ── COMPARISON WITH SIMILAR POSTS ──
    st.markdown("### 📊 So sánh với tin đăng tương tự")
    
    similar = scored[
        (scored["quan"] == post["quan"]) &
        (scored["loai_hinh"] == post["loai_hinh"]) &
        (scored["id"] != post["id"])
    ].copy()
    
    if len(similar) > 0:
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.markdown(f"**Tin đăng cùng quận ({post['quan']}) & loại hình ({post['loai_hinh']}):**")
            stats_compare = {
                "Chỉ số": ["Giá trung bình", "Giá trung vị", "DT trung bình", "Giá tin này", "Vị trí %"],
                "Giá trị": [
                    f"{similar['gia_ban'].mean():.2f} tỷ",
                    f"{similar['gia_ban'].median():.2f} tỷ",
                    f"{similar['dien_tich'].mean():.0f} m²",
                    f"{post['gia_ban']:.2f} tỷ",
                    f"Top {(similar['gia_ban'] > post['gia_ban']).sum() / len(similar) * 100:.0f}%",
                ]
            }
            st.dataframe(stats_compare, use_container_width=True, hide_index=True)
        
        with comp_col2:
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            ax3.scatter(similar["dien_tich"], similar["gia_ban"], alpha=0.4, color="#1a73e8", s=30, label="Tin khác")
            ax3.scatter(post["dien_tich"], post["gia_ban"], color="#e53935", s=120, zorder=5, 
                       marker="*", label=f"Tin #{post['id']}")
            ax3.set_xlabel("Diện tích (m²)")
            ax3.set_ylabel("Giá bán (tỷ)")
            ax3.set_title(f"So sánh: {post['quan']} — {post['loai_hinh']}")
            ax3.legend()
            ax3.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig3)
    else:
        st.info("Không đủ tin đăng tương tự để so sánh.")

main()
