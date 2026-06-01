import streamlit as st
import plotly.express as px

def render(data):

    st.header("📊 Tổng quan")

    fig = px.histogram(
        data,
        x="Age"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )