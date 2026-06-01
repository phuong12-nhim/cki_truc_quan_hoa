import streamlit as st
from XuLy.data_loader import load_data

from tabs.overview import render as render_overview
from tabs.health import render as render_health
from tabs.productivity import render as render_productivity

st.set_page_config(
    page_title="The Digital Balance Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)


df = load_data()
# ==========================================
# SIDEBAR & FILTERS
# ==========================================

st.title("📱 The Digital Balance")

st.sidebar.markdown(
    "Trực quan hóa tác động của Smartphone đến "
    "Sức khỏe và Năng suất làm việc"
)

st.markdown(
    f"Phân tích chuyên sâu trên mẫu dữ liệu gồm "
    f"**{len(df):,}** người dùng sau khi lọc."
)

st.markdown("---")

st.sidebar.header("🔎 Bộ lọc dữ liệu")

# =========================
# Device Type
# =========================

device_options = ["Tất cả"] + sorted(
    df["Device_Type"].unique().tolist()
)

selected_device = st.sidebar.selectbox(
    "Thiết bị sử dụng",
    device_options
)

# =========================
# Gender
# =========================

gender_options = ["Tất cả"] + sorted(
    df["Gender"].unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Giới tính",
    gender_options
)

# =========================
# Occupation
# =========================

occupation_options = ["Tất cả"] + sorted(
    df["Occupation"].unique().tolist()
)

selected_occupation = st.sidebar.selectbox(
    "Nghề nghiệp",
    occupation_options
)

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if selected_device != "Tất cả":
    filtered_df = filtered_df[
        filtered_df["Device_Type"] == selected_device
    ]

if selected_gender != "Tất cả":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_occupation != "Tất cả":
    filtered_df = filtered_df[
        filtered_df["Occupation"] == selected_occupation
    ]

# KPI Overview
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "👥 Tổng người dùng",
        f"{len(filtered_df):,}"
    )

with kpi2:
    st.metric(
        "📱 Giờ dùng điện thoại TB",
        round(filtered_df["Daily_Phone_Hours"].mean(), 1)
    )

with kpi3:
    st.metric(
        "😴 Giờ ngủ TB",
        round(filtered_df["Sleep_Hours"].mean(), 1)
    )

with kpi4:
    st.metric(
        "🎯 Năng suất TB",
        round(filtered_df["Work_Productivity_Score"].mean(), 1)
    )
    
tab1, tab2, tab3 = st.tabs([
    "📊 Tổng quan",
    "❤️ Sức khỏe",
    "🎯 Năng suất"
])

with tab1:
    render_overview(filtered_df)

with tab2:
    render_health(filtered_df)

with tab3:
    render_productivity(filtered_df)