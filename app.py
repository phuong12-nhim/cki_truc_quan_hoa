import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CẤU HÌNH TRANG & BẢNG MÀU (CHUNG)
# ==========================================
st.set_page_config(
    page_title="The Digital Balance Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khai báo bảng màu "Digital Well-being" thống nhất cho cả nhóm
COLOR_PRIMARY = "#7B2CBF"   # Tím (Deep work, Giấc ngủ)
COLOR_SECONDARY = "#00F5D4" # Xanh ngọc (Onscreen, Tech)
COLOR_ALERT = "#FF5A5F"     # Đỏ san hô (Stress, Cảnh báo)
COLOR_BG_GRAY = "#F8F9FA"

# Hoán đổi màu mượt mà cho các biểu đồ liên tục
COLOR_SCALE = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ALERT]

# ==========================================
# 2. LOAD VÀ CACHE DỮ LIỆU (NGƯỜI 1 SETUP)
# ==========================================
@st.cache_data
def load_data():
    """
    Hàm đọc dữ liệu từ file CSV. 
    Lưu ý: Bạn cần kiểm tra và sửa chính xác tên các cột 
    trong file CSV của bạn nếu chúng có khác biệt.
    """
    # Giả định file nằm trong thư mục data/
    df = pd.read_csv("Smartphone_Usage_Productivity_Dataset_50000.csv")
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("Không tìm thấy file dữ liệu! Vui lòng tạo thư mục 'data' và bỏ file 'Smartphone_Usage_Productivity_Dataset_50000.csv' vào.")
    st.stop()

def preprocess(df):

    st.subheader("DEBUG DATA")

    st.write("5 dòng đầu:")
    st.write(df.head())

    st.write("Tên cột:")
    st.write(df.columns)

    st.write("Kiểu dữ liệu:")
    st.write(df.dtypes)

    st.write("Missing values:")
    st.write(df.isnull().sum())

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    df = df.dropna()

    return df

df = df_raw.copy()
# ==========================================
# 3. SIDEBAR & BỘ LỌC TƯƠNG TÁC (NGƯỜI 1 SETUP)
# ==========================================
st.title("The Digital Balance")
st.sidebar.markdown("Trực quan hóa tác động của Smartphone đến Sức khỏe và Năng suất làm việc")
st.markdown(f"Phân tích chuyên sâu trên mẫu dữ liệu gồm **{len(df):,}** người dùng sau khi lọc.")
st.markdown("---")

st.sidebar.header("BỘ LỌC DỮ LIỆU")
st.sidebar.markdown("Thay đổi các tùy chọn dưới đây để cập nhật toàn bộ Dashboard.")

# Bộ lọc 1: Hệ điều hành
os_options = ["Tất cả"] + list(df_raw['Device_OS'].unique()) if 'Device_OS' in df_raw.columns else ["Tất cả"]
selected_os = st.sidebar.selectbox("Hệ điều hành", os_options)

# Bộ lọc 2: Giới tính
gender_options = ["Tất cả"] + list(df_raw['Gender'].unique()) if 'Gender' in df_raw.columns else ["Tất cả"]
selected_gender = st.sidebar.selectbox("Giới tính", gender_options)

# Áp dụng bộ lọc vào dữ liệu chung
if selected_os != "Tất cả":
    df = df[df['Device_OS'] == selected_os]
if selected_gender != "Tất cả":
    df = df[df['Gender'] == selected_gender]


# ==========================================
# 4. KHU VỰC TIÊU ĐỀ & KPI (CHUNG)
# ==========================================

# Hàng số KPI trực quan nhanh
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Tổng số mẫu phân tích", value=f"{len(df):,}")
with kpi2:
    # Sửa lại tên cột tương ứng trong file của bạn nếu khác 'Screen_Time'
    screen_candidates = df.columns[df.columns.str.contains('Screen|Time', case=False)]

    if 'Screen_Time' in df.columns:
        screen_col = 'Screen_Time'
    elif len(screen_candidates) > 0:    
        screen_col = screen_candidates[0]
    else:
        st.error("Không tìm thấy cột thời gian sử dụng màn hình.")
        st.stop()

    st.metric(label="Thời gian On-screen TB", value=f"{round(df[screen_col].mean(), 1)} giờ")
with kpi3:
    prod_col = 'Work_Productivity_Score' if 'Work_Productivity_Score' in df.columns else df.columns[df.columns.str.contains('Productivity', case=False)][0]
    st.metric(label="Điểm Năng suất TB", value=f"{round(df[prod_col].mean(), 1)}/100")
with kpi4:
    stress_col = 'Stress_Level' if 'Stress_Level' in df.columns else df.columns[df.columns.str.contains('Stress', case=False)][0]
    st.metric(label="Mức độ Stress TB", value=f"{round(df[stress_col].mean(), 1)}/10")


# ==========================================
# 5. ĐỊNH NGHĨA CÁC HÀM CHO TỪNG TAB
# ==========================================

# --- NGƯỜI 1: TAB TỔNG QUAN ---
def render_tab_tong_quan(data):
    st.header("Chân dung Người dùng & Tổng quan Hành vi")
    


# --- NGƯỜI 2: TAB SỨC KHỎE & GIẤC NGỦ ---
def render_tab_suc_khoe(data):
    st.header("Phân tích Sức khỏe Sinh học & Áp lực Tâm lý")
    


# --- NGƯỜI 3: TAB NĂNG SUẤT ---
def render_tab_nang_suat(data):
    st.header("Tác động của Công nghệ tới Hiệu suất làm việc")
    
    


# ==========================================
# 6. KHỞI TẠO TABS VÀ PHÂN PHỐI HÀM (CHUNG)
# ==========================================
tab_overview, tab_health, tab_productivity = st.tabs([
    "📊 Tổng quan người dùng", 
    "❤️ Sức khỏe & Giấc ngủ", 
    "🎯 Phân tích Năng suất"
])

# Chia việc hiển thị dữ liệu về đúng các Tab đã tạo
with tab_overview:
    render_tab_tong_quan(df)

with tab_health:
    render_tab_suc_khoe(df)

with tab_productivity:
    render_tab_nang_suat(df)