import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import requests

# --- 1. PRO UI CONFIG ---
st.set_page_config(page_title="Omusubitime 🌍", page_icon="🍙", layout="wide")

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
    .home-card { border: 2px solid #10b981; background: rgba(16, 185, 129, 0.1) !important; }
    .day-mode { border-top: 6px solid #fbbf24; }
    .night-mode { border-top: 6px solid #6366f1; }
    .time-val { font-size: 52px; font-weight: 900; color: #ffffff; margin: 0; }
    .diff-pill { background: #ff7675; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: 800; }
    .label-pro { font-size: 11px; text-transform: uppercase; color: #94a3b8; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL ENGINES ---
@st.cache_data(ttl=3600)
def fetch_fx():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()['rates']
    except: return {"JPY": 151.0, "EUR": 0.92}

COMMON_TZ = pytz.common_timezones

# --- 3. DYNAMIC LOCATION SETTINGS ---
with st.sidebar:
    st.header("⚙️ Personal Settings")
    # This becomes the "Standard Time" for the user
    home_city = st.selectbox("🏠 Set Your Home City (Standard)", 
                             options=COMMON_TZ, 
                             index=COMMON_TZ.index("US/Pacific"))
    
    base_currency = st.selectbox("💵 Your Home Currency", 
                                 options=["USD", "JPY", "EUR", "GBP", "CAD", "AUD"], 
                                 index=0)
    st.divider()
    st.info("The app now calculates everything relative to your Home City above.")

# --- 4. TARGET SELECTION ---
st.title("🍙 Omusubitime Pro")
c_target, c_cur = st.columns(2)

with c_target:
    target_city = st.selectbox("🎯 View Target City / Region", 
                               options=COMMON_TZ, 
                               index=COMMON_TZ.index("Asia/Tokyo"))
with c_cur:
    rates = fetch_fx()
    target_currency = st.selectbox("💱 View Target Currency", 
                                    options=list(rates.keys()), 
                                    index=list(rates.keys()).index("JPY"))

# --- 5. THE PRO LOGIC ---
tz_home = pytz.timezone(home_city)
tz_target = pytz.timezone(target_city)

now_home = datetime.now(tz_home)
now_target = datetime.now(tz_target)

# Instant Offset Calculation
diff_hours = (now_target.utcoffset().total_seconds() - now_home.utcoffset().total_seconds()) / 3600
is_day = 6 <= now_target.hour <= 18
target_theme = "day-mode" if is_day else "night-mode"

# Currency Logic
rate_home = rates.get(base_currency, 1.0)
rate_target = rates.get(target_currency, 1.0)
# Convert 1 unit of Home Currency to Target Currency
cross_rate = rate_target / rate_home

# --- 6. THE GLOBAL DASHBOARD ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="glass-card home-card">
            <div class="label-pro">🏠 Home: {home_city.split('/')[-1]}</div>
            <p class="time-val">{now_home.strftime("%H:%M")}</p>
            <div class="label-pro">{now_home.strftime("%b %d")}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="glass-card {target_theme}">
            <div class="label-pro">🎯 Target: {target_city.split('/')[-1]}</div>
            <p class="time-val">{now_target.strftime("%H:%M")}</p>
            <span class="diff-pill">{diff_hours:+.0f}H from Home</span>
            <div class="label-pro" style="margin-top:10px;">{now_target.strftime("%b %d")}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="glass-card">
            <div class="label-pro">💱 1 {base_currency} equals</div>
            <p class="time-val" style="color:#10b981; font-size:42px;">{cross_rate:,.2f}</p>
            <div class="label-pro">{target_currency}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. PRO CONVERTER ---
st.divider()
st.subheader(f"🧮 Fast Converter ({base_currency} to {target_currency})")
amt = st.number_input(f"Amount in {base_currency}", min_value=0.0, value=100.0)
st.success(f"**Total: {amt * cross_rate:,.2f} {target_currency}**")