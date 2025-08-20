import streamlit as st
import requests

# --- Custom CSS for Pink Vibe ---
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #ffe6f2, #ffd6eb, #ffccf9);
    }

    /* Title */
    h1 {
        color: #d63384;
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
    }

    /* Input fields & dropdowns */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #ff4da6;
        border-radius: 10px;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #ff66b2;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        padding: 8px 20px;
    }
    div.stButton > button:hover {
        background-color: #e60073;
        color: #fff;
    }

    /* Success/info/warning boxes */
    .stAlert {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Live Currency Converter with Flags")

# Frankfurter API endpoints
API_URL = "https://api.frankfurter.app/latest"
CURRENCIES_URL = "https://api.frankfurter.app/currencies"

# Currency → Flag mapping
currency_flags = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "NGN": "🇳🇬",
    "JPY": "🇯🇵",
    "CAD": "🇨🇦",
    "AUD": "🇦🇺",
    "CHF": "🇨🇭",
    "CNY": "🇨🇳",
    "INR": "🇮🇳"
}

# Fetch available currencies dynamically
try:
    response = requests.get(CURRENCIES_URL)
    currencies_data = response.json()
    currencies = sorted(list(currencies_data.keys()))  # list of ISO codes
except Exception:
    st.error("⚠️ Could not load currencies. Please refresh.")
    currencies = ["USD", "EUR"]  # fallback

# Function to format dropdown with flags
def format_currency(code):
    flag = currency_flags.get(code, "🏳️")  # default flag if not found
    return f"{flag} {code}"

# Session state for swap
if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"
if "to_currency" not in st.session_state:
    st.session_state.to_currency = "EUR"

# User input
amount = st.number_input("Enter amount:", min_value=0.0, format="%.2f")

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    from_currency = st.selectbox(
        "From:", 
        currencies, 
        index=currencies.index(st.session_state.from_currency) if st.session_state.from_currency in currencies else 0,
        format_func=format_currency,
        key="from_select"
    )

with col2:
    if st.button("🔄 Swap"):
        st.session_state.from_currency, st.session_state.to_currency = (
            st.session_state.to_currency, 
            st.session_state.from_currency
        )
        st.rerun()

with col3:
    to_currency = st.selectbox(
        "To:", 
        currencies, 
        index=currencies.index(st.session_state.to_currency) if st.session_state.to_currency in currencies else 1,
        format_func=format_currency,
        key="to_select"
    )

# Auto conversion (instant update)
if amount > 0 and from_currency != to_currency:
    try:
        response = requests.get(API_URL, params={
            "amount": amount,
            "from": from_currency,
            "to": to_currency
        })
        data = response.json()

        if "rates" in data and to_currency in data["rates"]:
            converted_amount = data["rates"][to_currency]
            rate = converted_amount / amount
            st.success(f"{amount:.2f} {format_currency(from_currency)} = {converted_amount:.2f} {format_currency(to_currency)}")
            st.info(f"💡 1 {format_currency(from_currency)} = {rate:.4f} {format_currency(to_currency)}")
        else:
            st.error("⚠️ Conversion failed. Please try again later.")
    except Exception as e:
        st.error(f"Error: {e}")
elif amount == 0:
    st.warning("Please enter an amount greater than 0.")
