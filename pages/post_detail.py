import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, score_all_posts, score_uploaded_csv

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
    
    # ══════════════════════════════════════════════
    # THREE TABS: Browse by ID / Text Search / CSV Upload
    # ══════════════════════════════════════════════
    tab_id, tab_search, tab_csv = st.tabs([
        "🔎 Chọn theo ID",
        "🔍 Tìm kiếm bằng text",
        "📤 Upload CSV phân tích",
    ])
    
    # ─────────────────────────────────────────
    # TAB 1: Select by ID (original functionality)
    # ─────────────────────────────────────────
    with tab_id:
        col_sel1, col_sel2 = st.columns([1, 2])
        
        with col_sel1:
            post_id = st.number_input("Nhập ID tin đăng", min_value=1, max_value=int(scored["id"].max()), value=1, step=1)
        
        with col_sel2:
            show_anomalous = st.checkbox("Chỉ hiện tin bất thường (Score ≥ 50)")
            if show_anomalous:
                anomalous_ids = scored[scored["anomaly_score"] >= 50]["id"].tolist()
                if anomalous_ids:
                    post_id = st.selectbox("Chọn tin bất thường", anomalous_ids, 
                                           format_func=lambda x: f"ID {x} — Score {scored[scored['id']==x]['anomaly_score'].values[0]}")
                else:
                    st.info("Không có tin đăng nào có Score ≥ 50.")
        
        post = scored[scored["id"] == post_id]
        if post.empty:
            st.warning(f"Không tìm thấy tin đăng ID {post_id}")
        else:
            _render_post_detail(post.iloc[0], scored)
    
    # ─────────────────────────────────────────
    # TAB 2: Text Search
    # ─────────────────────────────────────────
    with tab_search:
        st.markdown("### 🔍 Tìm kiếm tin đăng tương đương")
        st.markdown("""
        Nhập mô tả căn nhà bạn muốn tìm (VD: *nhà mặt tiền Gò Vấp 80m²*, 
        *hẻm Bình Thạnh 3 phòng ngủ*) để xem chi tiết phân tích bất thường.
        """)
        
        search_text = st.text_input(
            "🔍 Nhập mô tả",
            placeholder="VD: nhà mặt tiền Gò Vấp, hẻm xe hơi Bình Thạnh...",
            key="detail_search"
        )
        
        if search_text.strip():
            keywords = search_text.lower().strip().split()
            
            def row_matches(row):
                searchable = " ".join([
                    str(row.get("tieu_de", "")),
                    str(row.get("dia_chi", "")),
                    str(row.get("mo_ta", "")),
                    str(row.get("quan", "")),
                    str(row.get("loai_hinh", "")),
                ]).lower()
                return all(kw in searchable for kw in keywords)
            
            mask = scored.apply(row_matches, axis=1)
            results = scored[mask].sort_values("anomaly_score", ascending=False)
            
            if len(results) == 0:
                st.warning(f"Không tìm thấy tin đăng nào khớp với: **{search_text}**")
                st.info("💡 Thử rút gọn từ khóa.")
            else:
                st.success(f"Tìm thấy **{len(results):,}** tin phù hợp")
                
                # Let user pick one to view detail
                selected_id = st.selectbox(
                    "Chọn tin đăng để xem chi tiết",
                    results["id"].tolist(),
                    format_func=lambda x: (
                        f"ID {x} — {results[results['id']==x]['tieu_de'].values[0][:50]}... "
                        f"| Score: {results[results['id']==x]['anomaly_score'].values[0]}"
                    ),
                    key="search_select",
                )
                
                sel_post = results[results["id"] == selected_id].iloc[0]
                _render_post_detail(sel_post, scored)
        else:
            st.info("💡 Nhập từ khóa vào ô tìm kiếm phía trên để bắt đầu.")
    
    # ─────────────────────────────────────────
    # TAB 3: CSV Upload
    # ─────────────────────────────────────────
    with tab_csv:
        st.markdown("### 📤 Upload CSV — Xem chi tiết từng căn")
        st.markdown("""
        Upload file CSV từ dữ liệu **Nhà Tốt**. Hệ thống sẽ:
        1. **Parse dữ liệu thô** (giá, diện tích, quận, đặc điểm...) → dự đoán giá & chấm điểm
        2. Cho phép bạn **chọn từng căn** để xem phân tích chi tiết
        """)
        
        with st.expander("📋 Định dạng CSV yêu cầu"):
            st.markdown("""
            **Cột bắt buộc tối thiểu:** `gia_ban`, `dien_tich`
            
            **Cột nên có** (hệ thống tự parse):
            | Cột | Ví dụ | Mô tả |
            |-----|-------|-------|
            | `tieu_de` | Nhà cần bán mặt tiền đường | Tiêu đề tin |
            | `gia_ban` | 7,39 tỷ | Giá (tự parse) |
            | `dien_tich` | 45 m² | Diện tích (tự parse) |
            | `dia_chi` | ...Quận Phú Nhuận, Tp HCM | Trích xuất quận |
            | `mo_ta` | Nhà 1 lầu, chính chủ... | Trích xuất đặc điểm |
            | `loai_hinh` | Nhà ngõ, hẻm | Loại hình nhà |
            | `so_phong_ngu` | 2 phòng | Số phòng ngủ |
            | `dac_diem` | Hẻm xe hơi | Đặc điểm bổ sung |
            """)
            
            sample = pd.DataFrame({
                "tieu_de": ["Nhà cần bán mặt tiền đường", "Bán nhà hẻm xe hơi"],
                "gia_ban": ["7,39 tỷ", "3,5 tỷ"],
                "dien_tich": ["45 m²", "50 m²"],
                "dia_chi": ["Đường Phan Đăng Lưu, Quận Phú Nhuận, Tp HCM", "Đường Quang Trung, Quận Gò Vấp, Tp HCM"],
                "loai_hinh": ["Nhà ngõ, hẻm", "Nhà ngõ, hẻm"],
                "so_phong_ngu": ["2 phòng", "3 phòng"],
            })
            csv_sample = sample.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Tải CSV mẫu", csv_sample, "mau_du_lieu_nha_nhatot.csv", "text/csv", key="detail_csv_sample")
        
        uploaded_file = st.file_uploader("Chọn file CSV", type=["csv"],
                                         help="File CSV từ Nhà Tốt (ít nhất 2 cột: gia_ban, dien_tich)",
                                         key="detail_csv_upload")
        
        if uploaded_file is not None:
            try:
                try:
                    raw_df = pd.read_csv(uploaded_file, encoding="utf-8")
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    raw_df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
                
                with st.spinner("🔄 Đang phân tích..."):
                    scored_csv = score_uploaded_csv(raw_df, models)
                
                st.success(f"✅ Đã phân tích **{len(scored_csv):,}** căn nhà")
                
                # Summary table
                n_anomaly = len(scored_csv[scored_csv["anomaly_score"] >= 50])
                c1, c2, c3 = st.columns(3)
                c1.metric("Tổng tin", f"{len(scored_csv):,}")
                c2.metric("🔴🟠 Bất thường", f"{n_anomaly:,}")
                c3.metric("Score trung bình", f"{scored_csv['anomaly_score'].mean():.1f}")
                
                # Select one to view
                csv_select_id = st.selectbox(
                    "Chọn căn nhà để xem chi tiết",
                    scored_csv["id"].tolist(),
                    format_func=lambda x: (
                        f"#{x} — {scored_csv[scored_csv['id']==x]['quan'].values[0]} | "
                        f"{scored_csv[scored_csv['id']==x]['loai_hinh'].values[0]} | "
                        f"{scored_csv[scored_csv['id']==x]['dien_tich'].values[0]}m² | "
                        f"Score: {scored_csv[scored_csv['id']==x]['anomaly_score'].values[0]}"
                    ),
                    key="csv_detail_select",
                )
                
                csv_post = scored_csv[scored_csv["id"] == csv_select_id].iloc[0]
                _render_post_detail(csv_post, scored_csv)
                
            except ValueError as e:
                st.error(f"❌ Lỗi dữ liệu: {e}")
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
        else:
            st.info("📎 Kéo thả hoặc chọn file CSV để bắt đầu.")


# ══════════════════════════════════════════════
# SHARED: Render post detail
# ══════════════════════════════════════════════
def _render_post_detail(post, scored):
    """Render full detail view for a single post."""
    
    st.markdown("---")
    
    # ── POST HEADER ──
    badge_class = post.get("badge_class", "badge-normal")
    label = post.get("label", "🟢 Bình thường")
    score = post.get("anomaly_score", 0)
    tieu_de = post.get("tieu_de", f"{post.get('loai_hinh', '')} {post.get('quan', '')}")
    dia_chi = post.get("dia_chi", post.get("quan", ""))
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 24px; border-radius: 12px; margin-bottom: 16px;
                border-left: 5px solid {'#e53935' if score >= 50 else '#4caf50'};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h2 style="margin: 0 0 8px 0; color: #1a2a4a;">{tieu_de}</h2>
                <p style="color: #666; margin: 0;">📍 {dia_chi}</p>
            </div>
            <div style="text-align: right;">
                <span class="{badge_class}">{label}</span>
                <p style="font-size: 12px; color: #888; margin-top: 4px;">Score: {score}/100</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── KEY METRICS ──
    m1, m2, m3, m4, m5 = st.columns(5)
    gia_ban = float(post.get("gia_ban", 0))
    gia_du_bao = float(post.get("gia_du_bao", 0))
    diff = gia_ban - gia_du_bao
    
    with m1:
        st.metric("💰 Giá đăng", f"{gia_ban:.2f} tỷ")
    with m2:
        st.metric("🔮 Giá dự báo", f"{gia_du_bao:.2f} tỷ")
    with m3:
        st.metric("📊 Chênh lệch", f"{diff:+.2f} tỷ")
    with m4:
        st.metric("📐 Diện tích", f"{post.get('dien_tich', 0):.1f} m²")
    with m5:
        st.metric("🛏️ Phòng ngủ", f"{post.get('so_phong_ngu', 0)}")
    
    st.markdown("---")
    
    # ── TWO COLUMNS: INFO + ANOMALY ──
    info_col, anomaly_col = st.columns([1, 1])
    
    with info_col:
        st.markdown("### 📋 Thông tin chi tiết")
        
        mo_ta = post.get("mo_ta", "")
        if mo_ta:
            st.markdown(f"**Mô tả:** {mo_ta}")
            st.markdown("")
        
        info_data = {
            "Thuộc tính": [
                "Quận", "Loại hình", "Giấy tờ pháp lý", 
                "Diện tích", "Số phòng ngủ", "Điểm tiện nghi",
                "Giá khu vực TB", "Giá khu vực hiện tại",
            ],
            "Giá trị": [
                post.get("quan", "—"), post.get("loai_hinh", "—"), post.get("giay_to_phap_ly", "—"),
                f"{post.get('dien_tich', 0):.1f} m²", str(post.get("so_phong_ngu", 0)), str(post.get("tien_nghi_score", 0)),
                f"{post.get('gia_kv_mean', 0):.1f} triệu/m²", f"{post.get('gia_kv_hien_tai', 0):.1f} triệu/m²",
            ]
        }
        st.dataframe(info_data, use_container_width=True, hide_index=True)
        
        # Text features
        st.markdown("**Đặc điểm nhà (từ mô tả):**")
        text_feats = {
            "Mặt tiền": post.get("is_mat_tien", 0), "Hẻm xe hơi": post.get("is_hxh", 0),
            "Lô góc": post.get("is_lo_goc", 0), "Kinh doanh": post.get("is_kinh_doanh", 0),
            "Thang máy": post.get("has_thang_may", 0), "Nhà mới": post.get("is_nha_moi", 0),
            "Nhà nát": post.get("is_nha_nat", 0), "Sân thượng": post.get("has_san_thuong", 0),
            "Gara": post.get("has_gara", 0), "Chính chủ": post.get("is_chinh_chu", 0),
            "Ở ngay": post.get("o_ngay", 0), "Nở hậu": post.get("is_no_hau", 0),
            "Quy hoạch": post.get("has_quy_hoach", 0), "Ngộp bank": post.get("is_ngop_bank", 0),
            "Bán gấp": post.get("is_ban_gap", 0), "Dòng tiền": post.get("is_dong_tien", 0),
        }
        
        tags_on = [k for k, v in text_feats.items() if v == 1]
        
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
        fig_gauge, ax_gauge = plt.subplots(figsize=(6, 1.2))
        ax_gauge.barh(0, 100, height=0.5, color="#e0e0e0", edgecolor="none")
        score_color = "#e53935" if score >= 70 else ("#ff9800" if score >= 50 else ("#ffc107" if score >= 30 else "#4caf50"))
        ax_gauge.barh(0, score, height=0.5, color=score_color, edgecolor="none")
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
        s_resid = float(post.get("s_resid", 0))
        s_minmax = float(post.get("s_minmax", 0))
        s_percentile = float(post.get("s_percentile", 0))
        s_ml = float(post.get("s_ml", 0))
        
        components_data = {
            "Phương pháp": ["Residual-z (w=0.40)", "Min/Max (w=0.10)", "Percentile (w=0.20)", "Isolation Forest (w=0.30)"],
            "Score (0–1)": [s_resid, s_minmax, s_percentile, s_ml],
            "Đóng góp": [
                f"{s_resid * 0.40 * 100:.1f}",
                f"{s_minmax * 0.10 * 100:.1f}",
                f"{s_percentile * 0.20 * 100:.1f}",
                f"{s_ml * 0.30 * 100:.1f}",
            ]
        }
        st.dataframe(components_data, use_container_width=True, hide_index=True)
        
        # Interpretation
        z_score = post.get("z_score", 0)
        anomaly_type = post.get("anomaly_type", "")
        st.markdown(f"**Z-score:** {z_score} → {anomaly_type}")
        
        if score >= 50:
            st.error(f"""
            **Kết luận:** Tin đăng này được phân loại **{label}**.
            
            Giá đăng **{gia_ban:.2f} tỷ** chênh lệch **{diff:+.2f} tỷ** so với giá dự báo 
            **{gia_du_bao:.2f} tỷ**. 
            
            {"Giá đăng quá CAO — có thể do diện tích/vị trí đặc biệt hoặc sai thông tin." if z_score > 0 else "Giá đăng quá THẤP — có thể là deal tốt hoặc cần kiểm tra kỹ thông tin."}
            """)
        elif score >= 30:
            st.warning(f"""
            **Kết luận:** Tin đăng **{label}**. 
            Chênh lệch giá ở mức vừa phải, nên so sánh thêm với các tin tương tự.
            """)
        else:
            st.success(f"""
            **Kết luận:** Tin đăng **{label}**. 
            Giá đăng phù hợp với đặc điểm căn nhà và mặt bằng giá khu vực.
            """)
    
    st.markdown("---")
    
    # ── COMPARISON WITH SIMILAR POSTS ──
    st.markdown("### 📊 So sánh với tin đăng tương tự")
    
    post_quan = post.get("quan", "")
    post_loai = post.get("loai_hinh", "")
    post_id = post.get("id", -1)
    
    similar = scored[
        (scored["quan"] == post_quan) &
        (scored["loai_hinh"] == post_loai) &
        (scored["id"] != post_id)
    ].copy()
    
    if len(similar) > 0:
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.markdown(f"**Tin đăng cùng quận ({post_quan}) & loại hình ({post_loai}):**")
            stats_compare = {
                "Chỉ số": ["Giá trung bình", "Giá trung vị", "DT trung bình", "Giá tin này", "Vị trí %"],
                "Giá trị": [
                    f"{similar['gia_ban'].mean():.2f} tỷ",
                    f"{similar['gia_ban'].median():.2f} tỷ",
                    f"{similar['dien_tich'].mean():.0f} m²",
                    f"{gia_ban:.2f} tỷ",
                    f"Top {(similar['gia_ban'] > gia_ban).sum() / len(similar) * 100:.0f}%",
                ]
            }
            st.dataframe(stats_compare, use_container_width=True, hide_index=True)
        
        with comp_col2:
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            ax3.scatter(similar["dien_tich"], similar["gia_ban"], alpha=0.4, color="#1a73e8", s=30, label="Tin khác")
            ax3.scatter(post.get("dien_tich", 0), gia_ban, color="#e53935", s=120, zorder=5, 
                       marker="*", label=f"Tin #{post_id}")
            ax3.set_xlabel("Diện tích (m²)")
            ax3.set_ylabel("Giá bán (tỷ)")
            ax3.set_title(f"So sánh: {post_quan} — {post_loai}")
            ax3.legend()
            ax3.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig3)
    else:
        st.info("Không đủ tin đăng tương tự để so sánh.")

main()
