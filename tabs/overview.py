import streamlit as st
import plotly.express as px
from XuLy.config import *
import pandas as pd

def render(data):

    # =====================================
    # HÀNG 1
    # =====================================
    col1, col2 = st.columns(2)

    with col1:

        fig_age = px.histogram(
            data,
            x="Age",
            nbins=10,
            title="Phân bố độ tuổi người dùng",
            color_discrete_sequence=[COLOR_ZERO],
            opacity=0.9
        )

        fig_age.update_traces(
            texttemplate="%{y}",
            textposition="outside",
            hovertemplate="<b>%{x}</b> tuổi<br>Số lượng: %{y}<extra></extra>",
            marker=dict(
                line=dict(
                    color="black",
                    width=1
                )
        )

        )

        fig_age.update_layout(
            xaxis_title="Tuổi",
            yaxis_title="Số lượng"
        )

        st.plotly_chart(fig_age, use_container_width=True)

    with col2:

        gender_count = (
            data["Gender"]
            .value_counts()
            .reset_index()
        )

        gender_count.columns = ["Gender", "Count"]

        fig_gender = px.pie(
            gender_count,
            names="Gender",
            values="Count",
            title="Tỷ lệ giới tính",
            color_discrete_sequence=[
                COLOR_PRIMARY,
                COLOR_SECONDARY,
                COLOR_ALERT
            ]
        )

        st.plotly_chart(fig_gender, use_container_width=True)

    # =====================================
    # HÀNG 2
    # =====================================

    col3, col4 = st.columns(2)

    with col3:

        occupation_count = (
            data["Occupation"]
            .value_counts()
            .reset_index()
        )

        occupation_count.columns = [
            "Occupation",
            "Count"
        ]

        fig_occ = px.bar(
            occupation_count,
            x="Occupation",
            y="Count",
            title="Phân bố nghề nghiệp",
            color="Count",
            color_continuous_scale="Purples"
        )
        fig_occ.update_traces(
            hovertemplate="%{y}<extra></extra>"
        )

        fig_occ.update_layout(
            xaxis_title="Nghề nghiệp",
            yaxis_title="Số lượng"
        )

        st.plotly_chart(fig_occ, use_container_width=True)

    with col4:

        device_count = (
            data["Device_Type"]
            .value_counts()
            .reset_index()
        )

        device_count.columns = [
            "Device",
            "Count"
        ]

        fig_device = px.bar(
            device_count,
            x="Device",
            y="Count",
            title="Phân bố thiết bị sử dụng",
            color="Count",
            color_continuous_scale=[
                "#BBFFAA",
                "#8AFF7D",
                "#37BA35",
                "#248A41"
            ]
        )
        fig_device.update_traces(
            hovertemplate="%{y}<extra></extra>"
        )

        fig_device.update_layout(
            xaxis_title="Thiết bị",
            yaxis_title="Số lượng"
        )

        st.plotly_chart(fig_device, use_container_width=True)

    # =====================================
    # HÀNG 3
    # =====================================

    st.subheader("Thời gian sử dụng điện thoại theo nghề nghiệp")

    fig_phone_occ = px.box(
        data,
        x="Occupation",
        y="Daily_Phone_Hours",
        color="Occupation",
        title="Daily Phone Hours theo nghề nghiệp"
    )

    fig_phone_occ.update_layout(
        xaxis_title="Nghề nghiệp",
        yaxis_title="Giờ sử dụng mỗi ngày"
    )

    st.plotly_chart(
        fig_phone_occ,
        use_container_width=True
    )

    # =====================================
    # HÀNG 4
    # =====================================

    st.subheader("Phân bố số lượng ứng dụng được sử dụng")

    data["App_Group"] = pd.cut(
        data["App_Usage_Count"],
        bins=[0,10,20,40,100],
        labels=[
            "Ít (0-10)",
            "Trung bình (11-20)",
            "Rất nhiều (>40)",
            "Nhiều (21-40)"
        ]
    )

    app_group = (
        data["App_Group"]
        .value_counts()
        .reset_index()
    )

    app_group.columns = [
        "Nhóm",
        "Số lượng"
    ]

    fig_app_group = px.bar(
        app_group,
        x="Nhóm",
        y="Số lượng",
        title="Mức độ sử dụng ứng dụng",
        color="Số lượng",
        color_continuous_scale="Teal"
    )
    fig_app_group.update_traces(
        hovertemplate="%{y}<extra></extra>"
    )

    st.plotly_chart(
        fig_app_group,
        use_container_width=True
    )