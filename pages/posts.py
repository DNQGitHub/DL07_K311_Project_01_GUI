import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, score_all_posts, score_uploaded_csv

def main():
    sidebar.display()
    
    st.markdown("# 📋 Danh sách tin đăng")
    st.markdown("---")
    
    df = load_data()
    models = train_models()
    
    # Score all posts if not cached
    if "scored_df" not in st.session_state:
        with st.spinner("Đang phân tích bất thường cho toàn bộ tin đăng..."):
            st.session_state.scored_df = score_all_posts(df, models)
    
    scored = st.session_state.scored_df.copy()
    
    # ══════════════════════════════════════════════
    # THREE TABS: Browse / Text Search / CSV Upload
    # ══════════════════════════════════════════════
    tab_browse, tab_search, tab_csv = st.tabs([
        "📋 Duyệt tin đăng",
        "🔎 Tìm kiếm bằng text",
        "📤 Upload CSV phân tích",
    ])
    
    # ─────────────────────────────────────────
    # TAB 1: Browse (original functionality)
    # ─────────────────────────────────────────
    with tab_browse:
        _render_browse_tab(scored)
    
    # ─────────────────────────────────────────
    # TAB 2: Text Search
    # ─────────────────────────────────────────
    with tab_search:
        _render_search_tab(scored)
    
    # ─────────────────────────────────────────
    # TAB 3: CSV Upload
    # ─────────────────────────────────────────
    with tab_csv:
        _render_csv_tab(models)


# ══════════════════════════════════════════════
# TAB 1: Duyệt tin đăng (giữ nguyên logic cũ)
# ══════════════════════════════════════════════
def _render_browse_tab(scored):
    st.markdown("### 🔍 Bộ lọc")
    
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_quan = st.multiselect("Quận", options=sorted(scored["quan"].unique()), default=sorted(scored["quan"].unique()), key="browse_quan")
    with fc2:
        sel_loai = st.multiselect("Loại hình", options=sorted(scored["loai_hinh"].unique()), default=sorted(scored["loai_hinh"].unique()), key="browse_loai")
    with fc3:
        price_range = st.slider("Giá bán (tỷ)", 
                                float(scored["gia_ban"].min()), 
                                float(scored["gia_ban"].max()),
                                (float(scored["gia_ban"].min()), float(scored["gia_ban"].max())),
                                key="browse_price")
    with fc4:
        area_range = st.slider("Diện tích (m²)",
                               float(scored["dien_tich"].min()),
                               float(scored["dien_tich"].max()),
                               (float(scored["dien_tich"].min()), float(scored["dien_tich"].max())),
                               key="browse_area")
    
    fc5, fc6 = st.columns(2)
    with fc5:
        anomaly_filter = st.selectbox("Lọc theo mức bất thường", 
                                      ["Tất cả", "🟢 Bình thường", "🟡 Cần xem xét", "🟠 Bất thường", "🔴 Rất bất thường"],
                                      key="browse_anomaly")
    with fc6:
        sort_by = st.selectbox("Sắp xếp theo", 
                               ["Anomaly Score (cao → thấp)", "Anomaly Score (thấp → cao)", 
                                "Giá (cao → thấp)", "Giá (thấp → cao)", "Diện tích (lớn → nhỏ)"],
                               key="browse_sort")
    
    # Apply filters
    mask = (
        scored["quan"].isin(sel_quan) &
        scored["loai_hinh"].isin(sel_loai) &
        scored["gia_ban"].between(price_range[0], price_range[1]) &
        scored["dien_tich"].between(area_range[0], area_range[1])
    )
    if anomaly_filter != "Tất cả":
        mask = mask & (scored["label"] == anomaly_filter)
    
    filtered = scored[mask].copy()
    
    # Sort
    sort_map = {
        "Anomaly Score (cao → thấp)": ("anomaly_score", False),
        "Anomaly Score (thấp → cao)": ("anomaly_score", True),
        "Giá (cao → thấp)": ("gia_ban", False),
        "Giá (thấp → cao)": ("gia_ban", True),
        "Diện tích (lớn → nhỏ)": ("dien_tich", False),
    }
    sort_col, sort_asc = sort_map[sort_by]
    filtered = filtered.sort_values(sort_col, ascending=sort_asc)
    
    st.markdown("---")
    _render_results_table(filtered, "browse")


# ══════════════════════════════════════════════
# TAB 2: Tìm kiếm bằng text
# ══════════════════════════════════════════════
def _render_search_tab(scored):
    st.markdown("### 🔎 Tìm kiếm tin đăng tương đương")
    st.markdown("""
    Nhập từ khóa mô tả căn nhà bạn muốn tìm (ví dụ: *nhà mặt tiền Gò Vấp 80m²*, 
    *hẻm xe hơi Bình Thạnh 3 phòng ngủ*, *biệt thự Phú Nhuận*)
    và hệ thống sẽ tự động lọc các tin đăng phù hợp để phân tích bất thường.
    """)
    
    search_text = st.text_input(
        "🔍 Nhập mô tả căn nhà cần tìm",
        placeholder="VD: nhà mặt tiền Gò Vấp 80m², hẻm xe hơi Bình Thạnh...",
        key="search_text"
    )
    
    if search_text.strip():
        keywords = search_text.lower().strip().split()
        
        # Search across tieu_de, dia_chi, mo_ta, quan, loai_hinh
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
        results = scored[mask].copy()
        
        if len(results) == 0:
            st.warning(f"Không tìm thấy tin đăng nào khớp với: **{search_text}**")
            st.info("💡 Thử rút gọn từ khóa, ví dụ chỉ nhập tên quận hoặc loại hình nhà.")
        else:
            # Sort by anomaly score descending by default
            results = results.sort_values("anomaly_score", ascending=False)
            
            st.success(f"Tìm thấy **{len(results):,}** tin đăng khớp với: *{search_text}*")
            
            # Stats
            st.markdown("---")
            _render_results_table(results, "search")
    else:
        st.info("💡 Nhập từ khóa vào ô tìm kiếm phía trên để bắt đầu.")


# ══════════════════════════════════════════════
# TAB 3: Upload CSV phân tích
# ══════════════════════════════════════════════
def _render_csv_tab(models):
    st.markdown("### 📤 Upload file CSV để phân tích bất thường")
    st.markdown("""
    Upload file CSV chứa thông tin nhiều căn nhà. Hệ thống sẽ tự động:
    1. **Dự đoán giá** cho từng căn nhà bằng model Random Forest
    2. **Chấm điểm bất thường** (Anomaly Score 0–100) theo 4 phương pháp kết hợp
    3. **Phân loại** thành 4 mức: Bình thường / Cần xem xét / Bất thường / Rất bất thường
    """)
    
    # Show required format
    with st.expander("📋 Xem định dạng CSV mẫu (click để mở)", expanded=False):
        st.markdown("**Cột bắt buộc (5 cột):**")
        sample = pd.DataFrame({
            "quan": ["Gò Vấp", "Bình Thạnh", "Phú Nhuận"],
            "loai_hinh": ["Nhà trong hẻm", "Nhà mặt tiền", "Nhà phố"],
            "dien_tich": [65.0, 120.0, 45.0],
            "so_phong_ngu": [3, 5, 2],
            "gia_ban": [4.5, 15.0, 3.2],
        })
        st.dataframe(sample, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Các cột tuỳ chọn** (nếu không có sẽ dùng giá trị mặc định):
        - `giay_to_phap_ly`: Sổ hồng/ Sổ đỏ, Hợp đồng mua bán, chưa xác định
        - `is_mat_tien`, `is_hxh`, `is_lo_goc`, ... (0 hoặc 1)
        - `gia_kv_mean`, `gia_kv_hien_tai` (giá khu vực triệu/m²)
        - `tieu_de`, `dia_chi`, `mo_ta` (text mô tả)
        """)
        
        # Download sample CSV
        csv_sample = sample.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Tải file CSV mẫu",
            csv_sample,
            file_name="mau_du_lieu_nha.csv",
            mime="text/csv",
        )
    
    uploaded_file = st.file_uploader(
        "Chọn file CSV",
        type=["csv"],
        help="File CSV có ít nhất 5 cột: quan, loai_hinh, dien_tich, so_phong_ngu, gia_ban",
        key="csv_uploader",
    )
    
    if uploaded_file is not None:
        try:
            # Try reading with different encodings
            try:
                raw_df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                raw_df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            
            st.info(f"📄 Đã đọc file: **{uploaded_file.name}** — {len(raw_df):,} dòng, {len(raw_df.columns)} cột")
            
            # Preview raw data
            with st.expander("👀 Xem dữ liệu thô (5 dòng đầu)", expanded=False):
                st.dataframe(raw_df.head(), use_container_width=True, hide_index=True)
            
            # Score
            with st.spinner("🔄 Đang dự đoán giá và phân tích bất thường..."):
                scored_csv = score_uploaded_csv(raw_df, models)
            
            st.success(f"✅ Phân tích xong **{len(scored_csv):,}** căn nhà!")
            
            st.markdown("---")
            _render_results_table(scored_csv, "csv")
            
        except ValueError as e:
            st.error(f"❌ Lỗi dữ liệu: {e}")
        except Exception as e:
            st.error(f"❌ Lỗi khi xử lý file: {e}")
    else:
        st.info("📎 Kéo thả hoặc chọn file CSV để bắt đầu phân tích.")


# ══════════════════════════════════════════════
# SHARED: Render results table + charts
# ══════════════════════════════════════════════
def _render_results_table(filtered, prefix):
    """Shared function to render stats, table, and charts for any scored dataframe."""
    if len(filtered) == 0:
        st.warning("Không có dữ liệu để hiển thị.")
        return
    
    # ── STATS ──
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.metric("Tổng tin", f"{len(filtered):,}")
    with stat2:
        n_anomaly = len(filtered[filtered["anomaly_score"] >= 50])
        st.metric("🔴🟠 Bất thường", f"{n_anomaly:,}", f"{n_anomaly/max(len(filtered),1)*100:.1f}%")
    with stat3:
        st.metric("Giá trung vị", f"{filtered['gia_ban'].median():.2f} tỷ")
    with stat4:
        st.metric("DT trung bình", f"{filtered['dien_tich'].mean():.0f} m²")
    
    st.markdown("---")
    
    # ── TABLE ──
    display_cols = [c for c in [
        "id", "quan", "loai_hinh", "dien_tich", "so_phong_ngu",
        "gia_ban", "gia_du_bao", "anomaly_score", "label", "anomaly_type"
    ] if c in filtered.columns]
    
    col_rename = {
        "id": "ID", "quan": "Quận", "loai_hinh": "Loại hình",
        "dien_tich": "DT (m²)", "so_phong_ngu": "PN",
        "gia_ban": "Giá đăng (tỷ)", "gia_du_bao": "Giá dự báo (tỷ)",
        "anomaly_score": "Score", "label": "Phân loại", "anomaly_type": "Loại BT",
    }
    display_df = filtered[display_cols].rename(columns=col_rename)
    
    # Pagination
    page_size = 20
    total_pages = max(1, (len(display_df) - 1) // page_size + 1)
    page = st.number_input("Trang", min_value=1, max_value=total_pages, value=1, step=1, key=f"{prefix}_page")
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    column_config = {
        "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
        "Giá đăng (tỷ)": st.column_config.NumberColumn(format="%.2f"),
        "Giá dự báo (tỷ)": st.column_config.NumberColumn(format="%.2f"),
        "DT (m²)": st.column_config.NumberColumn(format="%.1f"),
    }
    
    st.dataframe(
        display_df.iloc[start_idx:end_idx],
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )
    
    st.caption(f"Hiển thị {start_idx+1}–{min(end_idx, len(display_df))} / {len(display_df)} tin đăng · Trang {page}/{total_pages}")
    
    # ── DOWNLOAD RESULTS ──
    csv_data = filtered[display_cols].to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Tải kết quả phân tích (CSV)",
        csv_data,
        file_name="ket_qua_phan_tich.csv",
        mime="text/csv",
        key=f"{prefix}_download",
    )
    
    st.markdown("---")
    
    # ── CHARTS ──
    st.markdown("### 📊 Phân bố Anomaly Score")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(filtered["anomaly_score"], bins=20, color="#1a73e8", edgecolor="white", alpha=0.85)
        ax.axvline(x=30, color="#ffc107", linestyle="--", label="Ngưỡng Cần xem xét (30)")
        ax.axvline(x=50, color="#ff9800", linestyle="--", label="Ngưỡng Bất thường (50)")
        ax.axvline(x=70, color="#e53935", linestyle="--", label="Ngưỡng Rất BT (70)")
        ax.set_xlabel("Anomaly Score")
        ax.set_ylabel("Số lượng")
        ax.legend(fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    with chart_col2:
        label_counts = filtered["label"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        colors_map = {
            "🟢 Bình thường": "#4caf50",
            "🟡 Cần xem xét": "#ffc107", 
            "🟠 Bất thường": "#ff9800",
            "🔴 Rất bất thường": "#e53935",
        }
        pie_colors = [colors_map.get(l, "#999") for l in label_counts.index]
        ax2.pie(label_counts.values, labels=label_counts.index, colors=pie_colors,
                autopct="%1.1f%%", startangle=90, textprops={"fontsize": 10})
        ax2.set_title("Phân loại bất thường", fontsize=13)
        plt.tight_layout()
        st.pyplot(fig2)
    
    st.markdown("---")
    st.info("💡 Nhấn vào **Chi tiết tin đăng** ở sidebar để xem phân tích chi tiết từng tin.")

main()
