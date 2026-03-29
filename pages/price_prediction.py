import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import components.sidebar as sidebar
from utils.helpers import (
    load_data, train_models, prepare_input, predict_price,
    predict_all_models, compute_anomaly_score,
    score_all_posts, score_uploaded_csv,
)

def main():
    sidebar.display()
    
    st.markdown("# 📝 Dự đoán giá & Kiểm tra bất thường")
    st.markdown("---")
    
    models = train_models()
    df = load_data()
    
    # ══════════════════════════════════════════════
    # THREE TABS: Manual Input / Text Search / CSV Upload
    # ══════════════════════════════════════════════
    tab_manual, tab_search, tab_csv = st.tabs([
        "📝 Nhập thông tin nhà",
        "🔎 Tìm kiếm bằng text",
        "📤 Upload CSV phân tích",
    ])
    
    # ─────────────────────────────────────────
    # TAB 1: Manual Input (original functionality)
    # ─────────────────────────────────────────
    with tab_manual:
        _render_manual_tab(models, df)
    
    # ─────────────────────────────────────────
    # TAB 2: Text Search
    # ─────────────────────────────────────────
    with tab_search:
        _render_search_tab(models, df)
    
    # ─────────────────────────────────────────
    # TAB 3: CSV Upload
    # ─────────────────────────────────────────
    with tab_csv:
        _render_csv_tab(models)


# ══════════════════════════════════════════════
# TAB 1: Nhập thông tin nhà (giữ nguyên logic cũ)
# ══════════════════════════════════════════════
def _render_manual_tab(models, df):
    st.markdown("""
    Nhập thông tin căn nhà bạn muốn đánh giá. Hệ thống sẽ:
    1. **Dự đoán giá bán** từ **4 mô hình Sklearn**
    2. **Kiểm tra bất thường** bằng Composite Score
    3. **Phân tích theo phân khúc** (Quận × Loại hình)
    """)
    
    st.markdown("### 📋 Thông tin cơ bản")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quan = st.selectbox("🏘️ Quận", ["Bình Thạnh", "Gò Vấp", "Phú Nhuận"], key="m_quan")
        loai_hinh = st.selectbox("🏠 Loại hình", ["Nhà trong hẻm", "Nhà mặt tiền", "Nhà phố", "Biệt thự"], key="m_loai")
        giay_to = st.selectbox("📄 Giấy tờ pháp lý", ["Sổ hồng/ Sổ đỏ", "Hợp đồng mua bán", "chưa xác định"], key="m_giay")
    
    with col2:
        dien_tich = st.number_input("📐 Diện tích (m²)", min_value=10.0, max_value=500.0, value=60.0, step=5.0, key="m_dt")
        so_phong_ngu = st.number_input("🛏️ Số phòng ngủ", min_value=1, max_value=10, value=3, step=1, key="m_pn")
        tien_nghi_score = st.slider("⭐ Điểm tiện nghi (0–5)", 0, 5, 2, key="m_tn")
    
    with col3:
        gia_ban_input = st.number_input(
            "💰 Giá đăng bán (tỷ VNĐ)", 
            min_value=0.1, max_value=100.0, value=5.0, step=0.1,
            help="Nhập giá bạn muốn đăng / giá bạn thấy trên tin đăng",
            key="m_gia"
        )
        gia_kv_mean = st.number_input("📊 Giá khu vực TB (triệu/m²)", min_value=10.0, max_value=200.0, value=70.0, step=5.0, key="m_kv")
        gia_kv_hien_tai = st.number_input("📈 Giá khu vực hiện tại (triệu/m²)", min_value=10.0, max_value=200.0, value=72.0, step=5.0, key="m_kvht")
    
    st.markdown("### 🏗️ Đặc điểm nhà")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    with feat_col1:
        is_mat_tien = st.checkbox("Mặt tiền", value=(loai_hinh == "Nhà mặt tiền"), key="m_mt")
        is_hxh = st.checkbox("Hẻm xe hơi", key="m_hxh")
        is_lo_goc = st.checkbox("Lô góc / 2 mặt tiền", key="m_lg")
        is_kinh_doanh = st.checkbox("Kinh doanh", key="m_kd")
    with feat_col2:
        has_thang_may = st.checkbox("Thang máy", key="m_tm")
        is_nha_moi = st.checkbox("Nhà mới xây", key="m_nm")
        is_nha_nat = st.checkbox("Nhà nát / cấp 4", key="m_nn")
        has_san_thuong = st.checkbox("Sân thượng", key="m_st")
    with feat_col3:
        has_gara = st.checkbox("Gara ô tô", key="m_gr")
        is_chinh_chu = st.checkbox("Chính chủ", value=True, key="m_cc")
        o_ngay = st.checkbox("Ở ngay", key="m_on")
        is_dong_tien = st.checkbox("Đang có dòng tiền", key="m_dt2")
    with feat_col4:
        is_no_hau = st.checkbox("Nở hậu", key="m_nh")
        has_quy_hoach = st.checkbox("⚠️ Quy hoạch", key="m_qh")
        is_ngop_bank = st.checkbox("⚠️ Ngộp bank", key="m_nb")
        is_ban_gap = st.checkbox("⚠️ Bán gấp", key="m_bg")
    
    st.markdown("---")
    
    if st.button("🔮 Dự đoán giá & Kiểm tra bất thường", type="primary", use_container_width=True, key="m_predict"):
        row = {
            "quan": quan, "loai_hinh": loai_hinh, "giay_to_phap_ly": giay_to,
            "dien_tich": dien_tich, "so_phong_ngu": so_phong_ngu,
            "tien_nghi_score": tien_nghi_score,
            "gia_kv_mean": gia_kv_mean, "gia_kv_hien_tai": gia_kv_hien_tai,
            "gia_kv_trend": 0.02, "gia_kv_volatility": 0.05,
            "is_mat_tien": int(is_mat_tien), "is_hxh": int(is_hxh),
            "is_lo_goc": int(is_lo_goc), "is_kinh_doanh": int(is_kinh_doanh),
            "is_dong_tien": int(is_dong_tien), "is_no_hau": int(is_no_hau),
            "has_thang_may": int(has_thang_may), "is_nha_moi": int(is_nha_moi),
            "is_nha_nat": int(is_nha_nat), "has_quy_hoach": int(has_quy_hoach),
            "is_chinh_chu": int(is_chinh_chu), "has_san_thuong": int(has_san_thuong),
            "has_gara": int(has_gara), "o_ngay": int(o_ngay),
            "is_ngop_bank": int(is_ngop_bank), "is_ban_gap": int(is_ban_gap),
        }
        
        input_features = prepare_input(row, models)
        predicted = predict_price(input_features, models)
        all_predictions = predict_all_models(input_features, models)
        anomaly = compute_anomaly_score(
            input_features, gia_ban_input, predicted, models,
            quan=quan, loai_hinh=loai_hinh
        )
        
        _render_prediction_results(gia_ban_input, predicted, all_predictions, anomaly, quan, loai_hinh)


# ══════════════════════════════════════════════
# TAB 2: Tìm kiếm bằng text
# ══════════════════════════════════════════════
def _render_search_tab(models, df):
    st.markdown("### 🔎 Tìm kiếm tin đăng — Dự đoán & Phân tích")
    st.markdown("""
    Nhập từ khóa mô tả căn nhà (VD: *nhà mặt tiền Gò Vấp 80m²*, *hẻm xe hơi Bình Thạnh 3 phòng ngủ*).
    Hệ thống sẽ tìm các tin đăng phù hợp, hiển thị **dự đoán giá** và **phân tích bất thường** cho từng căn.
    """)
    
    search_text = st.text_input(
        "🔍 Nhập mô tả căn nhà cần tìm",
        placeholder="VD: nhà mặt tiền Gò Vấp, hẻm xe hơi Bình Thạnh, biệt thự Phú Nhuận...",
        key="pred_search"
    )
    
    if search_text.strip():
        # Score all posts if not cached
        if "scored_df" not in st.session_state:
            with st.spinner("Đang phân tích toàn bộ tin đăng..."):
                st.session_state.scored_df = score_all_posts(df, models)
        
        scored = st.session_state.scored_df.copy()
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
            st.info("💡 Thử rút gọn từ khóa, ví dụ chỉ nhập tên quận hoặc loại hình nhà.")
        else:
            st.success(f"Tìm thấy **{len(results):,}** tin đăng phù hợp")
            
            # Stats
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Tổng tin", f"{len(results):,}")
            n_anom = len(results[results["anomaly_score"] >= 50])
            c2.metric("🔴🟠 Bất thường", f"{n_anom:,}")
            c3.metric("Giá trung vị", f"{results['gia_ban'].median():.2f} tỷ")
            c4.metric("Giá dự báo TB", f"{results['gia_du_bao'].mean():.2f} tỷ")
            
            st.markdown("---")
            
            # Results table
            display_cols = ["id", "tieu_de", "quan", "loai_hinh", "dien_tich", "so_phong_ngu",
                            "gia_ban", "gia_du_bao", "anomaly_score", "label", "anomaly_type"]
            display_cols = [c for c in display_cols if c in results.columns]
            
            display_df = results[display_cols].rename(columns={
                "id": "ID", "tieu_de": "Tiêu đề", "quan": "Quận", "loai_hinh": "Loại hình",
                "dien_tich": "DT (m²)", "so_phong_ngu": "PN",
                "gia_ban": "Giá đăng (tỷ)", "gia_du_bao": "Giá dự báo (tỷ)",
                "anomaly_score": "Score", "label": "Phân loại", "anomaly_type": "Loại BT",
            })
            
            st.dataframe(
                display_df,
                use_container_width=True, hide_index=True,
                column_config={
                    "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
                    "Giá đăng (tỷ)": st.column_config.NumberColumn(format="%.2f"),
                    "Giá dự báo (tỷ)": st.column_config.NumberColumn(format="%.2f"),
                }
            )
            
            # Allow viewing detail of one
            st.markdown("---")
            st.markdown("#### 🔬 Xem chi tiết dự đoán cho 1 căn")
            sel_id = st.selectbox(
                "Chọn tin đăng",
                results["id"].tolist(),
                format_func=lambda x: (
                    f"ID {x} — {results[results['id']==x]['tieu_de'].values[0][:40]}... "
                    f"| Giá: {results[results['id']==x]['gia_ban'].values[0]:.2f}T "
                    f"| Score: {results[results['id']==x]['anomaly_score'].values[0]}"
                ),
                key="pred_search_select",
            )
            
            post = results[results["id"] == sel_id].iloc[0]
            _render_prediction_results(
                post["gia_ban"], post["gia_du_bao"],
                {"Random Forest": post["gia_du_bao"]},  # simplified
                {
                    "anomaly_score": post["anomaly_score"], "label": post["label"],
                    "badge_class": post["badge_class"], "anomaly_type": post["anomaly_type"],
                    "z_score": post["z_score"],
                    "s_resid": post["s_resid"], "s_minmax": post["s_minmax"],
                    "s_percentile": post["s_percentile"], "s_ml": post["s_ml"],
                },
                post["quan"], post["loai_hinh"],
            )
    else:
        st.info("💡 Nhập từ khóa vào ô tìm kiếm phía trên để bắt đầu.")


# ══════════════════════════════════════════════
# TAB 3: Upload CSV phân tích
# ══════════════════════════════════════════════
def _render_csv_tab(models):
    st.markdown("### 📤 Upload CSV — Dự đoán giá hàng loạt")
    st.markdown("""
    Upload file CSV từ dữ liệu **Nhà Tốt**. Hệ thống sẽ tự động:
    1. **Parse dữ liệu thô** (giá "7,39 tỷ" → 7.39, diện tích "45 m²" → 45, trích xuất quận từ địa chỉ...)
    2. **Trích xuất đặc điểm** từ mô tả (mặt tiền, hẻm xe hơi, chính chủ, bán gấp...)
    3. **Dự đoán giá** bằng model Random Forest & **chấm điểm bất thường** (0–100)
    """)
    
    with st.expander("📋 Xem định dạng CSV mẫu", expanded=False):
        st.markdown("""
        **Cột bắt buộc tối thiểu:** `gia_ban`, `dien_tich`
        
        **Cột nên có** để kết quả chính xác hơn:
        | Cột | Ví dụ | Mô tả |
        |-----|-------|-------|
        | `tieu_de` | Nhà cần bán mặt tiền | Tiêu đề tin |
        | `gia_ban` | 7,39 tỷ | Giá (tự parse) |
        | `dien_tich` | 45 m² | Diện tích (tự parse) |
        | `dia_chi` | ...Quận Phú Nhuận... | Trích xuất quận |
        | `mo_ta` | Chính chủ, nhà mới... | Trích xuất đặc điểm |
        | `loai_hinh` | Nhà ngõ, hẻm | Loại hình |
        | `so_phong_ngu` | 2 phòng | Số phòng |
        | `don_gia` | 164,22 triệu/m² | Đơn giá |
        | `dac_diem` | Hẻm xe hơi | Đặc điểm bổ sung |
        """)
        
        sample = pd.DataFrame({
            "tieu_de": ["Nhà cần bán mặt tiền đường", "Bán nhà hẻm xe hơi"],
            "gia_ban": ["7,39 tỷ", "3,5 tỷ"],
            "don_gia": ["164,22 triệu/m²", "70 triệu/m²"],
            "dien_tich": ["45 m²", "50 m²"],
            "dia_chi": ["Đường Phan Đăng Lưu, Quận Phú Nhuận, Tp HCM", "Đường Quang Trung, Quận Gò Vấp, Tp HCM"],
            "mo_ta": ["Ngang 4,5 Dài 10, Nhà 1 lầu", "Nhà mới xây, chính chủ bán gấp"],
            "loai_hinh": ["Nhà ngõ, hẻm", "Nhà ngõ, hẻm"],
            "so_phong_ngu": ["2 phòng", "3 phòng"],
        })
        st.dataframe(sample, use_container_width=True, hide_index=True)
        csv_sample = sample.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Tải CSV mẫu", csv_sample, "mau_du_lieu_nha_nhatot.csv", "text/csv", key="pred_csv_sample")
    
    uploaded_file = st.file_uploader(
        "Chọn file CSV",
        type=["csv"],
        help="File CSV từ Nhà Tốt (ít nhất 2 cột: gia_ban, dien_tich)",
        key="pred_csv_upload",
    )
    
    if uploaded_file is not None:
        try:
            try:
                raw_df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                raw_df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            
            st.info(f"📄 Đã đọc file: **{uploaded_file.name}** — {len(raw_df):,} dòng, {len(raw_df.columns)} cột")
            
            with st.expander("👀 Xem dữ liệu thô (5 dòng đầu)", expanded=False):
                st.dataframe(raw_df.head(), use_container_width=True, hide_index=True)
            
            with st.spinner("🔄 Đang parse dữ liệu, dự đoán giá và phân tích bất thường..."):
                scored_csv = score_uploaded_csv(raw_df, models)
            
            st.success(f"✅ Phân tích xong **{len(scored_csv):,}** căn nhà!")
            
            # Stats
            st.markdown("---")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Tổng căn", f"{len(scored_csv):,}")
            n_anom = len(scored_csv[scored_csv["anomaly_score"] >= 50])
            c2.metric("🔴🟠 Bất thường", f"{n_anom:,}", f"{n_anom/max(len(scored_csv),1)*100:.1f}%")
            c3.metric("Giá TB đăng", f"{scored_csv['gia_ban'].mean():.2f} tỷ")
            c4.metric("Giá TB dự báo", f"{scored_csv['gia_du_bao'].mean():.2f} tỷ")
            c5.metric("Score TB", f"{scored_csv['anomaly_score'].mean():.1f}")
            
            # Table
            display_cols = [c for c in ["id", "tieu_de", "quan", "loai_hinh", "dien_tich",
                            "gia_ban", "gia_du_bao", "anomaly_score", "label", "anomaly_type"]
                            if c in scored_csv.columns]
            
            display_df = scored_csv[display_cols].rename(columns={
                "id": "ID", "tieu_de": "Tiêu đề", "quan": "Quận", "loai_hinh": "Loại hình",
                "dien_tich": "DT (m²)", "gia_ban": "Giá đăng (tỷ)", "gia_du_bao": "Giá dự báo (tỷ)",
                "anomaly_score": "Score", "label": "Phân loại", "anomaly_type": "Loại BT",
            })
            
            st.dataframe(
                display_df,
                use_container_width=True, hide_index=True,
                column_config={
                    "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
                    "Giá đăng (tỷ)": st.column_config.NumberColumn(format="%.2f"),
                    "Giá dự báo (tỷ)": st.column_config.NumberColumn(format="%.2f"),
                }
            )
            
            # Download results
            csv_out = scored_csv[display_cols].to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Tải kết quả phân tích (CSV)", csv_out,
                               "ket_qua_du_doan.csv", "text/csv", key="pred_csv_download")
            
            # Charts
            st.markdown("---")
            ch1, ch2 = st.columns(2)
            with ch1:
                st.markdown("#### Phân bố Anomaly Score")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.hist(scored_csv["anomaly_score"], bins=20, color="#1a73e8", edgecolor="white", alpha=0.85)
                ax.axvline(x=30, color="#ffc107", linestyle="--", label="Cần xem xét (30)")
                ax.axvline(x=50, color="#ff9800", linestyle="--", label="Bất thường (50)")
                ax.axvline(x=70, color="#e53935", linestyle="--", label="Rất BT (70)")
                ax.set_xlabel("Anomaly Score")
                ax.set_ylabel("Số lượng")
                ax.legend(fontsize=8)
                ax.spines[["top", "right"]].set_visible(False)
                plt.tight_layout()
                st.pyplot(fig)
            
            with ch2:
                st.markdown("#### Giá đăng vs Giá dự báo")
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                colors = ["#e53935" if s >= 50 else "#4caf50" for s in scored_csv["anomaly_score"]]
                ax2.scatter(scored_csv["gia_du_bao"], scored_csv["gia_ban"], c=colors, alpha=0.6, s=30)
                max_val = max(scored_csv["gia_ban"].max(), scored_csv["gia_du_bao"].max()) * 1.1
                ax2.plot([0, max_val], [0, max_val], "k--", alpha=0.3, label="Giá = Dự báo")
                ax2.set_xlabel("Giá dự báo (tỷ)")
                ax2.set_ylabel("Giá đăng (tỷ)")
                ax2.legend(fontsize=9)
                ax2.spines[["top", "right"]].set_visible(False)
                plt.tight_layout()
                st.pyplot(fig2)
            
            # Detail view
            st.markdown("---")
            st.markdown("#### 🔬 Xem chi tiết dự đoán cho 1 căn")
            sel_id = st.selectbox(
                "Chọn căn nhà",
                scored_csv["id"].tolist(),
                format_func=lambda x: (
                    f"#{x} — {scored_csv[scored_csv['id']==x]['quan'].values[0]} | "
                    f"{scored_csv[scored_csv['id']==x]['loai_hinh'].values[0]} | "
                    f"Giá: {scored_csv[scored_csv['id']==x]['gia_ban'].values[0]:.2f}T | "
                    f"Score: {scored_csv[scored_csv['id']==x]['anomaly_score'].values[0]}"
                ),
                key="pred_csv_detail_select",
            )
            
            post = scored_csv[scored_csv["id"] == sel_id].iloc[0]
            _render_prediction_results(
                post["gia_ban"], post["gia_du_bao"],
                {"Random Forest": post["gia_du_bao"]},
                {
                    "anomaly_score": post["anomaly_score"], "label": post["label"],
                    "badge_class": post.get("badge_class", "badge-normal"),
                    "anomaly_type": post.get("anomaly_type", ""),
                    "z_score": post.get("z_score", 0),
                    "s_resid": post.get("s_resid", 0), "s_minmax": post.get("s_minmax", 0),
                    "s_percentile": post.get("s_percentile", 0), "s_ml": post.get("s_ml", 0),
                },
                post["quan"], post["loai_hinh"],
            )
            
        except ValueError as e:
            st.error(f"❌ Lỗi dữ liệu: {e}")
        except Exception as e:
            st.error(f"❌ Lỗi khi xử lý file: {e}")
    else:
        st.info("📎 Kéo thả hoặc chọn file CSV để bắt đầu phân tích.")


# ══════════════════════════════════════════════
# SHARED: Render prediction results
# ══════════════════════════════════════════════
def _render_prediction_results(gia_ban_input, predicted, all_predictions, anomaly, quan, loai_hinh):
    """Render prediction and anomaly results for a single house."""
    
    st.markdown("---")
    st.markdown("## 📊 Kết quả dự đoán")
    
    # ─── Main result cards ───
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 24px; border-radius: 12px; text-align: center; border: 2px solid #4caf50;">
            <p style="color: #666; margin: 0; font-size: 14px;">💰 Giá dự báo (Random Forest)</p>
            <p style="font-size: 36px; font-weight: 800; color: #2e7d32; margin: 8px 0;">{predicted:.2f} tỷ</p>
            <p style="color: #888; margin: 0; font-size: 13px;">≈ {predicted * 1000:.0f} triệu VNĐ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with res_col2:
        diff = gia_ban_input - predicted
        diff_pct = (diff / predicted * 100) if predicted > 0 else 0
        diff_color = "#e53935" if abs(diff_pct) > 20 else ("#ff9800" if abs(diff_pct) > 10 else "#4caf50")
        direction = "cao hơn" if diff > 0 else "thấp hơn"
        st.markdown(f"""
        <div style="background: #fff3e0; padding: 24px; border-radius: 12px; text-align: center; border: 2px solid #ff9800;">
            <p style="color: #666; margin: 0; font-size: 14px;">📊 Chênh lệch giá</p>
            <p style="font-size: 36px; font-weight: 800; color: {diff_color}; margin: 8px 0;">{diff:+.2f} tỷ</p>
            <p style="color: #888; margin: 0; font-size: 13px;">Giá đăng {direction} {abs(diff_pct):.1f}% so với dự báo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with res_col3:
        score = anomaly['anomaly_score']
        st.markdown(f"""
        <div style="background: {'#ffebee' if score >= 50 else '#e8f5e9'}; 
                    padding: 24px; border-radius: 12px; text-align: center; 
                    border: 2px solid {'#e53935' if score >= 50 else '#4caf50'};">
            <p style="color: #666; margin: 0; font-size: 14px;">🔍 Anomaly Score</p>
            <p style="font-size: 36px; font-weight: 800; color: {'#c62828' if score >= 50 else '#2e7d32'}; margin: 8px 0;">
                {score}/100
            </p>
            <p style="margin: 0;"><span class="{anomaly['badge_class']}">{anomaly['label']}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # ─── Multi-model comparison (only if multiple models) ───
    if len(all_predictions) > 1:
        st.markdown("---")
        st.markdown("### 🤖 Dự đoán từ tất cả 4 mô hình Sklearn")
        
        pred_data = []
        for name, pred_val in all_predictions.items():
            pred_diff = gia_ban_input - pred_val
            pred_pct = (pred_diff / pred_val * 100) if pred_val > 0 else 0
            pred_data.append({
                "Mô hình": name,
                "Giá dự đoán (tỷ)": round(pred_val, 2),
                "Chênh lệch (tỷ)": round(pred_diff, 2),
                "Chênh lệch (%)": round(pred_pct, 1),
            })
        
        df_preds = pd.DataFrame(pred_data)
        
        col_table, col_chart = st.columns([2, 3])
        
        with col_table:
            st.dataframe(
                df_preds.style.format({
                    "Giá dự đoán (tỷ)": "{:.2f}",
                    "Chênh lệch (tỷ)": "{:+.2f}",
                    "Chênh lệch (%)": "{:+.1f}%",
                }),
                use_container_width=True, hide_index=True,
            )
            
            avg_pred = np.mean(list(all_predictions.values()))
            min_pred = min(all_predictions.values())
            max_pred = max(all_predictions.values())
            st.info(f"""
            **📊 Tổng hợp dự đoán:**
            - Trung bình: **{avg_pred:.2f} tỷ**
            - Khoảng: **{min_pred:.2f} – {max_pred:.2f} tỷ**
            - Giá đăng: **{gia_ban_input:.2f} tỷ**
            """)
        
        with col_chart:
            model_names = list(all_predictions.keys())
            pred_values = list(all_predictions.values())
            colors = ["#e74c3c" if name == "Random Forest" else "#3498db" for name in model_names]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=model_names, y=pred_values,
                marker_color=colors,
                text=[f"{v:.2f} tỷ" for v in pred_values],
                textposition="outside",
                name="Giá dự đoán",
            ))
            fig.add_hline(
                y=gia_ban_input, line_dash="dash", line_color="#ff9800",
                annotation_text=f"Giá đăng: {gia_ban_input:.2f} tỷ",
            )
            fig.update_layout(
                title="So sánh dự đoán — 4 mô hình Sklearn",
                yaxis_title="Giá (tỷ VNĐ)", height=400, showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ─── Anomaly detail ───
    st.markdown("---")
    st.markdown("### 🔍 Chi tiết phân tích bất thường")
    st.caption(f"Phân khúc phân tích: **{quan}** × **{loai_hinh}**")
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.markdown(f"**Loại bất thường:** {anomaly['anomaly_type']}")
        st.markdown(f"**Z-score:** {anomaly['z_score']}")
        
        st.markdown("**Đóng góp từng phương pháp:**")
        
        methods = ["Residual-z\n(w=0.40)", "Min/Max\n(w=0.10)", "Percentile\n(w=0.20)", "Isolation Forest\n(w=0.30)"]
        raw_scores = [anomaly["s_resid"], anomaly["s_minmax"], anomaly["s_percentile"], anomaly["s_ml"]]
        bar_colors = ["#e53935" if s > 0.5 else ("#ff9800" if s > 0.2 else "#4caf50") for s in raw_scores]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        bars = ax.barh(methods, raw_scores, color=bar_colors, edgecolor="white", height=0.6)
        ax.set_xlim(0, 1.1)
        ax.set_xlabel("Score (0–1)")
        ax.axvline(x=0.5, color="#999", linestyle="--", alpha=0.5)
        for bar, s in zip(bars, raw_scores):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                    f"{s:.3f}", va="center", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    with detail_col2:
        st.markdown("**Giải thích kết quả:**")
        
        if score >= 70:
            st.error(f"""
            🔴 **Rất bất thường** — Score {score}/100
            
            Giá đăng **{gia_ban_input:.2f} tỷ** {anomaly['anomaly_type'].lower()} so với 
            giá dự đoán **{predicted:.2f} tỷ**. Tin đăng này cần được kiểm tra kỹ.
            """)
        elif score >= 50:
            st.warning(f"""
            🟠 **Bất thường** — Score {score}/100
            
            Giá đăng chênh lệch đáng kể so với dự đoán. Có thể do đặc điểm đặc biệt 
            của căn nhà chưa được capture trong model.
            """)
        elif score >= 30:
            st.info(f"""
            🟡 **Cần xem xét** — Score {score}/100
            
            Giá đăng hơi khác biệt so với khu vực. Nên so sánh thêm với các tin đăng tương tự.
            """)
        else:
            st.success(f"""
            🟢 **Bình thường** — Score {score}/100
            
            Giá đăng **{gia_ban_input:.2f} tỷ** phù hợp với dự đoán **{predicted:.2f} tỷ** 
            và mặt bằng giá khu vực.
            """)
        
        # Summary
        avg_pred = np.mean(list(all_predictions.values()))
        st.markdown("**Tổng hợp:**")
        summary = {
            "Chỉ số": ["Giá đăng bán", "Giá dự báo (RF)", "Chênh lệch", "Anomaly Score", "Phân loại"],
            "Giá trị": [
                f"{gia_ban_input:.2f} tỷ", f"{predicted:.2f} tỷ",
                f"{diff:+.2f} tỷ ({diff_pct:+.1f}%)",
                f"{score}/100", anomaly['label'],
            ],
        }
        st.dataframe(summary, use_container_width=True, hide_index=True)

main()
