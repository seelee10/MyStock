import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt

# --- App Title ---
st.title("📊 Stock Price Viewer")

# --- Sidebar Inputs ---
st.sidebar.header("Settings")

# Stock ticker input
ticker = st.sidebar.text_input(
    "Enter Stock Ticker Symbol (e.g., NVDA, AAPL, TSLA):",
    value="NVDA"
).upper()

# Date range selection
start_date = st.sidebar.date_input("Start Date", dt.date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", dt.date.today())

# --- Fetch and Plot ---
if st.sidebar.button("Load Data"):
    if start_date >= end_date:
        st.error("⚠️ End date must be after start date.")
    else:
        with st.spinner("Downloading stock data..."):
            df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            st.warning("No data found for this ticker or date range.")
        else:
            st.success(f"Showing {ticker} data from {start_date} to {end_date}")

            # --- Plot the data ---
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df["Close"], label="Close Price", color="blue", linewidth=2)
            ax.set_title(f"{ticker} Stock Closing Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            # --- Download CSV ---
            csv = df.to_csv().encode("utf-8")
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name=f"{ticker}_stock_data.csv",
                mime="text/csv"
            )
else:
    st.info("👈 Enter a ticker and click **Load Data** to begin.")
