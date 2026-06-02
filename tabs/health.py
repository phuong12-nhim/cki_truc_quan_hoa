import streamlit as st
import pandas as pd
import plotly.express as px

def style_chart(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="Inter, Arial, sans-serif", size=10, color="#808080"),
        showlegend=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E0E0E0",
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10, color="#A95D24", weight="bold")
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#B0B0B0",
        linewidth=1,
        tickfont=dict(size=9),
        title_font=dict(size=10, color="#A95D24", weight="bold")
    )
    return fig

def render(data):
    st.header("❤️ Sức khỏe & Hệ lụy Sinh học")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Giờ ngủ TB", f"{data['Sleep_Hours'].mean().round(1)} giờ")
    with col_m2:
        st.metric("Caffeine tiêu thụ TB", f"{data['Caffeine_Intake_Cups'].mean().round(1)} cốc")
    with col_m3:
        st.metric("Mức độ Stress TB", f"{data['Stress_Level'].mean().round(1)}")
        
    st.markdown("---")
    
    chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 1])
    
    with chart_col1:
        st.subheader("😴 Giờ ngủ vs Stress")
        sleep_stress = data.groupby("Sleep_Hours")["Stress_Level"].mean().reset_index()
        fig1 = px.line(
            sleep_stress,
            x="Sleep_Hours",
            y="Stress_Level",
            markers=True,
            labels={"Sleep_Hours": "Số giờ ngủ", "Stress_Level": "Stress TB"},
            color_discrete_sequence=["#FF75A0"]
        )
        fig1.update_traces(
            line=dict(width=2.5), 
            marker=dict(size=5, color="#FF75A0", line=dict(width=1, color="#FFFFFF"))
        )
        fig1.update_layout(hovermode="x unified", height=280)
        style_chart(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        st.subheader("☕ Caffeine theo Stress")
        data_sorted = data.sort_values(by="Stress_Level")
        
        colors = [
            "#EED9C4", "#E4C19E", "#D4A373", "#C58A57", "#B7733B",
            "#A95D24", "#944B19", "#7F3A10", "#6B2B0A", "#581C05"
        ]
        color_map = {i: colors[i-1] for i in range(1, 11)}
        
        fig2 = px.box(
            data_sorted,
            x="Stress_Level",
            y="Caffeine_Intake_Cups",
            color="Stress_Level",
            color_discrete_map=color_map,
            labels={"Stress_Level": "Mức Stress", "Caffeine_Intake_Cups": "Số cốc"}
        )
        fig2.update_traces(
            boxpoints="outliers", 
            jitter=0.2, 
            opacity=0.8
        )
        fig2.update_layout(height=280, boxmode="overlay")
        fig2.update_xaxes(type="category")
        style_chart(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    with chart_col3:
        st.subheader("📱 On-screen: Thường vs Nghỉ")
        
        comparison_df = pd.DataFrame({
            "Thời điểm": ["Ngày thường", "Cuối tuần"],
            "Số giờ sử dụng": [
                data["Daily_Phone_Hours"].mean(),
                data["Weekend_Screen_Time_Hours"].mean()
            ]
        })
        
        fig3 = px.bar(
            comparison_df,
            x="Thời điểm",
            y="Số giờ sử dụng",
            color="Thời điểm",
            text_auto=".1f",
            labels={"Thời điểm": "", "Số giờ sử dụng": "Giờ TB"},
            color_discrete_sequence=["#A2D2FF", "#BDB2FF"]
        )
        fig3.update_traces(
            textposition="outside",
            textfont=dict(size=10, weight="bold")
        )
        fig3.update_layout(
            bargap=0.5,
            height=280,
            showlegend=False
        )
        style_chart(fig3)
        st.plotly_chart(fig3, use_container_width=True)