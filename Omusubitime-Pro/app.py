import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import requests

# --- 1. PRO UI CONFIG ---
st.set_page_config(page_title="Omusubitime Pro 🌍", page_icon="🍙", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    .home-card { border: 2px solid #10b981; background: rgba(16, 185, 129, 0.08) !important; }
    .day-glow { border-top: 6px solid #fbbf24; }
    .night-shade { border-top: 6px solid #6366f1; }
    .time-val { font-size: 52px; font-weight: 900; color: #ffffff; margin: 0; line-height: 1.1; }
    .diff-pill { background: #ff7675; color: white; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 800; }
    .label-pro { font-size: 11px; text-transform: uppercase; color: #94a3b8; letter-spacing: 2px; margin-bottom: 10px; }
    .fx-huge { font-size: 42px; font-weight: bold; color: #10b981; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL ENGINES ---
@st.cache_data(ttl=3600)
def fetch_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()['rates']
    except: return {"JPY": 151.0, "EUR": 0.92, "USD": 1.0}

ALL_TZ = pytz.common_timezones
RATES = fetch_rates()

# --- 3. SIDEBAR (YOUR HOME BASE) ---
with st.sidebar:
    st.title("🍙 Omusubitime")
    home_city = st.selectbox("🏠 Your Home City", ALL_TZ, index=ALL_TZ.index("US/Pacific"))
    home_curr = st.selectbox("💵 Your Currency", list(RATES.keys()), index=list(RATES.keys()).index("USD"))
    st.divider()
    st.info("Everything calculates relative to your selections here.")

# --- 4. TARGET SELECTION ---
st.title("🌐 Global Hub")
c1, c2 = st.columns(2)
with c1: target_city = st.selectbox("🎯 Target City", ALL_TZ, index=ALL_TZ.index("Asia/Tokyo"))
with c2: target_currency = st.selectbox("💱 Target Currency", list(RATES.keys()), index=list(RATES.keys()).index("JPY"))

# --- 5. LOGIC & MATH ---
tz_h, tz_t = pytz.timezone(home_city), pytz.timezone(target_city)
now_h, now_t = datetime.now(tz_h), datetime.now(tz_t)
diff = (now_t.utcoffset().total_seconds() - now_h.utcoffset().total_seconds()) / 3600
is_day = 6 <= now_t.hour <= 18
style = "day-glow" if is_day else "night-shade"
cross_rate = RATES[target_currency] / RATES[home_curr]

# --- 6. THE PRO DASHBOARD ---
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="glass-card home-card"><div class="label-pro">🏠 Home ({home_city.split("/")[-1]})</div><p class="time-val">{now_h.strftime("%H:%M")}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="glass-card {style}"><div class="label-pro">🎯 Target ({target_city.split("/")[-1]})</div><p class="time-val">{now_t.strftime("%H:%M")}</p><span class="diff-pill">{diff:+.0f}H from Home</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="glass-card"><div class="label-pro">💱 1 {home_curr} to {target_currency}</div><p class="fx-huge">{cross_rate:,.2f}</p><div class="label-pro">Live Rate</div></div>', unsafe_allow_html=True)

# --- 7. CONVERTER ---
st.divider()
amt = st.number_input(f"Amount in {home_curr}", min_value=0.0, value=100.0)
st.success(f"**Total: {amt * cross_rate:,.2f} {target_currency}**")