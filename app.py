import streamlit as st
import pandas as pd
import numpy as np
import os

DATA_FILE = "portfolio_data.csv"

st.set_page_config(page_title="Portfolio Management App", layout="wide")

st.title("📊 Portfolio Management Application")
st.write("Upload your portfolio CSV to analyze and save your portfolio data locally.")

# Example CSV format instruction
st.markdown("""
**CSV Format Example:**
| Ticker | Shares | Purchase_Price | Current_Price |
|---------|---------|----------------|----------------|
| AAPL | 10 | 150 | 170 |
| MSFT | 5 | 250 | 300 |
""")

# Load existing data if available
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.success("✅ Loaded saved portfolio data from local file.")
else:
    df = pd.DataFrame()

# File uploader
uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.to_csv(DATA_FILE, index=False)
    st.success("📁 Portfolio data saved locally as 'portfolio_data.csv'.")

if not df.empty:
    required_cols = {"Ticker", "Shares", "Purchase_Price", "Current_Price"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain these columns: {required_cols}")
    else:
        # Compute portfolio metrics
        df["Investment_Value"] = df["Shares"] * df["Purchase_Price"]
        df["Current_Value"] = df["Shares"] * df["Current_Price"]
        df["Profit/Loss"] = df["Current_Value"] - df["Investment_Value"]
        df["Return_%"] = np.where(df["Investment_Value"] != 0, 
                                  (df["Profit/Loss"] / df["Investment_Value"]) * 100, 0)
        
        total_investment = df["Investment_Value"].sum()
        total_value = df["Current_Value"].sum()
        total_profit = df["Profit/Loss"].sum()
        total_return = (total_profit / total_investment) * 100 if total_investment != 0 else 0

        # Display portfolio metrics
        st.subheader("📈 Portfolio Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Investment", f"${total_investment:,.2f}")
        col2.metric("Current Value", f"${total_value:,.2f}")
        col3.metric("Profit/Loss", f"${total_profit:,.2f}")
        col4.metric("Total Return", f"{total_return:.2f}%")

        # Display portfolio table
        st.subheader("📃 Detailed Portfolio Table")
        st.dataframe(df.style.format({
            "Purchase_Price": "${:,.2f}",
            "Current_Price": "${:,.2f}",
            "Investment_Value": "${:,.2f}",
            "Current_Value": "${:,.2f}",
            "Profit/Loss": "${:,.2f}",
            "Return_%": "{:.2f}%"
        }))

        # Charts
        st.subheader("📊 Portfolio Allocation")
        allocation = df.groupby("Ticker")["Current_Value"].sum()
        st.bar_chart(allocation)

        st.subheader("📉 Distribution of Returns")
        st.bar_chart(df.set_index("Ticker")["Return_%"])

        # Option to clear portfolio
        if st.button("🗑️ Clear Saved Portfolio"):
            os.remove(DATA_FILE)
            st.warning("Portfolio data cleared. Please reload the page.")
            st.stop()

else:
    st.info("Please upload your portfolio CSV file to begin.")
