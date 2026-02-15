import streamlit as st
from datetime import datetime
import pytz
import requests

# --- 1. PRO UI CONFIG (MEGA WIDE + BIG TEXT) ---
st.set_page_config(page_title="OmusubiTime Pro 🌍", page_icon="🍙", layout="wide")

st.markdown("""
    <style>
    /* 1. FORCE THE WHOLE APP WIDE */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 95% !important; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }

    /* 2. MEGA GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 60px 20px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }
    .home-card { border: 3px solid #10b981; background: rgba(16, 185, 129, 0.12) !important; }
    .day-glow { border-top: 15px solid #fbbf24; }
    .night-shade { border-top: 15px solid #6366f1; }

    /* 3. TYPOGRAPHY (MEGA SIZE) */
    .time-val { font-size: 110px; font-weight: 900; color: #ffffff; line-height: 1; }
    .fx-huge { font-size: 80px; font-weight: 900; color: #10b981; line-height: 1; }
    .label-pro { font-size: 22px; text-transform: uppercase; color: #94a3b8; letter-spacing: 5px; font-weight: 700; margin-bottom: 15px; }
    .diff-pill { background: #ff7675; color: white; padding: 10px 25px; border-radius: 30px; font-size: 22px; font-weight: 800; }

    /* 4. FIX SMALL INPUTS/LABELS (SELECTBOX & NUMBER) */
    div[data-testid="stWidgetLabel"] p { font-size: 24px !important; font-weight: bold !important; color: #ffffff !important; }
    div[data-baseweb="select"] { font-size: 22px !important; }
    input { font-size: 24px !important; font-weight: bold !important; }
    
    /* 5. SIDEBAR SCALING */
    .css-1d391kg { width: 350px; } 
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=3600)
def fetch_rates():
    try: return requests.get("https://open.er-api.com/v6/latest/USD").json()['rates']
    except: return {"JPY": 151.0, "EUR": 0.92, "USD": 1.0}

ALL_TZ, RATES = pytz.common_timezones, fetch_rates()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 40px;'>🍙 OmusubiTime</h1>", unsafe_allow_html=True)
    h_city = st.selectbox("🏠 Home City", ALL_TZ, index=ALL_TZ.index("US/Pacific"))
    h_curr = st.selectbox("💵 Home Currency", list(RATES.keys()), index=list(RATES.keys()).index("USD"))
    st.divider()
    st.info("Mission Control Active")

# --- 4. GLOBAL HUB SELECTION ---
st.markdown("<h1 style='text-align: center; font-size: 60px;'>🌐 Global Hub</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: t_city = st.selectbox("🎯 Target City", ALL_TZ, index=ALL_TZ.index("Asia/Tokyo"))
with c2: t_curr = st.selectbox("💱 Target Currency", list(RATES.keys()), index=list(RATES.keys()).index("JPY"))

# --- 5. LOGIC ---
tz_h, tz_t = pytz.timezone(h_city), pytz.timezone(t_city)
now_h, now_t = datetime.now(tz_h), datetime.now(tz_t)
diff = (now_t.utcoffset().total_seconds() - now_h.utcoffset().total_seconds()) / 3600
is_day = 6 <= now_t.hour <= 18
style = "day-glow" if is_day else "night-shade"
fx = RATES[t_curr] / RATES[h_curr]

# --- 6. THE DASHBOARD ---
st.write("") 
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="glass-card home-card"><div class="label-pro">🏠 {h_city.split("/")[-1]}</div><p class="time-val">{now_h.strftime("%H:%M")}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="glass-card {style}"><div class="label-pro">🎯 {t_city.split("/")[-1]}</div><p class="time-val">{now_t.strftime("%H:%M")}</p><span class="diff-pill">{diff:+.0f}H OFFSET</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="glass-card"><div class="label-pro">💱 1 {h_curr} to {t_curr}</div><p class="fx-huge">{fx:,.2f}</p></div>', unsafe_allow_html=True)

# --- 7. MEGA CONVERTER ---
st.divider()
amt = st.number_input(f"Amount in {h_curr}", min_value=0.0, value=100.0)
st.markdown(f"<h1 style='color: #10b981; font-size: 55px;'>Total: {amt * fx:,.2f} {t_curr}</h1>", unsafe_allow_html=True)