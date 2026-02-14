import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gold Dashboard", page_icon="🥇", layout="wide")

st.markdown("""
<style>
.stApp {background-color: #0a0a1a;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_price(ticker):
    try:
        d = yf.Ticker(ticker).history(period="5d")
        if d.empty:
            return None
        c = d['Close'].iloc[-1]
        p = d['Close'].iloc[-2] if len(d)>1 else c
        return {'price':round(c,2),'change':round(c-p,2),
                'pct':round(((c-p)/p)*100,3),
                'high':round(d['High'].iloc[-1],2),
                'low':round(d['Low'].iloc[-1],2)}
    except:
        return None

@st.cache_data(ttl=120)
def get_factor(ticker, name, icon, rel):
    try:
        d = yf.Ticker(ticker).history(period="1mo")
        if d.empty:
            return None
        c = d['Close'].iloc[-1]
        p = d['Close'].iloc[-2] if len(d)>1 else c
        pct = ((c-p)/p)*100
        w = d['Close'].iloc[-5] if len(d)>=5 else d['Close'].iloc[0]
        wpct = ((c-w)/w)*100

        if rel=="inverse":
            if pct>0.2: impact,s = "BEARISH",min(abs(pct)*15,100)
            elif pct<-0.2: impact,s = "BULLISH",min(abs(pct)*15,100)
            else: impact,s = "NEUTRAL",abs(pct)*5
        else:
            if pct>0.2: impact,s = "BULLISH",min(abs(pct)*15,100)
            elif pct<-0.2: impact,s = "BEARISH",min(abs(pct)*15,100)
            else: impact,s = "NEUTRAL",abs(pct)*5

        return {'name':name,'icon':icon,'val':round(c,2),
                'pct':round(pct,3),'wpct':round(wpct,3),
                'impact':impact,'str':round(min(s,100),1)}
    except:
        return None

# ============ HEADER ============
st.markdown("""
<div style="text-align:center;padding:15px;background:linear-gradient(135deg,#1a1a2e,#16213e);
border-radius:12px;border:1px solid #FFD700;margin-bottom:15px;">
<h1 style="color:#FFD700;margin:0;">🥇 GOLD TRADING DASHBOARD</h1>
<p style="color:#888;margin:5px 0 0 0;">Real-Time Factor Analysis</p>
</div>
""", unsafe_allow_html=True)

# ============ GOLD PRICE ============
gold = get_price("GC=F")

if gold is None:
    st.error("❌ Gold data nahi mila. Internet check karo!")
    st.stop()

ar = "▲" if gold['change']>=0 else "▼"
pc = "#00ff88" if gold['change']>=0 else "#ff4444"

st.markdown(f"""
<div style="text-align:center;padding:20px;background:linear-gradient(135deg,#1a1a2e,#0d1117);
border-radius:12px;border:1px solid rgba(255,215,0,0.3);margin-bottom:15px;">
<div style="color:#FFD700;font-size:13px;letter-spacing:3px;">GOLD (XAU/USD)</div>
<div style="color:#FFD700;font-size:48px;font-weight:bold;">${gold['price']:,.2f}</div>
<div style="color:{pc};font-size:20px;">{ar} ${abs(gold['change']):,.2f} ({gold['pct']:+.3f}%)</div>
<div style="color:#888;font-size:13px;">
<span style="color:#00ff88;">H: ${gold['high']:,.2f}</span> |
<span style="color:#ff4444;">L: ${gold['low']:,.2f}</span>
</div></div>
""", unsafe_allow_html=True)

# ============ FACTORS ============
configs = [
    ("DX-Y.NYB","US Dollar (DXY)","💵","inverse"),
    ("^GSPC","S&P 500","📊","inverse"),
    ("^TNX","10Y Bond Yield","📜","inverse"),
    ("^VIX","VIX Fear Index","😨","direct"),
    ("CL=F","Crude Oil","🛢️","direct"),
    ("SI=F","Silver","🥈","direct"),
    ("BTC-USD","Bitcoin","₿","inverse"),
    ("EURUSD=X","EUR/USD","💶","direct"),
]

with st.spinner("📊 Factors load ho rahe hain..."):
    all_f = []
    for t,n,i,r in configs:
        f = get_factor(t,n,i,r)
        if f: all_f.append(f)

bull = sorted([f for f in all_f if f['impact']=='BULLISH'], key=lambda x:x['str'], reverse=True)
bear = sorted([f for f in all_f if f['impact']=='BEARISH'], key=lambda x:x['str'], reverse=True)
neut = [f for f in all_f if f['impact']=='NEUTRAL']

bt = sum(f['str'] for f in bull)
brt = sum(f['str'] for f in bear)
tot = bt+brt
sent = (bt/tot*100) if tot>0 else 50

if sent>65: sig,sc = "🟢 STRONG BUY","#00ff88"
elif sent>55: sig,sc = "🟢 BUY","#00cc66"
elif sent<35: sig,sc = "🔴 STRONG SELL","#ff4444"
elif sent<45: sig,sc = "🔴 SELL","#ff6666"
else: sig,sc = "🟡 HOLD","#ffaa00"

# ============ SIGNAL ============
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown(f'<div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;border:1px solid {sc};"><small style="color:#888;">SIGNAL</small><h3 style="color:{sc};margin:5px 0;">{sig}</h3></div>', unsafe_allow_html=True)
with c2:
    stc = "#00ff88" if sent>60 else ("#ff4444" if sent<40 else "#ffaa00")
    st.markdown(f'<div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;"><small style="color:#888;">SENTIMENT</small><h3 style="color:{stc};margin:5px 0;">{sent:.1f}%</h3></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;"><small style="color:#888;">FACTORS</small><h3 style="margin:5px 0;"><span style="color:#00ff88;">🟢{len(bull)}</span> vs <span style="color:#ff4444;">🔴{len(bear)}</span></h3></div>', unsafe_allow_html=True)

# ============ SENTIMENT BAR ============
bw=sent; brw=100-sent
st.markdown(f"""
<div style="background:#1a1a2e;padding:12px;border-radius:10px;margin:10px 0;">
<div style="display:flex;justify-content:space-between;margin-bottom:4px;">
<span style="color:#00ff88;font-size:12px;">🟢 Bullish {bw:.0f}%</span>
<span style="color:#ff4444;font-size:12px;">Bearish {brw:.0f}% 🔴</span></div>
<div style="background:#333;border-radius:8px;height:24px;display:flex;overflow:hidden;">
<div style="background:#00ff88;width:{bw}%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;color:#000;">{bw:.0f}%</div>
<div style="background:#ff4444;width:{brw}%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;color:#fff;">{brw:.0f}%</div>
</div></div>
""", unsafe_allow_html=True)

# ============ BEARISH | BULLISH ============
left, right = st.columns(2)

with left:
    st.markdown('<h3 style="color:#ff4444;text-align:center;">🔴 BEARISH FACTORS</h3>', unsafe_allow_html=True)
    if bear:
        for f in bear:
            st.markdown(f"""
            <div style="background:rgba(255,0,0,0.08);border-left:4px solid #ff4444;padding:10px;margin:6px 0;border-radius:8px;">
            <div style="font-size:16px;">{f['icon']} <b style="color:#fff;">{f['name']}</b></div>
            <div style="color:#ccc;font-size:13px;">Value: <b>{f['val']}</b>
            <span style="color:#ff4444;font-weight:bold;"> ({f['pct']:+.2f}%)</span></div>
            <div style="background:#333;border-radius:4px;height:7px;margin-top:5px;">
            <div style="background:#ff4444;height:7px;border-radius:4px;width:{f['str']}%;"></div></div>
            <small style="color:#888;">Impact: {f['str']:.0f}%</small>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#888;text-align:center;">✅ No bearish factors active</p>', unsafe_allow_html=True)

with right:
    st.markdown('<h3 style="color:#00ff88;text-align:center;">🟢 BULLISH FACTORS</h3>', unsafe_allow_html=True)
    if bull:
        for f in bull:
            st.markdown(f"""
            <div style="background:rgba(0,255,0,0.08);border-left:4px solid #00ff88;padding:10px;margin:6px 0;border-radius:8px;">
            <div style="font-size:16px;">{f['icon']} <b style="color:#fff;">{f['name']}</b></div>
            <div style="color:#ccc;font-size:13px;">Value: <b>{f['val']}</b>
            <span style="color:#00ff88;font-weight:bold;"> ({f['pct']:+.2f}%)</span></div>
            <div style="background:#333;border-radius:4px;height:7px;margin-top:5px;">
            <div style="background:#00ff88;height:7px;border-radius:4px;width:{f['str']}%;"></div></div>
            <small style="color:#888;">Impact: {f['str']:.0f}%</small>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#888;text-align:center;">⚠️ No bullish factors active</p>', unsafe_allow_html=True)

# ============ CHART ============
st.markdown("---")
st.markdown('<h3 style="color:#FFD700;">📈 Gold Price Chart</h3>', unsafe_allow_html=True)

@st.cache_data(ttl=120)
def get_chart(p):
    try:
        return yf.Ticker("GC=F").history(period=p)
    except:
        return pd.DataFrame()

cp = st.selectbox("Period:",["1mo","3mo","6mo","1y"],index=1,
    format_func=lambda x:{"1mo":"1 Month","3mo":"3 Months","6mo":"6 Months","1y":"1 Year"}[x])

cd = get_chart(cp)
if not cd.empty:
    fig = make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.03,row_heights=[0.8,0.2])
    fig.add_trace(go.Candlestick(x=cd.index,open=cd['Open'],high=cd['High'],
        low=cd['Low'],close=cd['Close'],name='Gold',
        increasing_line_color='#00ff88',decreasing_line_color='#ff4444'),row=1,col=1)
    if len(cd)>=20:
        fig.add_trace(go.Scatter(x=cd.index,y=cd['Close'].rolling(20).mean(),
            name='SMA20',line=dict(color='#FFD700',width=1.5)),row=1,col=1)
    vc=['#00ff88' if c>=o else '#ff4444' for c,o in zip(cd['Close'],cd['Open'])]
    fig.add_trace(go.Bar(x=cd.index,y=cd['Volume'],marker_color=vc,
        opacity=0.5,name='Vol'),row=2,col=1)
    fig.update_layout(template='plotly_dark',height=450,xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

# ============ GAUGE + BAR ============
g1,g2 = st.columns(2)

with g1:
    fg = go.Figure(go.Indicator(mode="gauge+number",value=sent,
        number={'suffix':'%','font':{'size':30}},
        gauge={'axis':{'range':[0,100]},'bar':{'color':sc},
        'steps':[
            {'range':[0,20],'color':'rgba(255,0,0,0.3)'},
            {'range':[20,40],'color':'rgba(255,136,0,0.3)'},
            {'range':[40,60],'color':'rgba(255,255,0,0.3)'},
            {'range':[60,80],'color':'rgba(136,255,0,0.3)'},
            {'range':[80,100],'color':'rgba(0,255,0,0.3)'}]}))
    fg.update_layout(template='plotly_dark',height=250,
        paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=20,r=20,t=30,b=10),
        title={'text':'🎯 Sentiment Gauge','font':{'color':'#FFD700','size':14}})
    st.plotly_chart(fg, use_container_width=True)

with g2:
    ns,vs,cs = [],[],[]
    for f in bull:
        ns.append(f['icon']+' '+f['name'][:15]);vs.append(f['str']);cs.append('#00ff88')
    for f in bear:
        ns.append(f['icon']+' '+f['name'][:15]);vs.append(-f['str']);cs.append('#ff4444')
    if ns:
        fb=go.Figure(go.Bar(y=ns,x=vs,orientation='h',marker_color=cs,
            text=[f"{abs(v):.0f}%" for v in vs],textposition='auto'))
        fb.update_layout(template='plotly_dark',height=250,
            paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=30,b=10),
            title={'text':'⚖️ Bull vs Bear','font':{'color':'#FFD700','size':14}},
            xaxis=dict(zeroline=True,zerolinecolor='rgba(255,255,255,0.3)'))
        st.plotly_chart(fb, use_container_width=True)

# ============ ALL FACTORS TABLE (FIXED!) ============
st.markdown("---")
st.markdown('<h3 style="color:#FFD700;">📋 All Factors Summary</h3>', unsafe_allow_html=True)

if all_f:
    table_data = []
    for f in all_f:
        table_data.append({
            'Factor': f"{f['icon']} {f['name']}",
            'Value': f['val'],
            'Daily %': f"{f['pct']:+.2f}%",
            'Weekly %': f"{f['wpct']:+.2f}%",
            'Gold Impact': f['impact'],
            'Strength': f"{f['str']:.0f}%"
        })

    df_table = pd.DataFrame(table_data)

    def color_impact(val):
        if val == 'BULLISH':
            return 'color: #00ff88; font-weight: bold'
        elif val == 'BEARISH':
            return 'color: #ff4444; font-weight: bold'
        else:
            return 'color: #888'

    def color_change(val):
        try:
            num = float(val.replace('%','').replace('+',''))
            if num > 0:
                return 'color: #00ff88'
            elif num < 0:
                return 'color: #ff4444'
        except:
            pass
        return 'color: #888'

    styled = df_table.style.applymap(
        color_impact, subset=['Gold Impact']
    ).applymap(
        color_change, subset=['Daily %', 'Weekly %']
    ).set_properties(**{
        'background-color': '#1a1a2e',
        'color': '#ffffff',
        'border': '1px solid #333',
        'padding': '8px',
        'font-size': '14px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#0d1117'),
            ('color', '#FFD700'),
            ('border', '1px solid #333'),
            ('padding', '10px'),
            ('font-size', '14px')
        ]}
    ])

    st.dataframe(df_table, use_container_width=True, hide_index=True)

# ============ NEUTRAL FACTORS ============
if neut:
    st.markdown('<h4 style="color:#FFD700;">⚪ Neutral Factors</h4>', unsafe_allow_html=True)
    for f in neut:
        st.markdown(f"""
        <span style="background:#1a1a2e;padding:5px 12px;border-radius:15px;
        margin:3px;display:inline-block;font-size:13px;border:1px solid #333;color:#ccc;">
        {f['icon']} {f['name']}: {f['val']} ({f['pct']:+.2f}%)
        </span>""", unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;padding:10px;">
<p style="color:#FFD700;font-size:12px;">🔄 Updated: {datetime.now().strftime('%H:%M:%S')} | Auto-refresh: 60s</p>
<p style="color:#555;font-size:11px;">⚠️ Educational only. Not financial advice. | Data: Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)

# AUTO REFRESH
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)
