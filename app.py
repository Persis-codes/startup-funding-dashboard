import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Startup Funding Dashboard",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------

st.title("🚀 Startup Funding Analysis Dashboard")
st.markdown("Interactive analysis of startup funding trends, industries, investors, and cities.")

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("cleaned_startup_funding.csv")

# Convert Date Column
df['Date'] = pd.to_datetime(df['Date'])

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.header("🔍 Filter Data")

selected_year = st.sidebar.multiselect(
    "Select Year",
    sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

selected_city = st.sidebar.multiselect(
    "Select City",
    sorted(df['City'].dropna().unique()),
    default=sorted(df['City'].dropna().unique())
)

selected_industry = st.sidebar.multiselect(
    "Select Industry",
    sorted(df['Industry'].dropna().unique()),
    default=sorted(df['Industry'].dropna().unique())
)

selected_investment = st.sidebar.multiselect(
    "Select Investment Type",
    sorted(df['Investment Type'].dropna().unique()),
    default=sorted(df['Investment Type'].dropna().unique())
)

# -------------------------------
# FILTER DATAFRAME
# -------------------------------

filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['City'].isin(selected_city)) &
    (df['Industry'].isin(selected_industry)) &
    (df['Investment Type'].isin(selected_investment))
]

# -------------------------------
# KPI METRICS
# -------------------------------

total_funding = filtered_df['Amount (In USD)'].sum()
total_startups = filtered_df['Startup Name'].nunique()
total_investors = filtered_df['Investors’ Name'].nunique()
average_funding = filtered_df['Amount (In USD)'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Funding",
    f"${total_funding:,.0f}"
)

col2.metric(
    "🚀 Total Startups",
    total_startups
)

col3.metric(
    "👨‍💼 Total Investors",
    total_investors
)

col4.metric(
    "📈 Average Funding",
    f"${average_funding:,.0f}"
)

st.markdown("---")

# -------------------------------
# YEAR-WISE FUNDING TREND
# -------------------------------

st.subheader("📊 Year-wise Funding Trend")

year_funding = filtered_df.groupby(
    'Year'
)['Amount (In USD)'].sum()

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    year_funding.index,
    year_funding.values,
    marker='o',
    linewidth=3
)

ax.set_xlabel("Year")
ax.set_ylabel("Funding Amount")
ax.set_title("Funding Trend Over Years")

st.pyplot(fig)

# -------------------------------
# TOP INDUSTRIES
# -------------------------------

st.subheader("🏭 Top Industries by Funding")

industry_funding = filtered_df.groupby(
    'Industry'
)['Amount (In USD)'].sum().sort_values(
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(12, 5))

industry_funding.plot(
    kind='bar',
    ax=ax
)

ax.set_xlabel("Industry")
ax.set_ylabel("Funding Amount")

st.pyplot(fig)

# -------------------------------
# TOP CITIES
# -------------------------------

st.subheader("🌍 Top Cities by Funding")

city_funding = filtered_df.groupby(
    'City'
)['Amount (In USD)'].sum().sort_values(
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10, 5))

city_funding.plot(
    kind='bar',
    ax=ax
)

ax.set_xlabel("City")
ax.set_ylabel("Funding Amount")

st.pyplot(fig)

# -------------------------------
# INVESTMENT TYPE DISTRIBUTION
# -------------------------------

st.subheader("💼 Investment Type Distribution")

investment_counts = filtered_df[
    'Investment Type'
].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 8))

ax.pie(
    investment_counts.values,
    labels=investment_counts.index,
    autopct='%1.1f%%'
)

st.pyplot(fig)

# -------------------------------
# TOP INVESTORS
# -------------------------------

st.subheader("🏦 Most Active Investors")

top_investors = filtered_df[
    'Investors’ Name'
].value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 5))

top_investors.plot(
    kind='bar',
    ax=ax
)

ax.set_xlabel("Investor")
ax.set_ylabel("Number of Investments")

st.pyplot(fig)

# -------------------------------
# TOP STARTUPS
# -------------------------------

st.subheader("🚀 Top Funded Startups")

top_startups = filtered_df.groupby(
    'Startup Name'
)['Amount (In USD)'].sum().sort_values(
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(12, 5))

top_startups.plot(
    kind='barh',
    ax=ax
)

ax.set_xlabel("Funding Amount")
ax.set_ylabel("Startup")

st.pyplot(fig)

# -------------------------------
# FUNDING SEGMENTATION
# -------------------------------

st.subheader("📌 Startup Segmentation")

bins = [0, 1000000, 10000000, float('inf')]

labels = [
    'Small Startup',
    'Medium Startup',
    'Large Startup'
]

filtered_df['Funding Segment'] = pd.cut(
    filtered_df['Amount (In USD)'],
    bins=bins,
    labels=labels
)

segment_counts = filtered_df[
    'Funding Segment'
].value_counts()

fig, ax = plt.subplots(figsize=(8, 5))

sns.countplot(
    data=filtered_df,
    x='Funding Segment',
    ax=ax
)

st.pyplot(fig)

# -------------------------------
# CORRELATION HEATMAP
# -------------------------------

st.subheader("🔥 Correlation Heatmap")

correlation = filtered_df.corr(
    numeric_only=True
)

fig, ax = plt.subplots(figsize=(6, 4))

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm',
    ax=ax
)

st.pyplot(fig)

# -------------------------------
# DATA PREVIEW
# -------------------------------

st.subheader("🗂 Dataset Preview")

st.dataframe(filtered_df.head(20))

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_startup_data.csv',
    mime='text/csv'
)

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.markdown(
    "Developed using Streamlit, Pandas, Matplotlib, Seaborn, and Scikit-learn."
)