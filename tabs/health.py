import streamlit as st
import plotly.express as px

def render(data):

    st.header("❤️ Sức khỏe")

    fig = px.scatter(
        data,
        x="Daily_Phone_Hours",
        y="Sleep_Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )