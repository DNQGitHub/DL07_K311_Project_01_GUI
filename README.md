# 🏠 Dự đoán giá nhà & Phát hiện bất thường — TP.HCM

> **Đồ án AI tốt nghiệp** — Lớp DL07 · K311 · Team 9  
> **Trường:** ĐH Khoa Học Tự Nhiên TP.HCM  
> **GVHD:** ThS. Khuất Thùy Phương  
> **Thành viên:** Đoàn Nhật Quang · Phan Ngọc Minh Quân

---

## 📋 Giới thiệu

Ứng dụng web phân tích bất động sản TP.HCM, xây dựng trên nền tảng **Streamlit**, giải quyết 2 bài toán chính:

| Bài toán | Mô tả | Kết quả |
|----------|-------|---------|
| **Dự đoán giá nhà** | 8 models (4 Sklearn + 4 PySpark) dự đoán giá BĐS từ 29 features | Best R² = **0.846** (Random Forest) |
| **Phát hiện bất thường** | Composite Score kết hợp 4 phương pháp để phát hiện tin đăng giá bất thường | 4 mức phân loại (Bình thường → Rất bất thường) |

**Nguồn dữ liệu:** 6,979 tin đăng BĐS từ [nhatot.com](https://www.nhatot.com) — 3 quận trung tâm (Bình Thạnh, Gò Vấp, Phú Nhuận).

---

## 🚀 Tính năng chính

### 📝 Dự đoán giá
- Nhập thông tin căn nhà → nhận **dự đoán giá** từ 4 models Sklearn
- **Tìm kiếm bằng text** — nhập mô tả tự do (VD: *"nhà mặt tiền Gò Vấp 80m²"*) → tìm tin tương đương
- **Upload CSV** — upload file CSV từ Nhà Tốt → dự đoán giá hàng loạt

### 🔍 Phát hiện bất thường
- **Anomaly Score 0–100** kết hợp 4 phương pháp:
  - Residual Z-Score (40%)
  - Isolation Forest (30%)
  - Percentile P10–P90 (20%)
  - Min/Max Range (10%)
- Phân tích **theo phân khúc** (Quận × Loại hình) giảm false positive

### 📋 Danh sách & Chi tiết tin đăng
- Duyệt, lọc, sắp xếp toàn bộ tin đăng
- Xem chi tiết từng tin: thông tin, đặc điểm, gauge score, biểu đồ so sánh
- **Tìm kiếm text** + **Upload CSV** trên cả 2 trang

### 📊 So sánh Models & Báo cáo
- Bảng kết quả 8 models (MAE, RMSE, R², Feature Importance)
- Data & EDA — pipeline xử lý dữ liệu, thống kê, phân bố

---

## 🏗️ Kiến trúc dự án

```
DL07_K311_Project_01_GUI/
├── app.py                          # Entry point — Navigation + CSS
├── requirements.txt                # Dependencies
├── Procfile                        # Deploy config (Heroku/Render)
├── setup.sh                        # Server setup script
│
├── .streamlit/
│   └── config.toml                 # Streamlit config (hide default nav)
│
├── components/
│   └── sidebar.py                  # Custom sidebar navigation
│
├── pages/
│   ├── home.py                     # 🏠 Trang chủ — Tổng quan dự án
│   ├── business_problem.py         # 📊 Mô tả bài toán
│   ├── task_assignment.py          # 👥 Phân công nhiệm vụ
│   ├── price_prediction.py         # 📝 Dự đoán giá (Form + Search + CSV)
│   ├── model_comparison.py         # 📈 So sánh Models (Sklearn + PySpark)
│   ├── anomaly_results.py          # 🔍 Kết quả phát hiện bất thường
│   ├── data_understanding.py       # 📁 Data & EDA
│   ├── posts.py                    # 📋 Danh sách tin đăng (Browse + Search + CSV)
│   └── post_detail.py              # 🔎 Chi tiết tin đăng (ID + Search + CSV)
│
├── utils/
│   └── helpers.py                  # Core logic: data, models, scoring, CSV parsing
│
└── docs/
    └── REQUIREMENT.md              # Yêu cầu đồ án
```

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| **GUI** | Streamlit |
| **ML Framework** | Scikit-learn |
| **Big Data** | PySpark MLlib |
| **Anomaly Detection** | Composite Score (4 phương pháp) |
| **Visualization** | Plotly, Matplotlib |
| **Data** | Pandas, NumPy |

---

## ⚡ Cài đặt & Chạy

### 1. Clone repository

```bash
git clone https://github.com/DNQGitHub/DL07_K311_Project_01_GUI.git
cd DL07_K311_Project_01_GUI
```

### 2. Tạo virtual environment (khuyến nghị)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: **http://localhost:8501**

---

## 📤 Tính năng Upload CSV

Ứng dụng hỗ trợ upload file CSV **trực tiếp từ dữ liệu Nhà Tốt** (nhatot.com). Hệ thống tự động:

1. **Parse dữ liệu thô** — giá `"7,39 tỷ"` → `7.39`, diện tích `"45 m²"` → `45.0`
2. **Trích xuất quận** — từ địa chỉ `"...Quận Phú Nhuận..."` → `"Phú Nhuận"`
3. **Trích xuất đặc điểm** — từ mô tả/đặc điểm (mặt tiền, hẻm xe hơi, chính chủ, bán gấp...)
4. **Dự đoán giá** + **Chấm điểm bất thường** cho từng căn

### Cột CSV tối thiểu

| Cột | Ví dụ |
|-----|-------|
| `gia_ban` | 7,39 tỷ |
| `dien_tich` | 45 m² |

### Cột nên có (để kết quả chính xác hơn)

| Cột | Ví dụ | Mô tả |
|-----|-------|-------|
| `tieu_de` | Nhà cần bán mặt tiền | Tiêu đề tin |
| `dia_chi` | ...Quận Phú Nhuận, Tp HCM | Trích xuất quận |
| `mo_ta` | Chính chủ, nhà mới xây... | Trích xuất đặc điểm |
| `loai_hinh` | Nhà ngõ, hẻm | Loại hình nhà |
| `don_gia` | 164,22 triệu/m² | Đơn giá/m² |
| `so_phong_ngu` | 2 phòng | Số phòng ngủ |
| `giay_to_phap_ly` | Đã có sổ | Giấy tờ pháp lý |
| `dac_diem` | Hẻm xe hơi | Đặc điểm bổ sung |

---

## 🤖 Models & Phương pháp

### Bài toán 1: Dự đoán giá

| Model | Framework | R² | MAE (tỷ) |
|-------|-----------|-----|----------|
| **Random Forest** | Sklearn | **0.8455** | 0.140 |
| Gradient Boosting | Sklearn | 0.8256 | 0.158 |
| Ridge Regression | Sklearn | 0.7338 | 0.188 |
| Linear Regression | Sklearn | 0.7344 | 0.188 |
| **Random Forest** | PySpark | **0.8201** | — |
| GBT | PySpark | 0.8100 | — |
| Decision Tree | PySpark | 0.7800 | — |
| Linear Regression | PySpark | 0.7200 | — |

### Bài toán 2: Phát hiện bất thường

**Composite Anomaly Score** (0–100) kết hợp 4 phương pháp:

| Phương pháp | Trọng số | Mô tả |
|-------------|---------|-------|
| Residual Z-Score | 40% | Chênh lệch giá đăng vs giá dự đoán |
| Isolation Forest | 30% | Phát hiện outlier bằng ML |
| Percentile P10–P90 | 20% | So sánh với phân vị khu vực |
| Min/Max Range | 10% | So sánh với giá min/max khu vực |

**Phân loại:**

| Score | Nhãn | Ý nghĩa |
|-------|------|---------|
| 0–29 | 🟢 Bình thường | Giá đăng phù hợp thị trường |
| 30–49 | 🟡 Cần xem xét | Giá hơi khác biệt, nên so sánh thêm |
| 50–69 | 🟠 Bất thường | Giá chênh lệch đáng kể |
| 70–100 | 🔴 Rất bất thường | Cần kiểm tra kỹ thông tin |

---

## 📊 Features (29 thuộc tính)

| Nhóm | Features |
|------|----------|
| **Cơ bản** | `dien_tich`, `so_phong_ngu`, `quan`, `loai_hinh`, `giay_to_phap_ly` |
| **Text-mining** | `is_mat_tien`, `is_hxh`, `is_lo_goc`, `is_kinh_doanh`, `has_thang_may`, `is_nha_moi`, `is_nha_nat`, `has_san_thuong`, `has_gara`, `is_chinh_chu`, `o_ngay`, `is_no_hau`, `has_quy_hoach`, `is_ngop_bank`, `is_ban_gap`, `is_dong_tien` |
| **Giá khu vực** | `gia_kv_hien_tai`, `gia_kv_mean`, `gia_kv_trend`, `gia_kv_volatility` |
| **Tổng hợp** | `tien_nghi_score` |
| **Encoded** | `quan_encoded`, `loai_hinh_encoded`, `giay_to_encoded` |

---

## 📁 Data Pipeline

```
Dữ liệu thô (Nhà Tốt)     Sau Cleaning           Sau Feature Engineering
━━━━━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━    ━━━━━━━━━━━━━━━━━━━━━━━
  ~8,000 tin đăng      →    6,979 tin đăng   →     6,979 tin đăng
  15+ thuộc tính             20 thuộc tính           29 thuộc tính
  3 quận TP.HCM              Loại dòng lỗi          +16 text features
                                                     +4 giá khu vực
```

---

## 🌐 Deploy

Ứng dụng đã sẵn sàng deploy lên **Streamlit Cloud**, **Heroku**, hoặc **Render**:

```bash
# Streamlit Cloud — chỉ cần push lên GitHub, connect qua streamlit.io/cloud

# Heroku / Render — dùng Procfile có sẵn
web: sh setup.sh && streamlit run app.py
```

---

## 📝 License

Project này được phát triển cho mục đích học tập trong khuôn khổ đồ án AI tốt nghiệp tại ĐH Khoa Học Tự Nhiên TP.HCM.

---

<div align="center">

**DL07 — K311 — Team 9**  
Đoàn Nhật Quang · Phan Ngọc Minh Quân  
ĐH Khoa Học Tự Nhiên TP.HCM — 2026

</div>
