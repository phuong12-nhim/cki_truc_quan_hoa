import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/Smartphone_Usage_Productivity_Dataset_50000.csv"
    )

    return preprocess(df)

def preprocess(df):

    df.columns = (
        df.columns
        .str.strip()
    )

    numeric_cols = [
        "Age",
        "Daily_Phone_Hours",
        "Social_Media_Hours",
        "Work_Productivity_Score",
        "Sleep_Hours",
        "Stress_Level",
        "App_Usage_Count",
        "Caffeine_Intake_Cups",
        "Weekend_Screen_Time_Hours"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna()

    return df