import streamlit as st
import numpy as np
import pandas as pd
import components.sidebar as sidebar
from utils.helpers import (
    load_data, train_models, prepare_input, predict_price,
    predict_all_models, compute_anomaly_score
)

def main():
    sidebar.display()
    
    st.markdown("# 📝 Nhập thông tin nhà — Dự đoán giá & Kiểm tra bất thường")
    st.markdown("---")
    
    models = train_models()
    df = load_data()
    
    st.markdown("""
    Nhập thông tin căn nhà bạn muốn đánh giá. Hệ thống sẽ:
    1. **Dự đoán giá bán** từ **4 mô hình Sklearn** (Linear Regression, Ridge, Random Forest, Gradient Boosting)
    2. **Kiểm tra bất thường** bằng Composite Score (Residual-z + Isolation Forest + Percentile + Min/Max)
    3. **Phân tích theo phân khúc** (Quận × Loại hình) cho chẩn đoán chính xác hơn
    """)
    
    st.markdown("---")
    
    # ── INPUT FORM ──
    st.markdown("### 📋 Thông tin cơ bản")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quan = st.selectbox("🏘️ Quận", ["Bình Thạnh", "Gò Vấp", "Phú Nhuận"])
        loai_hinh = st.selectbox("🏠 Loại hình", ["Nhà trong hẻm", "Nhà mặt tiền", "Nhà phố", "Biệt thự"])
        giay_to = st.selectbox("📄 Giấy tờ pháp lý", ["Sổ hồng/ Sổ đỏ", "Hợp đồng mua bán", "chưa xác định"])
    
    with col2:
        dien_tich = st.number_input("📐 Diện tích (m²)", min_value=10.0, max_value=500.0, value=60.0, step=5.0)
        so_phong_ngu = st.number_input("🛏️ Số phòng ngủ", min_value=1, max_value=10, value=3, step=1)
        tien_nghi_score = st.slider("⭐ Điểm tiện nghi (0–5)", 0, 5, 2)
    
    with col3:
        gia_ban_input = st.number_input(
            "💰 Giá đăng bán (tỷ VNĐ)", 
            min_value=0.1, max_value=100.0, value=5.0, step=0.1,
            help="Nhập giá bạn muốn đăng / giá bạn thấy trên tin đăng"
        )
        gia_kv_mean = st.number_input("📊 Giá khu vực TB (triệu/m²)", min_value=10.0, max_value=200.0, value=70.0, step=5.0)
        gia_kv_hien_tai = st.number_input("📈 Giá khu vực hiện tại (triệu/m²)", min_value=10.0, max_value=200.0, value=72.0, step=5.0)
    
    st.markdown("### 🏗️ Đặc điểm nhà")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    with feat_col1:
        is_mat_tien = st.checkbox("Mặt tiền", value=(loai_hinh == "Nhà mặt tiền"))
        is_hxh = st.checkbox("Hẻm xe hơi")
        is_lo_goc = st.checkbox("Lô góc / 2 mặt tiền")
        is_kinh_doanh = st.checkbox("Kinh doanh")
    with feat_col2:
        has_thang_may = st.checkbox("Thang máy")
        is_nha_moi = st.checkbox("Nhà mới xây")
        is_nha_nat = st.checkbox("Nhà nát / cấp 4")
        has_san_thuong = st.checkbox("Sân thượng")
    with feat_col3:
        has_gara = st.checkbox("Gara ô tô")
        is_chinh_chu = st.checkbox("Chính chủ", value=True)
        o_ngay = st.checkbox("Ở ngay")
        is_dong_tien = st.checkbox("Đang có dòng tiền")
    with feat_col4:
        is_no_hau = st.checkbox("Nở hậu")
        has_quy_hoach = st.checkbox("⚠️ Quy hoạch")
        is_ngop_bank = st.checkbox("⚠️ Ngộp bank")
        is_ban_gap = st.checkbox("⚠️ Bán gấp")
    
    st.markdown("---")
    
    # ── PREDICT ──
    if st.button("🔮 Dự đoán giá & Kiểm tra bất thường", type="primary", use_container_width=True):
        
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
        
        # ── RESULTS ──
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
            st.markdown(f"""
            <div style="background: {'#ffebee' if anomaly['anomaly_score'] >= 50 else '#e8f5e9'}; 
                        padding: 24px; border-radius: 12px; text-align: center; 
                        border: 2px solid {'#e53935' if anomaly['anomaly_score'] >= 50 else '#4caf50'};">
                <p style="color: #666; margin: 0; font-size: 14px;">🔍 Anomaly Score</p>
                <p style="font-size: 36px; font-weight: 800; color: {'#c62828' if anomaly['anomaly_score'] >= 50 else '#2e7d32'}; margin: 8px 0;">
                    {anomaly['anomaly_score']}/100
                </p>
                <p style="margin: 0;"><span class="{anomaly['badge_class']}">{anomaly['label']}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        # ─── Multi-model prediction comparison (NEW) ───
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
                use_container_width=True,
                hide_index=True,
            )
            
            # Average and range
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
            import plotly.graph_objects as go
            
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
                yaxis_title="Giá (tỷ VNĐ)",
                height=400,
                showlegend=False,
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
            import matplotlib.pyplot as plt
            
            methods = ["Residual-z\n(w=0.40)", "Min/Max\n(w=0.10)", "Percentile\n(w=0.20)", "Isolation Forest\n(w=0.30)"]
            raw_scores = [anomaly["s_resid"], anomaly["s_minmax"], anomaly["s_percentile"], anomaly["s_ml"]]
            bar_colors = ["#e53935" if s > 0.5 else ("#ff9800" if s > 0.2 else "#4caf50") for s in raw_scores]
            
            fig, ax = plt.subplots(figsize=(6, 3))
            bars = ax.barh(methods, raw_scores, color=bar_colors, edgecolor="white", height=0.6)
            ax.set_xlim(0, 1.1)
            ax.set_xlabel("Score (0–1)")
            ax.axvline(x=0.5, color="#999", linestyle="--", alpha=0.5)
            for bar, score in zip(bars, raw_scores):
                ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                        f"{score:.3f}", va="center", fontsize=10)
            ax.spines[["top", "right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
        
        with detail_col2:
            st.markdown("**Giải thích kết quả:**")
            
            if anomaly["anomaly_score"] >= 70:
                st.error(f"""
                🔴 **Rất bất thường** — Score {anomaly['anomaly_score']}/100
                
                Giá đăng **{gia_ban_input:.2f} tỷ** {anomaly['anomaly_type'].lower()} so với 
                giá dự đoán **{predicted:.2f} tỷ**. Tin đăng này cần được kiểm tra kỹ.
                """)
            elif anomaly["anomaly_score"] >= 50:
                st.warning(f"""
                🟠 **Bất thường** — Score {anomaly['anomaly_score']}/100
                
                Giá đăng chênh lệch đáng kể so với dự đoán. Có thể do đặc điểm đặc biệt 
                của căn nhà chưa được capture trong model.
                """)
            elif anomaly["anomaly_score"] >= 30:
                st.info(f"""
                🟡 **Cần xem xét** — Score {anomaly['anomaly_score']}/100
                
                Giá đăng hơi khác biệt so với khu vực. Nên so sánh thêm với các tin đăng tương tự.
                """)
            else:
                st.success(f"""
                🟢 **Bình thường** — Score {anomaly['anomaly_score']}/100
                
                Giá đăng **{gia_ban_input:.2f} tỷ** phù hợp với dự đoán **{predicted:.2f} tỷ** 
                và mặt bằng giá khu vực.
                """)
            
            # Summary table
            st.markdown("**Tổng hợp:**")
            summary = {
                "Chỉ số": [
                    "Giá đăng bán", "Giá dự báo (RF)", "Giá trung bình 4 models",
                    "Chênh lệch", "Anomaly Score", "Phân loại"
                ],
                "Giá trị": [
                    f"{gia_ban_input:.2f} tỷ",
                    f"{predicted:.2f} tỷ",
                    f"{avg_pred:.2f} tỷ",
                    f"{diff:+.2f} tỷ ({diff_pct:+.1f}%)",
                    f"{anomaly['anomaly_score']}/100",
                    anomaly['label'],
                ],
            }
            st.dataframe(summary, use_container_width=True, hide_index=True)

main()
