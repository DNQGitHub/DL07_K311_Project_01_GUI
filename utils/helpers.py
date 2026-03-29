"""
Utility functions for data loading, prediction, and anomaly detection.
Uses demo/sample data and simplified models for the Streamlit GUI.
In production, replace with actual trained model files (.pkl / .joblib).
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# SAMPLE DATA (demo - replace with real data loading)
# ─────────────────────────────────────────────

def _generate_sample_data(n=500):
    """Generate realistic sample data matching the Nhà Tốt schema."""
    np.random.seed(42)

    quan_list = ["Bình Thạnh", "Gò Vấp", "Phú Nhuận"]
    quan_weights = [0.32, 0.53, 0.15]

    loai_hinh_list = ["Nhà mặt tiền", "Nhà trong hẻm", "Nhà phố", "Biệt thự"]
    giay_to_list = ["Sổ hồng/ Sổ đỏ", "Hợp đồng mua bán", "chưa xác định"]

    phuong_map = {
        "Bình Thạnh": [f"Phường {i}" for i in range(1, 15)],
        "Gò Vấp": [f"Phường {i}" for i in range(1, 13)],
        "Phú Nhuận": [f"Phường {i}" for i in range(1, 12)],
    }

    records = []
    for i in range(n):
        quan = np.random.choice(quan_list, p=quan_weights)
        phuong = np.random.choice(phuong_map[quan])
        loai_hinh = np.random.choice(loai_hinh_list, p=[0.2, 0.5, 0.2, 0.1])
        giay_to = np.random.choice(giay_to_list, p=[0.7, 0.2, 0.1])

        # Area depends on type
        if loai_hinh == "Biệt thự":
            dien_tich = np.random.uniform(100, 300)
        elif loai_hinh == "Nhà mặt tiền":
            dien_tich = np.random.uniform(40, 150)
        else:
            dien_tich = np.random.uniform(20, 100)

        so_phong_ngu = max(1, int(dien_tich / 20) + np.random.randint(-1, 2))
        so_phong_ngu = min(so_phong_ngu, 10)

        # Price model: base on area, type, district
        base_price = dien_tich * 0.06  # ~60 triệu/m²
        if loai_hinh == "Nhà mặt tiền":
            base_price *= 1.8
        elif loai_hinh == "Biệt thự":
            base_price *= 2.2
        if quan == "Phú Nhuận":
            base_price *= 1.3
        elif quan == "Bình Thạnh":
            base_price *= 1.15

        base_price *= np.random.uniform(0.7, 1.3)
        gia_ban = round(base_price, 2)

        # Text features
        is_mat_tien = 1 if loai_hinh == "Nhà mặt tiền" else int(np.random.random() < 0.1)
        is_hxh = 0 if is_mat_tien else int(np.random.random() < 0.4)
        is_lo_goc = int(np.random.random() < 0.12)
        is_kinh_doanh = int(np.random.random() < 0.2) if is_mat_tien else int(np.random.random() < 0.05)
        has_thang_may = int(np.random.random() < 0.15) if dien_tich > 60 else 0
        is_nha_moi = int(np.random.random() < 0.3)
        is_nha_nat = int(np.random.random() < 0.05)
        has_san_thuong = int(np.random.random() < 0.35)
        has_gara = int(np.random.random() < 0.15) if dien_tich > 50 else 0
        o_ngay = int(np.random.random() < 0.4)
        is_chinh_chu = int(np.random.random() < 0.6)
        has_quy_hoach = int(np.random.random() < 0.03)
        is_ngop_bank = int(np.random.random() < 0.04)
        is_ban_gap = int(np.random.random() < 0.06)
        is_dong_tien = int(np.random.random() < 0.1)
        is_no_hau = int(np.random.random() < 0.08)
        tien_nghi_score = np.random.randint(0, 6)

        # Giá khu vực
        gia_kv_mean = np.random.uniform(40, 120)
        gia_kv_hien_tai = gia_kv_mean * np.random.uniform(0.9, 1.1)
        gia_kv_trend = np.random.uniform(-0.05, 0.08)
        gia_kv_volatility = np.random.uniform(0.02, 0.15)

        # Title & description
        duong = f"Đường {np.random.choice(['Nguyễn Văn Đậu', 'Phan Đăng Lưu', 'Bạch Đằng', 'Lê Quang Định', 'Nguyễn Thái Sơn', 'Quang Trung', 'Phạm Văn Đồng', 'Hoàng Hoa Thám', 'Phan Xích Long', 'Nơ Trang Long'])}"
        tieu_de = f"Bán {loai_hinh.lower()} {duong}, {phuong}, {quan}"
        if is_ban_gap:
            tieu_de = "BÁN GẤP! " + tieu_de

        mo_ta = f"Diện tích {dien_tich:.0f}m², {so_phong_ngu} phòng ngủ, {giay_to.lower()}."
        if is_nha_moi:
            mo_ta += " Nhà mới xây, nội thất cao cấp."
        if is_mat_tien:
            mo_ta += " Mặt tiền kinh doanh sầm uất."

        dia_chi = f"{duong}, {phuong}, {quan}, TP.HCM"

        records.append({
            "id": i + 1,
            "tieu_de": tieu_de,
            "mo_ta": mo_ta,
            "dia_chi": dia_chi,
            "quan": quan,
            "phuong": phuong,
            "loai_hinh": loai_hinh,
            "giay_to_phap_ly": giay_to,
            "dien_tich": round(dien_tich, 1),
            "so_phong_ngu": so_phong_ngu,
            "gia_ban": gia_ban,
            "log_gia_ban": round(np.log(gia_ban), 4) if gia_ban > 0 else 0,
            "is_mat_tien": is_mat_tien,
            "is_hxh": is_hxh,
            "is_lo_goc": is_lo_goc,
            "is_kinh_doanh": is_kinh_doanh,
            "is_dong_tien": is_dong_tien,
            "is_no_hau": is_no_hau,
            "has_thang_may": has_thang_may,
            "is_nha_moi": is_nha_moi,
            "is_nha_nat": is_nha_nat,
            "has_quy_hoach": has_quy_hoach,
            "is_chinh_chu": is_chinh_chu,
            "has_san_thuong": has_san_thuong,
            "has_gara": has_gara,
            "o_ngay": o_ngay,
            "is_ngop_bank": is_ngop_bank,
            "is_ban_gap": is_ban_gap,
            "tien_nghi_score": tien_nghi_score,
            "gia_kv_hien_tai": round(gia_kv_hien_tai, 2),
            "gia_kv_mean": round(gia_kv_mean, 2),
            "gia_kv_trend": round(gia_kv_trend, 4),
            "gia_kv_volatility": round(gia_kv_volatility, 4),
        })

    df = pd.DataFrame(records)
    return df


@st.cache_data
def load_data():
    """Load dataset. Replace with actual data path in production."""
    return _generate_sample_data(500)


# ─────────────────────────────────────────────
# MODEL TRAINING (cached)
# ─────────────────────────────────────────────

PREDICTION_FEATURES = [
    "dien_tich", "so_phong_ngu",
    "is_mat_tien", "is_hxh", "is_lo_goc",
    "is_kinh_doanh", "is_dong_tien", "is_no_hau",
    "has_thang_may", "is_nha_moi", "is_nha_nat",
    "has_quy_hoach", "is_chinh_chu", "has_san_thuong",
    "has_gara", "o_ngay", "tien_nghi_score",
    "gia_kv_hien_tai", "gia_kv_mean",
    "gia_kv_trend", "gia_kv_volatility",
    "quan_encoded", "loai_hinh_encoded", "giay_to_encoded",
]

ANOMALY_FEATURES = PREDICTION_FEATURES  # same feature set for IF


@st.cache_resource
def train_models():
    """Train 4 Sklearn models + Isolation Forest. Returns dict of models + encoders + metrics."""
    df = load_data().copy()

    # Encode categoricals
    le_quan = LabelEncoder().fit(df["quan"])
    le_loai = LabelEncoder().fit(df["loai_hinh"])
    le_giay = LabelEncoder().fit(df["giay_to_phap_ly"])

    df["quan_encoded"] = le_quan.transform(df["quan"])
    df["loai_hinh_encoded"] = le_loai.transform(df["loai_hinh"])
    df["giay_to_encoded"] = le_giay.transform(df["giay_to_phap_ly"])

    X = df[PREDICTION_FEATURES].values
    y = df["gia_ban"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ── Define 4 Sklearn models ──
    sklearn_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, random_state=42),
    }

    sklearn_results = []
    trained_sklearn = {}

    for name, model in sklearn_models.items():
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        r2 = r2_score(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)

        trained_sklearn[name] = model
        sklearn_results.append({
            "Model": name,
            "MAE": round(mae, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 4),
            "Train_R2": round(train_r2, 4),
        })

    # Best model for prediction (RF)
    rf = trained_sklearn["Random Forest"]
    best_result = [r for r in sklearn_results if r["Model"] == "Random Forest"][0]

    # Feature importances from RF
    feature_importances = {}
    for fname, imp in zip(PREDICTION_FEATURES, rf.feature_importances_):
        feature_importances[fname] = round(float(imp), 4)

    # Isolation Forest for anomaly detection
    iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=42, n_jobs=-1)
    iso.fit(X)

    # Compute stats for anomaly scoring
    y_pred_all = rf.predict(X)
    residuals = y - y_pred_all

    # Per-segment stats for better anomaly detection
    segment_stats = {}
    for q in df["quan"].unique():
        for lt in df["loai_hinh"].unique():
            mask = (df["quan"] == q) & (df["loai_hinh"] == lt)
            if mask.sum() > 5:
                seg_prices = df.loc[mask, "gia_ban"]
                seg_residuals = residuals[mask.values]
                segment_stats[(q, lt)] = {
                    "p10": float(seg_prices.quantile(0.10)),
                    "p90": float(seg_prices.quantile(0.90)),
                    "resid_mean": float(seg_residuals.mean()),
                    "resid_std": float(seg_residuals.std()) if seg_residuals.std() > 0 else 1.0,
                    "price_min": float(seg_prices.quantile(0.01)),
                    "price_max": float(seg_prices.quantile(0.99)),
                }

    return {
        "rf_model": rf,
        "iso_model": iso,
        "le_quan": le_quan,
        "le_loai": le_loai,
        "le_giay": le_giay,
        "residual_mean": residuals.mean(),
        "residual_std": residuals.std(),
        "train_score": best_result["Train_R2"],
        "test_score": best_result["R2"],
        "sklearn_results": sklearn_results,
        "sklearn_models": trained_sklearn,
        "feature_importances": feature_importances,
        "segment_stats": segment_stats,
    }


def prepare_input(row_dict, models):
    """Prepare a single input row for prediction."""
    le_quan = models["le_quan"]
    le_loai = models["le_loai"]
    le_giay = models["le_giay"]

    # Safe transform with fallback
    def safe_encode(le, val):
        try:
            return le.transform([val])[0]
        except ValueError:
            return 0

    row_dict["quan_encoded"] = safe_encode(le_quan, row_dict.get("quan", "Gò Vấp"))
    row_dict["loai_hinh_encoded"] = safe_encode(le_loai, row_dict.get("loai_hinh", "Nhà trong hẻm"))
    row_dict["giay_to_encoded"] = safe_encode(le_giay, row_dict.get("giay_to_phap_ly", "chưa xác định"))

    features = [row_dict.get(f, 0) for f in PREDICTION_FEATURES]
    return np.array(features).reshape(1, -1)


def predict_price(input_features, models):
    """Predict price using Random Forest."""
    return models["rf_model"].predict(input_features)[0]


def predict_all_models(input_features, models):
    """Predict price using all 4 Sklearn models. Returns dict of predictions."""
    predictions = {}
    for name, model in models["sklearn_models"].items():
        predictions[name] = float(model.predict(input_features)[0])
    return predictions


def compute_anomaly_score(input_features, actual_price, predicted_price, models, quan=None, loai_hinh=None):
    """
    Compute composite anomaly score (0-100).
    Combines: Residual-z, Isolation Forest, Percentile range, Min/Max.
    Now supports per-segment scoring.
    """
    residual = actual_price - predicted_price

    # Try per-segment stats first
    seg_key = (quan, loai_hinh) if quan and loai_hinh else None
    seg = models.get("segment_stats", {}).get(seg_key) if seg_key else None

    if seg:
        z_score = (residual - seg["resid_mean"]) / (seg["resid_std"] + 1e-9)
        p10 = seg["p10"]
        p90 = seg["p90"]
        price_min = seg["price_min"]
        price_max = seg["price_max"]
    else:
        z_score = (residual - models["residual_mean"]) / (models["residual_std"] + 1e-9)
        p10 = 0.5
        p90 = 30.0
        price_min = 0.3
        price_max = 50.0

    # S1: Residual-z score (0-1)
    s_resid = min(abs(z_score) / 4, 1.0)

    # S2: Isolation Forest score (0-1)
    iso_score = -models["iso_model"].score_samples(input_features)[0]
    s_ml = min(max((iso_score - 0.4) / 0.2, 0), 1.0)

    # S3: Percentile check — based on actual P10/P90
    if actual_price < p10:
        s_percentile = min((p10 - actual_price) / (p10 + 1e-9), 1.0)
    elif actual_price > p90:
        s_percentile = min((actual_price - p90) / (p90 + 1e-9), 1.0)
    else:
        s_percentile = 0.0

    # S4: Min/Max violation
    s_minmax = 0.0
    if actual_price < price_min:
        s_minmax = min((price_min - actual_price) / (price_min + 1e-9), 1.0)
    elif actual_price > price_max:
        s_minmax = min((actual_price - price_max) / (price_max + 1e-9), 1.0)

    # Composite: w1=0.40, w2=0.10, w3=0.20, w4=0.30 (khớp notebook 08)
    total = 0.40 * s_resid + 0.10 * s_minmax + 0.20 * s_percentile + 0.30 * s_ml
    anomaly_score = round(total * 100, 1)

    # Label
    if anomaly_score >= 70:
        label = "🔴 Rất bất thường"
        badge_class = "badge-critical"
    elif anomaly_score >= 50:
        label = "🟠 Bất thường"
        badge_class = "badge-danger"
    elif anomaly_score >= 30:
        label = "🟡 Cần xem xét"
        badge_class = "badge-warning"
    else:
        label = "🟢 Bình thường"
        badge_class = "badge-normal"

    anomaly_type = "Giá CAO bất thường" if z_score > 0 else "Giá THẤP bất thường"

    return {
        "anomaly_score": anomaly_score,
        "label": label,
        "badge_class": badge_class,
        "z_score": round(z_score, 2),
        "anomaly_type": anomaly_type,
        "s_resid": round(s_resid, 3),
        "s_minmax": round(s_minmax, 3),
        "s_percentile": round(s_percentile, 3),
        "s_ml": round(s_ml, 3),
    }


def score_all_posts(df, models):
    """Score all posts in the dataframe for anomaly detection."""
    df = df.copy()
    le_quan = models["le_quan"]
    le_loai = models["le_loai"]
    le_giay = models["le_giay"]

    df["quan_encoded"] = df["quan"].apply(lambda x: safe_encode_series(le_quan, x))
    df["loai_hinh_encoded"] = df["loai_hinh"].apply(lambda x: safe_encode_series(le_loai, x))
    df["giay_to_encoded"] = df["giay_to_phap_ly"].apply(lambda x: safe_encode_series(le_giay, x))

    X = df[PREDICTION_FEATURES].values
    predictions = models["rf_model"].predict(X)
    df["gia_du_bao"] = predictions.round(2)

    # Anomaly scoring per row (with per-segment support)
    scores = []
    for idx in range(len(df)):
        row_features = X[idx:idx+1]
        actual = df.iloc[idx]["gia_ban"]
        pred = predictions[idx]
        quan = df.iloc[idx]["quan"]
        loai_hinh = df.iloc[idx]["loai_hinh"]
        result = compute_anomaly_score(row_features, actual, pred, models, quan=quan, loai_hinh=loai_hinh)
        scores.append(result)

    score_df = pd.DataFrame(scores)
    for col in score_df.columns:
        df[col] = score_df[col].values

    return df


def safe_encode_series(le, val):
    try:
        return le.transform([val])[0]
    except ValueError:
        return 0


def score_uploaded_csv(uploaded_df, models):
    """
    Score a user-uploaded CSV for anomaly detection.
    Required columns: quan, loai_hinh, dien_tich, so_phong_ngu, gia_ban.
    Missing feature columns are filled with sensible defaults.
    """
    df = uploaded_df.copy()

    # Validate required columns
    required = ["quan", "loai_hinh", "dien_tich", "so_phong_ngu", "gia_ban"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV thiếu các cột bắt buộc: {', '.join(missing)}")

    # ── Fill optional columns with defaults ──
    default_values = {
        "giay_to_phap_ly": "chưa xác định",
        "is_mat_tien": 0, "is_hxh": 0, "is_lo_goc": 0,
        "is_kinh_doanh": 0, "is_dong_tien": 0, "is_no_hau": 0,
        "has_thang_may": 0, "is_nha_moi": 0, "is_nha_nat": 0,
        "has_quy_hoach": 0, "is_chinh_chu": 0, "has_san_thuong": 0,
        "has_gara": 0, "o_ngay": 0, "is_ngop_bank": 0, "is_ban_gap": 0,
        "tien_nghi_score": 0,
        "gia_kv_hien_tai": 70.0, "gia_kv_mean": 70.0,
        "gia_kv_trend": 0.0, "gia_kv_volatility": 0.05,
    }
    for col, default in default_values.items():
        if col not in df.columns:
            df[col] = default

    # ── Add ID and metadata if missing ──
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))
    if "tieu_de" not in df.columns:
        df["tieu_de"] = df.apply(lambda r: f"{r['loai_hinh']} {r.get('dia_chi', r['quan'])}", axis=1)
    if "mo_ta" not in df.columns:
        df["mo_ta"] = ""
    if "dia_chi" not in df.columns:
        df["dia_chi"] = df["quan"]

    # ── Encode & predict ──
    le_quan = models["le_quan"]
    le_loai = models["le_loai"]
    le_giay = models["le_giay"]

    df["quan_encoded"] = df["quan"].apply(lambda x: safe_encode_series(le_quan, x))
    df["loai_hinh_encoded"] = df["loai_hinh"].apply(lambda x: safe_encode_series(le_loai, x))
    df["giay_to_encoded"] = df["giay_to_phap_ly"].apply(lambda x: safe_encode_series(le_giay, x))

    X = df[PREDICTION_FEATURES].values
    predictions = models["rf_model"].predict(X)
    df["gia_du_bao"] = predictions.round(2)

    # Anomaly scoring per row
    scores = []
    for idx in range(len(df)):
        row_features = X[idx:idx+1]
        actual = df.iloc[idx]["gia_ban"]
        pred = predictions[idx]
        quan = df.iloc[idx]["quan"]
        loai_hinh = df.iloc[idx]["loai_hinh"]
        result = compute_anomaly_score(row_features, actual, pred, models, quan=quan, loai_hinh=loai_hinh)
        scores.append(result)

    score_df = pd.DataFrame(scores)
    for col in score_df.columns:
        df[col] = score_df[col].values

    return df


# ─────────────────────────────────────────────
# PYSPARK RESULTS (hardcoded from notebook runs)
# ─────────────────────────────────────────────

def get_pyspark_results():
    """Return actual PySpark model results from notebook 06_model_pyspark.ipynb."""
    return [
        {"Model": "Random Forest", "R²": 0.8201, "RMSE_log": 0.2142, "MAE_log": 0.1588, "MAE_tỷ": 1.303, "RMSE_tỷ": 2.856, "Train_time": "53.8s", "Train_time_sec": 53.8},
        {"Model": "GBT (Gradient Boosted)", "R²": 0.8047, "RMSE_log": 0.2232, "MAE_log": 0.1626, "MAE_tỷ": 1.400, "RMSE_tỷ": 3.108, "Train_time": "384.7s", "Train_time_sec": 384.7},
        {"Model": "Decision Tree", "R²": 0.7653, "RMSE_log": 0.2447, "MAE_log": 0.1793, "MAE_tỷ": 1.481, "RMSE_tỷ": 3.048, "Train_time": "50.3s", "Train_time_sec": 50.3},
        {"Model": "Linear Regression", "R²": 0.6851, "RMSE_log": 0.2834, "MAE_log": 0.2113, "MAE_tỷ": 1.674, "RMSE_tỷ": 3.128, "Train_time": "32.1s", "Train_time_sec": 32.1},
    ]


def get_pyspark_feature_importances():
    """Return actual PySpark GBT feature importances from notebook."""
    return {
        "dien_tich": 0.3675,
        "so_phong_ngu": 0.1069,
        "gia_kv_mean": 0.0851,
        "gia_kv_hien_tai": 0.0657,
        "gia_kv_volatility": 0.0597,
        "gia_kv_trend": 0.0489,
        "tien_nghi_score": 0.0345,
        "is_nha_moi": 0.0169,
        "loai_hinh": 0.0159,
        "is_hxh": 0.0155,
        "is_kinh_doanh": 0.0152,
        "has_thang_may": 0.0135,
        "has_san_thuong": 0.0133,
        "is_mat_tien": 0.0131,
        "is_chinh_chu": 0.0122,
    }


def get_notebook_sklearn_results():
    """Return actual Sklearn results from notebook 05_model_sklearn.ipynb (on real 6979-row data)."""
    return [
        {"Model": "Random Forest", "MAE_log": 0.1402, "RMSE_log": 0.1968, "R²": 0.8455, "MAE_tỷ": 1.076, "RMSE_tỷ": 1.908},
        {"Model": "Gradient Boosting", "MAE_log": 0.1579, "RMSE_log": 0.2091, "R²": 0.8256, "MAE_tỷ": 1.186, "RMSE_tỷ": 1.892},
        {"Model": "Linear Regression", "MAE_log": 0.1875, "RMSE_log": 0.2580, "R²": 0.7344, "MAE_tỷ": 1.540, "RMSE_tỷ": 5.591},
        {"Model": "Ridge Regression", "MAE_log": 0.1877, "RMSE_log": 0.2583, "R²": 0.7338, "MAE_tỷ": 1.541, "RMSE_tỷ": 5.612},
    ]


def get_notebook_feature_importances():
    """Return actual RF feature importances from notebook 05_model_sklearn.ipynb."""
    return {
        "dien_tich": 0.6577,
        "so_phong_ngu": 0.0929,
        "gia_kv_mean": 0.0727,
        "gia_kv_hien_tai": 0.0268,
        "gia_kv_volatility": 0.0215,
        "gia_kv_trend": 0.0186,
        "tien_nghi_score": 0.0119,
        "has_thang_may": 0.0101,
        "loai_hinh": 0.0100,
        "has_san_thuong": 0.0097,
        "is_hxh": 0.0090,
        "is_mat_tien": 0.0082,
        "o_ngay": 0.0075,
        "is_chinh_chu": 0.0070,
        "is_kinh_doanh": 0.0063,
    }


def get_notebook_anomaly_results():
    """Return actual anomaly detection results from notebooks 07 & 08."""
    return {
        "total_posts": 6979,
        "weights": {"w1_resid": 0.40, "w2_minmax": 0.10, "w3_percentile": 0.20, "w4_ml": 0.30},
        "pyspark_distribution": {
            "🟢 Bình thường": 6364,
            "🟡 Cần xem xét": 444,
            "🟠 Bất thường": 127,
            "🔴 Rất bất thường": 44,
        },
        "total_anomalous_50": 171,  # score >= 50
        "pct_anomalous": 2.5,
        "score_stats": {"mean": 13.7, "std": 12.2, "min": 0.2, "max": 96.0},
        "by_district": {
            "Bình Thạnh": {"cao": 59, "thap": 15, "total": 74},
            "Gò Vấp": {"cao": 39, "thap": 19, "total": 58},
            "Phú Nhuận": {"cao": 27, "thap": 12, "total": 39},
        },
        "method_contributions": {
            "Residual-Z": {"detected": 87, "threshold": "|Z| > 3", "pct": 1.2},
            "Min/Max Bounds": {"detected": 679, "pct": 9.7},
            "Percentile P10-P90": {"detected": "~10%", "pct": 10.0},
            "Isolation Forest": {"detected": 265, "threshold": "S_ML > 0.6", "pct": 3.8},
        },
        "top_anomalies": [
            {"quan": "Gò Vấp", "loai_hinh": "Nhà mặt phố", "dien_tich": 106.0, "gia_thuc": 142.0, "gia_predict": 53.47, "score": 96.0, "s_resid": 1.0, "s_minmax": 1.0, "s_pctl": 1.0, "s_ml": 0.868},
            {"quan": "Gò Vấp", "loai_hinh": "Nhà ngõ, hẻm", "dien_tich": 48.0, "gia_thuc": 57.9, "gia_predict": 23.11, "score": 90.0, "s_resid": 1.0, "s_minmax": 1.0, "s_pctl": 0.885, "s_ml": 0.744},
            {"quan": "Gò Vấp", "loai_hinh": "Nhà ngõ, hẻm", "dien_tich": 18.0, "gia_thuc": 0.89, "gia_predict": 2.72, "score": 48.1, "s_resid": 0.481, "s_minmax": 0.0, "s_pctl": 0.0, "s_ml": 0.620},
            {"quan": "Gò Vấp", "loai_hinh": "Nhà ngõ, hẻm", "dien_tich": 96.0, "gia_thuc": 26.0, "gia_predict": 12.67, "score": 45.4, "s_resid": 0.454, "s_minmax": 0.0, "s_pctl": 0.0, "s_ml": 0.0},
            {"quan": "Bình Thạnh", "loai_hinh": "Nhà mặt phố", "dien_tich": 26.0, "gia_thuc": 12.0, "gia_predict": 5.73, "score": 44.8, "s_resid": 0.448, "s_minmax": 0.0, "s_pctl": 0.0, "s_ml": 0.0},
        ],
    }


def get_data_pipeline_info():
    """Return data pipeline summary from notebooks 01-04."""
    return {
        "raw_data": {"rows": 8273, "cols": 24, "sources": 3},
        "after_cleaning": {"rows": 7961, "cols": 9, "dropped_rows": 312, "dropped_cols": 15},
        "after_feature_eng": {"rows": 6979, "cols": 29, "new_features": 22},
        "feature_groups": {
            "Categorical": ["giay_to_phap_ly", "loai_hinh", "quan"],
            "Numeric gốc": ["dien_tich", "gia_ban", "so_phong_ngu"],
            "Giá khu vực": ["gia_kv_hien_tai", "gia_kv_mean", "gia_kv_trend", "gia_kv_volatility"],
            "Text: Vị trí": ["is_mat_tien", "is_hxh", "is_lo_goc"],
            "Text: Kinh tế": ["is_kinh_doanh", "is_dong_tien"],
            "Text: Đặc tính": ["is_no_hau", "has_thang_may", "is_nha_moi", "is_nha_nat",
                               "has_quy_hoach", "is_chinh_chu", "has_san_thuong", "has_gara", "o_ngay"],
            "Text: Bất thường": ["is_ngop_bank", "is_ban_gap"],
            "Tổng hợp": ["tien_nghi_score", "log_gia_ban"],
        },
        "top_correlations": [
            ("dien_tich", 0.69), ("so_phong_ngu", 0.58), ("gia_kv_mean", 0.28),
            ("is_mat_tien", 0.18), ("has_thang_may", 0.17), ("tien_nghi_score", 0.15),
        ],
        "price_stats": {"mean": 8.47, "median": 6.69, "std": 9.12, "min": 0.35, "max": 142.0},
    }
