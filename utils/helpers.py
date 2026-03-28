"""
Utility functions for data loading, prediction, and anomaly detection.
Uses demo/sample data and simplified models for the Streamlit GUI.
In production, replace with actual trained model files (.pkl / .joblib).
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
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
    """Train Random Forest + Isolation Forest. Returns dict of models + encoders."""
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
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    # Isolation Forest for anomaly detection
    iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=42, n_jobs=-1)
    iso.fit(X)
    
    # Compute stats for anomaly scoring
    y_pred_all = rf.predict(X)
    residuals = y - y_pred_all
    
    return {
        "rf_model": rf,
        "iso_model": iso,
        "le_quan": le_quan,
        "le_loai": le_loai,
        "le_giay": le_giay,
        "residual_mean": residuals.mean(),
        "residual_std": residuals.std(),
        "train_score": rf.score(X_train, y_train),
        "test_score": rf.score(X_test, y_test),
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


def compute_anomaly_score(input_features, actual_price, predicted_price, models):
    """
    Compute composite anomaly score (0-100).
    Combines: Residual-z, Isolation Forest, Percentile range, Min/Max.
    """
    residual = actual_price - predicted_price
    z_score = (residual - models["residual_mean"]) / (models["residual_std"] + 1e-9)
    
    # S1: Residual-z score (0-1)
    s_resid = min(abs(z_score) / 4, 1.0)
    
    # S2: Isolation Forest score (0-1)
    iso_score = -models["iso_model"].score_samples(input_features)[0]
    s_ml = min(max((iso_score - 0.4) / 0.2, 0), 1.0)
    
    # S3: Percentile check — ratio-based
    ratio = actual_price / (predicted_price + 1e-9)
    if ratio > 2.0 or ratio < 0.3:
        s_percentile = 1.0
    elif ratio > 1.5 or ratio < 0.5:
        s_percentile = 0.7
    elif ratio > 1.3 or ratio < 0.7:
        s_percentile = 0.4
    else:
        s_percentile = 0.0
    
    # S4: Min/Max violation
    s_minmax = 0.0
    if actual_price < 0.3:
        s_minmax = 1.0  # dưới 300 triệu → rất rẻ
    elif actual_price > 50:
        s_minmax = 0.8  # trên 50 tỷ → rất đắt
    
    # Composite: w1=0.35, w2=0.15, w3=0.20, w4=0.30
    total = 0.35 * s_resid + 0.15 * s_minmax + 0.20 * s_percentile + 0.30 * s_ml
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
    
    # Anomaly scoring per row
    scores = []
    for idx in range(len(df)):
        row_features = X[idx:idx+1]
        actual = df.iloc[idx]["gia_ban"]
        pred = predictions[idx]
        result = compute_anomaly_score(row_features, actual, pred, models)
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
