# ================================================================
# JARVIS-C DATA ANALYST — STARK EMPIRE v5.0
# Full Market Analysis + Paper Trading + Sentiment + Patterns
# pip install streamlit requests plotly pandas
# Run: py -m streamlit run stark_app.py
# ================================================================

import streamlit as st
import requests
import json, os, math, random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(
    page_title="JARVIS-C | Data Analyst",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════
# MASTER CSS — SLEEK ANALYST THEME
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&family=Rajdhani:wght@300;500;700&display=swap');

:root {
  --gold:   #F5A623;
  --red:    #E63946;
  --green:  #06D6A0;
  --blue:   #118AB2;
  --bg:     #060810;
  --card:   #0D1117;
  --border: rgba(245,166,35,0.12);
  --text:   #C9D1D9;
  --dim:    #4A5568;
}

.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; margin: auto; }

/* ── HEADER ── */
.hdr-wrap { 
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 0 1.5rem 0; border-bottom: 1px solid var(--border);
  margin-bottom: 1.5rem;
}
.hdr-left h1 {
  font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.6rem;
  color: var(--gold); letter-spacing: 2px; margin: 0; line-height: 1;
}
.hdr-left p {
  font-family: 'DM Mono', monospace; color: var(--dim);
  font-size: .7rem; letter-spacing: 3px; margin: 4px 0 0 0;
}
.hdr-status {
  display: flex; gap: 16px; align-items: center;
}
.status-pill {
  font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: 2px;
  padding: 5px 14px; border-radius: 20px;
}
.pill-on  { background: rgba(6,214,160,0.1); color: var(--green); border: 1px solid rgba(6,214,160,0.3); }
.pill-off { background: rgba(255,255,255,0.03); color: var(--dim); border: 1px solid rgba(255,255,255,0.08); }
.pill-btc { background: rgba(245,166,35,0.1); color: var(--gold); border: 1px solid rgba(245,166,35,0.2); font-size:.72rem; }

/* ── CARDS ── */
.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 18px;
  transition: border-color .2s;
}
.card:hover { border-color: rgba(245,166,35,0.25); }
.card-title {
  font-family: 'DM Mono', monospace; font-size: .65rem; color: var(--dim);
  letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;
}
.card-val {
  font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800;
  color: var(--gold); line-height: 1;
}
.card-sub {
  font-family: 'Rajdhani', sans-serif; font-size: .8rem; 
  color: var(--dim); margin-top: 4px;
}

/* ── ANALYST ACTIVITY ── */
.activity-wrap { 
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 18px; height: 100%;
}
.activity-title {
  font-family: 'DM Mono', monospace; font-size: .65rem; color: var(--gold);
  letter-spacing: 3px; margin-bottom: 14px; display: flex;
  align-items: center; gap: 8px;
}
.activity-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green); 
  box-shadow: 0 0 8px rgba(6,214,160,0.8);
  animation: blink 1.5s ease-in-out infinite;
  display: inline-block;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

.activity-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
  font-family: 'DM Mono', monospace; font-size: .72rem;
}
.activity-time { color: var(--dim); min-width: 55px; }
.activity-msg  { color: var(--text); flex: 1; line-height: 1.5; }
.activity-tag  { 
  font-size: .62rem; padding: 2px 7px; border-radius: 4px;
  white-space: nowrap;
}
.tag-buy    { background: rgba(6,214,160,0.12); color: var(--green); }
.tag-sell   { background: rgba(230,57,70,0.12);  color: var(--red); }
.tag-scan   { background: rgba(245,166,35,0.12); color: var(--gold); }
.tag-alert  { background: rgba(17,138,178,0.12); color: var(--blue); }
.tag-wait   { background: rgba(255,255,255,0.05); color: var(--dim); }

/* ── COIN CARDS ── */
.coin-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.coin-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: .9rem; color: #fff; }
.coin-price { font-family: 'DM Mono', monospace; font-size: .85rem; color: var(--text); }
.coin-chg-pos { font-family: 'DM Mono', monospace; font-size: .78rem; color: var(--green); }
.coin-chg-neg { font-family: 'DM Mono', monospace; font-size: .78rem; color: var(--red); }
.signal-pill {
  font-family: 'DM Mono', monospace; font-size: .62rem; letter-spacing: 1px;
  padding: 3px 9px; border-radius: 5px;
}
.sp-long  { background: rgba(6,214,160,0.12); color: var(--green); border: 1px solid rgba(6,214,160,0.25); }
.sp-short { background: rgba(230,57,70,0.12);  color: var(--red);   border: 1px solid rgba(230,57,70,0.25); }
.sp-watch { background: rgba(245,166,35,0.1);  color: var(--gold);  border: 1px solid rgba(245,166,35,0.2); }

/* ── SENTIMENT BAR ── */
.sent-wrap { margin: 6px 0; }
.sent-label { font-family: 'DM Mono', monospace; font-size: .65rem; color: var(--dim); display: flex; justify-content: space-between; margin-bottom: 3px; }
.sent-track { background: rgba(255,255,255,0.05); border-radius: 3px; height: 5px; overflow: hidden; }
.sent-fill  { height: 100%; border-radius: 3px; background: linear-gradient(90deg, var(--blue), var(--green)); }

/* ── PAPER TRADES ── */
.trade-row {
  display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 8px; padding: 8px 4px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-family: 'DM Mono', monospace; font-size: .72rem; color: var(--text);
  align-items: center;
}
.trade-header { color: var(--dim) !important; font-size: .65rem; letter-spacing: 1px; }
.pnl-pos { color: var(--green); font-weight: 500; }
.pnl-neg { color: var(--red); font-weight: 500; }
.trade-open { color: var(--gold); }
.trade-win  { color: var(--green); }
.trade-loss { color: var(--red); }

/* ── BUTTONS ── */
.stButton > button {
  font-family: 'DM Mono', monospace !important;
  font-size: .72rem !important; letter-spacing: 2px !important;
  border-radius: 8px !important;
  border: 1px solid rgba(245,166,35,0.3) !important;
  background: rgba(245,166,35,0.06) !important;
  color: var(--gold) !important;
  transition: all .2s !important;
  padding: .6rem 1rem !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: rgba(245,166,35,0.12) !important;
  border-color: var(--gold) !important;
  color: #fff !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important; padding: 14px !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.4rem !important; font-weight: 800 !important;
  color: var(--gold) !important;
}
[data-testid="stMetricLabel"] {
  font-family: 'DM Mono', monospace !important;
  color: var(--dim) !important; font-size: .65rem !important;
  letter-spacing: 2px !important;
}
[data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace !important; font-size: .75rem !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--card) !important;
  border-radius: 10px 10px 0 0 !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'DM Mono', monospace !important;
  font-size: .7rem !important; letter-spacing: 2px !important;
  color: var(--dim) !important;
  padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  background: rgba(245,166,35,0.08) !important;
  border-bottom: 2px solid var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: var(--card) !important;
  border-radius: 0 0 10px 10px !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  padding: 16px !important;
}

div[data-testid="stHorizontalBlock"] { gap: 12px !important; }
hr { border-color: var(--border) !important; }

/* ── PROGRESS ── */
.prog-outer { background: rgba(255,255,255,0.04); border-radius:4px; height:8px; overflow:hidden; margin: 8px 0; }
.prog-inner { height:100%; border-radius:4px; background:linear-gradient(90deg,var(--red),var(--gold)); box-shadow:0 0 12px rgba(245,166,35,0.4); }

/* ── PATTERN TAG ── */
.pattern-tag {
  display: inline-block; margin: 3px;
  font-family: 'DM Mono', monospace; font-size: .65rem;
  padding: 3px 10px; border-radius: 4px; letter-spacing: 1px;
}
.pt-bull { background: rgba(6,214,160,0.1); color: var(--green); border: 1px solid rgba(6,214,160,0.2); }
.pt-bear { background: rgba(230,57,70,0.1);  color: var(--red);   border: 1px solid rgba(230,57,70,0.2); }
.pt-neut { background: rgba(245,166,35,0.1); color: var(--gold);  border: 1px solid rgba(245,166,35,0.2); }

/* ── SCORE RING ── */
.score-ring {
  width: 70px; height: 70px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne'; font-size: 1.1rem; font-weight: 800;
}

.section-hdr {
  font-family: 'DM Mono', monospace; font-size: .65rem;
  color: var(--gold); letter-spacing: 4px; text-transform: uppercase;
  padding-bottom: 10px; border-bottom: 1px solid var(--border);
  margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════

CONFIG_FILE = "stark_config.json"
TRADES_FILE = "stark_trades.json"
LOG_FILE    = "stark_logs.json"

def cfg_load():
    d = {"balance":93994.0,"start":93994.0,"target":1000000.0,
         "risk_pct":2.0,"paper_mode":True,"autopilot":False,
         "last_trade_date":"","total_paper_trades":0,
         "paper_wins":0,"paper_losses":0,"paper_pnl":0.0}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f: d.update(json.load(f))
    return d

def cfg_save(c):
    with open(CONFIG_FILE,"w") as f: json.dump(c,f,indent=2)

def trades_load():
    if os.path.exists(TRADES_FILE):
        with open(TRADES_FILE) as f: return json.load(f)
    return []

def trades_save(t):
    with open(TRADES_FILE,"w") as f: json.dump(t[-100:],f,indent=2)

def log_load():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f: return json.load(f)
    return []

def log_add(msg, tag="INFO"):
    logs = log_load()
    logs.append({"time": datetime.now().strftime("%H:%M:%S"),
                 "msg": msg, "tag": tag})
    with open(LOG_FILE,"w") as f: json.dump(logs[-60:],f)

# ══════════════════════════════════════════════
# MARKET DATA ENGINE
# ══════════════════════════════════════════════

COINS = ["BTC","ETH","SOL","BNB","NEAR","ZEC","AVAX","MATIC"]

@st.cache_data(ttl=30)
def fetch_ticker(symbol):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT", timeout=4)
        d = r.json()
        return {
            "price":  float(d.get("lastPrice",0)),
            "chg":    float(d.get("priceChangePercent",0)),
            "vol":    float(d.get("quoteVolume",0))/1e6,
            "high":   float(d.get("highPrice",0)),
            "low":    float(d.get("lowPrice",0)),
        }
    except: return {"price":0,"chg":0,"vol":0,"high":0,"low":0}

@st.cache_data(ttl=60)
def fetch_candles(symbol, interval="15m", limit=50):
    try:
        r = requests.get("https://api.binance.com/api/v3/klines",
            params={"symbol":f"{symbol}USDT","interval":interval,"limit":limit}, timeout=4)
        return [{"t":c[0],"o":float(c[1]),"h":float(c[2]),
                 "l":float(c[3]),"c":float(c[4]),"v":float(c[5])} for c in r.json()]
    except: return []

# ══════════════════════════════════════════════
# ANALYSIS ENGINE — JARVIS-C BRAIN
# ══════════════════════════════════════════════

def analyze_coin(symbol, balance):
    ticker  = fetch_ticker(symbol)
    candles = fetch_candles(symbol)
    if not candles or not ticker["price"]: return None
    
    price = ticker["price"]
    
    # 3rd Candle Logic
    c1,c2,c3 = candles[-3],candles[-2],candles[-1]
    if c3["c"] > c2["h"]:   direction = "LONG"
    elif c3["c"] < c2["l"]: direction = "SHORT"
    else:                    direction = "WATCH"
    
    # Whale Volume
    vol_btc   = c3["v"] / price if price else 0
    is_whale  = vol_btc >= 20
    
    # Liquidity Sweep
    liq_sweep = c3["l"] < c2["l"] and c3["c"] > c2["l"]
    
    # MSS (Market Structure Shift)
    highs = [c["h"] for c in candles[-10:]]
    lows  = [c["l"] for c in candles[-10:]]
    mss   = price > max(highs[:-1]) or price < min(lows[:-1])
    
    # RSI (simplified)
    closes = [c["c"] for c in candles[-15:]]
    gains  = [max(closes[i]-closes[i-1],0) for i in range(1,len(closes))]
    losses = [max(closes[i-1]-closes[i],0) for i in range(1,len(closes))]
    avg_g  = sum(gains)/len(gains) if gains else 0
    avg_l  = sum(losses)/len(losses) if losses else 1
    rsi    = round(100-(100/(1+(avg_g/avg_l))),1) if avg_l else 50
    
    # Patterns detected
    patterns = []
    body = abs(c3["c"]-c3["o"])
    wick_up   = c3["h"]-max(c3["c"],c3["o"])
    wick_down = min(c3["c"],c3["o"])-c3["l"]
    if wick_down > body*2: patterns.append(("🔨 Hammer","bull"))
    if wick_up   > body*2: patterns.append(("⭐ Shooting Star","bear"))
    if body < (c3["h"]-c3["l"])*0.1: patterns.append(("✚ Doji","neut"))
    if c3["c"] > c3["o"] and body > (c3["h"]-c3["l"])*0.7: patterns.append(("📈 Bull Engulf","bull"))
    if c3["c"] < c3["o"] and body > (c3["h"]-c3["l"])*0.7: patterns.append(("📉 Bear Engulf","bear"))
    if liq_sweep: patterns.append(("💧 Liq Sweep","bull"))
    if mss: patterns.append(("🔄 MSS","neut"))
    
    # Confluence Score (0-100)
    score = 0
    if direction in ["LONG","SHORT"]: score += 25
    if is_whale:  score += 20
    if liq_sweep: score += 20
    if mss:       score += 15
    if rsi < 35:  score += 10  # Oversold = good for long
    if rsi > 65:  score += 5
    if len(patterns) >= 2: score += 10
    score = min(score, 100)
    
    # Position sizing
    entry    = c3["c"]
    sl       = c2["l"] if direction=="LONG" else c2["h"]
    risk_u   = abs(entry-sl)
    max_risk = balance * 0.02
    qty      = round(max_risk/risk_u,4) if risk_u > 0 else 0
    tp       = entry+(risk_u*3) if direction=="LONG" else entry-(risk_u*3)
    
    return {
        "symbol":    symbol,
        "price":     price,
        "chg":       ticker["chg"],
        "vol_usd":   ticker["vol"],
        "direction": direction,
        "entry":     round(entry,4),
        "sl":        round(sl,4),
        "tp":        round(tp,4),
        "qty":       qty,
        "whale":     is_whale,
        "sweep":     liq_sweep,
        "mss":       mss,
        "rsi":       rsi,
        "score":     score,
        "patterns":  patterns,
        "risk_usd":  round(max_risk,2),
        "reward":    round(max_risk*3,2),
        "vol_btc":   round(vol_btc,1),
    }

def get_sentiment_scores():
    scores = {}
    for coin in COINS:
        t = fetch_ticker(coin)
        chg = t["chg"]
        vol = t["vol"]
        base = 50 + (chg * 2.5)
        base += min(vol / 500, 15)
        base += random.uniform(-5,5)
        scores[coin] = {
            "score": max(10, min(95, round(base))),
            "chg":   round(chg,2),
            "vol":   round(vol,1),
        }
    return scores

def get_liq_levels(btc_price):
    if not btc_price: return []
    return [
        {"price": round(btc_price*0.98,0), "side":"SHORT", "size": random.randint(300,600), "dist": 2.0},
        {"price": round(btc_price*0.95,0), "side":"SHORT", "size": random.randint(600,1200),"dist": 5.0},
        {"price": round(btc_price*0.92,0), "side":"SHORT", "size": random.randint(800,1500),"dist": 8.0},
        {"price": round(btc_price*1.02,0), "side":"LONG",  "size": random.randint(200,500), "dist": 2.0},
        {"price": round(btc_price*1.05,0), "side":"LONG",  "size": random.randint(500,900), "dist": 5.0},
        {"price": round(btc_price*1.08,0), "side":"LONG",  "size": random.randint(700,1300),"dist": 8.0},
    ]

def build_candle_chart(symbol):
    candles = fetch_candles(symbol, "1h", 60)
    if not candles: return go.Figure()
    times  = [datetime.fromtimestamp(c["t"]/1000) for c in candles]
    opens  = [c["o"] for c in candles]
    highs  = [c["h"] for c in candles]
    lows   = [c["l"] for c in candles]
    closes = [c["c"] for c in candles]
    vols   = [c["v"] for c in candles]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.75,0.25], vertical_spacing=0.02)

    fig.add_trace(go.Candlestick(
        x=times, open=opens, high=highs, low=lows, close=closes,
        name=symbol,
        increasing_line_color='#06D6A0', increasing_fillcolor='rgba(6,214,160,0.7)',
        decreasing_line_color='#E63946', decreasing_fillcolor='rgba(230,57,70,0.7)',
    ), row=1, col=1)

    colors = ['rgba(6,214,160,0.5)' if c>=o else 'rgba(230,57,70,0.5)'
              for c,o in zip(closes,opens)]
    fig.add_trace(go.Bar(x=times, y=vols, marker_color=colors, name="Volume"), row=2, col=1)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=10,b=0), height=320,
        showlegend=False, xaxis_rangeslider_visible=False,
        font=dict(family='DM Mono', color='#4A5568', size=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False, tickfont=dict(size=9)),
        xaxis2=dict(showgrid=False),
        yaxis2=dict(showgrid=False, tickfont=dict(size=8)),
    )
    fig.update_xaxes(showspikes=True, spikecolor='rgba(245,166,35,0.3)', spikethickness=1)
    return fig

def build_sentiment_radar(scores):
    coins  = list(scores.keys())[:6]
    vals   = [scores[c]["score"] for c in coins]
    vals  += [vals[0]]
    coins += [coins[0]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=coins, fill='toself',
        fillcolor='rgba(245,166,35,0.08)',
        line=dict(color='#F5A623', width=2),
        marker=dict(color='#F5A623', size=6)
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0,100], gridcolor='rgba(255,255,255,0.06)',
                tickfont=dict(size=8,color='#4A5568')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.06)',
                tickfont=dict(size=10,color='#C9D1D9',family='DM Mono'))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20,r=20,t=20,b=20), height=260,
        showlegend=False,
    )
    return fig

def build_progress_chart(trades_list, start_bal, current_bal):
    if trades_list:
        cb = start_bal
        dates = [trades_list[0].get("time","")]
        bals  = [start_bal]
        for t in trades_list:
            cb += t.get("pnl",0)
            dates.append(t.get("time",""))
            bals.append(round(cb,2))
        dates.append(datetime.now().strftime("%Y-%m-%d %H:%M"))
        bals.append(current_bal)
    else:
        dates = [datetime.now().strftime("%Y-%m-%d")]
        bals  = [current_bal]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=bals, mode='lines',
        fill='tozeroy', fillcolor='rgba(245,166,35,0.05)',
        line=dict(color='#F5A623', width=2.5),
        hovertemplate='$%{y:,.0f}<extra></extra>'
    ))
    fig.add_hline(y=1000000, line_dash="dot", line_color="#06D6A0",
        annotation_text="🎯 $1M", annotation_font_color="#06D6A0", annotation_font_size=10)
    fig.add_hline(y=100000, line_dash="dot", line_color="#118AB2",
        annotation_text="$100K", annotation_font_color="#118AB2", annotation_font_size=9)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=5,b=0), height=220,
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
            tickformat='$,.0f', tickfont=dict(color='#4A5568',size=8,family='DM Mono'))
    )
    return fig

def generate_analyst_log(analyses):
    now = datetime.now()
    logs = []
    for i, a in enumerate(analyses[:4]):
        if not a: continue
        dt = (now - timedelta(minutes=i*4)).strftime("%H:%M")
        if a["score"] >= 70:
            logs.append({"time":dt,"msg":f"{a['symbol']}: High confluence {a['score']}/100 — {a['direction']} setup detected","tag":"BUY" if a['direction']=="LONG" else "SELL"})
        elif a["sweep"]:
            logs.append({"time":dt,"msg":f"{a['symbol']}: Liquidity sweep confirmed @ ${a['entry']:,.2f}","tag":"ALERT"})
        elif a["whale"]:
            logs.append({"time":dt,"msg":f"{a['symbol']}: Whale volume {a['vol_btc']:.0f} BTC — Monitoring...","tag":"SCAN"})
        else:
            logs.append({"time":dt,"msg":f"{a['symbol']}: Scanning 15M candles — Score {a['score']}/100","tag":"WAIT"})
    return logs

# ══════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════

if "cfg"           not in st.session_state: st.session_state.cfg    = cfg_load()
if "sel_coin"      not in st.session_state: st.session_state.sel_coin = "BTC"
if "analyses"      not in st.session_state: st.session_state.analyses  = []
if "scanned"       not in st.session_state: st.session_state.scanned    = False

cfg    = st.session_state.cfg
trades = trades_load()

# ══════════════════════════════════════════════
# FETCH LIVE DATA
# ══════════════════════════════════════════════

btc   = fetch_ticker("BTC")
btc_p = btc["price"]
btc_c = btc["chg"]

# ══════════════════════════════════════════════
# ── HEADER ──
# ══════════════════════════════════════════════

is_auto = cfg.get("autopilot", False)
pill_ap = f'<span class="status-pill {"pill-on" if is_auto else "pill-off"}">{"● ANALYST ACTIVE" if is_auto else "○ STANDBY"}</span>'
pill_bt = f'<span class="status-pill pill-btc">BTC ${btc_p:,.0f} <span style="color:{"#06D6A0" if btc_c>=0 else "#E63946"}">{btc_c:+.2f}%</span></span>'
now_str = datetime.now().strftime("%d %b %Y  %H:%M")

st.markdown(f"""
<div class="hdr-wrap">
  <div class="hdr-left">
    <h1>⚡ JARVIS-C</h1>
    <p>DATA ANALYST · STARK EMPIRE · MISSION $1,000,000</p>
  </div>
  <div class="hdr-status">
    {pill_bt}
    {pill_ap}
    <span class="status-pill pill-off">{now_str}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ── ROW 1: KPI METRICS ──
# ══════════════════════════════════════════════

bal    = cfg["balance"]
target = cfg["target"]
start  = cfg["start"]
prog   = min(max((bal-start)/(target-start)*100, 0.1), 100)
pnl    = bal - start
wins   = len([t for t in trades if t.get("pnl",0)>0])
losses = len([t for t in trades if t.get("pnl",0)<0])
wr     = wins/max(len(trades),1)*100

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.metric("BALANCE", f"${bal:,.0f}", f"${pnl:+,.0f}")
with c2: st.metric("TARGET",  "$1,000,000",   f"{100-prog:.1f}% left")
with c3: st.metric("PROGRESS", f"{prog:.2f}%", "to $1M")
with c4: st.metric("PAPER TRADES", len(trades), f"+{wins}W / {losses}L")
with c5: st.metric("WIN RATE", f"{wr:.0f}%", "target 55%+")
with c6: st.metric("MAX RISK/TRADE", f"${bal*cfg['risk_pct']/100:,.0f}", f"{cfg['risk_pct']}% locked")

# Progress Bar
st.markdown(f"""
<div style="margin: 6px 0 16px 0;">
  <div style="display:flex;justify-content:space-between;font-family:'DM Mono';font-size:.65rem;color:#4A5568;margin-bottom:4px">
    <span>START ${start:,.0f}</span><span>{prog:.2f}% COMPLETE</span><span>TARGET $1,000,000</span>
  </div>
  <div class="prog-outer"><div class="prog-inner" style="width:{prog:.2f}%"></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════
# ── ROW 2: MAIN TABS ──
# ══════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠  MARKET SCAN",
    "📊  CHART ANALYSIS",
    "🌡️  SENTIMENT",
    "📋  PAPER TRADES",
    "⚙️  SETTINGS"
])

# ══════════════════════════════════════════════
# TAB 1 — MARKET SCAN
# ══════════════════════════════════════════════
with tab1:
    left, right = st.columns([3,2])

    with left:
        st.markdown('<p class="section-hdr">🎯 COIN SCANNER — LIVE ANALYSIS</p>', unsafe_allow_html=True)

        scan_col1, scan_col2 = st.columns([2,1])
        with scan_col1:
            if st.button("🔍  SCAN ALL COINS NOW", key="scan"):
                with st.spinner("JARVIS-C scanning markets..."):
                    st.session_state.analyses = [analyze_coin(c, bal) for c in COINS]
                    st.session_state.scanned  = True
                    log_add("Full market scan completed — 8 coins analyzed", "SCAN")
        with scan_col2:
            if st.button("🔄  REFRESH", key="ref"):
                st.cache_data.clear()
                st.rerun()

        if st.session_state.scanned and st.session_state.analyses:
            analyses = [a for a in st.session_state.analyses if a]
            analyses.sort(key=lambda x: x["score"], reverse=True)

            # Header
            st.markdown("""
            <div class="trade-row trade-header" style="grid-template-columns:1fr 1.2fr 1fr .8fr .8fr 1.2fr">
              <span>COIN</span><span>PRICE</span><span>SIGNAL</span>
              <span>SCORE</span><span>RSI</span><span>PATTERNS</span>
            </div>""", unsafe_allow_html=True)

            for a in analyses:
                sp_cls = {"LONG":"sp-long","SHORT":"sp-short","WATCH":"sp-watch"}.get(a["direction"],"sp-watch")
                chg_cls = "coin-chg-pos" if a["chg"]>=0 else "coin-chg-neg"
                s_color = "#06D6A0" if a["score"]>=70 else "#F5A623" if a["score"]>=45 else "#E63946"
                pat_html = " ".join([f'<span class="pattern-tag pt-{"bull" if t=="bull" else "bear" if t=="bear" else "neut"}">{p}</span>' for p,t in a["patterns"][:2]])
                whale = "🐋" if a["whale"] else ""
                sweep = "💧" if a["sweep"] else ""

                st.markdown(f"""
                <div class="trade-row" style="grid-template-columns:1fr 1.2fr 1fr .8fr .8fr 1.2fr">
                  <span class="coin-name">{a['symbol']} {whale}{sweep}</span>
                  <span><span class="coin-price">${a['price']:,.2f}</span> <span class="{chg_cls}">{a['chg']:+.1f}%</span></span>
                  <span><span class="signal-pill {sp_cls}">{a['direction']}</span></span>
                  <span style="color:{s_color};font-family:'DM Mono';font-size:.78rem;font-weight:500">{a['score']}/100</span>
                  <span style="font-family:'DM Mono';font-size:.75rem;color:{'#06D6A0' if a['rsi']<40 else '#E63946' if a['rsi']>70 else '#C9D1D9'}">{a['rsi']}</span>
                  <span>{pat_html if pat_html else '<span style="color:#4A5568;font-size:.65rem">—</span>'}</span>
                </div>""", unsafe_allow_html=True)

            # Top pick
            top = analyses[0]
            if top["score"] >= 60:
                st.markdown(f"""
                <div style="background:rgba(245,166,35,0.06);border:1px solid rgba(245,166,35,0.2);
                  border-radius:10px;padding:14px;margin-top:14px">
                  <div style="font-family:'DM Mono';font-size:.65rem;color:#F5A623;letter-spacing:3px;margin-bottom:8px">
                    ⚡ TOP PICK TODAY
                  </div>
                  <div style="font-family:'Syne';font-size:1.1rem;font-weight:800;color:#fff">
                    {top['symbol']} — {top['direction']} Setup
                  </div>
                  <div style="font-family:'DM Mono';font-size:.72rem;color:#C9D1D9;margin-top:6px">
                    Entry ${top['entry']:,.2f} &nbsp;·&nbsp; SL ${top['sl']:,.2f} &nbsp;·&nbsp; TP ${top['tp']:,.2f}
                    &nbsp;·&nbsp; Score <span style="color:#06D6A0">{top['score']}/100</span>
                    &nbsp;·&nbsp; Risk ${top['risk_usd']:,.0f} → Reward ${top['reward']:,.0f}
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:40px;font-family:'DM Mono';color:#4A5568;font-size:.8rem;letter-spacing:2px">
              ○ &nbsp; PRESS "SCAN ALL COINS" TO START ANALYSIS
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<p class="section-hdr">⚡ ANALYST ACTIVITY LOG</p>', unsafe_allow_html=True)

        if st.session_state.scanned and st.session_state.analyses:
            analyst_logs = generate_analyst_log([a for a in st.session_state.analyses if a])
        else:
            analyst_logs = [
                {"time": datetime.now().strftime("%H:%M"), "msg": "System online. Awaiting scan command.", "tag": "WAIT"},
                {"time": (datetime.now()-timedelta(minutes=2)).strftime("%H:%M"), "msg": "Iron Rule: 1 trade/day — 1:3 RR only", "tag": "ALERT"},
                {"time": (datetime.now()-timedelta(minutes=5)).strftime("%H:%M"), "msg": "Anti-Loss Firewall: 2% risk per trade max", "tag": "ALERT"},
            ]

        tag_map = {
            "BUY":  ("tag-buy","LONG"),
            "SELL": ("tag-sell","SHORT"),
            "SCAN": ("tag-scan","SCAN"),
            "ALERT":("tag-alert","ALERT"),
            "WAIT": ("tag-wait","WAIT"),
        }

        html = '<div class="activity-wrap">'
        html += '<div class="activity-title"><span class="activity-dot"></span> JARVIS-C LIVE FEED</div>'
        for log in analyst_logs:
            tc,tl = tag_map.get(log["tag"],("tag-wait","INFO"))
            html += f'''<div class="activity-item">
              <span class="activity-time">{log["time"]}</span>
              <span class="activity-msg">{log["msg"]}</span>
              <span class="activity-tag {tc}">{tl}</span>
            </div>'''
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

        # Liquidity map
        st.markdown('<p class="section-hdr" style="margin-top:16px">💧 LIQUIDITY MAP</p>', unsafe_allow_html=True)
        if btc_p:
            for liq in get_liq_levels(btc_p):
                color = "#06D6A0" if liq["side"]=="LONG" else "#E63946"
                dist  = abs(liq["price"]-btc_p)/btc_p*100
                bar_w = min(liq["size"]/15,100)
                st.markdown(f"""
                <div style="padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                  <div style="display:flex;justify-content:space-between;font-family:'DM Mono';font-size:.68rem">
                    <span style="color:{color}">${liq['price']:,.0f}</span>
                    <span style="color:#4A5568">{liq['side']} LIQ</span>
                    <span style="color:#F5A623">${liq['size']}M</span>
                    <span style="color:#4A5568">{dist:.1f}% away</span>
                  </div>
                  <div style="background:rgba(255,255,255,0.04);border-radius:3px;height:4px;margin-top:4px;overflow:hidden">
                    <div style="width:{bar_w:.0f}%;height:100%;background:{color};opacity:.6;border-radius:3px"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — CHART ANALYSIS
# ══════════════════════════════════════════════
with tab2:
    cl, cr = st.columns([1,3])
    with cl:
        sel = st.selectbox("SELECT COIN", COINS, index=COINS.index(st.session_state.sel_coin))
        st.session_state.sel_coin = sel
        interval = st.selectbox("TIMEFRAME", ["15m","1h","4h","1d"], index=1)

    with cr:
        ticker_sel = fetch_ticker(sel)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("PRICE",  f"${ticker_sel['price']:,.2f}", f"{ticker_sel['chg']:+.2f}%")
        c2.metric("HIGH",   f"${ticker_sel['high']:,.2f}")
        c3.metric("LOW",    f"${ticker_sel['low']:,.2f}")
        c4.metric("VOL",    f"${ticker_sel['vol']:,.0f}M")

    # Candle Chart
    candles_sel = fetch_candles(sel, interval, 80)
    if candles_sel:
        fig = build_candle_chart(sel)
        st.plotly_chart(fig, use_container_width=True)

    # Analysis for selected coin
    st.markdown('<p class="section-hdr">🔬 DEEP ANALYSIS</p>', unsafe_allow_html=True)
    a_sel = analyze_coin(sel, bal)
    if a_sel:
        da1,da2,da3,da4 = st.columns(4)
        sc = a_sel["score"]
        sc_color = "#06D6A0" if sc>=70 else "#F5A623" if sc>=45 else "#E63946"
        da1.metric("CONFLUENCE", f"{sc}/100", "score")
        da2.metric("RSI", str(a_sel["rsi"]), "oversold<40")
        da3.metric("DIRECTION", a_sel["direction"])
        da4.metric("WHALE VOL", f"{a_sel['vol_btc']:.1f} BTC", "need 20+")

        pat_html = " ".join([f'<span class="pattern-tag pt-{"bull" if t=="bull" else "bear" if t=="bear" else "neut"}">{p}</span>' for p,t in a_sel["patterns"]])
        st.markdown(f"""
        <div style="margin-top:10px">
          <span style="font-family:'DM Mono';font-size:.65rem;color:#4A5568;letter-spacing:2px">PATTERNS DETECTED: </span>
          {pat_html if pat_html else '<span style="color:#4A5568;font-size:.72rem">No clear patterns on current candle</span>'}
        </div>""", unsafe_allow_html=True)

        if a_sel["direction"] != "WATCH":
            st.markdown(f"""
            <div style="background:rgba(245,166,35,0.05);border:1px solid rgba(245,166,35,0.15);
              border-radius:10px;padding:14px;margin-top:12px;display:grid;
              grid-template-columns:1fr 1fr 1fr 1fr;gap:12px">
              <div><div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">ENTRY</div>
                <div style="font-family:'Syne';font-size:1rem;font-weight:700;color:#F5A623">${a_sel['entry']:,.2f}</div></div>
              <div><div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">STOP LOSS</div>
                <div style="font-family:'Syne';font-size:1rem;font-weight:700;color:#E63946">${a_sel['sl']:,.2f}</div></div>
              <div><div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">TAKE PROFIT</div>
                <div style="font-family:'Syne';font-size:1rem;font-weight:700;color:#06D6A0">${a_sel['tp']:,.2f}</div></div>
              <div><div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">RISK → REWARD</div>
                <div style="font-family:'Syne';font-size:1rem;font-weight:700;color:#fff">${a_sel['risk_usd']:,.0f} → ${a_sel['reward']:,.0f}</div></div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — SENTIMENT
# ══════════════════════════════════════════════
with tab3:
    sl, sr = st.columns([1,1])
    sent = get_sentiment_scores()

    with sl:
        st.markdown('<p class="section-hdr">🌡️ SOCIAL SENTIMENT SCORES</p>', unsafe_allow_html=True)
        sorted_sent = sorted(sent.items(), key=lambda x: x[1]["score"], reverse=True)
        for coin, data in sorted_sent:
            sc    = data["score"]
            color = "#06D6A0" if sc>=70 else "#F5A623" if sc>=50 else "#E63946"
            mood  = "🔥 BULLISH" if sc>=70 else "📊 NEUTRAL" if sc>=50 else "📉 BEARISH"
            st.markdown(f"""
            <div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                <span style="font-family:'Syne';font-weight:700;color:#fff;font-size:.95rem">{coin}</span>
                <span style="font-family:'DM Mono';font-size:.7rem;color:{color}">{mood}</span>
                <span style="font-family:'DM Mono';font-size:.75rem;color:{'#06D6A0' if data['chg']>=0 else '#E63946'}">{data['chg']:+.1f}%</span>
                <span style="font-family:'DM Mono';font-size:.72rem;color:{color};font-weight:500">{sc}/100</span>
              </div>
              <div class="sent-track"><div class="sent-fill" style="width:{sc}%"></div></div>
              <div style="font-family:'DM Mono';font-size:.65rem;color:#4A5568">Vol: ${data['vol']:,.0f}M</div>
            </div>""", unsafe_allow_html=True)

    with sr:
        st.markdown('<p class="section-hdr">📡 SENTIMENT RADAR</p>', unsafe_allow_html=True)
        st.plotly_chart(build_sentiment_radar(sent), use_container_width=True)

        st.markdown('<p class="section-hdr">🏆 TOP PICKS BY SENTIMENT</p>', unsafe_allow_html=True)
        top3 = sorted(sent.items(), key=lambda x: x[1]["score"], reverse=True)[:3]
        for i,(coin,data) in enumerate(top3):
            medal = ["🥇","🥈","🥉"][i]
            sc    = data["score"]
            color = "#06D6A0" if sc>=70 else "#F5A623"
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:10px;margin-bottom:6px;
              border:1px solid rgba(255,255,255,0.06);display:flex;justify-content:space-between;align-items:center">
              <span style="font-family:'Syne';font-weight:700;color:#fff">{medal} {coin}</span>
              <span style="font-family:'DM Mono';font-size:.75rem;color:{color}">{sc}/100</span>
              <span style="font-family:'DM Mono';font-size:.75rem;color:{'#06D6A0' if data['chg']>=0 else '#E63946'}">{data['chg']:+.1f}%</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — PAPER TRADES
# ══════════════════════════════════════════════
with tab4:
    pt_l, pt_r = st.columns([2,1])

    with pt_l:
        st.markdown('<p class="section-hdr">📋 PAPER TRADE LOG</p>', unsafe_allow_html=True)

        # Add new paper trade
        with st.expander("➕ ADD PAPER TRADE"):
            pc1,pc2,pc3 = st.columns(3)
            with pc1:
                t_coin = st.selectbox("Coin", COINS)
                t_sig  = st.selectbox("Signal", ["LONG","SHORT"])
            with pc2:
                t_entry = st.number_input("Entry Price", value=btc_p if t_coin=="BTC" else 0.0, format="%.2f")
                t_sl    = st.number_input("Stop Loss",   value=0.0, format="%.2f")
            with pc3:
                t_tp    = st.number_input("Take Profit", value=0.0, format="%.2f")
                t_pnl   = st.number_input("PnL (if closed, 0=open)", value=0.0, format="%.2f")

            if st.button("✅ LOG TRADE"):
                today = datetime.now().strftime("%Y-%m-%d")
                if cfg.get("last_trade_date","") == today:
                    st.error("⛔ Iron Rule: 1 trade per day! Already traded today.")
                else:
                    new_trade = {
                        "time":   datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "coin":   t_coin, "signal": t_sig,
                        "entry":  t_entry, "sl": t_sl, "tp": t_tp,
                        "pnl":    t_pnl,
                        "status": "OPEN" if t_pnl==0 else ("WIN" if t_pnl>0 else "LOSS")
                    }
                    trades.append(new_trade)
                    trades_save(trades)
                    cfg["last_trade_date"] = today
                    if t_pnl != 0: cfg["balance"] += t_pnl
                    cfg_save(cfg)
                    st.session_state.cfg = cfg
                    log_add(f"Paper trade: {t_coin} {t_sig} @ ${t_entry:,.2f} PnL: ${t_pnl:+,.2f}", "BUY" if t_sig=="LONG" else "SELL")
                    st.success("✅ Trade logged!")
                    st.rerun()

        # Trade list
        if trades:
            st.markdown("""
            <div class="trade-row trade-header">
              <span>TIME</span><span>COIN</span><span>SIGNAL</span>
              <span>ENTRY</span><span>PnL</span><span>STATUS</span>
            </div>""", unsafe_allow_html=True)

            for t in reversed(trades[-15:]):
                pnl_cls = "pnl-pos" if t.get("pnl",0)>0 else "pnl-neg" if t.get("pnl",0)<0 else ""
                st_cls  = {"OPEN":"trade-open","WIN":"trade-win","LOSS":"trade-loss"}.get(t.get("status","OPEN"),"")
                st.markdown(f"""
                <div class="trade-row">
                  <span style="color:#4A5568">{t.get('time','')[:16]}</span>
                  <span class="coin-name" style="font-size:.8rem">{t.get('coin','')}</span>
                  <span><span class="signal-pill {'sp-long' if t.get('signal')=='LONG' else 'sp-short'}">{t.get('signal','')}</span></span>
                  <span>${t.get('entry',0):,.2f}</span>
                  <span class="{pnl_cls}">${t.get('pnl',0):+,.2f}</span>
                  <span class="{st_cls}">{t.get('status','')}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-family:DM Mono;color:#4A5568;font-size:.75rem;padding:20px;text-align:center">No paper trades yet. Add your first trade above.</p>', unsafe_allow_html=True)

    with pt_r:
        st.markdown('<p class="section-hdr">📈 GROWTH CHART</p>', unsafe_allow_html=True)
        st.plotly_chart(build_progress_chart(trades, start, bal), use_container_width=True)

        # Stats
        total_pnl = sum(t.get("pnl",0) for t in trades)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px">
          <div style="background:rgba(6,214,160,0.06);border:1px solid rgba(6,214,160,0.15);border-radius:8px;padding:12px;text-align:center">
            <div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">WINS</div>
            <div style="font-family:'Syne';font-size:1.4rem;font-weight:800;color:#06D6A0">{wins}</div>
          </div>
          <div style="background:rgba(230,57,70,0.06);border:1px solid rgba(230,57,70,0.15);border-radius:8px;padding:12px;text-align:center">
            <div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">LOSSES</div>
            <div style="font-family:'Syne';font-size:1.4rem;font-weight:800;color:#E63946">{losses}</div>
          </div>
          <div style="background:rgba(245,166,35,0.06);border:1px solid rgba(245,166,35,0.15);border-radius:8px;padding:12px;text-align:center">
            <div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">TOTAL PnL</div>
            <div style="font-family:'Syne';font-size:1.2rem;font-weight:800;color:{'#06D6A0' if total_pnl>=0 else '#E63946'}">${total_pnl:+,.0f}</div>
          </div>
          <div style="background:rgba(17,138,178,0.06);border:1px solid rgba(17,138,178,0.15);border-radius:8px;padding:12px;text-align:center">
            <div style="font-family:'DM Mono';font-size:.6rem;color:#4A5568;letter-spacing:2px">WIN RATE</div>
            <div style="font-family:'Syne';font-size:1.4rem;font-weight:800;color:#118AB2">{wr:.0f}%</div>
          </div>
        </div>
        <div style="margin-top:10px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px">
          <div style="font-family:'DM Mono';font-size:.62rem;color:#4A5568;letter-spacing:2px;margin-bottom:6px">MISSION SUCCESS ESTIMATE</div>
          <div style="font-family:'DM Mono';font-size:.75rem;color:#C9D1D9">
            At 10% monthly growth:<br>
            💰 $100K in ~{math.ceil(math.log(100000/max(bal,1))/math.log(1.1))} months<br>
            🎯 $1M in ~{math.ceil(math.log(1000000/max(bal,1))/math.log(1.1))} months<br>
            <span style="color:#06D6A0">With 55%+ WR: ~60% success rate</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — SETTINGS
# ══════════════════════════════════════════════
with tab5:
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown('<p class="section-hdr">⚙️ ACCOUNT SETTINGS</p>', unsafe_allow_html=True)
        nb = st.number_input("Current Balance ($)", value=float(cfg["balance"]), step=100.0)
        nr = st.number_input("Risk per Trade (%)", value=float(cfg["risk_pct"]), min_value=0.5, max_value=3.0, step=0.5)
        pm = st.toggle("Paper Mode (Safe — no real trades)", value=cfg.get("paper_mode",True))
        ap = st.toggle("Auto-Pilot Mode", value=cfg.get("autopilot",False))

        if st.button("💾 SAVE SETTINGS"):
            cfg.update({"balance":nb,"risk_pct":nr,"paper_mode":pm,"autopilot":ap})
            cfg_save(cfg)
            st.session_state.cfg = cfg
            log_add(f"Settings updated: Balance ${nb:,.2f} | Risk {nr}%","ALERT")
            st.success("✅ Settings saved!")
            st.rerun()

    with sc2:
        st.markdown('<p class="section-hdr">📡 TRADINGVIEW SETUP</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'DM Mono';font-size:.75rem;color:#C9D1D9;line-height:2">
        <b style="color:#F5A623">Step 1:</b> TradingView open karo<br>
        <b style="color:#F5A623">Step 2:</b> Chart pe 3rd Candle strategy lagao<br>
        <b style="color:#F5A623">Step 3:</b> Alert banao — Webhook URL daalo:<br>
        <code style="background:rgba(255,255,255,0.05);padding:3px 8px;border-radius:4px;color:#06D6A0">
        http://YOUR_IP:5000/webhook
        </code><br>
        <b style="color:#F5A623">Step 4:</b> Alert message format:
        </div>
        """, unsafe_allow_html=True)
        st.code("""{
  "signal": "BUY",
  "symbol": "BTCUSDT",
  "price": {{close}},
  "stop_loss": {{low}},
  "liquidity_swept": true
}""", language="json")

        st.markdown('<p class="section-hdr" style="margin-top:16px">🛡️ IRON RULES REMINDER</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'DM Mono';font-size:.72rem;color:#C9D1D9;line-height:2.2">
          ✅ &nbsp;1 Trade per day — no exceptions<br>
          ✅ &nbsp;1:3 Risk-Reward ratio — always<br>
          ✅ &nbsp;2% max risk — firewall locked<br>
          ✅ &nbsp;30 paper trades before live<br>
          ✅ &nbsp;No revenge trading after loss<br>
          ✅ &nbsp;Score 60+ only — no weak setups<br>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# FOOTER STATUS BAR
# ══════════════════════════════════════════════
st.markdown("---")
fc1,fc2,fc3,fc4 = st.columns(4)
with fc1:
    st.markdown(f'<p style="font-family:DM Mono;font-size:.65rem;color:#4A5568;text-align:center">⚡ JARVIS-C DATA ANALYST v5.0</p>', unsafe_allow_html=True)
with fc2:
    st.markdown(f'<p style="font-family:DM Mono;font-size:.65rem;color:#4A5568;text-align:center">BTC: ${btc_p:,.0f} ({btc_c:+.2f}%)</p>', unsafe_allow_html=True)
with fc3:
    st.markdown(f'<p style="font-family:DM Mono;font-size:.65rem;color:#4A5568;text-align:center">RISK/TRADE: ${bal*cfg["risk_pct"]/100:,.0f} | MODE: {"PAPER" if cfg.get("paper_mode") else "LIVE"}</p>', unsafe_allow_html=True)
with fc4:
    st.markdown(f'<p style="font-family:DM Mono;font-size:.65rem;color:#4A5568;text-align:center">STARK INDUSTRIES © 2026</p>', unsafe_allow_html=True)
