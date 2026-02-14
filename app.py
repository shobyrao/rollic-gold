import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Gold Intelligence", page_icon="🥇", layout="wide")

# ============ APPLE-STYLE PREMIUM CSS ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background-color: #000000;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
header {visibility: hidden;}

/* Remove streamlit padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Apple Glass Card */
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

/* Factor Card */
.factor-bull {
    background: rgba(48, 209, 88, 0.06);
    border: 1px solid rgba(48, 209, 88, 0.15);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 6px 0;
    transition: all 0.3s ease;
}

.factor-bear {
    background: rgba(255, 69, 58, 0.06);
    border: 1px solid rgba(255, 69, 58, 0.15);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 6px 0;
    transition: all 0.3s ease;
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

/* Signal Badge */
.signal-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Progress Bar Apple Style */
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
    transition: width 0.5s ease;
}

.progress-fill-red {
    background: linear-gradient(90deg, #FF453A, #FF6961);
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* Sentiment Meter */
.meter-container {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.meter-bar {
    height: 8px;
    border-radius: 4px;
    display: flex;
    overflow: hidden;
    background: rgba(255,255,255,0.05);
}

/* Correlation Badge */
.corr-pos {
    color: #30D158;
    font-weight: 700;
    font-size: 15px;
}

.corr-neg {
    color: #FF453A;
    font-weight: 700;
    font-size: 15px;
}

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

/* Metric Mini */
.metric-mini {
    text-align: center;
    padding: 12px;
}

.metric-label {
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}

/* Hide extra streamlit elements */
div[data-testid="stToolbar"] {display: none;}
div[data-testid="stDecoration"] {display: none;}
div[data-testid="stStatusWidget"] {display: none;}

</style>
""", unsafe_allow_html=True)

# ============ DATA FUNCTIONS ============

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
def get_history(ticker, period="3mo"):
    try:
        return yf.Ticker(ticker).history(period=period)
    except:
        return pd.DataFrame()

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
def compute_real_yield():
    """Real Yield = US10Y Nominal - 10Y Breakeven Inflation (T10YIE proxy)"""
    try:
        # US 10Y Nominal
        us10y = yf.Ticker("^TNX").history(period="3mo")
        # TIP ETF as inflation expectation proxy
        tip = yf.Ticker("TIP").history(period="3mo")

        if us10y.empty: return None

        nom = us10y['Close'].iloc[-1]
        nom_prev = us10y['Close'].iloc[-2] if len(us10y)>1 else nom

        # Approximate breakeven: 10Y nominal - real yield
        # Using TIP changes as proxy for inflation expectations
        if not tip.empty:
            tip_cur = tip['Close'].iloc[-1]
            tip_prev = tip['Close'].iloc[-2] if len(tip)>1 else tip_cur
            tip_pct = ((tip_cur - tip_prev)/tip_prev)*100
            # Estimate breakeven ~2.3% base + TIP movement
            breakeven = 2.3 + (tip_pct * 0.1)
        else:
            breakeven = 2.3

        real_yield = nom - breakeven
        real_prev = nom_prev - breakeven
        ry_change = real_yield - real_prev

        # Weekly
        nom_w = us10y['Close'].iloc[-5] if len(us10y)>=5 else us10y['Close'].iloc[0]
        real_w = nom_w - breakeven
        ry_wpct = real_yield - real_w

        return {
            'val': round(real_yield, 3),
            'nominal': round(nom, 3),
            'breakeven': round(breakeven, 3),
            'change': round(ry_change, 4),
            'pct': round(ry_change, 3),
            'wpct': round(ry_wpct, 3),
            'nom_series': us10y['Close']
        }
    except:
        return None

@st.cache_data(ttl=300)
def compute_correlations():
    """Gold vs major factors ki 90-day correlation"""
    try:
        tickers = {
            'Gold':'GC=F',
            'DXY':'DX-Y.NYB',
            'US10Y':'^TNX',
            'S&P500':'^GSPC',
            'Silver':'SI=F',
            'Oil':'CL=F',
            'VIX':'^VIX',
            'EUR/USD':'EURUSD=X',
            'TIP':'TIP'
        }
        data = {}
        for name, tk in tickers.items():
            try:
                d = yf.Ticker(tk).history(period="3mo")
                if not d.empty:
                    data[name] = d['Close'].pct_change().dropna()
            except:
                continue
        if len(data) < 3: return None
        df = pd.DataFrame(data)
        return df.corr()
    except:
        return None

# ============ INSTITUTIONAL LOGIC ============

def analyze_factor(name, data, relation, weight,
                   explanation_bull, explanation_bear):
    """
    Institutional grade factor analysis
    relation: inverse / direct
    weight: 0.0 - 1.0 importance
    """
    if data is None:
        return None

    pct = data['pct']
    wpct = data['wpct']

    # Multi-timeframe scoring
    daily_score = 0
    weekly_score = 0

    threshold_low = 0.15
    threshold_high = 1.0

    if relation == "inverse":
        daily_score = -pct
        weekly_score = -wpct
    else:
        daily_score = pct
        weekly_score = wpct

    # Combined score with weekly having more weight
    combined = (daily_score * 0.3) + (weekly_score * 0.7)

    # Normalize to strength 0-100
    strength = min(abs(combined) * 12, 100)

    # Determine impact
    if combined > 0.3:
        impact = "BULLISH"
        explanation = explanation_bull
    elif combined < -0.3:
        impact = "BEARISH"
        explanation = explanation_bear
    else:
        impact = "NEUTRAL"
        explanation = "Currently not significantly impacting gold"

    weighted_strength = strength * weight

    return {
        'name': name,
        'val': data['val'],
        'pct': pct,
        'wpct': wpct,
        'mpct': data.get('mpct', 0),
        'impact': impact,
        'strength': round(strength, 1),
        'weighted': round(weighted_strength, 1),
        'weight': weight,
        'explanation': explanation,
        'relation': relation
    }

# ============ MAIN APP ============

def main():

    # Header
    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;">
        <div style="font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:3px;
             text-transform:uppercase;margin-bottom:4px;">INSTITUTIONAL GRADE</div>
        <div style="font-size:28px;font-weight:700;color:#FFD700;letter-spacing:-0.5px;">
            Gold Intelligence Terminal</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.25);margin-top:4px;">
            Multi-Factor Analysis Engine · {datetime.now().strftime('%d %b %Y · %H:%M UTC')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ============ FETCH ALL DATA ============
    with st.spinner(""):
        gold = get_price("GC=F")
        if gold is None:
            st.error("Market data unavailable. Please retry.")
            st.stop()

        # Core Factors Data
        dxy_data = get_factor_data("DX-Y.NYB", "3mo")
        us10y_data = get_factor_data("^TNX", "3mo")
        real_yield = compute_real_yield()
        sp500_data = get_factor_data("^GSPC", "3mo")
        vix_data = get_factor_data("^VIX", "3mo")
        oil_data = get_factor_data("CL=F", "3mo")
        silver_data = get_factor_data("SI=F", "3mo")
        eurusd_data = get_factor_data("EURUSD=X", "3mo")
        copper_data = get_factor_data("HG=F", "3mo")
        tnx5_data = get_factor_data("^FVX", "3mo")
        jpy_data = get_factor_data("JPY=X", "3mo")
        gld_data = get_factor_data("GLD", "3mo")

        corr_matrix = compute_correlations()

    # ============ ANALYZE FACTORS (INSTITUTIONAL LOGIC) ============
    factors = []

    # 1. DXY - THE #1 FACTOR
    f = analyze_factor(
        "US Dollar Index (DXY)", dxy_data, "inverse", 0.25,
        "Dollar weakness = Gold priced in USD becomes cheaper for foreign buyers → Demand ↑",
        "Dollar strength = Gold becomes expensive globally → Demand ↓ → Price pressure"
    )
    if f: f['icon']='💵'; factors.append(f)

    # 2. REAL YIELD - #2 FACTOR
    if real_yield:
        ry_impact = "BEARISH" if real_yield['val'] > 1.5 else (
            "BULLISH" if real_yield['val'] < 0.5 else "NEUTRAL")
        ry_strength = abs(real_yield['val'] - 1.0) * 30
        ry_strength = min(ry_strength, 100)

        if real_yield['change'] > 0.02:
            ry_impact = "BEARISH"
            ry_strength = max(ry_strength, abs(real_yield['change']) * 200)
        elif real_yield['change'] < -0.02:
            ry_impact = "BULLISH"
            ry_strength = max(ry_strength, abs(real_yield['change']) * 200)

        ry_strength = min(ry_strength, 100)

        if ry_impact == "BULLISH":
            ry_exp = f"Real Yield falling ({real_yield['val']:.2f}%) → Gold opportunity cost decreasing → Institutional allocation ↑"
        elif ry_impact == "BEARISH":
            ry_exp = f"Real Yield rising ({real_yield['val']:.2f}%) → Bonds more attractive vs zero-yield gold → Capital outflow from gold"
        else:
            ry_exp = f"Real Yield at {real_yield['val']:.2f}% → Neutral zone for gold allocation"

        factors.append({
            'name': 'Real Yield (US10Y − Breakeven)',
            'icon': '📐',
            'val': real_yield['val'],
            'pct': real_yield['pct'],
            'wpct': real_yield['wpct'],
            'mpct': 0,
            'impact': ry_impact,
            'strength': round(ry_strength, 1),
            'weighted': round(ry_strength * 0.22, 1),
            'weight': 0.22,
            'explanation': ry_exp,
            'relation': 'inverse'
        })

    # 3. US 10Y NOMINAL
    f = analyze_factor(
        "US 10Y Treasury Yield", us10y_data, "inverse", 0.15,
        "Yields falling → Lower opportunity cost for holding gold → Institutional buying ↑",
        "Yields rising → Higher opportunity cost → Money moves from gold to bonds"
    )
    if f: f['icon']='📜'; factors.append(f)

    # 4. S&P 500
    f = analyze_factor(
        "S&P 500 (Risk Sentiment)", sp500_data, "inverse", 0.10,
        "Equities declining → Risk-off mode → Flight to safety → Gold demand ↑",
        "Equities rallying → Risk-on sentiment → Gold less attractive as safe haven"
    )
    if f: f['icon']='📊'; factors.append(f)

    # 5. VIX
    f = analyze_factor(
        "VIX (Volatility / Fear)", vix_data, "direct", 0.08,
        "Fear rising → Hedging demand ↑ → Institutional gold allocation increases",
        "Low volatility → Complacency → Less need for gold as portfolio hedge"
    )
    if f: f['icon']='😨'; factors.append(f)

    # 6. CRUDE OIL
    f = analyze_factor(
        "Crude Oil (Inflation Input)", oil_data, "direct", 0.08,
        "Oil rising → Inflation expectations ↑ → Gold as inflation hedge becomes attractive",
        "Oil falling → Deflationary signal → Less need for inflation protection via gold"
    )
    if f: f['icon']='🛢️'; factors.append(f)

    # 7. SILVER (Confirmation)
    f = analyze_factor(
        "Silver (Precious Metals Trend)", silver_data, "direct", 0.05,
        "Silver confirming strength → Broad precious metals bid → Gold sentiment positive",
        "Silver weakness → Precious metals sector under pressure → Gold may follow"
    )
    if f: f['icon']='🥈'; factors.append(f)

    # 8. EUR/USD
    f = analyze_factor(
        "EUR/USD (Dollar Proxy)", eurusd_data, "direct", 0.04,
        "Euro strengthening vs Dollar → Dollar weakness confirmed → Gold bullish",
        "Euro weakening → Dollar strength confirmed from FX side → Gold bearish"
    )
    if f: f['icon']='💶'; factors.append(f)

    # 9. COPPER (Economic Health)
    f = analyze_factor(
        "Copper (Dr. Copper / Economy)", copper_data, "direct", 0.04,
        "Copper rising → Economic demand strong → Can support commodity complex including gold",
        "Copper falling → Economic slowdown signal → Mixed for gold (flight to safety vs deflation)"
    )
    if f: f['icon']='🔶'; factors.append(f)

    # 10. 5Y YIELD (Yield Curve Signal)
    f = analyze_factor(
        "US 5Y Treasury Yield", tnx5_data, "inverse", 0.04,
        "5Y yields falling → Rate cut expectations increasing → Bullish for gold",
        "5Y yields rising → Tighter policy expected → Bearish for gold"
    )
    if f: f['icon']='📉'; factors.append(f)

    # 11. JPY (Safe Haven Peer)
    if jpy_data:
        # JPY ticker is USD/JPY, so inverse logic
        f = analyze_factor(
            "USD/JPY (Safe Haven Peer)", jpy_data, "inverse", 0.03,
            "Yen strengthening (USD/JPY ↓) → Risk-off across markets → Gold safe haven demand ↑",
            "Yen weakening (USD/JPY ↑) → Risk-on → Less safe haven demand for gold"
        )
        if f: f['icon']='🇯🇵'; factors.append(f)

    # 12. GLD ETF Flows (Proxy)
    f = analyze_factor(
        "GLD ETF (Institutional Flow)", gld_data, "direct", 0.03,
        "GLD rising → Institutional inflows into gold ETFs → Smart money buying",
        "GLD falling → Institutional outflows → Smart money reducing gold exposure"
    )
    if f: f['icon']='🏦'; factors.append(f)

    # ============ SEPARATE & SCORE ============
    bull = sorted([f for f in factors if f['impact']=='BULLISH'],
                  key=lambda x: x['weighted'], reverse=True)
    bear = sorted([f for f in factors if f['impact']=='BEARISH'],
                  key=lambda x: x['weighted'], reverse=True)
    neut = [f for f in factors if f['impact']=='NEUTRAL']

    bt = sum(f['weighted'] for f in bull)
    brt = sum(f['weighted'] for f in bear)
    tot = bt + brt
    sent = (bt / tot * 100) if tot > 0 else 50

    # Institutional Signal Logic
    if sent > 72: sig,sc,sb = "STRONG BUY","#30D158","rgba(48,209,88,0.15)"
    elif sent > 58: sig,sc,sb = "BUY","#34C759","rgba(52,199,89,0.12)"
    elif sent < 28: sig,sc,sb = "STRONG SELL","#FF453A","rgba(255,69,58,0.15)"
    elif sent < 42: sig,sc,sb = "SELL","#FF6961","rgba(255,105,97,0.12)"
    else: sig,sc,sb = "HOLD","#FFD60A","rgba(255,214,10,0.12)"

    confidence = abs(sent - 50) * 2

    # ============ GOLD PRICE DISPLAY ============
    ar = "▲" if gold['change'] >= 0 else "▼"
    pc_class = "price-change-pos" if gold['change'] >= 0 else "price-change-neg"

    st.markdown(f"""
    <div class="glass-card-gold">
        <div class="section-title" style="text-align:center;">GOLD SPOT · XAU/USD</div>
        <div class="price-main">${gold['price']:,.2f}</div>
        <div class="{pc_class}" style="margin-top:6px;">
            {ar} ${abs(gold['change']):,.2f} ({gold['pct']:+.3f}%)
        </div>
        <div style="text-align:center;margin-top:12px;font-size:12px;color:rgba(255,255,255,0.3);">
            Open ${gold['open']:,.2f} &nbsp;·&nbsp;
            High <span style="color:#30D158;">${gold['high']:,.2f}</span> &nbsp;·&nbsp;
            Low <span style="color:#FF453A;">${gold['low']:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ SIGNAL + METRICS ROW ============
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(f"""
        <div class="glass-card" style="border-color:{sc}20;">
            <div class="metric-label">SIGNAL</div>
            <div style="color:{sc};font-size:22px;font-weight:700;text-align:center;">{sig}</div>
        </div>""", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">SENTIMENT</div>
            <div class="metric-value" style="text-align:center;color:{sc};">{sent:.1f}<span style="font-size:14px;color:rgba(255,255,255,0.3);">%</span></div>
        </div>""", unsafe_allow_html=True)

    with s3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">CONFIDENCE</div>
            <div class="metric-value" style="text-align:center;">{confidence:.0f}<span style="font-size:14px;color:rgba(255,255,255,0.3);">%</span></div>
        </div>""", unsafe_allow_html=True)

    with s4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">ACTIVE FACTORS</div>
            <div style="text-align:center;font-size:18px;font-weight:600;">
                <span style="color:#30D158;">{len(bull)}↑</span>
                <span style="color:rgba(255,255,255,0.2);"> · </span>
                <span style="color:#FF453A;">{len(bear)}↓</span>
                <span style="color:rgba(255,255,255,0.2);"> · </span>
                <span style="color:rgba(255,255,255,0.3);">{len(neut)}−</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ============ SENTIMENT METER ============
    st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="font-size:12px;color:#30D158;font-weight:500;">Bullish {sent:.0f}%</span>
            <span style="font-size:11px;color:rgba(255,255,255,0.2);">MARKET BIAS</span>
            <span style="font-size:12px;color:#FF453A;font-weight:500;">Bearish {100-sent:.0f}%</span>
        </div>
        <div class="meter-bar">
            <div style="width:{sent}%;background:linear-gradient(90deg,#30D158,#34C759);height:100%;border-radius:4px 0 0 4px;transition:width 0.8s;"></div>
            <div style="width:{100-sent}%;background:linear-gradient(90deg,#FF453A,#FF6961);height:100%;border-radius:0 4px 4px 0;transition:width 0.8s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ BEARISH | BULLISH FACTORS ============
    col_bear, col_bull = st.columns(2)

    with col_bear:
        st.markdown(f"""
        <div class="section-title" style="text-align:center;color:#FF453A;">
            ● BEARISH FACTORS ({len(bear)})
        </div>""", unsafe_allow_html=True)

        if bear:
            for f in bear:
                chg_color = "#FF453A" if f['pct'] < 0 else "#30D158"
                st.markdown(f"""
                <div class="factor-bear">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div class="factor-name">{f['icon']} {f['name']}</div>
                            <div class="factor-detail">
                                Daily <span style="color:{chg_color};font-weight:600;">{f['pct']:+.2f}%</span>
                                &nbsp;·&nbsp; Weekly <span style="color:{'#FF453A' if f['wpct']<0 else '#30D158'};font-weight:600;">{f['wpct']:+.2f}%</span>
                                &nbsp;·&nbsp; Weight: {f['weight']*100:.0f}%
                            </div>
                        </div>
                        <div class="factor-value">{f['val']}</div>
                    </div>
                    <div class="factor-detail" style="margin-top:6px;font-style:italic;">
                        💡 {f['explanation']}
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill-red" style="width:{f['strength']}%;"></div>
                    </div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.25);margin-top:4px;">
                        Weighted Impact: {f['weighted']:.1f} · Raw Strength: {f['strength']:.0f}%
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="factor-neutral" style="text-align:center;">
                <div style="color:rgba(255,255,255,0.4);font-size:13px;">No bearish factors active</div>
            </div>""", unsafe_allow_html=True)

    with col_bull:
        st.markdown(f"""
        <div class="section-title" style="text-align:center;color:#30D158;">
            ● BULLISH FACTORS ({len(bull)})
        </div>""", unsafe_allow_html=True)

        if bull:
            for f in bull:
                chg_color = "#30D158" if f['pct'] > 0 else "#FF453A"
                st.markdown(f"""
                <div class="factor-bull">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div class="factor-name">{f['icon']} {f['name']}</div>
                            <div class="factor-detail">
                                Daily <span style="color:{chg_color};font-weight:600;">{f['pct']:+.2f}%</span>
                                &nbsp;·&nbsp; Weekly <span style="color:{'#30D158' if f['wpct']>0 else '#FF453A'};font-weight:600;">{f['wpct']:+.2f}%</span>
                                &nbsp;·&nbsp; Weight: {f['weight']*100:.0f}%
                            </div>
                        </div>
                        <div class="factor-value">{f['val']}</div>
                    </div>
                    <div class="factor-detail" style="margin-top:6px;font-style:italic;">
                        💡 {f['explanation']}
                    </div>
                    <div class="progress-track">
                        <div class="progress-fill-green" style="width:{f['strength']}%;"></div>
                    </div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.25);margin-top:4px;">
                        Weighted Impact: {f['weighted']:.1f} · Raw Strength: {f['strength']:.0f}%
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="factor-neutral" style="text-align:center;">
                <div style="color:rgba(255,255,255,0.4);font-size:13px;">No bullish factors active</div>
            </div>""", unsafe_allow_html=True)

    # ============ REAL YIELD SPOTLIGHT ============
    if real_yield:
        st.markdown("---")
        ry_col1, ry_col2, ry_col3 = st.columns(3)

        with ry_col1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">REAL YIELD</div>
                <div class="metric-value" style="text-align:center;color:{'#FF453A' if real_yield['val']>1 else '#30D158'};">
                    {real_yield['val']:.3f}%
                </div>
                <div style="text-align:center;font-size:11px;color:rgba(255,255,255,0.3);margin-top:4px;">
                    US10Y − Breakeven Inflation
                </div>
            </div>""", unsafe_allow_html=True)

        with ry_col2:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">10Y NOMINAL</div>
                <div class="metric-value" style="text-align:center;">{real_yield['nominal']:.3f}%</div>
                <div style="text-align:center;font-size:11px;color:rgba(255,255,255,0.3);margin-top:4px;">
                    US Treasury 10-Year
                </div>
            </div>""", unsafe_allow_html=True)

        with ry_col3:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">BREAKEVEN INFLATION</div>
                <div class="metric-value" style="text-align:center;">{real_yield['breakeven']:.3f}%</div>
                <div style="text-align:center;font-size:11px;color:rgba(255,255,255,0.3);margin-top:4px;">
                    10Y Inflation Expectation (Est.)
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">📐 Real Yield Framework</div>
            <div class="insight-text">
                Real Yield = Nominal Yield − Inflation Expectation. Gold ka sabse important institutional-level
                factor yeh hai. Jab real yields NEGATIVE ya FALLING hoti hain, gold ka opportunity cost
                zero ho jata hai aur institutions gold allocate karti hain. Jab real yields POSITIVE aur
                RISING hoti hain, bonds gold se zyada attractive ho jaati hain.
            </div>
        </div>""", unsafe_allow_html=True)

    # ============ CORRELATION MATRIX ============
    st.markdown("---")
    st.markdown('<div class="section-title">CORRELATION ANALYSIS · 90 DAY</div>', unsafe_allow_html=True)

    if corr_matrix is not None and 'Gold' in corr_matrix.columns:
        gold_corr = corr_matrix['Gold'].drop('Gold').sort_values()

        corr_html = '<div class="glass-card"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">'

        for asset, corr_val in gold_corr.items():
            corr_class = "corr-pos" if corr_val > 0 else "corr-neg"
            bar_color = "#30D158" if corr_val > 0 else "#FF453A"
            bar_width = abs(corr_val) * 100

            meaning = ""
            if asset == "DXY":
                meaning = "Inverse → Dollar ↑ = Gold ↓"
            elif asset == "US10Y":
                meaning = "Inverse → Yields ↑ = Gold ↓"
            elif asset == "S&P500":
                meaning = "Weak Inverse → Stocks ↑ = Gold neutral/↓"
            elif asset == "Silver":
                meaning = "Strong Positive → Precious metals move together"
            elif asset == "Oil":
                meaning = "Positive → Inflation link"
            elif asset == "VIX":
                meaning = "Positive → Fear = Gold safe haven"
            elif asset == "EUR/USD":
                meaning = "Positive → Euro ↑ = Dollar ↓ = Gold ↑"
            elif asset == "TIP":
                meaning = "Positive → Inflation protection demand"

            corr_html += f"""
            <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:13px;color:#fff;font-weight:500;">{asset}</span>
                    <span class="{corr_class}">{corr_val:+.3f}</span>
                </div>
                <div style="background:rgba(255,255,255,0.05);height:3px;border-radius:2px;margin:6px 0;">
                    <div style="background:{bar_color};height:100%;width:{bar_width}%;border-radius:2px;"></div>
                </div>
                <div style="font-size:10px;color:rgba(255,255,255,0.3);">{meaning}</div>
            </div>"""

        corr_html += '</div></div>'
        st.markdown(corr_html, unsafe_allow_html=True)

    # ============ INSTITUTIONAL INSIGHTS ============
    st.markdown("---")
    st.markdown('<div class="section-title">INSTITUTIONAL INSIGHTS</div>', unsafe_allow_html=True)

    insights = []

    # DXY insight
    if dxy_data:
        if dxy_data['wpct'] < -1:
            insights.append(("Dollar Weakness Trend","DXY weekly change "
                f"{dxy_data['wpct']:+.2f}% — Sustained dollar weakness is the strongest "
                "single driver for gold. Foreign buyers get better value, "
                "and central bank reserves diversification accelerates."))
        elif dxy_data['wpct'] > 1:
            insights.append(("Dollar Strength Headwind","DXY weekly change "
                f"{dxy_data['wpct']:+.2f}% — Strong dollar creates significant "
                "headwind for gold. Watch for DXY exhaustion signals for gold entry."))

    # Real yield insight
    if real_yield:
        if real_yield['val'] < 0:
            insights.append(("Negative Real Yields",
                f"Real yield at {real_yield['val']:.2f}% (NEGATIVE) — "
                "Historically, negative real yields are the most powerful institutional "
                "signal for gold accumulation. Money loses purchasing power in bonds."))
        elif real_yield['val'] > 2:
            insights.append(("High Real Yields Warning",
                f"Real yield at {real_yield['val']:.2f}% — High real yields create "
                "strong competition from bonds. Gold typically underperforms when "
                "real yields are above 2%. Watch for reversal."))

    # VIX insight
    if vix_data:
        if vix_data['val'] > 25:
            insights.append(("Elevated Fear Level",
                f"VIX at {vix_data['val']:.1f} — Above 25 signals significant market stress. "
                "Gold typically benefits from flight-to-safety flows during high-VIX "
                "environments. Portfolio hedging demand increases."))
        elif vix_data['val'] < 14:
            insights.append(("Extreme Complacency",
                f"VIX at {vix_data['val']:.1f} — Extremely low fear. Markets may be "
                "underpricing risk. Gold allocation typically low during complacency, "
                "but historically these periods precede volatility spikes."))

    # Gold/Silver ratio insight
    if gold and silver_data:
        gsr = gold['price'] / silver_data['val'] if silver_data['val'] > 0 else 0
        if gsr > 85:
            insights.append(("Gold/Silver Ratio Elevated",
                f"Gold/Silver ratio at {gsr:.1f}x — Above 85x historically signals "
                "silver undervaluation OR extreme risk-off. If ratio mean-reverts, "
                "silver could outperform gold. Watch for breakout."))
        elif gsr < 70:
            insights.append(("Gold/Silver Ratio Compressed",
                f"Gold/Silver ratio at {gsr:.1f}x — Below 70x signals industrial "
                "demand strength and precious metals sector health."))

    # Yield curve
    if us10y_data and tnx5_data:
        spread = us10y_data['val'] - tnx5_data['val']
        if spread < 0:
            insights.append(("Yield Curve Inversion Signal",
                f"10Y-5Y spread at {spread:.3f}% (INVERTED) — Curve inversion "
                "historically precedes recession. Gold benefits from recession fears "
                "and subsequent rate cuts."))

    # Oil inflation insight
    if oil_data and oil_data['wpct'] > 5:
        insights.append(("Oil-Driven Inflation Risk",
            f"Oil weekly change {oil_data['wpct']:+.2f}% — Rapid oil price increase "
            "feeds into CPI. If inflation expectations rise faster than nominal yields, "
            "real yields fall → Bullish for gold via inflation channel."))

    for title, text in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🔍 {title}</div>
            <div class="insight-text">{text}</div>
        </div>""", unsafe_allow_html=True)

    if not insights:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">📊 Markets in Equilibrium</div>
            <div class="insight-text">No extreme readings detected across monitored factors.
            Gold likely to trade within range. Watch for catalyst-driven breakouts.</div>
        </div>""", unsafe_allow_html=True)

    # ============ FACTOR IMPACT CHART ============
    st.markdown("---")
    st.markdown('<div class="section-title">FACTOR IMPACT VISUALIZATION</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Weighted Impact Bar
        all_sorted = sorted(factors, key=lambda x: x['weighted']
            if x['impact']=='BULLISH' else -x['weighted'])

        names_c = []
        vals_c = []
        cols_c = []
        for f in factors:
            names_c.append(f['icon']+' '+f['name'][:22])
            if f['impact'] == 'BULLISH':
                vals_c.append(f['weighted'])
                cols_c.append('#30D158')
            elif f['impact'] == 'BEARISH':
                vals_c.append(-f['weighted'])
                cols_c.append('#FF453A')
            else:
                vals_c.append(0)
                cols_c.append('rgba(255,255,255,0.15)')

        fig_bar = go.Figure(go.Bar(
            y=names_c, x=vals_c, orientation='h',
            marker_color=cols_c,
            text=[f"{abs(v):.1f}" for v in vals_c],
            textposition='auto',
            textfont=dict(size=10, color='white')
        ))
        fig_bar.update_layout(
            template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=40, b=10),
            title=dict(text='Weighted Impact Score',
                      font=dict(color='#FFD700', size=13)),
            xaxis=dict(zeroline=True,
                      zerolinecolor='rgba(255,255,255,0.1)',
                      gridcolor='rgba(255,255,255,0.03)',
                      title='← Bearish · Bullish →'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.03)'),
            font=dict(size=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sent,
            number={'suffix':'%', 'font':{'size':36, 'color':'white'}},
            gauge={
                'axis':{'range':[0,100], 'tickcolor':'rgba(255,255,255,0.2)'},
                'bar':{'color':sc, 'thickness':0.3},
                'bgcolor':'rgba(255,255,255,0.03)',
                'borderwidth':0,
                'steps':[
                    {'range':[0,20],'color':'rgba(255,69,58,0.2)'},
                    {'range':[20,40],'color':'rgba(255,105,97,0.15)'},
                    {'range':[40,60],'color':'rgba(255,214,10,0.1)'},
                    {'range':[60,80],'color':'rgba(52,199,89,0.15)'},
                    {'range':[80,100],'color':'rgba(48,209,88,0.2)'}
                ],
                'threshold':{
                    'line':{'color':'white','width':2},
                    'thickness':0.8, 'value':sent
                }
            }
        ))
        fig_gauge.update_layout(
            template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=30, t=50, b=10),
            title=dict(text='Sentiment Gauge',
                      font=dict(color='#FFD700', size=13)),
            font=dict(color='white')
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ============ FACTORS TABLE ============
    st.markdown("---")
    st.markdown('<div class="section-title">ALL FACTORS · DETAILED VIEW</div>', unsafe_allow_html=True)

    if factors:
        table_data = []
        for f in sorted(factors, key=lambda x: x['weighted'], reverse=True):
            table_data.append({
                'Factor': f"{f['icon']} {f['name']}",
                'Value': f['val'],
                'Daily': f"{f['pct']:+.2f}%",
                'Weekly': f"{f['wpct']:+.2f}%",
                'Impact': f['impact'],
                'Strength': f"{f['strength']:.0f}%",
                'Weight': f"{f['weight']*100:.0f}%",
                'Weighted': f"{f['weighted']:.1f}",
            })
        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True,
            hide_index=True
        )

    # ============ METHODOLOGY ============
    with st.expander("📖 Methodology & Factor Weights"):
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);font-size:13px;line-height:1.8;">

        **Factor Weighting System:**
        | Factor | Weight | Rationale |
        |--------|--------|-----------|
        | DXY (US Dollar) | 25% | Primary pricing currency, strongest inverse correlation |
        | Real Yield | 22% | Institutional benchmark for gold allocation decisions |
        | US 10Y Nominal | 15% | Opportunity cost of holding zero-yield gold |
        | S&P 500 | 10% | Risk sentiment indicator |
        | VIX | 8% | Fear/hedging demand proxy |
        | Crude Oil | 8% | Inflation expectations input |
        | Silver | 5% | Precious metals sector confirmation |
        | EUR/USD | 4% | Dollar strength cross-validation |
        | Copper | 4% | Economic health indicator |
        | 5Y Yield | 4% | Rate policy expectations |
        | USD/JPY | 3% | Safe haven peer confirmation |
        | GLD ETF | 3% | Institutional flow proxy |

        **Scoring Logic:**
        - Daily change (30% weight) + Weekly change (70% weight) = Combined score
        - Multi-timeframe approach reduces noise from single-day moves
        - Weekly trend more reliable for directional bias

        **Real Yield Calculation:**
        - Real Yield = US 10Y Nominal Yield − 10Y Breakeven Inflation Rate
        - Breakeven estimated using TIP ETF movements as proxy
        - Negative real yield = Strongest institutional gold buy signal

        </div>
        """, unsafe_allow_html=True)

    # ============ FOOTER ============
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0;margin-top:20px;">
        <div style="font-size:11px;color:rgba(255,255,255,0.15);letter-spacing:1px;">
            GOLD INTELLIGENCE TERMINAL · v2.0
        </div>
        <div style="font-size:10px;color:rgba(255,255,255,0.1);margin-top:4px;">
            Auto-refresh 90s · Data: Yahoo Finance · Not Financial Advice
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============ RUN ============
main()

# Auto refresh
st.markdown('<meta http-equiv="refresh" content="90">', unsafe_allow_html=True)
