import streamlit as st
import pandas as pd
import components.sidebar as sidebar
from utils.helpers import load_data, train_models, score_all_posts

def main():
    sidebar.display()
    
    st.markdown("# 📋 Danh sách tin đăng")
    st.markdown("---")
    
    df = load_data()
    models = train_models()
    
    # Score all posts
    if "scored_df" not in st.session_state:
        with st.spinner("Đang phân tích bất thường cho toàn bộ tin đăng..."):
            st.session_state.scored_df = score_all_posts(df, models)
    
    scored = st.session_state.scored_df.copy()
    
    # ── FILTERS ──
    st.markdown("### 🔍 Bộ lọc")
    
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_quan = st.multiselect("Quận", options=sorted(scored["quan"].unique()), default=sorted(scored["quan"].unique()))
    with fc2:
        sel_loai = st.multiselect("Loại hình", options=sorted(scored["loai_hinh"].unique()), default=sorted(scored["loai_hinh"].unique()))
    with fc3:
        price_range = st.slider("Giá bán (tỷ)", 
                                float(scored["gia_ban"].min()), 
                                float(scored["gia_ban"].max()),
                                (float(scored["gia_ban"].min()), float(scored["gia_ban"].max())))
    with fc4:
        area_range = st.slider("Diện tích (m²)",
                               float(scored["dien_tich"].min()),
                               float(scored["dien_tich"].max()),
                               (float(scored["dien_tich"].min()), float(scored["dien_tich"].max())))
    
    fc5, fc6 = st.columns(2)
    with fc5:
        anomaly_filter = st.selectbox("Lọc theo mức bất thường", 
                                      ["Tất cả", "🟢 Bình thường", "🟡 Cần xem xét", "🟠 Bất thường", "🔴 Rất bất thường"])
    with fc6:
        sort_by = st.selectbox("Sắp xếp theo", 
                               ["Anomaly Score (cao → thấp)", "Anomaly Score (thấp → cao)", 
                                "Giá (cao → thấp)", "Giá (thấp → cao)", "Diện tích (lớn → nhỏ)"])
    
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
    
    # ── STATS ──
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.metric("Tổng tin lọc được", f"{len(filtered):,}")
    with stat2:
        n_anomaly = len(filtered[filtered["anomaly_score"] >= 50])
        st.metric("🔴🟠 Bất thường", f"{n_anomaly:,}", f"{n_anomaly/max(len(filtered),1)*100:.1f}%")
    with stat3:
        st.metric("Giá trung vị", f"{filtered['gia_ban'].median():.2f} tỷ" if len(filtered) > 0 else "—")
    with stat4:
        st.metric("DT trung bình", f"{filtered['dien_tich'].mean():.0f} m²" if len(filtered) > 0 else "—")
    
    st.markdown("---")
    
    # ── TABLE ──
    display_cols = [
        "id", "quan", "loai_hinh", "dien_tich", "so_phong_ngu",
        "gia_ban", "gia_du_bao", "anomaly_score", "label", "anomaly_type"
    ]
    
    display_df = filtered[display_cols].rename(columns={
        "id": "ID",
        "quan": "Quận",
        "loai_hinh": "Loại hình",
        "dien_tich": "DT (m²)",
        "so_phong_ngu": "PN",
        "gia_ban": "Giá đăng (tỷ)",
        "gia_du_bao": "Giá dự báo (tỷ)",
        "anomaly_score": "Score",
        "label": "Phân loại",
        "anomaly_type": "Loại BT",
    })
    
    # Pagination
    page_size = 20
    total_pages = max(1, (len(display_df) - 1) // page_size + 1)
    page = st.number_input("Trang", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(
        display_df.iloc[start_idx:end_idx],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=100,
                format="%d",
            ),
            "Giá đăng (tỷ)": st.column_config.NumberColumn(format="%.2f"),
            "Giá dự báo (tỷ)": st.column_config.NumberColumn(format="%.2f"),
            "DT (m²)": st.column_config.NumberColumn(format="%.1f"),
        }
    )
    
    st.caption(f"Hiển thị {start_idx+1}–{min(end_idx, len(display_df))} / {len(display_df)} tin đăng · Trang {page}/{total_pages}")
    
    st.markdown("---")
    
    # ── CHARTS ──
    st.markdown("### 📊 Phân bố Anomaly Score")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        import matplotlib.pyplot as plt
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
