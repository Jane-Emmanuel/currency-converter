import streamlit as st
import requests

st.title("💱 Live Currency Converter")

# Free API endpoint
API_URL = "https://api.exchangerate.host/convert"

# User input
amount = st.number_input("Enter amount:", min_value=0.0, format="%.2f")

currencies = ["USD", "EUR", "GBP", "NGN", "JPY", "CAD"]

from_currency = st.selectbox("From:", currencies)
to_currency = st.selectbox("To:", currencies)

if st.button("Convert"):
    if amount > 0:
        try:
            response = requests.get(API_URL, params={
                "from": from_currency,
                "to": to_currency,
                "amount": amount
            })
            data = response.json()
            converted_amount = data["result"]

            if converted_amount:
                st.success(f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
            else:
                st.error("Conversion failed. Try again later.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter an amount greater than 0.")
