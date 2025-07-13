import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Airbnb Data Analysis", layout="wide")
st.title("🏡 Airbnb Data Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("compressed_data.csv")
    df['last review'] = pd.to_datetime(df['last review'], errors='coerce')
    df.fillna({'reviews per month': 0, 'last review': df['last review'].mean()}, inplace=True)
    df.dropna(subset=['NAME', 'host name'], inplace=True)
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
    df['service fee'] = df['service fee'].replace(r'[\$,]', '', regex=True).astype(float)
    df.drop_duplicates(inplace=True)
    df = df.drop(columns=['license', 'house_rules'], errors='ignore')
    return df

df = load_data()

# Sidebar navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to", [
    "📊 Distribution of Prices",
    "🛏️ Room Type Analysis",
    "📍 Neighbourhood Analysis",
    "💰 Price vs. Room Type",
    "🕒 Review Over Time",
    "📁 Raw Data"
])

# Section 1: Price Distribution
if section == "📊 Distribution of Prices":
    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['price'], bins=50, ax=ax, kde=True, color="skyblue")
    ax.set_xlabel("Price")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Section 2: Room Type Analysis
elif section == "🛏️ Room Type Analysis":
    st.subheader("Room Type Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='room type', color='hotpink', ax=ax)
    ax.set_title('Room Type Distribution')
    ax.set_xlabel('Room Type')
    ax.set_ylabel('Count')
    st.pyplot(fig)

# Section 3: Neighbourhood Analysis
elif section == "📍 Neighbourhood Analysis":
    st.subheader("Top 10 Neighbourhoods by Listings")
    top_neigh = df['neighbourhood group'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(y=top_neigh.index, x=top_neigh.values, color='lightgreen', ax=ax)
    ax.set_title('Neighbourhood Distribution')
    ax.set_xlabel('Count')
    ax.set_ylabel('Neighbourhood Group')
    st.pyplot(fig)

# Section 4: Price vs. Room Type
elif section == "💰 Price vs. Room Type":
    st.subheader("Price vs. Room Type")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(data=df, x='room type', y='price', palette='Set1', ax=ax)
    ax.set_title('Price vs. Room Type')
    ax.set_xlabel('Room Type')
    ax.set_ylabel('Price ($)')
    st.pyplot(fig)

# Section 5: Review Over Time
elif section == "🕒 Review Over Time":
    st.subheader("Reviews Over Time")
    df_time = df.copy()
    df_time = df_time.dropna(subset=['last review'])
    df_time['year_month'] = df_time['last review'].dt.to_period('M').astype(str)

    if 'reviews per month' in df_time.columns:
        review_trend = df_time.groupby('year_month')['reviews per month'].mean().reset_index()
        ylabel = "Average Reviews per Month"
    else:
        review_trend = df_time.groupby('year_month')['last review'].count().reset_index()
        review_trend.rename(columns={'last review': 'review count'}, inplace=True)
        ylabel = "Review Count"

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(review_trend['year_month'], review_trend[review_trend.columns[1]], color='blue')
    ax.set_title('Number of Reviews Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Section 6: Raw Data
elif section == "📁 Raw Data":
    st.subheader("📁 Raw Dataset Preview")

    st.write("🧾 Column Names:")
    st.code(df.columns.tolist())

    st.write("🔍 Top 10 Rows:")
    st.dataframe(df.head(10))

    st.write("🔍 Full Dataset (paginated):")
    st.dataframe(df, use_container_width=True)
