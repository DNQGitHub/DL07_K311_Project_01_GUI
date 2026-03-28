"""
📊 Model Comparison — Tổng hợp kết quả Bài toán 1: Dự đoán giá nhà

Displays evaluation metrics for 4 Sklearn models and 4 PySpark models,
feature importance analysis, and final model selection conclusions.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import components.sidebar as sidebar

from utils.helpers import (
    train_models,
    get_pyspark_results,
    get_pyspark_feature_importances,
    get_notebook_sklearn_results,
    get_notebook_feature_importances,
)


def render():
    sidebar.display()
    st.markdown("## 📊 Tổng hợp kết quả — Bài toán 1: Dự đoán giá nhà")
    st.markdown("""
    > **Mục tiêu**: So sánh hiệu năng của **8 mô hình** trên **2 nền tảng** (Sklearn & PySpark),
    > chọn model phù hợp nhất cho bài toán dự đoán giá nhà BĐS tại TP.HCM.
    """)

    st.divider()

    # ────────── Tab layout ──────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Sklearn Results",
        "⚡ PySpark Results",
        "🔬 Feature Importance",
        "🏆 Kết luận & Đề xuất",
    ])

    # ==================================================
    # TAB 1: SKLEARN RESULTS
    # ==================================================
    with tab1:
        render_sklearn_tab()

    # ==================================================
    # TAB 2: PYSPARK RESULTS
    # ==================================================
    with tab2:
        render_pyspark_tab()

    # ==================================================
    # TAB 3: FEATURE IMPORTANCE
    # ==================================================
    with tab3:
        render_feature_importance_tab()

    # ==================================================
    # TAB 4: CONCLUSION
    # ==================================================
    with tab4:
        render_conclusion_tab()


def render_sklearn_tab():
    st.markdown("### 🐍 Kết quả mô hình Sklearn (4 models)")
    st.info("""
    **Dữ liệu**: 6,979 tin đăng BĐS tại 3 quận (Bình Thạnh, Gò Vấp, Phú Nhuận)  
    **Target**: `log_gia_ban` (giá bán tính theo log — đơn vị gốc: tỷ VNĐ)  
    **Split**: 80% train / 20% test  
    **Features**: 24 thuộc tính (diện tích, vị trí, tiện nghi, giá khu vực, ...)
    """)

    results = get_notebook_sklearn_results()
    df = pd.DataFrame(results)

    # Styled table
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📋 Bảng metrics (trên tập Test)")
        styled_df = df.copy()
        styled_df.columns = ["Mô hình", "MAE (log)", "RMSE (log)", "R²", "MAE (tỷ VNĐ)", "RMSE (tỷ VNĐ)"]

        # Highlight best
        st.dataframe(
            styled_df.style
            .highlight_min(subset=["MAE (log)", "RMSE (log)", "MAE (tỷ VNĐ)"], color="#2ecc71", props="font-weight: bold")
            .highlight_max(subset=["R²"], color="#2ecc71", props="font-weight: bold")
            .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ VNĐ)": "{:.3f}", "RMSE (tỷ VNĐ)": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.markdown("#### 🏅 Xếp hạng")
        rankings = [
            ("🥇", "Random Forest", "R² = 0.846", "Tốt nhất"),
            ("🥈", "Gradient Boosting", "R² = 0.826", "Thứ 2"),
            ("🥉", "Linear Regression", "R² = 0.734", "Thứ 3"),
            ("4️⃣", "Ridge Regression", "R² = 0.734", "Thứ 4"),
        ]
        for icon, name, score, rank in rankings:
            st.markdown(f"**{icon} {name}** — {score} ({rank})")

    st.markdown("---")

    # Charts
    st.markdown("#### 📊 Biểu đồ so sánh")
    col_a, col_b = st.columns(2)

    with col_a:
        fig_r2 = px.bar(
            df, x="Model", y="R²",
            color="R²",
            color_continuous_scale="Greens",
            title="R² Score (càng cao càng tốt)",
            text="R²",
        )
        fig_r2.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_r2.update_layout(yaxis_range=[0.5, 1.0], showlegend=False, height=400, coloraxis_showscale=False)
        st.plotly_chart(fig_r2, use_container_width=True)

    with col_b:
        fig_mae = px.bar(
            df, x="Model", y="MAE_log",
            color="MAE_log",
            color_continuous_scale="Reds_r",
            title="MAE trên log-scale (càng thấp càng tốt)",
            text="MAE_log",
        )
        fig_mae.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig_mae.update_layout(yaxis_range=[0, 0.3], showlegend=False, height=400, coloraxis_showscale=False)
        st.plotly_chart(fig_mae, use_container_width=True)

    # Radar chart
    st.markdown("#### 🕸️ Radar so sánh tổng thể")
    categories = ["R² (×100)", "MAE_log (×100, ngược)", "RMSE_log (×100, ngược)"]

    fig_radar = go.Figure()
    colors = ["#27ae60", "#3498db", "#e74c3c", "#f39c12"]
    for i, row in df.iterrows():
        r_values = [
            row["R²"] * 100,
            (1 - row["MAE_log"]) * 100,
            (1 - row["RMSE_log"]) * 100,
        ]
        fig_radar.add_trace(go.Scatterpolar(
            r=r_values + [r_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=row["Model"],
            line_color=colors[i],
            opacity=0.6,
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[60, 100])),
        showlegend=True, height=450,
        title="Radar — So sánh đa chiều (Sklearn)",
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Interpretation
    st.markdown("#### 💡 Phân tích kết quả Sklearn")
    st.success("""
    **🏆 Random Forest đạt hiệu năng vượt trội:**
    - **R² = 0.846** → Giải thích được **84.6%** biến thiên giá nhà
    - **MAE = 0.140** (log-scale), tương đương sai số trung bình **~1.08 tỷ VNĐ** trên giá thực
    - Xử lý tốt mối quan hệ **phi tuyến** giữa diện tích, vị trí, tiện nghi và giá
    - **Kháng overfitting** tốt hơn mô hình đơn lẻ (ensemble method)
    """)

    st.warning("""
    **⚠️ Linear & Ridge Regression hạn chế:**
    - R² chỉ đạt **0.734** — cho thấy mối quan hệ giá nhà **không hoàn toàn tuyến tính**
    - RMSE thực tế rất cao (**~5.6 tỷ**) do không khớp được các giá trị outlier
    - Phù hợp làm **baseline** nhưng không nên dùng cho production
    """)


def render_pyspark_tab():
    st.markdown("### ⚡ Kết quả mô hình PySpark (4 models)")
    st.info("""
    **Nền tảng**: Apache Spark MLlib (distributed computing)  
    **Dữ liệu**: 6,979 tin đăng (xử lý qua PySpark DataFrame)  
    **Target**: `log_gia_ban`  
    **Lưu ý**: PySpark được chạy offline trên notebook — kết quả hiển thị dưới dạng báo cáo
    """)

    results = get_pyspark_results()
    df = pd.DataFrame(results)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📋 Bảng metrics PySpark")
        styled_df = df.drop(columns=["Train_time_sec"], errors="ignore").copy()
        styled_df.columns = ["Mô hình", "R²", "RMSE (log)", "MAE (log)", "MAE (tỷ VNĐ)", "RMSE (tỷ VNĐ)", "Thời gian train"]
        st.dataframe(
            styled_df.style
            .highlight_max(subset=["R²"], color="#2ecc71", props="font-weight: bold")
            .highlight_min(subset=["MAE (log)", "RMSE (log)"], color="#2ecc71", props="font-weight: bold")
            .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ VNĐ)": "{:.3f}", "RMSE (tỷ VNĐ)": "{:.3f}"}),
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.markdown("#### 🏅 Xếp hạng")
        rankings = [
            ("🥇", "Random Forest", "R² = 0.820"),
            ("🥈", "GBT", "R² = 0.805"),
            ("🥉", "Decision Tree", "R² = 0.765"),
            ("4️⃣", "Linear Regression", "R² = 0.685"),
        ]
        for icon, name, score in rankings:
            st.markdown(f"**{icon} {name}** — {score}")

    st.markdown("---")

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(
            df, x="Model", y="R²",
            color="R²", color_continuous_scale="Blues",
            title="R² Score — PySpark Models",
            text="R²",
        )
        fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(yaxis_range=[0.5, 1.0], showlegend=False, height=400, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig_time = px.bar(
            df, x="Model", y="Train_time_sec",
            title="⏱ Thời gian train",
            text="Train_time",
            color="Model",
            color_discrete_sequence=["#3498db", "#2ecc71", "#e74c3c", "#f39c12"],
        )
        fig_time.update_traces(textposition='outside')
        fig_time.update_layout(showlegend=False, height=400, yaxis_title="seconds")
        st.plotly_chart(fig_time, use_container_width=True)

    st.markdown("#### 💡 Phân tích kết quả PySpark")
    st.success("""
    **🏆 Random Forest PySpark** cũng đạt hiệu năng tốt nhất:
    - **R² = 0.820** — gần tương đương Sklearn (0.846)
    - **MAE = 0.159** (log-scale), sai số ~1.30 tỷ VNĐ
    - Phù hợp cho **xử lý dữ liệu lớn** (distributed computing)
    """)

    st.info("""
    **🔄 So sánh Sklearn vs PySpark:** Sklearn đạt R² cao hơn ~3% do hyperparameter tuning tốt hơn
    trên tập dữ liệu nhỏ. Khi dữ liệu lớn hơn (>100K), PySpark sẽ có lợi thế về tốc độ.
    """)


def render_feature_importance_tab():
    st.markdown("### 🔬 Phân tích Feature Importance")

    col1, col2 = st.columns(2)

    # ── Sklearn RF Feature Importances ──
    with col1:
        st.markdown("#### 🐍 Random Forest (Sklearn)")
        fi_sklearn = get_notebook_feature_importances()
        fi_df = pd.DataFrame([
            {"Feature": k, "Importance": v} for k, v in fi_sklearn.items()
        ]).sort_values("Importance", ascending=True)

        fig = px.bar(
            fi_df, x="Importance", y="Feature",
            orientation='h',
            color="Importance",
            color_continuous_scale="Greens",
            title="Top 15 Features — RF Sklearn",
            text=fi_df["Importance"].apply(lambda x: f"{x*100:.1f}%"),
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=500, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── PySpark GBT Feature Importances ──
    with col2:
        st.markdown("#### ⚡ GBT (PySpark)")
        fi_pyspark = get_pyspark_feature_importances()
        fi_df2 = pd.DataFrame([
            {"Feature": k, "Importance": v} for k, v in fi_pyspark.items()
        ]).sort_values("Importance", ascending=True)

        fig2 = px.bar(
            fi_df2, x="Importance", y="Feature",
            orientation='h',
            color="Importance",
            color_continuous_scale="Blues",
            title="Top 15 Features — GBT PySpark",
            text=fi_df2["Importance"].apply(lambda x: f"{x*100:.1f}%"),
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(height=500, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Insights
    st.markdown("#### 📌 Nhận xét đáng chú ý")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🏠 Diện tích", "65.8% (Sklearn)", "36.8% (PySpark)")
        st.caption("Yếu tố quyết định chính: Giá ≈ Đơn giá × Diện tích")
    with c2:
        st.metric("🛏️ Số phòng ngủ", "9.3% (Sklearn)", "10.7% (PySpark)")
        st.caption("Phản ánh quy mô nhà, tương quan mạnh với diện tích")
    with c3:
        st.metric("📍 Giá khu vực", "7.3% (Sklearn)", "8.5% (PySpark)")
        st.caption("Giá trung bình khu vực — yếu tố vị trí gián tiếp")

    st.markdown("---")

    # Interpretation
    st.markdown("#### 💡 Insights kinh doanh từ Feature Importance")
    st.markdown("""
    | Insight | Giải thích | Ứng dụng |
    |---------|-----------|----------|
    | **Quy luật "Diện tích là vua"** | 65.8% importance → Giá nhà phụ thuộc lớn vào m² | Chiến lược pricing nên tập trung vào đơn giá/m² |
    | **Vị trí vẫn rất quan trọng** | Features giá khu vực chiếm ~10-20% | Cùng diện tích khác quận → chênh giá lớn |
    | **Tiện nghi là "cherry on top"** | Thang máy, sân thượng chỉ ~1-3% | Không quyết định giá nhưng tạo điểm cộng |
    | **Text features hữu ích** | is_mat_tien, is_hxh có ảnh hưởng | Mặt tiền vs hẻm → chênh lệch giá đáng kể |
    """)

    st.info("""
    **🔑 Key insight**: Sklearn RF cho diện tích importance rất cao (65.8%) vì model chủ yếu
    dự đoán theo diện tích rồi mới điều chỉnh bởi các features khác. PySpark GBT phân bổ
    importance đều hơn (36.8%) do ensemble khác nhau, nhưng thứ tự ưu tiên giống nhau.
    """)


def render_conclusion_tab():
    st.markdown("### 🏆 Kết luận & Đề xuất")

    # Combined comparison table
    st.markdown("#### 📊 Bảng tổng hợp 8 mô hình (cả hai nền tảng)")

    combined = []
    for r in get_notebook_sklearn_results():
        combined.append({
            "Nền tảng": "🐍 Sklearn",
            "Mô hình": r["Model"],
            "R²": r["R²"],
            "MAE (log)": r["MAE_log"],
            "RMSE (log)": r["RMSE_log"],
            "MAE (tỷ)": r["MAE_tỷ"],
        })
    for r in get_pyspark_results():
        combined.append({
            "Nền tảng": "⚡ PySpark",
            "Mô hình": r["Model"],
            "R²": r["R²"],
            "MAE (log)": r["MAE_log"],
            "RMSE (log)": r["RMSE_log"],
            "MAE (tỷ)": r["MAE_tỷ"],
        })

    df_combined = pd.DataFrame(combined).sort_values("R²", ascending=False)

    st.dataframe(
        df_combined.style
        .highlight_max(subset=["R²"], color="#2ecc71", props="font-weight: bold")
        .highlight_min(subset=["MAE (log)", "RMSE (log)"], color="#2ecc71", props="font-weight: bold")
        .format({"R²": "{:.4f}", "MAE (log)": "{:.4f}", "RMSE (log)": "{:.4f}", "MAE (tỷ)": "{:.3f}"}),
        use_container_width=True,
        hide_index=True,
    )

    # Comparison chart
    fig = go.Figure()
    sklearn_r2 = [r["R²"] for r in get_notebook_sklearn_results()]
    spark_r2 = [r["R²"] for r in get_pyspark_results()]
    sklearn_names = [r["Model"] for r in get_notebook_sklearn_results()]
    spark_names = [r["Model"] for r in get_pyspark_results()]

    fig.add_trace(go.Bar(
        name="Sklearn", x=sklearn_names, y=sklearn_r2,
        marker_color="#27ae60", text=[f"{v:.4f}" for v in sklearn_r2],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="PySpark", x=spark_names, y=spark_r2,
        marker_color="#3498db", text=[f"{v:.4f}" for v in spark_r2],
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group", title="So sánh R² — Sklearn vs PySpark",
        yaxis_range=[0.5, 1.0], height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Conclusion boxes
    st.markdown("#### ✅ Kết luận")

    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **🏆 Model tốt nhất: Random Forest (Sklearn)**
        
        | Metric | Giá trị |
        |--------|---------|
        | R² | **0.846** |
        | MAE (log) | **0.140** |
        | RMSE (log) | **0.197** |
        | MAE thực | **~1.08 tỷ VNĐ** |
        
        **Lý do chọn:**
        1. R² cao nhất trong 8 models
        2. MAE & RMSE thấp nhất
        3. Kháng overfitting tốt (ensemble)
        4. Feature importance dễ giải thích
        5. Train time hợp lý
        """)

    with col2:
        st.info("""
        **📊 Đánh giá chất lượng tổng thể**
        
        | Tiêu chí | Đánh giá |
        |----------|----------|
        | Accuracy (R² = 84.6%) | ⭐⭐⭐⭐⭐ Xuất sắc |
        | Precision (MAE = 0.140) | ⭐⭐⭐⭐⭐ Rất tốt |
        | Generalization | ⭐⭐⭐⭐ Tốt |
        | Interpretability | ⭐⭐⭐⭐ Tốt |
        
        **Giải thích kết quả:**
        - Mô hình bắt được **logic thị trường** ✓
        - Diện tích và vị trí là 2 yếu tố chính ✓
        - Tiện nghi là yếu tố phụ ✓
        - Sẵn sàng cho **production** 🎯
        """)

    st.markdown("---")

    # Recommendations
    st.markdown("#### 🚀 Khuyến nghị triển khai")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        **Cho Nhà Tốt Platform:**
        1. 💰 **Auto-pricing**: Gợi ý giá bán hợp lý dựa trên RF
        2. 🚨 **Price validation**: Cảnh báo tin đăng giá chênh >20%
        3. 📈 **Market insights**: Phân tích trend giá theo quận
        4. 👤 **User experience**: Hiển thị "Estimated price range"
        """)

    with col_b:
        st.markdown("""
        **Cải thiện mô hình trong tương lai:**
        1. 🔧 **Feature engineering**: Thêm giao thông, trường học
        2. 🤖 **Ensemble**: Kết hợp RF + XGBoost + Neural Network
        3. 🗺️ **Regional models**: Train riêng model cho từng quận
        4. 🔄 **Real-time update**: Cập nhật khi có data mới
        """)

render()

