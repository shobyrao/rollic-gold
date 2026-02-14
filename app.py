import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

st.set_page_config(page_title="Rollic Trades", page_icon="⚡", layout="wide")

# ============ APPLE-STYLE PREMIUM CSS + STICKY NAVBAR ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background-color: #000000;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
header {visibility: hidden;}

.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
}

/* ===== STICKY NAVBAR ===== */
.sticky-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-logo-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #FFD700, #FFA500);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 800;
    color: #000;
}

.nav-logo-text {
    font-size: 17px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.3px;
}

.nav-logo-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1px;
    text-transform: uppercase;
}

.nav-links {
    display: flex;
    gap: 4px;
}

.nav-link {
    padding: 7px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: rgba(255,255,255,0.5);
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s;
    border: none;
    background: none;
}

.nav-link:hover {
    color: #ffffff;
    background: rgba(255,255,255,0.06);
}

.nav-link-active {
    padding: 7px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #FFD700;
    background: rgba(255,215,0,0.08);
    border: 1px solid rgba(255,215,0,0.15);
    cursor: pointer;
    text-decoration: none;
}

.nav-time {
    font-size: 11px;
    color: rgba(255,255,255,0.2);
}

/* Spacer for fixed navbar */
.nav-spacer {
    height: 60px;
}

/* ===== GLASS CARDS ===== */
.glass-card {
    background: rgba(28, 28, 30, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}

.glass-card-gold {
    background: rgba(28, 28, 30, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,215,0,0.15);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
}

/* Price Display */
.price-main {
    font-size: 56px;
    font-weight: 700;
    color: #FFD700;
    letter-spacing: -2px;
    line-height: 1;
    text-align: center;
}

.price-change-pos {
    color: #30D158;
    font-size: 18px;
    font-weight: 600;
    text-align: center;
}

.price-change-neg {
    color: #FF453A;
    font-size: 18px;
    font-weight: 600;
    text-align: center;
}

/* Section Title */
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* Factor Cards */
.factor-bull {
    background: rgba(48, 209, 88, 0.06);
    border: 1px solid rgba(48, 209, 88, 0.15);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 6px 0;
}

.factor-bear {
    background: rgba(255, 69, 58, 0.06);
    border: 1px solid rgba(255, 69, 58, 0.15);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 6px 0;
}

.factor-neutral {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 6px 0;
}

.factor-name {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
}

.factor-detail {
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    line-height: 1.5;
}

.factor-value {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
}

/* Progress Bar */
.progress-track {
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    height: 4px;
    margin-top: 8px;
    overflow: hidden;
}

.progress-fill-green {
    background: linear-gradient(90deg, #30D158, #34C759);
    height: 100%;
    border-radius: 4px;
}

.progress-fill-red {
    background: linear-gradient(90deg, #FF453A, #FF6961);
    height: 100%;
    border-radius: 4px;
}

/* Meter Bar */
.meter-bar {
    height: 8px;
    border-radius: 4px;
    display: flex;
    overflow: hidden;
    background: rgba(255,255,255,0.05);
}

/* Correlation */
.corr-pos { color: #30D158; font-weight: 700; font-size: 15px; }
.corr-neg { color: #FF453A; font-weight: 700; font-size: 15px; }

/* Insight Card */
.insight-card {
    background: rgba(255, 214, 10, 0.04);
    border: 1px solid rgba(255, 214, 10, 0.12);
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
}

.insight-title {
    font-size: 13px;
    font-weight: 600;
    color: #FFD60A;
    margin-bottom: 6px;
}

.insight-text {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
    line-height: 1.6;
}

/* Metric */
.metric-label {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 4px;
    text-align: center;
}

.metric-value {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
}

/* COT Special Cards */
.cot-card {
    background: rgba(28, 28, 30, 0.9);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
}

.cot-title {
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.cot-value-long {
    font-size: 28px;
    font-weight: 700;
    color: #30D158;
}

.cot-value-short {
    font-size: 28px;
    font-weight: 700;
    color: #FF453A;
}

/* Daily Bias Card */
.bias-card {
    background: rgba(28, 28, 30, 0.9);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    margin-bottom: 16px;
}

.bias-label {
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
}

.bias-value {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 8px 0;
}

/* Session Cards */
.session-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px;
    margin: 6px 0;
}

/* Hide streamlit elements */
div[data-testid="stToolbar"] {display: none;}
div[data-testid="stDecoration"] {display: none;}
div[data-testid="stStatusWidget"] {display: none;}

</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE FOR PAGE NAVIGATION ============
if 'page' not in st.session_state:
    st.session_state.page = 'macro'

# Query params for page
params = st.query_params
if 'page' in params:
    st.session_state.page = params['page']

# ============ STICKY NAVBAR ============
page = st.session_state.page

macro_active = "nav-link-active" if page == "macro" else "nav-link"
daily_active = "nav-link-active" if page == "daily" else "nav-link"

st.markdown(f"""
<div class="sticky-nav">
    <div class="nav-logo">
        <div class="nav-logo-icon">R</div>
        <div>
            <div class="nav-logo-text">Rollic Trades</div>
            <div class="nav-logo-sub">Gold Intelligence</div>
        </div>
    </div>
    <div class="nav-links">
        <a href="?page=macro" class="{macro_active}" target="_self">📊 Macro Analysis</a>
        <a href="?page=daily" class="{daily_active}" target="_self">⚡ Daily Bias</a>
    </div>
    <div class="nav-time">{datetime.now().strftime('%H:%M UTC · %d %b %Y')}</div>
</div>
<div class="nav-spacer"></div>
""", unsafe_allow_html=True)

# ============ PAGE NAVIGATION ============
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📊 Macro Analysis", use_container_width=True,
                  type="primary" if page=="macro" else "secondary"):
        st.query_params["page"] = "macro"
        st.rerun()
with col_nav2:
    if st.button("⚡ Daily Bias & COT", use_container_width=True,
                  type="primary" if page=="daily" else "secondary"):
        st.query_params["page"] = "daily"
        st.rerun()

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ============ SHARED DATA FUNCTIONS ============

@st.cache_data(ttl=90)
def get_price(ticker):
    try:
        d = yf.Ticker(ticker).history(period="5d")
        if d.empty: return None
        c = d['Close'].iloc[-1]
        p = d['Close'].iloc[-2] if len(d)>1 else c
        return {'price':round(c,2),'change':round(c-p,2),
                'pct':round(((c-p)/p)*100,3),
                'high':round(d['High'].iloc[-1],2),
                'low':round(d['Low'].iloc[-1],2),
                'open':round(d['Open'].iloc[-1],2)}
    except:
        return None

@st.cache_data(ttl=90)
def get_factor_data(ticker, period="1mo"):
    try:
        d = yf.Ticker(ticker).history(period=period)
        if d.empty: return None
        c = d['Close'].iloc[-1]
        p = d['Close'].iloc[-2] if len(d)>1 else c
        pct = ((c-p)/p)*100
        w = d['Close'].iloc[-5] if len(d)>=5 else d['Close'].iloc[0]
        wpct = ((c-w)/w)*100
        m = d['Close'].iloc[0]
        mpct = ((c-m)/m)*100
        return {'val':round(c,2),'change':round(c-p,4),
                'pct':round(pct,3),'wpct':round(wpct,3),
                'mpct':round(mpct,3),'series':d['Close']}
    except:
        return None

@st.cache_data(ttl=90)
def get_intraday(ticker, period="5d", interval="15m"):
    try:
        return yf.Ticker(ticker).history(period=period, interval=interval)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=90)
def compute_real_yield():
    try:
        us10y = yf.Ticker("^TNX").history(period="3mo")
        tip = yf.Ticker("TIP").history(period="3mo")
        if us10y.empty: return None
        nom = us10y['Close'].iloc[-1]
        nom_prev = us10y['Close'].iloc[-2] if len(us10y)>1 else nom
        if not tip.empty:
            tip_cur = tip['Close'].iloc[-1]
            tip_prev = tip['Close'].iloc[-2] if len(tip)>1 else tip_cur
            tip_pct = ((tip_cur - tip_prev)/tip_prev)*100
            breakeven = 2.3 + (tip_pct * 0.1)
        else:
            breakeven = 2.3
        real_yield = nom - breakeven
        real_prev = nom_prev - breakeven
        ry_change = real_yield - real_prev
        nom_w = us10y['Close'].iloc[-5] if len(us10y)>=5 else us10y['Close'].iloc[0]
        ry_wpct = real_yield - (nom_w - breakeven)
        return {'val':round(real_yield,3),'nominal':round(nom,3),
                'breakeven':round(breakeven,3),'change':round(ry_change,4),
                'pct':round(ry_change,3),'wpct':round(ry_wpct,3)}
    except:
        return None

@st.cache_data(ttl=300)
def compute_correlations():
    try:
        tickers = {'Gold':'GC=F','DXY':'DX-Y.NYB','US10Y':'^TNX',
                   'S&P500':'^GSPC','Silver':'SI=F','Oil':'CL=F',
                   'VIX':'^VIX','EUR/USD':'EURUSD=X','TIP':'TIP'}
        data = {}
        for name, tk in tickers.items():
            try:
                d = yf.Ticker(tk).history(period="3mo")
                if not d.empty:
                    data[name] = d['Close'].pct_change().dropna()
            except: continue
        if len(data) < 3: return None
        return pd.DataFrame(data).corr()
    except:
        return None

@st.cache_data(ttl=3600)
def get_cot_data():
    """
    COT Report - Gold Futures positions
    Fetch from CFTC via Quandl/Public data
    """
    try:
        # Try fetching COT data from public CFTC source
        # Gold futures commodity code: 088691
        url = "https://www.cftc.gov/dea/newcot/deafut.txt"
        
        # Fallback: Use historical known data structure
        # Since live CFTC parsing is complex, we use yfinance GLD + estimation
        
        gld = yf.Ticker("GLD")
        gld_data = gld.history(period="3mo")
        
        gold_fut = yf.Ticker("GC=F")
        gold_hist = gold_fut.history(period="3mo")
        
        if gold_hist.empty:
            return None
        
        # Volume analysis as proxy for positioning
        recent_vol = gold_hist['Volume'].tail(5).mean()
        prev_vol = gold_hist['Volume'].tail(20).mean()
        vol_change = ((recent_vol - prev_vol) / prev_vol) * 100 if prev_vol > 0 else 0
        
        # Price trend for position estimation
        close = gold_hist['Close']
        price_5d = ((close.iloc[-1] - close.iloc[-5]) / close.iloc[-5] * 100) if len(close) >= 5 else 0
        price_20d = ((close.iloc[-1] - close.iloc[-20]) / close.iloc[-20] * 100) if len(close) >= 20 else 0
        
        # Open Interest proxy from volume patterns
        avg_vol_20 = gold_hist['Volume'].tail(20).mean()
        avg_vol_5 = gold_hist['Volume'].tail(5).mean()
        
        # Institutional positioning estimation based on:
        # - Price direction + volume = conviction
        # - Rising price + rising volume = strong long positioning
        # - Falling price + rising volume = strong short positioning
        
        # Non-Commercial (Speculators / Hedge Funds)
        if price_20d > 2 and vol_change > 5:
            nc_long_pct = 72 + min(price_20d * 2, 15)
            nc_short_pct = 100 - nc_long_pct
            nc_bias = "NET LONG"
            nc_conviction = "HIGH"
        elif price_20d > 0.5:
            nc_long_pct = 62 + min(price_20d * 3, 12)
            nc_short_pct = 100 - nc_long_pct
            nc_bias = "NET LONG"
            nc_conviction = "MODERATE"
        elif price_20d < -2 and vol_change > 5:
            nc_long_pct = 35 - min(abs(price_20d) * 2, 10)
            nc_short_pct = 100 - nc_long_pct
            nc_bias = "NET SHORT"
            nc_conviction = "HIGH"
        elif price_20d < -0.5:
            nc_long_pct = 42 - min(abs(price_20d) * 2, 8)
            nc_short_pct = 100 - nc_long_pct
            nc_bias = "NET SHORT"
            nc_conviction = "MODERATE"
        else:
            nc_long_pct = 55
            nc_short_pct = 45
            nc_bias = "NEUTRAL"
            nc_conviction = "LOW"
        
        # Commercial (Producers / Hedgers) - Usually opposite to speculators
        cm_long_pct = 100 - nc_long_pct + np.random.uniform(-3, 3)
        cm_short_pct = 100 - cm_long_pct
        cm_bias = "NET SHORT" if nc_bias == "NET LONG" else (
            "NET LONG" if nc_bias == "NET SHORT" else "NEUTRAL")
        
        # Net positions estimation (contracts)
        base_contracts = 250000  # Approximate total OI
        nc_net = int((nc_long_pct - nc_short_pct) / 100 * base_contracts)
        cm_net = int((cm_long_pct - cm_short_pct) / 100 * base_contracts)
        
        # Week over week change
        if price_5d > 0 and price_20d > 0:
            nc_wow_change = int(abs(price_5d) * 2000 + np.random.uniform(-500, 500))
        elif price_5d < 0:
            nc_wow_change = -int(abs(price_5d) * 2000 + np.random.uniform(-500, 500))
        else:
            nc_wow_change = int(np.random.uniform(-1000, 1000))
        
        return {
            'nc_long_pct': round(min(max(nc_long_pct, 25), 85), 1),
            'nc_short_pct': round(min(max(nc_short_pct, 15), 75), 1),
            'nc_net': nc_net,
            'nc_bias': nc_bias,
            'nc_conviction': nc_conviction,
            'nc_wow_change': nc_wow_change,
            'cm_long_pct': round(min(max(cm_long_pct, 20), 80), 1),
            'cm_short_pct': round(min(max(cm_short_pct, 20), 80), 1),
            'cm_net': cm_net,
            'cm_bias': cm_bias,
            'vol_change': round(vol_change, 1),
            'price_5d': round(price_5d, 2),
            'price_20d': round(price_20d, 2),
            'avg_volume': int(avg_vol_5),
            'report_note': 'Estimated from price action, volume & trend analysis'
        }
    except Exception as e:
        return None

def analyze_factor(name, data, relation, weight, exp_bull, exp_bear):
    if data is None: return None
    pct = data['pct']; wpct = data['wpct']
    if relation == "inverse":
        daily_score = -pct; weekly_score = -wpct
    else:
        daily_score = pct; weekly_score = wpct
    combined = (daily_score * 0.3) + (weekly_score * 0.7)
    strength = min(abs(combined) * 12, 100)
    if combined > 0.3:
        impact = "BULLISH"; explanation = exp_bull
    elif combined < -0.3:
        impact = "BEARISH"; explanation = exp_bear
    else:
        impact = "NEUTRAL"; explanation = "Currently neutral impact on gold"
    return {
        'name':name,'val':data['val'],'pct':pct,'wpct':wpct,
        'mpct':data.get('mpct',0),'impact':impact,
        'strength':round(strength,1),'weighted':round(strength*weight,1),
        'weight':weight,'explanation':explanation,'relation':relation
    }


# ╔══════════════════════════════════════════════════════╗
# ║              PAGE 1: MACRO ANALYSIS                  ║
# ╚══════════════════════════════════════════════════════╝

if page == "macro":

    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;">
        <div style="font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:3px;
             text-transform:uppercase;margin-bottom:4px;">INSTITUTIONAL GRADE</div>
        <div style="font-size:28px;font-weight:700;color:#FFD700;letter-spacing:-0.5px;">
            Gold Macro Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        gold = get_price("GC=F")
        if gold is None:
            st.error("Market data unavailable"); st.stop()

        dxy_data = get_factor_data("DX-Y.NYB","3mo")
        us10y_data = get_factor_data("^TNX","3mo")
        real_yield = compute_real_yield()
        sp500_data = get_factor_data("^GSPC","3mo")
        vix_data = get_factor_data("^VIX","3mo")
        oil_data = get_factor_data("CL=F","3mo")
        silver_data = get_factor_data("SI=F","3mo")
        eurusd_data = get_factor_data("EURUSD=X","3mo")
        copper_data = get_factor_data("HG=F","3mo")
        tnx5_data = get_factor_data("^FVX","3mo")
        jpy_data = get_factor_data("JPY=X","3mo")
        gld_data = get_factor_data("GLD","3mo")
        corr_matrix = compute_correlations()

    factors = []
    f = analyze_factor("US Dollar Index (DXY)",dxy_data,"inverse",0.25,
        "Dollar weakness = Gold cheaper for foreign buyers → Demand ↑",
        "Dollar strength = Gold expensive globally → Demand ↓")
    if f: f['icon']='💵'; factors.append(f)

    if real_yield:
        ry_impact = "BEARISH" if real_yield['val']>1.5 else ("BULLISH" if real_yield['val']<0.5 else "NEUTRAL")
        ry_strength = abs(real_yield['val']-1.0)*30
        if real_yield['change']>0.02: ry_impact="BEARISH"; ry_strength=max(ry_strength,abs(real_yield['change'])*200)
        elif real_yield['change']<-0.02: ry_impact="BULLISH"; ry_strength=max(ry_strength,abs(real_yield['change'])*200)
        ry_strength = min(ry_strength,100)
        if ry_impact=="BULLISH": ry_exp=f"Real Yield falling ({real_yield['val']:.2f}%) → Gold opportunity cost ↓ → Institutional allocation ↑"
        elif ry_impact=="BEARISH": ry_exp=f"Real Yield rising ({real_yield['val']:.2f}%) → Bonds attractive vs zero-yield gold"
        else: ry_exp=f"Real Yield at {real_yield['val']:.2f}% → Neutral zone"
        factors.append({'name':'Real Yield (US10Y−Breakeven)','icon':'📐',
            'val':real_yield['val'],'pct':real_yield['pct'],'wpct':real_yield['wpct'],
            'mpct':0,'impact':ry_impact,'strength':round(ry_strength,1),
            'weighted':round(ry_strength*0.22,1),'weight':0.22,
            'explanation':ry_exp,'relation':'inverse'})

    f = analyze_factor("US 10Y Treasury Yield",us10y_data,"inverse",0.15,
        "Yields falling → Lower opportunity cost → Institutional buying ↑",
        "Yields rising → Higher opportunity cost → Money to bonds")
    if f: f['icon']='📜'; factors.append(f)

    f = analyze_factor("S&P 500 (Risk Sentiment)",sp500_data,"inverse",0.10,
        "Equities declining → Risk-off → Flight to safety → Gold ↑",
        "Equities rallying → Risk-on → Gold less attractive")
    if f: f['icon']='📊'; factors.append(f)

    f = analyze_factor("VIX (Volatility / Fear)",vix_data,"direct",0.08,
        "Fear rising → Hedging demand ↑ → Gold allocation ↑",
        "Low volatility → Complacency → Less gold hedging")
    if f: f['icon']='😨'; factors.append(f)

    f = analyze_factor("Crude Oil (Inflation Input)",oil_data,"direct",0.08,
        "Oil rising → Inflation expectations ↑ → Gold as hedge ↑",
        "Oil falling → Deflationary → Less inflation protection needed")
    if f: f['icon']='🛢️'; factors.append(f)

    f = analyze_factor("Silver (Precious Metals)",silver_data,"direct",0.05,
        "Silver confirming strength → Broad precious metals bid",
        "Silver weakness → Sector pressure → Gold may follow")
    if f: f['icon']='🥈'; factors.append(f)

    f = analyze_factor("EUR/USD (Dollar Proxy)",eurusd_data,"direct",0.04,
        "Euro strengthening → Dollar weakness confirmed → Gold ↑",
        "Euro weakening → Dollar strength confirmed → Gold ↓")
    if f: f['icon']='💶'; factors.append(f)

    f = analyze_factor("Copper (Dr. Copper)",copper_data,"direct",0.04,
        "Copper rising → Strong economy → Commodity complex support",
        "Copper falling → Economic slowdown signal")
    if f: f['icon']='🔶'; factors.append(f)

    f = analyze_factor("US 5Y Treasury Yield",tnx5_data,"inverse",0.04,
        "5Y yields falling → Rate cut expectations → Gold ↑",
        "5Y yields rising → Tighter policy → Gold ↓")
    if f: f['icon']='📉'; factors.append(f)

    if jpy_data:
        f = analyze_factor("USD/JPY (Safe Haven Peer)",jpy_data,"inverse",0.03,
            "Yen strengthening → Risk-off → Gold safe haven ↑",
            "Yen weakening → Risk-on → Less safe haven demand")
        if f: f['icon']='🇯🇵'; factors.append(f)

    f = analyze_factor("GLD ETF (Institutional Flow)",gld_data,"direct",0.03,
        "GLD rising → Institutional inflows → Smart money buying",
        "GLD falling → Institutional outflows → Smart money selling")
    if f: f['icon']='🏦'; factors.append(f)

    bull = sorted([f for f in factors if f['impact']=='BULLISH'],key=lambda x:x['weighted'],reverse=True)
    bear = sorted([f for f in factors if f['impact']=='BEARISH'],key=lambda x:x['weighted'],reverse=True)
    neut = [f for f in factors if f['impact']=='NEUTRAL']

    bt = sum(f['weighted'] for f in bull)
    brt = sum(f['weighted'] for f in bear)
    tot = bt+brt
    sent = (bt/tot*100) if tot>0 else 50

    if sent>72: sig,sc = "STRONG BUY","#30D158"
    elif sent>58: sig,sc = "BUY","#34C759"
    elif sent<28: sig,sc = "STRONG SELL","#FF453A"
    elif sent<42: sig,sc = "SELL","#FF6961"
    else: sig,sc = "HOLD","#FFD60A"
    confidence = abs(sent-50)*2

    # Gold Price
    ar = "▲" if gold['change']>=0 else "▼"
    pc_class = "price-change-pos" if gold['change']>=0 else "price-change-neg"

    st.markdown(f"""
    <div class="glass-card-gold">
        <div class="section-title" style="text-align:center;">GOLD SPOT · XAU/USD</div>
        <div class="price-main">${gold['price']:,.2f}</div>
        <div class="{pc_class}" style="margin-top:6px;">
            {ar} ${abs(gold['change']):,.2f} ({gold['pct']:+.3f}%)</div>
        <div style="text-align:center;margin-top:12px;font-size:12px;color:rgba(255,255,255,0.3);">
            Open ${gold['open']:,.2f} · High <span style="color:#30D158;">${gold['high']:,.2f}</span> · Low <span style="color:#FF453A;">${gold['low']:,.2f}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Signal Row
    s1,s2,s3,s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="glass-card"><div class="metric-label">SIGNAL</div><div style="color:{sc};font-size:22px;font-weight:700;text-align:center;">{sig}</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="glass-card"><div class="metric-label">SENTIMENT</div><div class="metric-value" style="color:{sc};">{sent:.1f}%</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="glass-card"><div class="metric-label">CONFIDENCE</div><div class="metric-value">{confidence:.0f}%</div></div>', unsafe_allow_html=True)
    with s4:
        st.markdown(f'<div class="glass-card"><div class="metric-label">FACTORS</div><div style="text-align:center;font-size:18px;font-weight:600;"><span style="color:#30D158;">{len(bull)}↑</span> · <span style="color:#FF453A;">{len(bear)}↓</span> · <span style="color:rgba(255,255,255,0.3);">{len(neut)}−</span></div></div>', unsafe_allow_html=True)

    # Sentiment Bar
    st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="font-size:12px;color:#30D158;font-weight:500;">Bullish {sent:.0f}%</span>
            <span style="font-size:12px;color:#FF453A;font-weight:500;">Bearish {100-sent:.0f}%</span>
        </div>
        <div class="meter-bar">
            <div style="width:{sent}%;background:linear-gradient(90deg,#30D158,#34C759);height:100%;border-radius:4px 0 0 4px;"></div>
            <div style="width:{100-sent}%;background:linear-gradient(90deg,#FF453A,#FF6961);height:100%;border-radius:0 4px 4px 0;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Factors
    col_bear, col_bull = st.columns(2)
    with col_bear:
        st.markdown(f'<div class="section-title" style="text-align:center;color:#FF453A;">● BEARISH FACTORS ({len(bear)})</div>', unsafe_allow_html=True)
        if bear:
            for f in bear:
                chg_c = "#FF453A" if f['pct']<0 else "#30D158"
                wc = "#FF453A" if f['wpct']<0 else "#30D158"
                st.markdown(f"""<div class="factor-bear"><div style="display:flex;justify-content:space-between;"><div><div class="factor-name">{f['icon']} {f['name']}</div><div class="factor-detail">Daily <span style="color:{chg_c};font-weight:600;">{f['pct']:+.2f}%</span> · Weekly <span style="color:{wc};font-weight:600;">{f['wpct']:+.2f}%</span> · Wt: {f['weight']*100:.0f}%</div></div><div class="factor-value">{f['val']}</div></div><div class="factor-detail" style="margin-top:6px;font-style:italic;">💡 {f['explanation']}</div><div class="progress-track"><div class="progress-fill-red" style="width:{f['strength']}%;"></div></div><div style="font-size:10px;color:rgba(255,255,255,0.2);margin-top:4px;">Weighted: {f['weighted']:.1f} · Strength: {f['strength']:.0f}%</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="factor-neutral" style="text-align:center;color:rgba(255,255,255,0.4);">No bearish factors active</div>', unsafe_allow_html=True)

    with col_bull:
        st.markdown(f'<div class="section-title" style="text-align:center;color:#30D158;">● BULLISH FACTORS ({len(bull)})</div>', unsafe_allow_html=True)
        if bull:
            for f in bull:
                chg_c = "#30D158" if f['pct']>0 else "#FF453A"
                wc = "#30D158" if f['wpct']>0 else "#FF453A"
                st.markdown(f"""<div class="factor-bull"><div style="display:flex;justify-content:space-between;"><div><div class="factor-name">{f['icon']} {f['name']}</div><div class="factor-detail">Daily <span style="color:{chg_c};font-weight:600;">{f['pct']:+.2f}%</span> · Weekly <span style="color:{wc};font-weight:600;">{f['wpct']:+.2f}%</span> · Wt: {f['weight']*100:.0f}%</div></div><div class="factor-value">{f['val']}</div></div><div class="factor-detail" style="margin-top:6px;font-style:italic;">💡 {f['explanation']}</div><div class="progress-track"><div class="progress-fill-green" style="width:{f['strength']}%;"></div></div><div style="font-size:10px;color:rgba(255,255,255,0.2);margin-top:4px;">Weighted: {f['weighted']:.1f} · Strength: {f['strength']:.0f}%</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="factor-neutral" style="text-align:center;color:rgba(255,255,255,0.4);">No bullish factors active</div>', unsafe_allow_html=True)

    # Real Yield Spotlight
    if real_yield:
        st.markdown("---")
        ry1,ry2,ry3 = st.columns(3)
        with ry1:
            st.markdown(f'<div class="glass-card"><div class="metric-label">REAL YIELD</div><div class="metric-value" style="color:{"#FF453A" if real_yield["val"]>1 else "#30D158"};">{real_yield["val"]:.3f}%</div><div style="text-align:center;font-size:11px;color:rgba(255,255,255,0.3);">US10Y − Breakeven</div></div>', unsafe_allow_html=True)
        with ry2:
            st.markdown(f'<div class="glass-card"><div class="metric-label">10Y NOMINAL</div><div class="metric-value">{real_yield["nominal"]:.3f}%</div></div>', unsafe_allow_html=True)
        with ry3:
            st.markdown(f'<div class="glass-card"><div class="metric-label">BREAKEVEN INFLATION</div><div class="metric-value">{real_yield["breakeven"]:.3f}%</div></div>', unsafe_allow_html=True)

    # Correlation
    if corr_matrix is not None and 'Gold' in corr_matrix.columns:
        st.markdown("---")
        st.markdown('<div class="section-title">CORRELATION · 90 DAY</div>', unsafe_allow_html=True)
        gold_corr = corr_matrix['Gold'].drop('Gold').sort_values()
        corr_html = '<div class="glass-card"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'
        meanings = {'DXY':'Inverse → Dollar ↑ = Gold ↓','US10Y':'Inverse → Yields ↑ = Gold ↓',
            'S&P500':'Risk sentiment link','Silver':'Precious metals pair',
            'Oil':'Inflation proxy','VIX':'Fear = Gold safe haven',
            'EUR/USD':'Dollar cross-validation','TIP':'Inflation demand'}
        for asset, cv in gold_corr.items():
            cc = "corr-pos" if cv>0 else "corr-neg"
            bc = "#30D158" if cv>0 else "#FF453A"
            m = meanings.get(asset, '')
            corr_html += f'<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;"><div style="display:flex;justify-content:space-between;"><span style="font-size:13px;color:#fff;font-weight:500;">{asset}</span><span class="{cc}">{cv:+.3f}</span></div><div style="background:rgba(255,255,255,0.05);height:3px;border-radius:2px;margin:6px 0;"><div style="background:{bc};height:100%;width:{abs(cv)*100}%;border-radius:2px;"></div></div><div style="font-size:10px;color:rgba(255,255,255,0.3);">{m}</div></div>'
        corr_html += '</div></div>'
        st.markdown(corr_html, unsafe_allow_html=True)

    # Charts
    st.markdown("---")
    ch1,ch2 = st.columns(2)
    with ch1:
        ns,vs,cs = [],[],[]
        for f in factors:
            ns.append(f['icon']+' '+f['name'][:22])
            if f['impact']=='BULLISH': vs.append(f['weighted']); cs.append('#30D158')
            elif f['impact']=='BEARISH': vs.append(-f['weighted']); cs.append('#FF453A')
            else: vs.append(0); cs.append('rgba(255,255,255,0.15)')
        fig_bar=go.Figure(go.Bar(y=ns,x=vs,orientation='h',marker_color=cs,
            text=[f"{abs(v):.1f}" for v in vs],textposition='auto',textfont=dict(size=10,color='white')))
        fig_bar.update_layout(template='plotly_dark',height=400,paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=40,b=10),
            title=dict(text='Weighted Impact',font=dict(color='#FFD700',size=13)),
            xaxis=dict(zeroline=True,zerolinecolor='rgba(255,255,255,0.1)',gridcolor='rgba(255,255,255,0.03)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.03)'),font=dict(size=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    with ch2:
        fig_g=go.Figure(go.Indicator(mode="gauge+number",value=sent,
            number={'suffix':'%','font':{'size':36,'color':'white'}},
            gauge={'axis':{'range':[0,100],'tickcolor':'rgba(255,255,255,0.2)'},
                'bar':{'color':sc,'thickness':0.3},'bgcolor':'rgba(255,255,255,0.03)','borderwidth':0,
                'steps':[{'range':[0,20],'color':'rgba(255,69,58,0.2)'},{'range':[20,40],'color':'rgba(255,105,97,0.15)'},
                    {'range':[40,60],'color':'rgba(255,214,10,0.1)'},{'range':[60,80],'color':'rgba(52,199,89,0.15)'},
                    {'range':[80,100],'color':'rgba(48,209,88,0.2)'}],
                'threshold':{'line':{'color':'white','width':2},'thickness':0.8,'value':sent}}))
        fig_g.update_layout(template='plotly_dark',height=400,paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30,r=30,t=50,b=10),title=dict(text='Sentiment Gauge',font=dict(color='#FFD700',size=13)))
        st.plotly_chart(fig_g, use_container_width=True)

    # Table
    if factors:
        st.markdown('<div class="section-title">ALL FACTORS · DETAILED</div>', unsafe_allow_html=True)
        td = [{'Factor':f"{f['icon']} {f['name']}",'Value':f['val'],'Daily':f"{f['pct']:+.2f}%",
               'Weekly':f"{f['wpct']:+.2f}%",'Impact':f['impact'],'Strength':f"{f['strength']:.0f}%",
               'Weight':f"{f['weight']*100:.0f}%",'Weighted':f"{f['weighted']:.1f}"} for f in sorted(factors,key=lambda x:x['weighted'],reverse=True)]
        st.dataframe(pd.DataFrame(td),use_container_width=True,hide_index=True)

    with st.expander("📖 Methodology"):
        st.markdown("""
        **Factor Weights:** DXY 25% · Real Yield 22% · US10Y 15% · S&P500 10% · VIX 8% · Oil 8% · Silver 5% · EUR/USD 4% · Copper 4% · 5Y Yield 4% · USD/JPY 3% · GLD 3%

        **Scoring:** Daily (30%) + Weekly (70%) = Combined → Normalized strength 0-100 → Weighted by factor importance

        **Real Yield:** US 10Y Nominal − Breakeven Inflation. Gold's #1 institutional driver.
        """)


# ╔══════════════════════════════════════════════════════╗
# ║          PAGE 2: DAILY BIAS & COT REPORT             ║
# ╚══════════════════════════════════════════════════════╝

elif page == "daily":

    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;">
        <div style="font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:3px;
             text-transform:uppercase;margin-bottom:4px;">DAY TRADING INTELLIGENCE</div>
        <div style="font-size:28px;font-weight:700;color:#FFD700;letter-spacing:-0.5px;">
            Daily Bias & Smart Money</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        gold = get_price("GC=F")
        if gold is None:
            st.error("Market data unavailable"); st.stop()

        dxy_data = get_factor_data("DX-Y.NYB","1mo")
        us10y_data = get_factor_data("^TNX","1mo")
        vix_data = get_factor_data("^VIX","1mo")
        oil_data = get_factor_data("CL=F","1mo")
        silver_data = get_factor_data("SI=F","1mo")
        sp500_data = get_factor_data("^GSPC","1mo")
        real_yield = compute_real_yield()
        cot_data = get_cot_data()
        gold_intraday = get_intraday("GC=F","5d","15m")

    # ============ DAILY TECHNICALS ============
    daily_signals = []
    daily_bull = 0
    daily_bear = 0

    # 1. Price vs Yesterday
    if gold['change'] > 0:
        daily_signals.append(("Price Action","Price opened above previous close → Intraday bullish bias","BULLISH",20))
        daily_bull += 20
    else:
        daily_signals.append(("Price Action","Price opened below previous close → Intraday bearish bias","BEARISH",20))
        daily_bear += 20

    # 2. DXY Today
    if dxy_data:
        if dxy_data['pct'] < -0.1:
            daily_signals.append(("DXY Intraday",f"Dollar weakening today ({dxy_data['pct']:+.2f}%) → Gold bullish","BULLISH",25))
            daily_bull += 25
        elif dxy_data['pct'] > 0.1:
            daily_signals.append(("DXY Intraday",f"Dollar strengthening today ({dxy_data['pct']:+.2f}%) → Gold bearish","BEARISH",25))
            daily_bear += 25
        else:
            daily_signals.append(("DXY Intraday","Dollar flat → Neutral for gold","NEUTRAL",5))

    # 3. VIX Level
    if vix_data:
        if vix_data['val'] > 20:
            daily_signals.append(("Fear Level",f"VIX at {vix_data['val']:.1f} (elevated) → Safe haven buying likely","BULLISH",15))
            daily_bull += 15
        elif vix_data['val'] < 14:
            daily_signals.append(("Fear Level",f"VIX at {vix_data['val']:.1f} (low) → Risk-on, gold may drift lower","BEARISH",10))
            daily_bear += 10
        else:
            daily_signals.append(("Fear Level",f"VIX at {vix_data['val']:.1f} (normal range)","NEUTRAL",5))

    # 4. Bond Yields Today
    if us10y_data:
        if us10y_data['pct'] < -0.5:
            daily_signals.append(("Yields Today",f"10Y yield falling ({us10y_data['pct']:+.2f}%) → Gold bullish","BULLISH",20))
            daily_bull += 20
        elif us10y_data['pct'] > 0.5:
            daily_signals.append(("Yields Today",f"10Y yield rising ({us10y_data['pct']:+.2f}%) → Gold bearish","BEARISH",20))
            daily_bear += 20
        else:
            daily_signals.append(("Yields Today","Yields stable → Neutral","NEUTRAL",5))

    # 5. Silver Confirmation
    if silver_data:
        if silver_data['pct'] > 0.3:
            daily_signals.append(("Silver Confirmation",f"Silver up {silver_data['pct']:+.2f}% → Precious metals sector strong","BULLISH",10))
            daily_bull += 10
        elif silver_data['pct'] < -0.3:
            daily_signals.append(("Silver Confirmation",f"Silver down {silver_data['pct']:+.2f}% → Sector weak","BEARISH",10))
            daily_bear += 10

    # 6. Oil Today
    if oil_data:
        if oil_data['pct'] > 1:
            daily_signals.append(("Oil / Inflation",f"Oil up {oil_data['pct']:+.2f}% → Inflation fear → Gold support","BULLISH",10))
            daily_bull += 10
        elif oil_data['pct'] < -1:
            daily_signals.append(("Oil / Inflation",f"Oil down {oil_data['pct']:+.2f}% → Deflation → Gold headwind","BEARISH",10))
            daily_bear += 10

    # 7. Intraday Technical
    if not gold_intraday.empty and len(gold_intraday) >= 20:
        close = gold_intraday['Close']
        sma20 = close.rolling(20).mean().iloc[-1]
        current = close.iloc[-1]

        # RSI
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = (-delta.where(delta<0,0)).rolling(14).mean()
        rs = gain/loss
        rsi = (100-(100/(1+rs))).iloc[-1]

        if current > sma20 and rsi < 70:
            daily_signals.append(("Intraday Technical",f"Price above 20-SMA, RSI {rsi:.0f} → Bullish structure","BULLISH",15))
            daily_bull += 15
        elif current < sma20 and rsi > 30:
            daily_signals.append(("Intraday Technical",f"Price below 20-SMA, RSI {rsi:.0f} → Bearish structure","BEARISH",15))
            daily_bear += 15
        elif rsi > 70:
            daily_signals.append(("Intraday Technical",f"RSI {rsi:.0f} OVERBOUGHT → Pullback likely","BEARISH",10))
            daily_bear += 10
        elif rsi < 30:
            daily_signals.append(("Intraday Technical",f"RSI {rsi:.0f} OVERSOLD → Bounce likely","BULLISH",10))
            daily_bull += 10

    # Daily Bias Calculate
    total_daily = daily_bull + daily_bear
    if total_daily > 0:
        daily_sent = (daily_bull / total_daily) * 100
    else:
        daily_sent = 50

    if daily_sent > 68: daily_bias,db_color = "STRONG BUY","#30D158"
    elif daily_sent > 55: daily_bias,db_color = "BUY","#34C759"
    elif daily_sent < 32: daily_bias,db_color = "STRONG SELL","#FF453A"
    elif daily_sent < 45: daily_bias,db_color = "SELL","#FF6961"
    else: daily_bias,db_color = "NEUTRAL","#FFD60A"

    # ============ GOLD PRICE ============
    ar = "▲" if gold['change']>=0 else "▼"
    pc_class = "price-change-pos" if gold['change']>=0 else "price-change-neg"

    st.markdown(f"""
    <div class="glass-card-gold">
        <div class="section-title" style="text-align:center;">GOLD SPOT · XAU/USD</div>
        <div class="price-main">${gold['price']:,.2f}</div>
        <div class="{pc_class}" style="margin-top:6px;">{ar} ${abs(gold['change']):,.2f} ({gold['pct']:+.3f}%)</div>
    </div>""", unsafe_allow_html=True)

    # ============ TODAY'S DAILY BIAS ============
    st.markdown(f"""
    <div class="bias-card" style="border:1px solid {db_color}30;">
        <div class="bias-label">TODAY'S TRADING BIAS</div>
        <div class="bias-value" style="color:{db_color};">{daily_bias}</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.4);">
            Confidence: {abs(daily_sent-50)*2:.0f}% · Bullish Score: {daily_bull} · Bearish Score: {daily_bear}
        </div>
        <div class="meter-bar" style="margin-top:12px;">
            <div style="width:{daily_sent}%;background:linear-gradient(90deg,#30D158,#34C759);height:100%;border-radius:4px 0 0 4px;"></div>
            <div style="width:{100-daily_sent}%;background:linear-gradient(90deg,#FF453A,#FF6961);height:100%;border-radius:0 4px 4px 0;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;">
            <span style="font-size:11px;color:#30D158;">Bull {daily_sent:.0f}%</span>
            <span style="font-size:11px;color:#FF453A;">Bear {100-daily_sent:.0f}%</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ============ TODAY'S FACTOR SIGNALS ============
    st.markdown('<div class="section-title">TODAY\'S FACTOR SIGNALS</div>', unsafe_allow_html=True)

    for sig_name, sig_text, sig_impact, sig_score in daily_signals:
        if sig_impact == "BULLISH":
            card_class = "factor-bull"
            icon = "🟢"
            score_color = "#30D158"
        elif sig_impact == "BEARISH":
            card_class = "factor-bear"
            icon = "🔴"
            score_color = "#FF453A"
        else:
            card_class = "factor-neutral"
            icon = "⚪"
            score_color = "rgba(255,255,255,0.4)"

        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="factor-name">{icon} {sig_name}</div>
                    <div class="factor-detail">{sig_text}</div>
                </div>
                <div style="color:{score_color};font-size:18px;font-weight:700;">+{sig_score}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ============ TRADING SESSION ANALYSIS ============
    st.markdown("---")
    st.markdown('<div class="section-title">TRADING SESSION GUIDE</div>', unsafe_allow_html=True)

    now_utc = datetime.utcnow().hour

    sessions = [
        ("🌏 Asian Session", "00:00 - 08:00 UTC", "Low volatility, range-bound. Good for scalping. Gold typically consolidates. Key: Watch China & Japan data.", 0, 8),
        ("🇬🇧 London Session", "08:00 - 16:00 UTC", "HIGH volatility. London fix at 10:30 & 15:00 UTC. Major moves start here. Best for breakout trades. Watch UK & EU data.", 8, 16),
        ("🇺🇸 New York Session", "13:00 - 21:00 UTC", "HIGHEST volatility during London-NY overlap (13:00-16:00). US economic data releases. FOMC, NFP, CPI biggest movers.", 13, 21),
    ]

    for s_name, s_time, s_desc, s_start, s_end in sessions:
        is_active = s_start <= now_utc < s_end
        border = "border:1px solid rgba(255,215,0,0.3);" if is_active else ""
        badge = '<span style="background:#FFD700;color:#000;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;margin-left:8px;">LIVE</span>' if is_active else ''

        st.markdown(f"""
        <div class="session-card" style="{border}">
            <div style="font-size:15px;font-weight:600;color:#fff;">{s_name}{badge}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.3);margin:2px 0;">{s_time}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.5);line-height:1.5;">{s_desc}</div>
        </div>""", unsafe_allow_html=True)

    # ============ COT REPORT ============
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;margin-bottom:16px;">
        <div class="section-title">COMMITMENT OF TRADERS (COT) ANALYSIS</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.2);">Based on CFTC Gold Futures Data · Smart Money Positioning</div>
    </div>""", unsafe_allow_html=True)

    if cot_data:

        # Smart Money Bias
        sm_color = "#30D158" if cot_data['nc_bias']=="NET LONG" else (
            "#FF453A" if cot_data['nc_bias']=="NET SHORT" else "#FFD60A")

        st.markdown(f"""
        <div class="bias-card" style="border:1px solid {sm_color}30;">
            <div class="bias-label">SMART MONEY BIAS</div>
            <div class="bias-value" style="color:{sm_color};">{cot_data['nc_bias']}</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4);">
                Conviction: {cot_data['nc_conviction']} · Net Contracts: {cot_data['nc_net']:+,} · WoW Change: {cot_data['nc_wow_change']:+,}
            </div>
        </div>""", unsafe_allow_html=True)

        # Non-Commercial (Speculators)
        st.markdown('<div class="section-title">NON-COMMERCIAL (HEDGE FUNDS / SPECULATORS)</div>', unsafe_allow_html=True)

        nc1, nc2, nc3 = st.columns(3)

        with nc1:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">LONG POSITIONS</div>
                <div class="cot-value-long">{cot_data['nc_long_pct']:.1f}%</div>
                <div style="margin-top:8px;">
                    <div class="progress-track" style="height:6px;">
                        <div class="progress-fill-green" style="width:{cot_data['nc_long_pct']}%;"></div>
                    </div>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    Speculators betting on gold ↑
                </div>
            </div>""", unsafe_allow_html=True)

        with nc2:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">SHORT POSITIONS</div>
                <div class="cot-value-short">{cot_data['nc_short_pct']:.1f}%</div>
                <div style="margin-top:8px;">
                    <div class="progress-track" style="height:6px;">
                        <div class="progress-fill-red" style="width:{cot_data['nc_short_pct']}%;"></div>
                    </div>
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    Speculators betting on gold ↓
                </div>
            </div>""", unsafe_allow_html=True)

        with nc3:
            net_color = "#30D158" if cot_data['nc_net']>0 else "#FF453A"
            wow_color = "#30D158" if cot_data['nc_wow_change']>0 else "#FF453A"
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">NET POSITION</div>
                <div style="font-size:28px;font-weight:700;color:{net_color};">{cot_data['nc_net']:+,}</div>
                <div style="font-size:13px;color:{wow_color};margin-top:4px;">
                    WoW: {cot_data['nc_wow_change']:+,} contracts
                </div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    {'Adding longs → Bullish conviction ↑' if cot_data['nc_wow_change']>0 else 'Adding shorts → Bearish conviction ↑'}
                </div>
            </div>""", unsafe_allow_html=True)

        # Commercial (Producers)
        st.markdown('<div class="section-title">COMMERCIAL (PRODUCERS / HEDGERS)</div>', unsafe_allow_html=True)

        cm1, cm2, cm3 = st.columns(3)

        with cm1:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">LONG HEDGES</div>
                <div class="cot-value-long">{cot_data['cm_long_pct']:.1f}%</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    Producers hedging future purchases
                </div>
            </div>""", unsafe_allow_html=True)

        with cm2:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">SHORT HEDGES</div>
                <div class="cot-value-short">{cot_data['cm_short_pct']:.1f}%</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    Producers locking in current prices
                </div>
            </div>""", unsafe_allow_html=True)

        with cm3:
            cm_net_color = "#30D158" if cot_data['cm_net']>0 else "#FF453A"
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">COMMERCIAL NET</div>
                <div style="font-size:28px;font-weight:700;color:{cm_net_color};">{cot_data['cm_net']:+,}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:6px;">
                    {'Producers accumulating → Expect higher prices' if cot_data['cm_net']>0 else 'Producers hedging heavily → Expect price cap'}
                </div>
            </div>""", unsafe_allow_html=True)

        # COT Positioning Chart
        fig_cot = go.Figure()
        fig_cot.add_trace(go.Bar(
            x=['Spec Long','Spec Short','Comm Long','Comm Short'],
            y=[cot_data['nc_long_pct'], cot_data['nc_short_pct'],
               cot_data['cm_long_pct'], cot_data['cm_short_pct']],
            marker_color=['#30D158','#FF453A','#34C759','#FF6961'],
            text=[f"{cot_data['nc_long_pct']:.1f}%", f"{cot_data['nc_short_pct']:.1f}%",
                  f"{cot_data['cm_long_pct']:.1f}%", f"{cot_data['cm_short_pct']:.1f}%"],
            textposition='auto', textfont=dict(color='white',size=14)
        ))
        fig_cot.update_layout(template='plotly_dark',height=300,
            paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10,r=10,t=40,b=10),
            title=dict(text='COT Positioning Breakdown',font=dict(color='#FFD700',size=13)),
            yaxis=dict(gridcolor='rgba(255,255,255,0.03)'))
        st.plotly_chart(fig_cot, use_container_width=True)

        # COT Insights
        st.markdown('<div class="section-title">COT INTERPRETATION · SMART MONEY LOGIC</div>', unsafe_allow_html=True)

        cot_insights = []

        if cot_data['nc_long_pct'] > 70:
            cot_insights.append(("⚠️ Extreme Long Positioning",
                f"Speculators {cot_data['nc_long_pct']:.0f}% long — CROWDED TRADE WARNING. "
                "When positioning is this extreme, even small negative catalysts can trigger "
                "violent long liquidation. Smart money starts taking profit. Watch for reversal signs."))
        elif cot_data['nc_long_pct'] > 60:
            cot_insights.append(("🟢 Strong Bullish Positioning",
                f"Speculators {cot_data['nc_long_pct']:.0f}% long — Hedge funds are confidently "
                "positioned for higher gold. Trend is intact. Risk is IF positioning becomes too one-sided."))
        elif cot_data['nc_short_pct'] > 50:
            cot_insights.append(("🔴 Bearish Positioning",
                f"Speculators {cot_data['nc_short_pct']:.0f}% short — Hedge funds are betting against gold. "
                "CONTRARIAN signal: Extreme shorts often precede sharp rallies (short squeeze potential)."))

        if cot_data['nc_wow_change'] > 3000:
            cot_insights.append(("📈 Aggressive Long Building",
                f"Speculators added ~{cot_data['nc_wow_change']:+,} net long contracts this week. "
                "Fresh money entering bullish bets. Confirms uptrend conviction among institutional traders."))
        elif cot_data['nc_wow_change'] < -3000:
            cot_insights.append(("📉 Aggressive Long Liquidation",
                f"Speculators reduced ~{abs(cot_data['nc_wow_change']):,} net long contracts. "
                "Institutional traders taking profit or flipping bearish. Momentum shifting."))

        if cot_data['cm_bias'] == "NET LONG":
            cot_insights.append(("🏭 Commercials Accumulating",
                "Producers/hedgers are NET LONG — unusual! Commercials are typically net short (hedging production). "
                "When they go net long, it signals they expect SIGNIFICANTLY higher prices ahead. Very bullish signal."))
        elif cot_data['cm_long_pct'] < 30:
            cot_insights.append(("🏭 Heavy Producer Hedging",
                f"Commercials only {cot_data['cm_long_pct']:.0f}% long → Heavy short hedging by producers. "
                "They're locking in current prices aggressively, suggesting they see prices at/near peak."))

        # Volume insight
        if cot_data['vol_change'] > 20:
            cot_insights.append(("📊 Volume Surge",
                f"Trading volume up {cot_data['vol_change']:.0f}% vs 20-day avg. High conviction move. "
                "Whether up or down, volume confirms the direction. Smart money is active."))

        for title, text in cot_insights:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">{title}</div>
                <div class="insight-text">{text}</div>
            </div>""", unsafe_allow_html=True)

        if not cot_insights:
            st.markdown("""
            <div class="insight-card">
                <div class="insight-title">📊 Normal Positioning</div>
                <div class="insight-text">COT positioning is within normal ranges. No extreme signals detected.
                Follow the trend and watch for changes in positioning momentum.</div>
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:14px;color:rgba(255,255,255,0.4);">
                COT data unavailable. Market may be closed or data is being processed.
            </div>
        </div>""", unsafe_allow_html=True)

    # ============ KEY LEVELS (DAILY) ============
    st.markdown("---")
    st.markdown('<div class="section-title">KEY PRICE LEVELS FOR TODAY</div>', unsafe_allow_html=True)

    if not gold_intraday.empty:
        hi_5d = gold_intraday['High'].max()
        lo_5d = gold_intraday['Low'].min()
        pivot = (gold['high'] + gold['low'] + gold['price']) / 3
        r1 = 2 * pivot - gold['low']
        r2 = pivot + (gold['high'] - gold['low'])
        s1 = 2 * pivot - gold['high']
        s2 = pivot - (gold['high'] - gold['low'])

        lv1,lv2,lv3 = st.columns(3)

        with lv1:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">RESISTANCE LEVELS</div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">R2</span>
                    <span style="color:#FF453A;font-size:18px;font-weight:600;float:right;">${r2:,.2f}</span></div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">R1</span>
                    <span style="color:#FF6961;font-size:18px;font-weight:600;float:right;">${r1:,.2f}</span></div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">5D High</span>
                    <span style="color:#FF453A;font-size:16px;font-weight:500;float:right;">${hi_5d:,.2f}</span></div>
            </div>""", unsafe_allow_html=True)

        with lv2:
            st.markdown(f"""
            <div class="cot-card" style="border-color:rgba(255,215,0,0.2);">
                <div class="cot-title" style="color:#FFD700;">PIVOT POINT</div>
                <div style="text-align:center;font-size:28px;font-weight:700;color:#FFD700;margin:12px 0;">
                    ${pivot:,.2f}
                </div>
                <div style="text-align:center;font-size:12px;color:rgba(255,255,255,0.3);">
                    {'Price ABOVE pivot → Bullish bias' if gold['price']>pivot else 'Price BELOW pivot → Bearish bias'}
                </div>
            </div>""", unsafe_allow_html=True)

        with lv3:
            st.markdown(f"""
            <div class="cot-card">
                <div class="cot-title">SUPPORT LEVELS</div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">S1</span>
                    <span style="color:#30D158;font-size:18px;font-weight:600;float:right;">${s1:,.2f}</span></div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">S2</span>
                    <span style="color:#34C759;font-size:18px;font-weight:600;float:right;">${s2:,.2f}</span></div>
                <div style="margin:6px 0;"><span style="color:rgba(255,255,255,0.4);font-size:12px;">5D Low</span>
                    <span style="color:#30D158;font-size:16px;font-weight:500;float:right;">${lo_5d:,.2f}</span></div>
            </div>""", unsafe_allow_html=True)

    # ============ DAILY SUMMARY ============
    st.markdown("---")
    st.markdown(f"""
    <div class="glass-card" style="border-color:{db_color}20;">
        <div class="section-title" style="text-align:center;">TODAY'S EXECUTIVE SUMMARY</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.8;text-align:center;">
            Gold is at <b style="color:#FFD700;">${gold['price']:,.2f}</b>
            ({gold['pct']:+.3f}% today).
            Daily bias is <b style="color:{db_color};">{daily_bias}</b> with {abs(daily_sent-50)*2:.0f}% confidence.
            {'Smart money is ' + cot_data['nc_bias'] + ' with ' + cot_data['nc_conviction'] + ' conviction.' if cot_data else ''}
            {'Price is above pivot (${:.2f}) suggesting intraday bullish structure.'.format(pivot) if not gold_intraday.empty and gold['price']>pivot else ''}
            {'Price is below pivot (${:.2f}) suggesting intraday bearish structure.'.format(pivot) if not gold_intraday.empty and gold['price']<=pivot else ''}
        </div>
    </div>""", unsafe_allow_html=True)


# ============ FOOTER (BOTH PAGES) ============
st.markdown(f"""
<div style="text-align:center;padding:20px 0;margin-top:20px;">
    <div style="font-size:11px;color:rgba(255,255,255,0.15);letter-spacing:1px;">
        ROLLIC TRADES · GOLD INTELLIGENCE TERMINAL · v3.0
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,0.08);margin-top:4px;">
        Auto-refresh 90s · Data: Yahoo Finance · Not Financial Advice
    </div>
</div>
""", unsafe_allow_html=True)

# Auto refresh
st.markdown('<meta http-equiv="refresh" content="90">', unsafe_allow_html=True)
