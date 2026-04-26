import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("📊 Superstore Profitability Insights")

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding='latin1')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
    return df

df = load_data()

# 侧边栏筛选
category = st.sidebar.multiselect("选择产品类别:", df['Category'].unique(), default=df['Category'].unique())
filtered_df = df[df['Category'].isin(category)]

# 主界面展示
col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(filtered_df.groupby('Region')['Profit'].sum().reset_index(), x='Region', y='Profit', title="各区域总利润")
    st.plotly_chart(fig1)
with col2:
    fig2 = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', title="销售额与利润相关性")
    st.plotly_chart(fig2)

st.write("数据概览:", filtered_df.head())
