import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("💰 Personal Finance Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Ensure required columns
    if not {"Date", "Description", "Amount"}.issubset(df.columns):
        st.error("CSV must contain columns: Date, Description, Amount")
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")

        # --- Load Categories ---
        with open("categories.json") as f:
            categories = json.load(f)

        def categorize(description):
            for cat, keywords in categories.items():
                if any(kw.lower() in str(description).lower() for kw in keywords):
                    return cat
            return "Other"

        df["Category"] = df["Description"].apply(categorize)

        # --- Aggregations ---
        spending_by_cat = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        monthly_spending = df.groupby("Month")["Amount"].sum()

        # --- Display Data ---
        st.subheader("📋 Transactions Preview")
        st.dataframe(df.head(20))

        # --- Category Breakdown ---
        st.subheader("📊 Spending by Category")
        fig1, ax1 = plt.subplots(figsize=(8,5))
        spending_by_cat.plot(kind="bar", color="skyblue", ax=ax1)
        ax1.set_ylabel("Amount ($)")
        ax1.set_title("Spending by Category")
        st.pyplot(fig1)

        # --- Monthly Trend ---
        st.subheader("📈 Monthly Spending Trend")
        fig2, ax2 = plt.subplots(figsize=(8,5))
        monthly_spending.plot(kind="line", marker="o", color="green", ax=ax2)
        ax2.set_ylabel("Amount ($)")
        ax2.set_title("Monthly Spending Trend")
        st.pyplot(fig2)

        # --- Pie Chart ---
        st.subheader("🥧 Spending Distribution")
        fig3, ax3 = plt.subplots(figsize=(6,6))
        spending_by_cat.plot(kind="pie", autopct="%1.1f%%", startangle=140, ylabel="", ax=ax3)
        ax3.set_title("Spending by Category")
        st.pyplot(fig3)

else:
    st.info("👆 Upload a CSV file to get started.")
