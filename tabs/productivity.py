import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from XuLy.config import *

def _sample_data(df, sample_size=2000):
    if len(df) > sample_size:
        return df.sample(sample_size, random_state=42)
    return df.copy()

def _add_trendline(fig, df, x_col, y_col):
    trend_df = df[[x_col, y_col]].dropna().sort_values(x_col)

    if len(trend_df) < 2 or trend_df[x_col].nunique() < 2:
        return

    x = trend_df[x_col]
    y = trend_df[y_col]
    slope = x.cov(y) / x.var()
    intercept = y.mean() - slope * x.mean()

    fig.add_trace(
        go.Scatter(
            x=x.tolist(),
            y=(slope * x + intercept).tolist(),
            mode="lines",
            name="Đường xu hướng",
            line=dict(color=COLOR_ALERT, width=3),
            hovertemplate=(
                "On-screen: %{x:.1f} giờ<br>"
                "Năng suất dự đoán: %{y:.2f}<extra></extra>"
            )
        )
    )


def render(data):
    st.header("🎯 Năng suất")

    df = data.copy()
    if df.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")
        return

    sample_df = _sample_data(df)
    st.caption(f"Hiển thị biểu đồ với {len(sample_df):,} dòng dữ liệu mẫu.")

    col1, col2 = st.columns(2)

    with col1:
        fig_screen_productivity = px.scatter(
            sample_df,
            x="Daily_Phone_Hours",
            y="Work_Productivity_Score",
            color="Device_Type",
            title="Thời gian on-screen vs điểm năng suất",
            opacity=0.65,
            color_discrete_sequence=[
                COLOR_PRIMARY,
                COLOR_SECONDARY,
                COLOR_ALERT
            ],
            labels={
                "Daily_Phone_Hours": "Thời gian on-screen mỗi ngày (giờ)",
                "Work_Productivity_Score": "Điểm năng suất",
                "Device_Type": "Hệ điều hành"
            }
        )

        _add_trendline(
            fig_screen_productivity,
            sample_df,
            "Daily_Phone_Hours",
            "Work_Productivity_Score"
        )

        fig_screen_productivity.update_traces(
            selector=dict(mode="markers"),
            marker=dict(size=7, line=dict(width=0.4, color="white")),
            hovertemplate=(
                "On-screen: %{x:.1f} giờ<br>"
                "Năng suất: %{y}<extra></extra>"
            )
        )

        fig_screen_productivity.update_layout(
            xaxis_title="Thời gian on-screen mỗi ngày (giờ)",
            yaxis_title="Điểm năng suất",
            legend_title_text="Hệ điều hành"
        )

        fig_screen_productivity.update_layout(height=430)
        st.plotly_chart(fig_screen_productivity, use_container_width=True)

    with col2:
        fig_app_heatmap = px.density_heatmap(
            sample_df,
            x="App_Usage_Count",
            y="Work_Productivity_Score",
            nbinsx=25,
            nbinsy=10,
            title="Số lượng app sử dụng vs điểm năng suất",
            color_continuous_scale="Viridis",
            labels={
                "App_Usage_Count": "Số lượng app sử dụng",
                "Work_Productivity_Score": "Điểm năng suất"
            }
        )

        fig_app_heatmap.update_traces(
            hovertemplate=(
                "Số app: %{x}<br>"
                "Năng suất: %{y}<br>"
                "Số người dùng: %{z}<extra></extra>"
            )
        )

        fig_app_heatmap.update_layout(
            xaxis_title="Số lượng app sử dụng",
            yaxis_title="Điểm năng suất",
            coloraxis_colorbar_title="Số người dùng"
        )

        fig_app_heatmap.update_layout(height=430)
        st.plotly_chart(fig_app_heatmap, use_container_width=True)

    # ==============================
    # So sánh theo hệ điều hành
    # ==============================
    os_compare = (
        df.groupby("Device_Type", as_index=False)
        .agg(
            productivity_score=("Work_Productivity_Score", "mean"),
            onscreen_hours=("Daily_Phone_Hours", "mean")
        )
    )

    col3, col4 = st.columns(2)

    with col3:
        fig_productivity = px.bar(
            os_compare,
            x="Device_Type",
            y="productivity_score",
            color="Device_Type",
            title="So sánh điểm năng suất TB theo hệ điều hành",
            text_auto=".2f",
            labels={
                "Device_Type": "Hệ điều hành",
                "productivity_score": "Điểm năng suất trung bình"
                }
)
        fig_productivity.update_layout(bargap=0.6)

        st.plotly_chart(fig_productivity, use_container_width=True)

    with col4:
        fig_onscreen = px.bar(
            os_compare,
            x="Device_Type",
            y="onscreen_hours",
            color="Device_Type",
            title="So sánh thời gian on-screen TB",
            text_auto=".2f",
            labels={
                "Device_Type": "Hệ điều hành",
                "onscreen_hours": "Thời gian on-screen trung bình"
            }
)
        fig_onscreen.update_layout(bargap=0.6)

        st.plotly_chart(fig_onscreen, use_container_width=True)

