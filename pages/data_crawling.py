"""
🕷️ Data Crawling — Tự thu thập dữ liệu từ nhatot.com

Mô tả tính năng và quá trình crawl dữ liệu BĐS từ nhatot.com
cho tất cả các quận huyện TP.HCM.
"""
import streamlit as st
import pandas as pd
import components.sidebar as sidebar


# ── Danh sách 22 quận/huyện đã crawl ──
DISTRICTS = [
    {"area_code": 96,  "name": "Quận 1",            "slug": "quan-1"},
    {"area_code": 98,  "name": "Quận 3",            "slug": "quan-3"},
    {"area_code": 99,  "name": "Quận 4",            "slug": "quan-4"},
    {"area_code": 100, "name": "Quận 5",            "slug": "quan-5"},
    {"area_code": 101, "name": "Quận 6",            "slug": "quan-6"},
    {"area_code": 102, "name": "Quận 7",            "slug": "quan-7"},
    {"area_code": 103, "name": "Quận 8",            "slug": "quan-8"},
    {"area_code": 105, "name": "Quận 10",           "slug": "quan-10"},
    {"area_code": 106, "name": "Quận 11",           "slug": "quan-11"},
    {"area_code": 107, "name": "Quận 12",           "slug": "quan-12"},
    {"area_code": 108, "name": "Quận Bình Tân",     "slug": "quan-binh-tan"},
    {"area_code": 109, "name": "Quận Bình Thạnh",   "slug": "quan-binh-thanh"},
    {"area_code": 110, "name": "Quận Gò Vấp",       "slug": "quan-go-vap"},
    {"area_code": 111, "name": "Quận Phú Nhuận",    "slug": "quan-phu-nhuan"},
    {"area_code": 112, "name": "Quận Tân Bình",     "slug": "quan-tan-binh"},
    {"area_code": 113, "name": "Quận Tân Phú",      "slug": "quan-tan-phu"},
    {"area_code": 114, "name": "Huyện Bình Chánh",  "slug": "huyen-binh-chanh"},
    {"area_code": 115, "name": "Huyện Cần Giờ",     "slug": "huyen-can-gio"},
    {"area_code": 116, "name": "Huyện Củ Chi",      "slug": "huyen-cu-chi"},
    {"area_code": 117, "name": "Huyện Hóc Môn",     "slug": "huyen-hoc-mon"},
    {"area_code": 118, "name": "Huyện Nhà Bè",      "slug": "huyen-nha-be"},
    {"area_code": 119, "name": "TP. Thủ Đức",       "slug": "thanh-pho-thu-duc"},
]


def render():
    sidebar.display()

    st.markdown("## 🕷️ Data Crawling — Thu thập dữ liệu từ Nhà Tốt")
    st.markdown("""
    > **Bonus Feature**: Hệ thống tự động crawl dữ liệu bất động sản từ
    > [nhatot.com](https://www.nhatot.com) cho **tất cả 22 quận/huyện TP.HCM**,
    > mở rộng từ 3 quận ban đầu (8,273 tin) lên toàn thành phố.
    """)

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏗️ Kiến trúc Crawler",
        "🛡️ Anti-blocking",
        "📊 Kết quả Crawl",
        "📋 Data Schema & Quận/Huyện",
    ])

    with tab1:
        render_architecture_tab()
    with tab2:
        render_antiblock_tab()
    with tab3:
        render_results_tab()
    with tab4:
        render_schema_tab()


def render_architecture_tab():
    st.markdown("### 🏗️ Kiến trúc Crawler")

    st.markdown("""
    Crawler được xây dựng bằng Python, sử dụng `curl_cffi` để giả lập TLS fingerprint
    của Chrome 131, bypass hệ thống anti-bot của Nhà Tốt.
    """)

    # Pipeline flow
    st.markdown("#### 📐 Quy trình crawl mỗi quận")

    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0;">
        <div class="info-card info-card-blue" style="text-align: center;">
            <p style="font-size: 28px; margin: 0;">1️⃣</p>
            <h4 style="color: #1d4ed8; margin: 8px 0 4px 0;">Build URL</h4>
            <p style="color: #475569; font-size: 13px; margin: 0;">
                <code>nhatot.com/mua-ban-bat-dong-san-{slug}-tp-ho-chi-minh?page={N}</code>
            </p>
        </div>
        <div class="info-card info-card-green" style="text-align: center;">
            <p style="font-size: 28px; margin: 0;">2️⃣</p>
            <h4 style="color: #16a34a; margin: 8px 0 4px 0;">Web Scrape</h4>
            <p style="color: #475569; font-size: 13px; margin: 0;">
                Parse HTML → <code>__NEXT_DATA__</code> (Next.js JSON)
            </p>
        </div>
        <div class="info-card info-card-amber" style="text-align: center;">
            <p style="font-size: 28px; margin: 0;">3️⃣</p>
            <h4 style="color: #d97706; margin: 8px 0 4px 0;">Fallback API</h4>
            <p style="color: #475569; font-size: 13px; margin: 0;">
                <code>gateway.chotot.com/v1/public</code><br>nếu web scrape thất bại
            </p>
        </div>
        <div class="info-card info-card-red" style="text-align: center;">
            <p style="font-size: 28px; margin: 0;">4️⃣</p>
            <h4 style="color: #dc2626; margin: 8px 0 4px 0;">Parse & Save</h4>
            <p style="color: #475569; font-size: 13px; margin: 0;">
                Giá (VNĐ→tỷ), DT, PN, địa chỉ, mô tả → CSV
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 🔧 Công nghệ sử dụng")

    st.markdown("""
    | Thành phần | Công nghệ | Vai trò |
    |-----------|-----------|---------|
    | **HTTP Client** | `curl_cffi` | Giả lập TLS fingerprint Chrome 131 |
    | **HTML Parser** | `BeautifulSoup` | Parse HTML, trích xuất `__NEXT_DATA__` |
    | **Data Processing** | `pandas` | Parse, validate, export CSV |
    | **Anti-bot** | `impersonate="chrome131"` | Bypass TLS detection của Nhà Tốt |
    | **Fallback** | Chợ Tốt Gateway API | Backup khi web scrape thất bại |
    """)

    st.divider()

    st.markdown("#### 💻 Code Highlights")

    st.code("""
# ── Session dùng curl_cffi (giả lập Chrome TLS fingerprint) ──
from curl_cffi import requests as cffi_requests

session = cffi_requests.Session(impersonate="chrome131")

def warmup_session():
    \"\"\"Truy cập trang chủ trước để lấy cookies — giống user thật\"\"\"
    resp = session.get('https://www.nhatot.com/', timeout=15)
    return True

# ── Crawl 1 quận ──
def crawl_district_data(area_code, district_info, max_pages=300):
    slug = district_info['slug']
    for page in range(1, max_pages + 1):
        url = f"https://www.nhatot.com/mua-ban-bat-dong-san-{slug}"
              f"-tp-ho-chi-minh?page={page}"
        # Web scrape → Fallback API → Parse → Deduplicate
        ...
    """, language="python")

    st.markdown("""
    <div class="info-card info-card-blue">
        <p style="color: #334155; margin: 0;">
            <strong>Notebook tham khảo:</strong> <code>notebooks/00_crawl_data.ipynb</code> —
            Chứa toàn bộ source code crawler với đầy đủ error handling, retry logic và data validation.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_antiblock_tab():
    st.markdown("### 🛡️ Anti-blocking Features")

    st.markdown("""
    Nhà Tốt sử dụng hệ thống anti-bot để phát hiện và chặn crawler.
    Hệ thống crawl của chúng tôi sử dụng nhiều kỹ thuật để bypass:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card info-card-blue">
            <h4 style="color: #1d4ed8; margin-top: 0;">🔐 TLS Fingerprint Impersonation</h4>
            <p style="color: #334155;">
                Sử dụng <code>curl_cffi</code> với <code>impersonate="chrome131"</code>
                để TLS handshake giống hệt Chrome 131 thật.
            </p>
            <p style="color: #64748b; font-size: 13px;">
                <strong>Vấn đề:</strong> Nhà Tốt detect TLS fingerprint của thư viện <code>requests</code>
                Python (khác với browser thật) → trả về 403.<br>
                <strong>Giải pháp:</strong> <code>curl_cffi</code> tạo TLS handshake giống hệt Chrome → bypass.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card info-card-green">
            <h4 style="color: #16a34a; margin-top: 0;">🍪 Session Warmup</h4>
            <p style="color: #334155;">
                Truy cập trang chủ <code>nhatot.com</code> trước khi crawl để lấy cookies tự nhiên —
                giống hành vi người dùng thật.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card info-card-amber">
            <h4 style="color: #d97706; margin-top: 0;">⏱️ Random Delays</h4>
            <p style="color: #334155;">
                <strong>Giữa các trang:</strong> 2–4 giây (random)<br>
                <strong>Mỗi 10 trang:</strong> Nghỉ thêm 5–10 giây<br>
                <strong>Giữa các quận:</strong> Delay riêng + random
            </p>
            <p style="color: #64748b; font-size: 13px;">
                Mô phỏng tốc độ duyệt web của người thật, tránh rate limiting.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card info-card-red">
            <h4 style="color: #dc2626; margin-top: 0;">🔄 Retry Logic & Error Handling</h4>
            <p style="color: #334155;">
                <strong>Max 3 retries</strong> với exponential backoff khi bị 403/429<br>
                <strong>Dừng tự động</strong> sau 3 trang trống liên tiếp<br>
                <strong>Fallback:</strong> Web scrape → API gateway
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📊 So sánh: requests vs curl_cffi")

    st.markdown("""
    | Tiêu chí | `requests` (Python) | `curl_cffi` (Chrome 131) |
    |----------|:-------------------:|:------------------------:|
    | TLS Fingerprint | Python/urllib3 | Chrome 131 thật |
    | Nhà Tốt Response | **403 Forbidden** | **200 OK** |
    | Cookie Handling | Manual | Automatic (như browser) |
    | HTTP/2 Support | Không | Có |
    | Anti-bot Bypass | Không | **Có** |
    """)


def render_results_tab():
    st.markdown("### 📊 Kết quả Crawl Data")

    # Summary stats
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px;">
        <div class="stat-box">
            <div class="stat-icon">📊</div>
            <div class="stat-label">Tổng records</div>
            <div class="stat-value" style="color: #2563eb;">59,590</div>
            <div class="stat-detail">Từ 22 quận/huyện</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">🏘️</div>
            <div class="stat-label">Quận/Huyện</div>
            <div class="stat-value" style="color: #16a34a;">22</div>
            <div class="stat-detail">Toàn TP.HCM</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">📄</div>
            <div class="stat-label">Max pages/quận</div>
            <div class="stat-value">300</div>
            <div class="stat-detail">~20 ads/page</div>
        </div>
        <div class="stat-box">
            <div class="stat-icon">📐</div>
            <div class="stat-label">Data schema</div>
            <div class="stat-value">24</div>
            <div class="stat-detail">Cột dữ liệu</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Comparison: original vs crawled
    st.markdown("#### 📈 So sánh: Dữ liệu gốc vs Crawl mở rộng")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card info-card-amber">
            <h4 style="color: #d97706; margin-top: 0;">📁 Dữ liệu gốc (ban đầu)</h4>
            <ul style="color: #334155; margin: 8px 0; padding-left: 20px;">
                <li><strong>3 quận:</strong> Bình Thạnh, Gò Vấp, Phú Nhuận</li>
                <li><strong>8,273</strong> tin đăng</li>
                <li>Dữ liệu được cung cấp sẵn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card info-card-green">
            <h4 style="color: #16a34a; margin-top: 0;">🕷️ Dữ liệu crawl (mở rộng)</h4>
            <ul style="color: #334155; margin: 8px 0; padding-left: 20px;">
                <li><strong>22 quận/huyện:</strong> Toàn TP.HCM</li>
                <li><strong>59,590</strong> tin đăng (~7.2× lớn hơn)</li>
                <li>Tự thu thập bằng crawler</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("#### 📉 Data Quality")

    quality_data = {
        "Chỉ số": [
            "Tổng records",
            "Missing giá_bán",
            "Missing số_phòng_ngủ",
            "Missing diện_tích",
            "Records hợp lệ (sau validate)",
        ],
        "Giá trị": [
            "59,590",
            "~2.5%",
            "~23.2%",
            "< 1%",
            "~55,000+",
        ],
        "Ghi chú": [
            "22 quận/huyện TP.HCM",
            "Tin chưa công bố giá",
            "Không bắt buộc khi đăng tin",
            "Hầu hết tin đều có diện tích",
            "Sau khi loại missing giá & DT",
        ],
    }
    st.dataframe(quality_data, use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("#### 🎯 Tại sao tự crawl?")

    st.markdown("""
    | Lý do | Giải thích |
    |-------|-----------|
    | **Mở rộng phạm vi** | Dữ liệu gốc chỉ có 3 quận → crawler cho phép mở rộng **24 quận**, bao phủ toàn TP.HCM |
    | **Dữ liệu realtime** | Có thể chạy lại crawler bất kỳ lúc nào để lấy **dữ liệu mới nhất** |
    | **Kiểm soát chất lượng** | Tùy chỉnh parsing logic, tự quyết định fields cần lấy |
    | **Tái sử dụng** | Crawler có thể mở rộng cho các thành phố khác (Hà Nội, Đà Nẵng...) |
    | **Kỹ năng Data Engineering** | Thể hiện khả năng xây dựng **end-to-end data pipeline** |
    """)


def render_schema_tab():
    st.markdown("### 📋 Data Schema")

    st.markdown("#### Cấu trúc dữ liệu output (mỗi quận → 1 file CSV)")

    schema_data = {
        "Cột": [
            "url", "tieu_de", "gia_ban", "don_gia", "dien_tich",
            "so_phong_ngu", "so_tang", "loai_hinh", "giay_to_phap_ly",
            "dia_chi", "quan", "phuong", "duong",
            "mo_ta", "dac_diem", "bieu_do_gia",
        ],
        "Kiểu": [
            "str", "str", "float", "str", "float",
            "int", "int", "str", "str",
            "str", "str", "str", "str",
            "str", "str", "str",
        ],
        "Mô tả": [
            "Link tin đăng trên nhatot.com",
            "Tiêu đề tin đăng",
            "Giá bán (tỷ VNĐ) — đã convert từ VNĐ",
            "Đơn giá (triệu/m²)",
            "Diện tích (m²)",
            "Số phòng ngủ",
            "Số tầng",
            "Loại hình (Nhà ngõ/hẻm, Nhà mặt phố, ...)",
            "Giấy tờ pháp lý (Sổ hồng, HĐ mua bán, ...)",
            "Địa chỉ đầy đủ",
            "Quận/Huyện",
            "Phường/Xã",
            "Đường",
            "Mô tả chi tiết tin đăng",
            "Đặc điểm bổ sung (Hẻm xe hơi, ...)",
            "Dữ liệu biểu đồ giá khu vực (JSON)",
        ],
    }
    st.dataframe(schema_data, use_container_width=True, hide_index=True)

    st.divider()

    # District list
    st.markdown("#### 🏘️ Danh sách 22 quận/huyện đã crawl")

    n_quan = len([d for d in DISTRICTS if d["name"].startswith("Quận")])
    n_huyen = len([d for d in DISTRICTS if d["name"].startswith("Huyện")])
    n_tp = len([d for d in DISTRICTS if d["name"].startswith("TP")])

    c1, c2, c3 = st.columns(3)
    c1.metric("Quận", f"{n_quan}")
    c2.metric("Huyện", f"{n_huyen}")
    c3.metric("Thành phố", f"{n_tp}")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Quận nội thành:**")
        for d in DISTRICTS:
            if d["name"].startswith("Quận"):
                st.markdown(f"- {d['name']} (`{d['slug']}`)")

    with col_right:
        st.markdown("**Huyện & TP. Thủ Đức:**")
        for d in DISTRICTS:
            if not d["name"].startswith("Quận"):
                st.markdown(f"- {d['name']} (`{d['slug']}`)")

    st.divider()

    st.markdown("#### 🔗 URL Pattern")
    st.code("""
# Listing URL (web scrape)
https://www.nhatot.com/mua-ban-bat-dong-san-{slug}-tp-ho-chi-minh?page={N}

# Ví dụ:
https://www.nhatot.com/mua-ban-bat-dong-san-quan-1-tp-ho-chi-minh?page=1
https://www.nhatot.com/mua-ban-bat-dong-san-quan-binh-thanh-tp-ho-chi-minh?page=5
https://www.nhatot.com/mua-ban-bat-dong-san-thanh-pho-thu-duc-tp-ho-chi-minh?page=10

# Fallback API
https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&area_v2={area_code}&cg=1000&o={offset}&page={N}
    """, language="text")

    st.markdown("""
    <div class="info-card info-card-blue">
        <p style="color: #334155; margin: 0;">
            <strong>Lưu ý:</strong> Crawler output được lưu tại <code>data/raw/quan-{area_code}-{slug}.csv</code>
            cho từng quận và <code>data/raw/all_districts_combined.csv</code> cho toàn bộ.
            Dữ liệu gốc của 3 quận (Bình Thạnh, Gò Vấp, Phú Nhuận) được sử dụng cho modeling trong dự án này.
        </p>
    </div>
    """, unsafe_allow_html=True)


render()
