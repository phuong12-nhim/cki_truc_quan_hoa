import streamlit as st
import plotly.express as px

def render(data):

    st.header("🎯 Năng suất")

    fig = px.scatter(
        data,
        x="Daily_Phone_Hours",
        y="Work_Productivity_Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )