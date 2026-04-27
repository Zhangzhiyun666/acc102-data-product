import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

st.title("📊 Superstore Profitability Insights")
st.markdown("### Interactive Analysis of Sales and Profit Performance")

@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding='latin1')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
    return df

df = load_data()

st.sidebar.header("Filters")
category = st.sidebar.multiselect(
    "Select Product Category:",
    options=df['Category'].unique(),
    default=list(df['Category'].unique())
)

filtered_df = df[df['Category'].isin(category)]

st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
with col3:
    st.metric("Avg Profit Margin", f"{filtered_df['Profit Margin'].mean():.2f}%")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(
        filtered_df.groupby('Region')['Profit'].sum().reset_index(),
        x='Region', y='Profit',
        title="Total Profit by Region",
        color_discrete_sequence=['#2E86C1']
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(
        filtered_df, 
        x='Sales', 
        y='Profit', 
        color='Category',
        title="Sales vs Profit by Category",
        opacity=0.7
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Data Overview")
st.write("First 5 rows of the current filtered dataset:")
st.dataframe(filtered_df.head(), use_container_width=True)

st.caption("Superstore Sales Dashboard | Final Version")
