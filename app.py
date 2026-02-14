# ============================================
# 🥇 GOLD TRADING DASHBOARD
# Streamlit Version - AUTO REFRESH!
# ============================================

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="🥇 Gold Trading Dashboard",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# DARK THEME CSS
# ============================================
st.markdown("""
<style>
    /* Dark Background */
    .stApp {
        background-color: #0a0a1a;
    }
    
    /* Header styling */
    .gold-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 15px;
        border: 1px solid #FFD700;
        margin-bottom: 20px;
    }
    .gold-header h1 {
        color: #FFD700 !important;
        font-size: 32px !important;
        margin: 0 !important;
    }
    .gold-header p {
        color: #888 !important;
        margin: 5px 0 0 0 !important;
    }
    
    /* Price Box */
    .price-box {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #1a1a2e, #0d1117);
        border-radius: 15px;
        border: 1px solid rgba(255,215,0,0.3);
        margin-bottom: 20px;
    }
    .price-label {
        color: #FFD700;
        font-size: 14px;
        letter-spacing: 3px;
    }
    .price-value {
        color: #FFD700;
        font-size: 52px;
        font-weight: bold;
        margin: 5px 0;
    }
    .price-change-up {
        color: #00ff88;
        font-size: 22px;
    }
    .price-change-down {
        color: #ff4444;
        font-size: 22px;
    }
    .price-details {
        color: #888;
        font-size: 14px;
    }
    
    /* Signal Cards */
    .signal-card {
        background: #1a1a2e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    
    /* Factor Cards */
    .bearish-card {
        background: rgba(255,0,0,0.08);
        border-left: 4px solid #ff4444;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
    }
    .bullish-card {
        background: rgba(0,255,0,0.08);
        border-left: 4px solid #00ff88;
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
    }
    
    /* Sentiment Bar */
    .sent-bar-container {
        background: #1a1a2e;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Tech Cards */
    .tech-card {
        background: #1a1a2e;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Summary Table */
    .summary-table {
        width: 100%;
        border-collapse: collapse;
    }
    .summary-table th {
        padding: 10px;
        text-align: left;
        color: #888;
        border-bottom: 1px solid #333;
    }
    .summary-table td {
        padding: 10px;
        border-bottom: 1px solid #222;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA FETCHING FUNCTIONS
# ============================================

@st.cache_data(ttl=60)
def get_gold_price():
    """Gold ka live price"""
    try:
        gold = yf.Ticker("GC=F")
        data = gold.history(period="5d")
        if data.empty:
            return None
        current = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2] if len(data) > 1 else current
        ch = current - prev
        return {
            'price': round(current, 2),
            'change': round(ch, 2),
            'pct': round((ch/prev)*100, 3),
            'high': round(data['High'].iloc[-1], 2),
            'low': round(data['Low'].iloc[-1], 2),
            'open': round(data['Open'].iloc[-1], 2),
        }
    except:
        return None

@st.cache_data(ttl=60)
def get_gold_chart(period="3mo"):
    """Gold chart data"""
    try:
        return yf.Ticker("GC=F").history(period=period)
    except:
        return pd.DataFrame()

@st.cache_data(ttl=60)
def get_factor(ticker, name, icon, relation="inverse"):
    """Ek factor ka data"""
    try:
        data = yf.Ticker(ticker).history(period="1mo")
        if data.empty:
            return None
        current = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2] if len(data) > 1 else current
        ch = current - prev
        pct = (ch/prev)*100
        
        week = data['Close'].iloc[-5] if len(data) >= 5 else data['Close'].iloc[0]
        wpct = ((current - week) / week) * 100

        if relation == "inverse":
            if pct > 0.2:
                impact, strength = "bearish", min(abs(pct)*15, 100)
            elif pct < -0.2:
                impact, strength = "bullish", min(abs(pct)*15, 100)
            else:
                impact, strength = "neutral", abs(pct)*5
        else:
            if pct > 0.2:
                impact, strength = "bullish", min(abs(pct)*15, 100)
            elif pct < -0.2:
                impact, strength = "bearish", min(abs(pct)*15, 100)
            else:
                impact, strength = "neutral", abs(pct)*5

        return {
            'name': name, 'icon': icon,
            'value': round(current, 2),
            'change': round(ch, 2),
            'pct': round(pct, 3),
            'wpct': round(wpct, 3),
            'impact': impact,
            'strength': round(min(strength, 100), 1)
        }
    except:
        return None

@st.cache_data(ttl=60)
def get_all_factors():
    """Saare factors"""
    configs = [
        ("DX-Y.NYB", "US Dollar (DXY)", "💵", "inverse"),
        ("^GSPC", "S&P 500", "📊", "inverse"),
        ("^TNX", "10Y Bond Yield", "📜", "inverse"),
        ("^VIX", "VIX Fear Index", "😨", "direct"),
        ("CL=F", "Crude Oil", "🛢️", "direct"),
        ("SI=F", "Silver", "🥈", "direct"),
        ("BTC-USD", "Bitcoin", "₿", "inverse"),
        ("EURUSD=X", "EUR/USD", "💶", "direct"),
    ]
    factors = {}
    for ticker, name, icon, rel in configs:
        key = name.lower().replace(" ","_").replace("(","").replace(")","")
        factors[key] = get_factor(ticker, name, icon, rel)
    return factors

@st.cache_data(ttl=60)
def get_technicals():
    """Technical indicators"""
    try:
        data = yf.Ticker("GC=F").history(period="3mo")
        if data.empty or len(data) < 50:
            return None
        close = data['Close']
        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = (100 - (100 / (1 + rs))).iloc[-1]
        cur = close.iloc[-1]
        return {
            'sma20': round(sma20, 2), 'sma50': round(sma50, 2),
            'rsi': round(rsi, 1),
            'above20': cur > sma20, 'above50': cur > sma50,
            'trend': 'BULLISH' if sma20 > sma50 else 'BEARISH',
            'rsi_sig': 'OVERBOUGHT' if rsi > 70 else ('OVERSOLD' if rsi < 30 else 'NEUTRAL'),
        }
    except:
        return None

@st.cache_data(ttl=300)
def get_correlation():
    """Correlation matrix"""
    try:
        tickers = {'Gold':'GC=F','Silver':'SI=F','DXY':'DX-Y.NYB',
                   'S&P500':'^GSPC','Oil':'CL=F','Bitcoin':'BTC-USD'}
        data = {}
        for name, ticker in tickers.items():
            try:
                d = yf.Ticker(ticker).history(period="3mo")
                if not d.empty:
                    data[name] = d['Close'].pct_change().dropna()
            except:
                continue
        if len(data) >= 3:
            return pd.DataFrame(data).corr()
    except:
        pass
    return None

# ============================================
# MAIN DASHBOARD
# ============================================

def main():
    
    # HEADER
    st.markdown("""
    <div class="gold-header">
        <h1>🥇 GOLD TRADING DASHBOARD</h1>
        <p>Real-Time Factor Analysis | Auto-Refresh Every 60 Seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FETCH DATA
    with st.spinner("📊 Data fetch ho raha hai..."):
        gold = get_gold_price()
        factors = get_all_factors()
        tech = get_technicals()
        chart_data = get_gold_chart("3mo")
        corr = get_correlation()
    
    if gold is None:
        st.error("❌ Gold data nahi mila! Internet check karo ya thodi der baad try karo.")
        return
    
    # Separate factors
    bullish = []
    bearish = []
    neutral_list = []
    for k, f in factors.items():
        if f is None:
            continue
        if f['impact'] == 'bullish':
            bullish.append(f)
        elif f['impact'] == 'bearish':
            bearish.append(f)
        else:
            neutral_list.append(f)
    
    bullish.sort(key=lambda x: x['strength'], reverse=True)
    bearish.sort(key=lambda x: x['strength'], reverse=True)
    
    bt = sum(f['strength'] for f in bullish)
    brt = sum(f['strength'] for f in bearish)
    total = bt + brt
    sentiment = (bt / total * 100) if total > 0 else 50
    
    if sentiment > 65:
        signal, sig_color = "🟢 STRONG BUY", "#00ff88"
    elif sentiment > 55:
        signal, sig_color = "🟢 BUY", "#00cc66"
    elif sentiment < 35:
        signal, sig_color = "🔴 STRONG SELL", "#ff4444"
    elif sentiment < 45:
        signal, sig_color = "🔴 SELL", "#ff6666"
    else:
        signal, sig_color = "🟡 HOLD", "#ffaa00"
    
    # ==========================================
    # GOLD PRICE
    # ==========================================
    arrow = "▲" if gold['change'] >= 0 else "▼"
    pc = "price-change-up" if gold['change'] >= 0 else "price-change-down"
    
    st.markdown(f"""
    <div class="price-box">
        <div class="price-label">GOLD (XAU/USD)</div>
        <div class="price-value">${gold['price']:,.2f}</div>
        <div class="{pc}">
            {arrow} ${abs(gold['change']):,.2f} ({gold['pct']:+.3f}%)
        </div>
        <div class="price-details">
            <span style="color:#00ff88;">H: ${gold['high']:,.2f}</span> &nbsp;|&nbsp;
            <span style="color:#ff4444;">L: ${gold['low']:,.2f}</span> &nbsp;|&nbsp;
            <span style="color:#6ec6ff;">O: ${gold['open']:,.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # SIGNAL ROW
    # ==========================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="signal-card" style="border:1px solid {sig_color};">
            <div style="color:#888; font-size:12px;">SIGNAL</div>
            <div style="color:{sig_color}; font-size:28px; font-weight:bold;">{signal}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sent_color = "#00ff88" if sentiment > 60 else ("#ff4444" if sentiment < 40 else "#ffaa00")
        st.markdown(f"""
        <div class="signal-card">
            <div style="color:#888; font-size:12px;">SENTIMENT SCORE</div>
            <div style="color:{sent_color}; font-size:28px; font-weight:bold;">{sentiment:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="signal-card">
            <div style="color:#888; font-size:12px;">ACTIVE FACTORS</div>
            <div style="font-size:22px;">
                <span style="color:#00ff88;">🟢 {len(bullish)}</span>
                <span style="color:#888;"> vs </span>
                <span style="color:#ff4444;">🔴 {len(bearish)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==========================================
    # SENTIMENT BAR
    # ==========================================
    st.markdown("")
    bw = sentiment
    brw = 100 - sentiment
    
    st.markdown(f"""
    <div class="sent-bar-container">
        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
            <span style="color:#00ff88; font-size:13px;">🟢 Bullish {bw:.0f}%</span>
            <span style="color:#ff4444; font-size:13px;">Bearish {brw:.0f}% 🔴</span>
        </div>
        <div style="background:#333; border-radius:8px; height:28px; display:flex; overflow:hidden;">
            <div style="background:linear-gradient(90deg, #00ff88, #00cc66); width:{bw}%;
                 height:100%; display:flex; align-items:center; justify-content:center;
                 font-size:12px; font-weight:bold; color:#000; border-radius:8px 0 0 8px;">
                {bw:.0f}%
            </div>
            <div style="background:linear-gradient(90deg, #ff6666, #ff4444); width:{brw}%;
                 height:100%; display:flex; align-items:center; justify-content:center;
                 font-size:12px; font-weight:bold; color:#fff; border-radius:0 8px 8px 0;">
                {brw:.0f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # BEARISH (LEFT) | BULLISH (RIGHT)
    # ==========================================
    col_bear, col_bull = st.columns(2)
    
    with col_bear:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(255,0,0,0.05);
             border:1px solid rgba(255,0,0,0.3); border-radius:12px 12px 0 0;">
            <h3 style="color:#ff4444; margin:0;">🔴 BEARISH FACTORS</h3>
            <p style="color:#888; font-size:12px; margin:0;">Gold ko neeche le jaane wale</p>
        </div>
        """, unsafe_allow_html=True)
        
        if bearish:
            for f in bearish:
                st.markdown(f"""
                <div class="bearish-card">
                    <div style="font-size:18px; margin-bottom:4px;">
                        {f['icon']} <b style="color:#fff;">{f['name']}</b>
                    </div>
                    <div style="color:#ccc; font-size:13px;">
                        Value: <b>{f['value']}</b>
                        <span style="color:#ff4444; font-weight:bold;"> ({f['pct']:+.2f}%)</span>
                    </div>
                    <div style="color:#888; font-size:11px; margin-top:2px;">
                        Weekly: {f['wpct']:+.2f}%
                    </div>
                    <div style="margin-top:6px;">
                        <div style="background:#333; border-radius:4px; height:8px;">
                            <div style="background:#ff4444; height:8px; border-radius:4px;
                                 width:{f['strength']}%;"></div>
                        </div>
                        <small style="color:#888;">Impact Strength: {f['strength']:.0f}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:20px; color:#888;">
                ✅ Koi bearish factor active nahi hai
            </div>
            """, unsafe_allow_html=True)
    
    with col_bull:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(0,255,0,0.05);
             border:1px solid rgba(0,255,0,0.3); border-radius:12px 12px 0 0;">
            <h3 style="color:#00ff88; margin:0;">🟢 BULLISH FACTORS</h3>
            <p style="color:#888; font-size:12px; margin:0;">Gold ko upar le jaane wale</p>
        </div>
        """, unsafe_allow_html=True)
        
        if bullish:
            for f in bullish:
                st.markdown(f"""
                <div class="bullish-card">
                    <div style="font-size:18px; margin-bottom:4px;">
                        {f['icon']} <b style="color:#fff;">{f['name']}</b>
                    </div>
                    <div style="color:#ccc; font-size:13px;">
                        Value: <b>{f['value']}</b>
                        <span style="color:#00ff88; font-weight:bold;"> ({f['pct']:+.2f}%)</span>
                    </div>
                    <div style="color:#888; font-size:11px; margin-top:2px;">
                        Weekly: {f['wpct']:+.2f}%
                    </div>
                    <div style="margin-top:6px;">
                        <div style="background:#333; border-radius:4px; height:8px;">
                            <div style="background:#00ff88; height:8px; border-radius:4px;
                                 width:{f['strength']}%;"></div>
                        </div>
                        <small style="color:#888;">Impact Strength: {f['strength']:.0f}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:20px; color:#888;">
                ⚠️ Koi bullish factor active nahi hai
            </div>
            """, unsafe_allow_html=True)
    
    # ==========================================
    # TECHNICAL INDICATORS
    # ==========================================
    st.markdown("---")
    st.markdown('<h3 style="color:#FFD700;">📐 Technical Indicators</h3>', 
                unsafe_allow_html=True)
    
    if tech:
        tc1, tc2, tc3, tc4 = st.columns(4)
        
        trend_color = "#00ff88" if tech['trend'] == "BULLISH" else "#ff4444"
        rsi_color = "#ff4444" if tech['rsi'] > 70 else ("#00ff88" if tech['rsi'] < 30 else "#ffaa00")
        
        with tc1:
            st.markdown(f"""
            <div class="tech-card">
                <div style="color:#888; font-size:12px;">TREND</div>
                <div style="color:{trend_color}; font-size:22px; font-weight:bold;">
                    {'🟢' if tech['trend']=='BULLISH' else '🔴'} {tech['trend']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tc2:
            st.markdown(f"""
            <div class="tech-card">
                <div style="color:#888; font-size:12px;">RSI ({tech['rsi']})</div>
                <div style="color:{rsi_color}; font-size:22px; font-weight:bold;">
                    {tech['rsi_sig']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tc3:
            sma20_icon = "✅" if tech['above20'] else "❌"
            sma20_color = "#00ff88" if tech['above20'] else "#ff4444"
            st.markdown(f"""
            <div class="tech-card">
                <div style="color:#888; font-size:12px;">SMA 20</div>
                <div style="color:#fff; font-size:18px;">${tech['sma20']:,.2f}</div>
                <div style="color:{sma20_color}; font-size:13px;">
                    {sma20_icon} Price {'Above' if tech['above20'] else 'Below'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with tc4:
            sma50_icon = "✅" if tech['above50'] else "❌"
            sma50_color = "#00ff88" if tech['above50'] else "#ff4444"
            st.markdown(f"""
            <div class="tech-card">
                <div style="color:#888; font-size:12px;">SMA 50</div>
                <div style="color:#fff; font-size:18px;">${tech['sma50']:,.2f}</div>
                <div style="color:{sma50_color}; font-size:13px;">
                    {sma50_icon} Price {'Above' if tech['above50'] else 'Below'}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ==========================================
    # GOLD CHART
    # ==========================================
    st.markdown("---")
    st.markdown('<h3 style="color:#FFD700;">📈 Gold Price Chart</h3>', 
                unsafe_allow_html=True)
    
    chart_period = st.selectbox("Chart Period:", 
        ["1mo", "3mo", "6mo", "1y"], index=1,
        format_func=lambda x: {"1mo":"1 Month","3mo":"3 Months",
                               "6mo":"6 Months","1y":"1 Year"}[x])
    
    chart_data = get_gold_chart(chart_period)
    
    if not chart_data.empty:
        fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.03, row_heights=[0.8, 0.2])
        
        fig1.add_trace(go.Candlestick(
            x=chart_data.index, open=chart_data['Open'],
            high=chart_data['High'], low=chart_data['Low'],
            close=chart_data['Close'], name='Gold',
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff4444'), row=1, col=1)
        
        if len(chart_data) >= 20:
            s20 = chart_data['Close'].rolling(20).mean()
            fig1.add_trace(go.Scatter(x=chart_data.index, y=s20,
                name='SMA 20', line=dict(color='#FFD700', width=1.5)), row=1, col=1)
        
        if len(chart_data) >= 50:
            s50 = chart_data['Close'].rolling(50).mean()
            fig1.add_trace(go.Scatter(x=chart_data.index, y=s50,
                name='SMA 50', line=dict(color='#6ec6ff', width=1.5)), row=1, col=1)
        
        vc = ['#00ff88' if c >= o else '#ff4444' 
              for c, o in zip(chart_data['Close'], chart_data['Open'])]
        fig1.add_trace(go.Bar(x=chart_data.index, y=chart_data['Volume'],
            marker_color=vc, opacity=0.5, name='Volume'), row=2, col=1)
        
        fig1.update_layout(template='plotly_dark', height=500,
            xaxis_rangeslider_visible=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10))
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # ==========================================
    # 3 CHARTS ROW
    # ==========================================
    ch1, ch2, ch3 = st.columns(3)
    
    # Gauge
    with ch1:
        st.markdown('<h4 style="color:#FFD700;">🎯 Sentiment Gauge</h4>', 
                    unsafe_allow_html=True)
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number", value=sentiment,
            number={'suffix': '%', 'font': {'size': 30}},
            gauge={'axis': {'range': [0, 100]},
                'bar': {'color': sig_color},
                'steps': [
                    {'range': [0, 20], 'color': 'rgba(255,0,0,0.3)'},
                    {'range': [20, 40], 'color': 'rgba(255,136,0,0.3)'},
                    {'range': [40, 60], 'color': 'rgba(255,255,0,0.3)'},
                    {'range': [60, 80], 'color': 'rgba(136,255,0,0.3)'},
                    {'range': [80, 100], 'color': 'rgba(0,255,0,0.3)'}],
                'threshold': {'line': {'color': 'white', 'width': 3},
                    'thickness': 0.75, 'value': sentiment}}))
        fig2.update_layout(template='plotly_dark', height=250,
            paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=10))
        st.plotly_chart(fig2, use_container_width=True)
    
    # Bar Chart
    with ch2:
        st.markdown('<h4 style="color:#FFD700;">⚖️ Bull vs Bear</h4>', 
                    unsafe_allow_html=True)
        names, vals, cols = [], [], []
        for f in bullish:
            names.append(f['icon'] + ' ' + f['name'][:15])
            vals.append(f['strength'])
            cols.append('#00ff88')
        for f in bearish:
            names.append(f['icon'] + ' ' + f['name'][:15])
            vals.append(-f['strength'])
            cols.append('#ff4444')
        
        if names:
            fig3 = go.Figure(go.Bar(y=names, x=vals, orientation='h',
                marker_color=cols,
                text=[f"{abs(v):.0f}%" for v in vals],
                textposition='auto'))
            fig3.update_layout(template='plotly_dark', height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(zeroline=True, zerolinecolor='rgba(255,255,255,0.3)'))
            st.plotly_chart(fig3, use_container_width=True)
    
    # Heatmap
    with ch3:
        st.markdown('<h4 style="color:#FFD700;">🔥 Correlation</h4>', 
                    unsafe_allow_html=True)
        if corr is not None:
            fig4 = go.Figure(go.Heatmap(
                z=corr.values, x=corr.columns, y=corr.columns,
                colorscale='RdYlGn', zmid=0,
                text=[[f'{v:.2f}' for v in r] for r in corr.values],
                texttemplate='%{text}', textfont={"size": 10}))
            fig4.update_layout(template='plotly_dark', height=250,
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Correlation loading...")
    
    # ==========================================
    # ALL FACTORS TABLE
    # ==========================================
    st.markdown("---")
    st.markdown('<h3 style="color:#FFD700;">📋 All Factors Summary</h3>', 
                unsafe_allow_html=True)
    
    table_html = """
    <table class="summary-table">
        <tr>
            <th>Factor</th>
            <th style="text-align:right;">Value</th>
            <th style="text-align:right;">Daily Change</th>
            <th style="text-align:right;">Weekly</th>
            <th style="text-align:center;">Gold Impact</th>
            <th style="text-align:right;">Strength</th>
        </tr>
    """
    
    for k, f in factors.items():
        if f is None:
            continue
        ic = "#00ff88" if f['impact'] == 'bullish' else (
            "#ff4444" if f['impact'] == 'bearish' else "#888")
        cc = "#00ff88" if f['pct'] > 0 else "#ff4444"
        wc = "#00ff88" if f['wpct'] > 0 else "#ff4444"
        
        table_html += f"""
        <tr>
            <td style="color:#fff;">{f['icon']} {f['name']}</td>
            <td style="text-align:right; color:#fff;">{f['value']}</td>
            <td style="text-align:right; color:{cc};">{f['pct']:+.2f}%</td>
            <td style="text-align:right; color:{wc};">{f['wpct']:+.2f}%</td>
            <td style="text-align:center; color:{ic}; font-weight:bold;">
                {f['impact'].upper()}</td>
            <td style="text-align:right; color:#fff;">{f['strength']:.0f}%</td>
        </tr>
        """
    
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    
    # ==========================================
    # FOOTER
    # ==========================================
    st.markdown("---")
    
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <div style="text-align:center; padding:10px;">
        <p style="color:#FFD700; font-size:13px;">
            🔄 Last Updated: {update_time} | Auto-refresh: 60 seconds
        </p>
        <p style="color:#555; font-size:12px;">
            ⚠️ Educational purpose only. Not financial advice.<br>
            Data Source: Yahoo Finance
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN + AUTO REFRESH
# ============================================
main()

# Auto Refresh - har 60 second
st.markdown("""
<script>
    setTimeout(function(){
        window.location.reload();
    }, 60000);
</script>
""", unsafe_allow_html=True)

# Manual refresh button bhi
if st.sidebar.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ⏰ Auto Refresh")
st.sidebar.markdown("Page har **60 seconds** mein khud refresh hota hai")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Factors Explained")
st.sidebar.markdown("""
- **DXY ↑** = Gold ↓ (Inverse)
- **VIX ↑** = Gold ↑ (Fear = Safe Haven)
- **Oil ↑** = Gold ↑ (Inflation)
- **S&P500 ↑** = Gold ↓ (Risk-On)
- **Yields ↑** = Gold ↓ (Opportunity Cost)
- **Silver ↑** = Gold ↑ (Correlated)
- **Bitcoin ↑** = Gold ↓ (Alternative)
""")
