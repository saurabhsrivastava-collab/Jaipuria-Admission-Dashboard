import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Jaipuria Admission Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* Hide Streamlit Menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Main Layout */
.block-container{
    padding-top:0.1rem;
    padding-left:2rem;
    padding-right:2rem;
    max-width:100%;
}

/* Sidebar logo */
.jaipuria-sidebar-logo {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 2px 0 10px 0;
}
.jaipuria-sidebar-logo img {
    width: 245px;
    max-width: 92%;
    height: auto;
    display: block;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0F172A;
    width:320px !important;
}

section[data-testid="stSidebar"] *{
    color:white !important;
    font-size:18px !important;
}

/* Headings */
h1{
    font-size:44px !important;
    font-weight:700 !important;
    margin-top:-1.5rem !important;
    margin-bottom:-0.65rem !important;
    line-height:1.1 !important;
}

/* Only compact the two top header elements and divider. */
.block-container > div:first-child div:has(h1) {
    margin-bottom:-0.35rem !important;
}
.block-container > div:first-child div:has(h3) {
    margin-top:-0.35rem !important;
    margin-bottom:-0.45rem !important;
}


h2{
    font-size:34px !important;
    margin-top:0 !important;
    margin-bottom:0 !important;
    line-height:1.1 !important;
}

h3{
    font-size:26px !important;
    margin-top:0 !important;
    margin-bottom:0 !important;
    line-height:1.2 !important;
}

/* Keep the top dashboard header compact — about 1.5-line spacing. */
.block-container > div:first-child {
    margin-top:0 !important;
}
[data-testid="stDivider"] {
    margin-top:0.2rem !important;
    margin-bottom:0.2rem !important;
}

p,span,div,label{
    font-size:18px !important;
}

/* Metric */
[data-testid="stMetricValue"]{
    font-size:42px !important;
}

[data-testid="stMetricLabel"]{
    font-size:20px !important;
}



/* ============================================================
   UNIVERSAL KPI BOX STYLE — applied across ALL dashboard tabs
   Keeps existing KPI content/layout, only upgrades the card design.
   ============================================================ */
.kpi-card, .owner-card, .sch-card {
    border: 1px solid #DCE5EF !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(15,23,42,.07) !important;
    overflow: hidden !important;
    position: relative !important;
    transition: transform .2s ease, box-shadow .2s ease !important;
    animation: jaipuria-kpi-float 3.6s ease-in-out infinite !important;
    will-change: transform;
}
.kpi-card:hover, .owner-card:hover, .sch-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(15,23,42,.12) !important;
}

/* Entrance Exam cards */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(1) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(1) .sch-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(1) .owner-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(1) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#EFF6FF 100%) !important;
    border-left: 5px solid #2563EB !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(2) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(2) .sch-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(2) .owner-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(2) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#F5F3FF 100%) !important;
    border-left: 5px solid #7C3AED !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(3) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(3) .sch-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(3) .owner-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(3) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#ECFEFF 100%) !important;
    border-left: 5px solid #0891B2 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(4) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(4) .sch-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(4) .owner-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(4) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#FFF7ED 100%) !important;
    border-left: 5px solid #EA580C !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(5) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(5) .sch-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(5) .owner-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(5) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#ECFDF5 100%) !important;
    border-left: 5px solid #059669 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(6) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(6) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#FFF1F2 100%) !important;
    border-left: 5px solid #E11D48 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(7) .kpi-card,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(7) [data-testid="stMetric"] {
    background: linear-gradient(145deg,#FFFFFF 0%,#F0FDFA 100%) !important;
    border-left: 5px solid #0F766E !important;
}

/* Gentle synchronized up/down floating for every visible KPI box */
.kpi-card, .owner-card, .sch-card, .tab-kpi-card, .cc-kpi-card, [data-testid="stMetric"] {
    animation: jaipuria-kpi-float 3.6s ease-in-out infinite !important;
    animation-delay: 0s !important;
    will-change: transform;
}

@keyframes jaipuria-kpi-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* ------------------------------------------------------------
   TAB-SPECIFIC KPI PALETTES
   Each dashboard tab gets its own colour family while keeping
   the same clean card structure.
   ------------------------------------------------------------ */
.kpi-tab-marker { display:none !important; }

/* Insights — blue / violet / teal / amber */
.kpi-scope-insights div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(1) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#EFF6FF)!important;border-bottom:4px solid #2563EB!important; }
.kpi-scope-insights div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(2) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#F5F3FF)!important;border-bottom:4px solid #7C3AED!important; }
.kpi-scope-insights div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(3) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#ECFEFF)!important;border-bottom:4px solid #0891B2!important; }
.kpi-scope-insights div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(4) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#FFF7ED)!important;border-bottom:4px solid #EA580C!important; }

/* Gender — rose / indigo / emerald / orange */
.kpi-scope-gender div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(1) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#FFF1F2)!important;border-bottom:4px solid #E11D48!important; }
.kpi-scope-gender div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(2) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#EEF2FF)!important;border-bottom:4px solid #4F46E5!important; }
.kpi-scope-gender div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(3) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#ECFDF5)!important;border-bottom:4px solid #059669!important; }
.kpi-scope-gender div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(4) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#FFF7ED)!important;border-bottom:4px solid #F97316!important; }

/* Stream — violet / cyan / lime / sky */
.kpi-scope-stream div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(1) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#F5F3FF)!important;border-bottom:4px solid #8B5CF6!important; }
.kpi-scope-stream div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(2) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#ECFEFF)!important;border-bottom:4px solid #06B6D4!important; }
.kpi-scope-stream div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(3) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#F7FEE7)!important;border-bottom:4px solid #65A30D!important; }
.kpi-scope-stream div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(4) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#F0F9FF)!important;border-bottom:4px solid #0284C7!important; }

/* State & City — sky / teal / amber / red */
.kpi-scope-geo div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(1) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#EFF6FF)!important;border-bottom:4px solid #0284C7!important; }
.kpi-scope-geo div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(2) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#F0FDFA)!important;border-bottom:4px solid #0D9488!important; }
.kpi-scope-geo div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(3) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#FFFBEB)!important;border-bottom:4px solid #D97706!important; }
.kpi-scope-geo div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]):nth-child(4) [data-testid="stMetric"] { background:linear-gradient(145deg,#FFFFFF,#FFF1F2)!important;border-bottom:4px solid #DC2626!important; }

/* Owner — indigo / gold / teal / purple / rose */
.kpi-scope-owner div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(1) .owner-card { background:linear-gradient(145deg,#FFFFFF,#EEF2FF)!important;border-left:5px solid #4F46E5!important; }
.kpi-scope-owner div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(2) .owner-card { background:linear-gradient(145deg,#FFFFFF,#FFFBEB)!important;border-left:5px solid #D97706!important; }
.kpi-scope-owner div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(3) .owner-card { background:linear-gradient(145deg,#FFFFFF,#F0FDFA)!important;border-left:5px solid #0D9488!important; }
.kpi-scope-owner div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(4) .owner-card { background:linear-gradient(145deg,#FFFFFF,#F5F3FF)!important;border-left:5px solid #9333EA!important; }
.kpi-scope-owner div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.owner-card):nth-child(5) .owner-card { background:linear-gradient(145deg,#FFFFFF,#FFF1F2)!important;border-left:5px solid #E11D48!important; }

/* Scholarship — emerald / gold / blue / purple / coral */
.kpi-scope-scholarship div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(1) .sch-card { background:linear-gradient(145deg,#FFFFFF,#ECFDF5)!important;border-left:5px solid #059669!important; }
.kpi-scope-scholarship div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(2) .sch-card { background:linear-gradient(145deg,#FFFFFF,#FFFBEB)!important;border-left:5px solid #D97706!important; }
.kpi-scope-scholarship div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(3) .sch-card { background:linear-gradient(145deg,#FFFFFF,#EFF6FF)!important;border-left:5px solid #2563EB!important; }
.kpi-scope-scholarship div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(4) .sch-card { background:linear-gradient(145deg,#FFFFFF,#F5F3FF)!important;border-left:5px solid #7C3AED!important; }
.kpi-scope-scholarship div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.sch-card):nth-child(5) .sch-card { background:linear-gradient(145deg,#FFFFFF,#FFF1F2)!important;border-left:5px solid #F43F5E!important; }

/* Entrance Exam — seven distinct exam colours */
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(1) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#EEF2FF)!important;border-left:5px solid #4F46E5!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(2) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#EFF6FF)!important;border-left:5px solid #2563EB!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(3) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#ECFDF5)!important;border-left:5px solid #059669!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(4) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#ECFEFF)!important;border-left:5px solid #0891B2!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(5) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#FFF1F2)!important;border-left:5px solid #E11D48!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(6) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#FFF7ED)!important;border-left:5px solid #EA580C!important; }
.kpi-scope-entrance div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.kpi-card):nth-child(7) .kpi-card { background:linear-gradient(145deg,#FFFFFF,#F5F3FF)!important;border-left:5px solid #7C3AED!important; }

/* Streamlit native metric cards used by Insights / Gender / Stream / State & City */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]) [data-testid="stMetric"] {
    min-height: 104px !important;
    padding: 18px 18px 16px 18px !important;
    box-sizing: border-box !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 14px rgba(15,23,42,.07) !important;
    border-top: 1px solid #DCE5EF !important;
    border-right: 1px solid #DCE5EF !important;
    border-bottom: 4px solid #DCE5EF !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]) [data-testid="stMetricLabel"] {
    font-weight: 700 !important;
    color: #526174 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has([data-testid="stMetric"]) [data-testid="stMetricValue"] {
    font-weight: 800 !important;
    color: #1E293B !important;
}

/* Common card typography */
.owner-card-label, .sch-label { color:#526174 !important; font-weight:700 !important; }
.owner-card-value, .sch-value { color:#1E293B !important; font-weight:800 !important; }
.owner-card-note, .sch-note { color:#94A3B8 !important; }

</style>
""", unsafe_allow_html=True)
# ---------------- Sidebar ----------------

JAIPURIA_LOGO_B64 = "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"
st.sidebar.markdown(
    f'<div class="jaipuria-sidebar-logo"><img src="data:image/webp;base64,{JAIPURIA_LOGO_B64}" alt="Jaipuria Institute of Management"></div>',
    unsafe_allow_html=True,
)
# IMPORTANT PERFORMANCE FIX
# Data is kept in Streamlit session_state after the first load.
# Earlier, st.cache_data returned a fresh copy of large DataFrames on every
# tab click/rerun, which could make navigation noticeably slow.
if st.sidebar.button("🔄 Refresh Live Data", use_container_width=True):
    for _k in ["_jaipuria_data", "_jaipuria_data_loaded"]:
        st.session_state.pop(_k, None)
    st.cache_data.clear()
    st.rerun()

page = st.sidebar.radio(
    "Navigation",
    [
        "🚀 Command Center",
        "🎯 Insights",
        "👨 Gender",
        "🎓 Stream",
        "📝 Entrance Exam",
        "📍 State & City",
        "👤 Owner Analysis",
        "💰 Scholarship",
        "📥 Download Report"
    ]
)

# ---------------- Main Page ----------------

st.title("🎓 Jaipuria Admission Dashboard")
st.subheader("Live Google Sheet Connected 🟢")
st.divider()


# ============================================================
# FILTER / CURRENT VIEW NAVIGATION STYLE
# ============================================================
st.markdown("""
<style>
.jaipuria-filter-title {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #243447;
    margin: 4px 0 0 0;
    padding-bottom: 7px;
    border-bottom: 5px solid #F59E0B;
    line-height: 1.15;
}
.jaipuria-filter-area {
    margin-top: 12px;
}
/* Command Center KPI cards: colourful static cards */
.cc-kpi-boxes {
    width: 100%;
    display: flex;
    gap: 18px;
    margin: 18px 0 20px 0;
    align-items: stretch;
}
.cc-kpi-card {
    flex: 1 1 0;
    min-width: 0;
    min-height: 104px;
    padding: 18px 18px 16px 18px;
    box-sizing: border-box;
    border: 1px solid #DCE5EF;
    border-radius: 14px;
    background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
    box-shadow: 0 4px 14px rgba(15,23,42,.07);
    transition: transform .2s ease, box-shadow .2s ease;
    position: relative;
    overflow: hidden;
}
.cc-kpi-card::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 4px;
    border-radius: 0 0 14px 14px;
}
.cc-kpi-card:nth-child(1) {
    border-left: 5px solid #2563EB;
    background: linear-gradient(145deg, #FFFFFF 0%, #EFF6FF 100%);
}
.cc-kpi-card:nth-child(1)::after { background: #2563EB; }
.cc-kpi-card:nth-child(2) {
    border-left: 5px solid #7C3AED;
    background: linear-gradient(145deg, #FFFFFF 0%, #F5F3FF 100%);
}
.cc-kpi-card:nth-child(2)::after { background: #7C3AED; }
.cc-kpi-card:nth-child(3) {
    border-left: 5px solid #0891B2;
    background: linear-gradient(145deg, #FFFFFF 0%, #ECFEFF 100%);
}
.cc-kpi-card:nth-child(3)::after { background: #0891B2; }
.cc-kpi-card:nth-child(4) {
    border-left: 5px solid #EA580C;
    background: linear-gradient(145deg, #FFFFFF 0%, #FFF7ED 100%);
}
.cc-kpi-card:nth-child(4)::after { background: #EA580C; }
.cc-kpi-card:nth-child(5) {
    border-left: 5px solid #059669;
    background: linear-gradient(145deg, #FFFFFF 0%, #ECFDF5 100%);
}
.cc-kpi-card:nth-child(5)::after { background: #059669; }
.cc-kpi-card:hover {
    box-shadow: 0 8px 20px rgba(15,23,42,.12);
}
.cc-kpi-title {
    color: #526174;
    font-size: 14px;
    font-weight: 700;
    line-height: 1.25;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tab-kpi-grid {
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:18px;
    width:100%;
    margin:14px 0 20px 0;
}
.tab-kpi-card {
    min-height:96px;
    padding:16px 18px 14px 18px;
    box-sizing:border-box;
    border:1px solid #DCE5EF;
    border-left:5px solid var(--kpi-accent);
    border-radius:14px;
    background:linear-gradient(145deg,#FFFFFF 0%,#F8FAFC 100%);
    box-shadow:0 4px 14px rgba(15,23,42,.07);
    position:relative;
    overflow:hidden;
    transition:transform .2s ease, box-shadow .2s ease;
}
.tab-kpi-card::after {
    content:"";
    position:absolute;
    left:0; right:0; bottom:0;
    height:4px;
    background:var(--kpi-accent);
    opacity:.9;
}
.tab-kpi-card:hover { box-shadow:0 8px 20px rgba(15,23,42,.12); }
.tab-kpi-label { color:#475569; font-size:15px!important; font-weight:700!important; line-height:1.25; }
.tab-kpi-value { color:#1E293B; font-size:25px!important; font-weight:850!important; line-height:1.2; margin-top:7px; word-break:break-word; }
@media (max-width:900px) { .tab-kpi-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:560px) { .tab-kpi-grid { grid-template-columns:1fr; } }

.cc-kpi-value {
    color: #1E293B;
    font-size: 21px;
    font-weight: 800;
    line-height: 1.2;
    margin-top: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
@media (max-width: 1100px) {
    .cc-kpi-boxes { gap: 12px; }
    .cc-kpi-card { padding: 15px 13px; }
    .cc-kpi-title { font-size: 13px; }
    .cc-kpi-value { font-size: 18px; }
}
@media (max-width: 700px) {
    .jaipuria-filter-title { font-size: 19px !important; }
}

/* Page heading motion: the selected tab heading gently travels left ↔ right. */
.jaipuria-page-heading-wrap {
    width: 100%;
    overflow: hidden;
    margin: -25px 0 5px 0 !important;
    position: relative;
    min-height: 34px;
}
.jaipuria-page-heading {
    display: block;
    width: max-content;
    white-space: nowrap;
    color: #26384B;
    font-size: 25px;
    font-weight: 800;
    line-height: 1.25;
    animation: jaipuria-heading-ltr 5.5s ease-in-out infinite alternate;
    will-change: transform;
}
/* Full-width travel: heading starts at the left edge and reaches the right edge. */
@keyframes jaipuria-heading-ltr {
    0%   { transform: translateX(0); }
    100% { transform: translateX(calc(100vw - 380px - 100%)); }
}
.entrance-page-title, .owner-title, .sch-title {
    position: relative;
    width: max-content;
    animation: jaipuria-heading-ltr 5.5s ease-in-out infinite alternate;
    will-change: transform;
}
@media (prefers-reduced-motion: reduce) {
    .jaipuria-page-heading, .entrance-page-title, .owner-title, .sch-title {
        animation: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

def show_colour_kpi_cards(items, theme="blue"):
    """Render static colourful KPI cards; each dashboard tab can use its own palette."""
    import html
    palettes = {
        "insights": ["#2563EB", "#7C3AED", "#0891B2", "#EA580C"],
        "gender": ["#E11D48", "#4F46E5", "#059669", "#F97316"],
        "stream": ["#8B5CF6", "#06B6D4", "#65A30D", "#0284C7"],
        "geo": ["#0284C7", "#0D9488", "#D97706", "#DC2626"],
    }
    colors = palettes.get(theme, palettes["insights"])
    cards = []
    for i, (label, value) in enumerate(items):
        color = colors[i % len(colors)]
        safe_label = html.escape(str(label))
        safe_value = html.escape(str(value))
        cards.append(
            f"""<div class='tab-kpi-card' style='--kpi-accent:{color};'>
                <div class='tab-kpi-label'>{safe_label}</div>
                <div class='tab-kpi-value'>{safe_value}</div>
            </div>"""
        )
    st.markdown("<div class='tab-kpi-grid'>" + "".join(cards) + "</div>", unsafe_allow_html=True)


def show_page_heading(text):
    import html
    st.markdown(
        f"<div class='jaipuria-page-heading-wrap'><div class='jaipuria-page-heading'>{html.escape(str(text))}</div></div>",
        unsafe_allow_html=True,
    )

def show_command_center_kpi_cards(items):
    import html
    cards = "".join(
        f"""<div class='cc-kpi-card'>
                <div class='cc-kpi-title'>{html.escape(title)}</div>
                <div class='cc-kpi-value'>{html.escape(value)}</div>
            </div>"""
        for title, value in items
    )
    st.markdown(f"""
    <div class='cc-kpi-boxes'>
        {cards}
    </div>
    """, unsafe_allow_html=True)

SHEET_ID = "1RKLRXNSFxeq4kXEYxA9y0EFuK-5Ozukrr3ejjxm0764"

# ============================================================
# FAST DATA LOADING
# Google Sheet data is downloaded only once per browser session.
# All tab switches reuse the same in-memory DataFrames.
# ============================================================
@st.cache_data(ttl=3600, show_spinner=False)
def load_sheet(gid, batch):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    data = pd.read_csv(url, low_memory=False)
    data.columns = data.columns.astype(str).str.strip()
    data["Batch"] = batch
    return data

@st.cache_data(ttl=3600, show_spinner=False)
def load_all_data():
    df2026 = load_sheet(0, "2026-28")
    df2025 = load_sheet(1713921462, "2025-27")
    df2024 = load_sheet(1951957125, "2024-26")
    combined = pd.concat([df2026, df2025, df2024], ignore_index=True, copy=False)
    return df2026, df2025, df2024, combined

# session_state avoids repeated cache deserialization/copying on every widget click
if "_jaipuria_data" not in st.session_state:
    with st.spinner("Loading admission data for the first time..."):
        st.session_state["_jaipuria_data"] = load_all_data()

df2026, df2025, df2024, df = st.session_state["_jaipuria_data"]

if page == "🎯 Insights":

    show_page_heading("🎯 Insights Dashboard")
    admitted_status = ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
    summary_df = df[df["Final Status"].isin(admitted_status)].copy()

    # ---------------- Modern Filters / Slicers ----------------
    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div><div class="jaipuria-filter-area">', unsafe_allow_html=True)
    f1,f2,f3,f4 = st.columns(4)
    prog_col = "Final Course Selected" if "Final Course Selected" in summary_df.columns else None
    gender_col = "Gender" if "Gender" in summary_df.columns else None
    state_col = "Correspondence State" if "Correspondence State" in summary_df.columns else None
    programs = sorted(summary_df[prog_col].dropna().astype(str).unique()) if prog_col else []
    genders = sorted(summary_df[gender_col].dropna().astype(str).str.upper().unique()) if gender_col else []
    states = sorted(summary_df[state_col].dropna().astype(str).unique()) if state_col else []
    with f1:
        batch_filter = st.selectbox("Batch", ["All Batches","2024-26","2025-27","2026-28"], key="summary_batch")
    with f2:
        programme_filter = st.selectbox("Programme", ["All Programmes"] + programs, key="summary_programme")
    with f3:
        gender_filter = st.selectbox("Gender", ["All Genders"] + genders, key="summary_gender")
    with f4:
        state_filter = st.selectbox("State", ["All States"] + states, key="summary_state")
    st.markdown("</div>", unsafe_allow_html=True)

    filtered = summary_df.copy()
    if batch_filter != "All Batches":
        filtered = filtered[filtered["Batch"] == batch_filter]
    if prog_col and programme_filter != "All Programmes":
        filtered = filtered[filtered[prog_col].astype(str) == programme_filter]
    if gender_col and gender_filter != "All Genders":
        filtered = filtered[filtered[gender_col].astype(str).str.upper() == gender_filter]
    if state_col and state_filter != "All States":
        filtered = filtered[filtered[state_col].astype(str) == state_filter]

    # ---------------- KPI Cards ----------------
    academic_mask = pd.Series(True, index=filtered.index)
    for c in ["10th Percentage","12th Percentage","Graduation Percentage"]:
        if c in filtered.columns:
            academic_mask &= pd.to_numeric(filtered[c], errors="coerce").ge(60)
        else:
            academic_mask &= False
    eligible_df = filtered[academic_mask]
    batch_counts = filtered.groupby("Batch").size().reindex(["2024-26","2025-27","2026-28"], fill_value=0)

    show_colour_kpi_cards([
        ("👨‍🎓 Total Admitted Students", f"{len(filtered):,}"),
        ("🎯 60%+ Throughout", f"{len(eligible_df):,}"),
        ("🎓 Top Programme", filtered[prog_col].mode().iloc[0] if prog_col and not filtered.empty and not filtered[prog_col].dropna().empty else "—"),
        ("🏆 Best Performing Batch", batch_counts.idxmax() if batch_counts.sum()>0 else "—")
    ], "insights")

    st.divider()
    c1,c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("📈 Total Admission Trend")
        trend = batch_counts.rename_axis("Batch").reset_index(name="Students")
        fig = px.line(trend, x="Batch", y="Students", markers=True, text="Students")
        fig.update_traces(line_width=4, textposition="top center")
        fig.update_layout(template="plotly_white", height=420, margin=dict(l=20,r=20,t=35,b=20), yaxis_title="Students")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("🎯 Academic Quality by Batch")
        q = eligible_df.groupby("Batch").size().reindex(["2024-26","2025-27","2026-28"], fill_value=0).rename_axis("Batch").reset_index(name="Students")
        fig = px.bar(q, x="Batch", y="Students", text="Students", color="Batch")
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white", height=420, showlegend=False, margin=dict(l=20,r=20,t=35,b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏅 Programme-wise Admissions")
    if prog_col and not filtered.empty:
        ps = filtered.groupby(prog_col).size().reset_index(name="Students").sort_values("Students", ascending=False)
        fig = px.bar(ps.head(12), x="Students", y=prog_col, orientation="h", text="Students", color="Students", color_continuous_scale="Blues")
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(template="plotly_white", height=480, coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Selected filters ke liye data available nahi hai.")

elif page == "👨 Gender":

    show_page_heading("👨 Gender Analysis")
    admitted_status=["FULL FEE","PARTIAL FEE","WAITLIST FEE"]
    gender_df=df[df["Final Status"].isin(admitted_status)].copy()
    gender_df["Gender"]=gender_df["Gender"].fillna("Not Available").astype(str).str.upper().replace({"M":"MALE","F":"FEMALE"})

    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div><div class="jaipuria-filter-area">', unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    programme_col="Final Course Selected" if "Final Course Selected" in gender_df.columns else None
    gprogrammes=sorted(gender_df[programme_col].dropna().astype(str).unique()) if programme_col else []
    with f1: gbatch_filter=st.selectbox("Batch",["All Batches","2024-26","2025-27","2026-28"],key="gender_batch")
    with f2: ggender_filter=st.selectbox("Gender",["All Genders"]+sorted(gender_df["Gender"].unique()),key="gender_gender")
    with f3: gprogramme_filter=st.selectbox("Programme",["All Programmes"]+gprogrammes,key="gender_programme")
    st.markdown("</div>", unsafe_allow_html=True)

    gfiltered=gender_df.copy()
    if gbatch_filter != "All Batches": gfiltered=gfiltered[gfiltered["Batch"]==gbatch_filter]
    if ggender_filter != "All Genders": gfiltered=gfiltered[gfiltered["Gender"]==ggender_filter]
    if programme_col and gprogramme_filter != "All Programmes": gfiltered=gfiltered[gfiltered[programme_col].astype(str)==gprogramme_filter]

    summary=(gfiltered.groupby(["Batch","Gender"]).size().unstack(fill_value=0)
             .reindex(index=["2024-26","2025-27","2026-28"],fill_value=0))
    for c in ["MALE","FEMALE"]:
        if c not in summary.columns: summary[c]=0
    summary=summary.reset_index()
    summary["Total"]=summary[["MALE","FEMALE"]].sum(axis=1)

    top_batch=summary.loc[summary["Total"].idxmax(),"Batch"] if not summary.empty and summary["Total"].sum()>0 else "—"
    show_colour_kpi_cards([
        ("👨 Male", int(gfiltered["Gender"].eq("MALE").sum())),
        ("👩 Female", int(gfiltered["Gender"].eq("FEMALE").sum())),
        ("👥 Total", len(gfiltered)),
        ("🏆 Best Batch", top_batch)
    ], "gender")

    c1,c2=st.columns(2,gap="large")
    with c1:
        st.subheader("📊 Year-wise Gender Comparison")
        long=summary.melt(id_vars="Batch",value_vars=["MALE","FEMALE"],var_name="Gender",value_name="Students")
        fig=px.bar(long,x="Batch",y="Students",color="Gender",barmode="group",text="Students",color_discrete_map={"MALE":"#2563EB","FEMALE":"#EC4899"})
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white",height=470)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.subheader("🥧 Overall Gender Mix")
        mix=gfiltered.groupby("Gender").size().reset_index(name="Students")
        if not mix.empty:
            fig=px.pie(mix,names="Gender",values="Students",hole=.58)
            fig.update_traces(textinfo="percent+label")
            fig.update_layout(template="plotly_white",height=470)
            st.plotly_chart(fig,use_container_width=True)

    st.subheader("🎓 Gender Distribution by Programme")
    if programme_col and not gfiltered.empty:
        gp=gfiltered.groupby([programme_col,"Gender"]).size().reset_index(name="Students")
        fig=px.bar(gp,x=programme_col,y="Students",color="Gender",barmode="stack",text="Students",color_discrete_map={"MALE":"#2563EB","FEMALE":"#EC4899"})
        fig.update_layout(template="plotly_white",height=480,xaxis_tickangle=-25)
        st.plotly_chart(fig,use_container_width=True)

elif page == "🎓 Stream":

    show_page_heading("🎓 Graduation Stream Analysis")
    admitted_status=["FULL FEE","PARTIAL FEE","WAITLIST FEE"]
    stream_df=df[df["Final Status"].isin(admitted_status)].copy()
    stream_col="Graduation Stream"
    stream_df[stream_col]=stream_df[stream_col].fillna("Not Available").astype(str).str.strip().replace("","Not Available")

    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div><div class="jaipuria-filter-area">', unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    streams=sorted(stream_df[stream_col].unique())
    programme_col="Final Course Selected" if "Final Course Selected" in stream_df.columns else None
    sprogrammes=sorted(stream_df[programme_col].dropna().astype(str).unique()) if programme_col else []
    with f1: sbatch_filter=st.selectbox("Batch",["All Batches","2024-26","2025-27","2026-28"],key="stream_batch")
    with f2: stream_filter=st.selectbox("Graduation Stream",["All Streams"]+streams,key="stream_filter")
    with f3: sprogramme_filter=st.selectbox("Programme",["All Programmes"]+sprogrammes,key="stream_programme")
    st.markdown("</div>", unsafe_allow_html=True)

    sfiltered=stream_df.copy()
    if sbatch_filter != "All Batches": sfiltered=sfiltered[sfiltered["Batch"]==sbatch_filter]
    if stream_filter != "All Streams": sfiltered=sfiltered[sfiltered[stream_col]==stream_filter]
    if programme_col and sprogramme_filter != "All Programmes": sfiltered=sfiltered[sfiltered[programme_col].astype(str)==sprogramme_filter]

    stream_summary=(sfiltered.groupby([stream_col,"Batch"]).size().unstack(fill_value=0)
                    .reindex(columns=["2024-26","2025-27","2026-28"],fill_value=0).reset_index())
    stream_summary["Total"]=stream_summary[["2024-26","2025-27","2026-28"]].sum(axis=1)

    top_stream=stream_summary.sort_values("Total",ascending=False).iloc[0][stream_col] if not stream_summary.empty else "—"
    top_batch=sfiltered.groupby("Batch").size().idxmax() if not sfiltered.empty else "—"
    show_colour_kpi_cards([
        ("👨‍🎓 Total Students", len(sfiltered)),
        ("🎓 Active Streams", sfiltered[stream_col].nunique()),
        ("🏆 Top Stream", top_stream),
        ("📈 Best Batch", top_batch)
    ], "stream")

    c1,c2=st.columns([1.2,1],gap="large")
    with c1:
        st.subheader("📊 Stream-wise Comparison")
        long=stream_summary.melt(id_vars=stream_col,value_vars=["2024-26","2025-27","2026-28"],var_name="Batch",value_name="Students")
        fig=px.bar(long,x=stream_col,y="Students",color="Batch",barmode="group",text="Students")
        fig.update_traces(textposition="outside")
        fig.update_layout(template="plotly_white",height=500,xaxis_tickangle=-25)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.subheader("🥧 Overall Stream Mix")
        mix=sfiltered.groupby(stream_col).size().reset_index(name="Students").sort_values("Students",ascending=False).head(10)
        if not mix.empty:
            fig=px.pie(mix,names=stream_col,values="Students",hole=.55)
            fig.update_layout(template="plotly_white",height=500)
            st.plotly_chart(fig,use_container_width=True)

    st.subheader("📋 Live Stream Summary")
    st.dataframe(stream_summary.sort_values("Total",ascending=False),use_container_width=True,hide_index=True)

elif page == "📝 Entrance Exam":


    # =========================================================
    # ENTRANCE EXAM ANALYSIS — EXACT IMAGE STYLE
    # =========================================================
    st.markdown("""
    <style>
    .entrance-page-title{font-size:30px!important;font-weight:800!important;color:#243447;margin:0 0 8px 0}
    .batch-note{margin-top:25px;background:#EAF2FF;border-left:4px solid #2F80ED;border-radius:10px;padding:14px 18px;color:#31445A;font-size:15px!important;font-weight:600;min-height:52px;display:flex;align-items:center}
    .kpi-card{background:#fff;border:1px solid #E5E7EB;border-radius:14px;padding:13px 16px;min-height:86px;box-shadow:0 2px 8px rgba(15,23,42,.06);display:flex;align-items:center;gap:13px}
    .kpi-icon{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:23px!important;flex-shrink:0}
    .kpi-label{color:#64748B;font-size:13px!important;font-weight:700;line-height:1.1}
    .kpi-value{color:#1E293B;font-size:26px!important;font-weight:850;line-height:1.2;margin-top:4px}
    .section-heading{color:#26384B;font-size:20px!important;font-weight:800;margin:16px 0 10px 0}
    .exam-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;width:100%;margin-top:8px}
    .exam-box{background:#fff;border-radius:10px;overflow:hidden;border:1px solid #E2E8F0;box-shadow:0 2px 8px rgba(15,23,42,.05)}
    .exam-name{color:#fff;text-align:center;font-size:17px!important;font-weight:800;padding:9px 8px;letter-spacing:.3px}
    .score-table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:11px!important}
    .score-table th,.score-table td{border:1px solid #E2E8F0;padding:6px 3px;text-align:center;white-space:nowrap;font-size:11px!important;color:#334155}
    .score-table th{background:#F8FAFC;font-weight:750;color:#475569}
    .score-table .range-col{width:15%;text-align:left;padding-left:8px;white-space:normal}
    .score-table .year-head{background:#F1F5F9;font-size:11px!important;font-weight:800}
    .score-table .program-head{font-size:9px!important;padding:5px 1px}
    .score-table .grand-row td{color:#fff!important;font-weight:800;padding-top:7px;padding-bottom:7px}
    .score-table .grand-label{text-align:left!important;padding-left:8px!important}
    @media(max-width:1100px){.exam-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
    @media(max-width:700px){.exam-grid{grid-template-columns:1fr;}}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="entrance-page-title">🎯 Entrance Exam Analysis</div>', unsafe_allow_html=True)

    admitted_status=["FULL FEE","PARTIAL FEE","WAITLIST FEE"]
    exam_df=df[df["Final Status"].isin(admitted_status)].copy()
    # ============================================================
    # ENTRANCE EXAM FINAL LOGIC
    # EAS decides WHICH exam will be counted.
    # Percentile decides WHICH RANGE/BAND it will go into.
    #
    # CAT block:        AQ / AR / AS  -> CAT Exam / Percentile CAT / EAS
    # Other exam block: AT / AU / AV  -> Entrance Exam / Percentile score / EAS
    #
    # IMPORTANT: One student is counted in ONLY ONE exam.
    # ============================================================
    exam_df["Percentile CAT"] = pd.to_numeric(exam_df["Percentile CAT"], errors="coerce")
    exam_df["Percentile score"] = pd.to_numeric(exam_df["Percentile score"], errors="coerce")
    exam_df["Entrance Exam"] = exam_df["Entrance Exam"].fillna("").astype(str).str.upper().str.strip()
    exam_df["Final Course Selected"] = exam_df["Final Course Selected"].fillna("").astype(str).str.upper().str.strip()

    # Safely identify EAS columns by their position immediately after
    # the corresponding percentile columns. This works even when Google
    # Sheets has duplicate header names such as EAS and EAS.1.
    cat_eas_col = None
    other_eas_col = None

    try:
        cat_pct_pos = exam_df.columns.get_loc("Percentile CAT")
        if isinstance(cat_pct_pos, slice):
            cat_pct_pos = cat_pct_pos.start
        if isinstance(cat_pct_pos, int) and cat_pct_pos + 1 < len(exam_df.columns):
            cat_eas_col = exam_df.columns[cat_pct_pos + 1]
    except Exception:
        pass

    try:
        other_pct_pos = exam_df.columns.get_loc("Percentile score")
        if isinstance(other_pct_pos, slice):
            other_pct_pos = other_pct_pos.start
        if isinstance(other_pct_pos, int) and other_pct_pos + 1 < len(exam_df.columns):
            other_eas_col = exam_df.columns[other_pct_pos + 1]
    except Exception:
        pass

    # Additional fallback if the sheet structure changes.
    eas_like_cols = [c for c in exam_df.columns if str(c).strip().upper().startswith("EAS")]
    if cat_eas_col is None and len(eas_like_cols) >= 1:
        cat_eas_col = eas_like_cols[0]
    if other_eas_col is None and len(eas_like_cols) >= 2:
        other_eas_col = eas_like_cols[1]

    exam_df["_CAT_EAS"] = (
        pd.to_numeric(exam_df[cat_eas_col], errors="coerce")
        if cat_eas_col in exam_df.columns else pd.Series(float("nan"), index=exam_df.index)
    )
    exam_df["_OTHER_EAS"] = (
        pd.to_numeric(exam_df[other_eas_col], errors="coerce")
        if other_eas_col in exam_df.columns else pd.Series(float("nan"), index=exam_df.index)
    )

    # Final selected exam and its percentile.
    exam_df["_Winning_Exam"] = ""
    exam_df["_Winning_Percentile"] = float("nan")

    valid_other_exam = exam_df["Entrance Exam"].isin(["CMAT", "MAT", "XAT", "ATMA", "GMAT"])

    cat_ready = exam_df["_CAT_EAS"].notna() & exam_df["Percentile CAT"].notna()
    other_ready = (
        valid_other_exam
        & exam_df["_OTHER_EAS"].notna()
        & exam_df["Percentile score"].notna()
    )

    # Highest EAS wins. In an exact tie, CAT gets priority so there is
    # still no double counting.
    cat_wins = cat_ready & (~other_ready | (exam_df["_CAT_EAS"] >= exam_df["_OTHER_EAS"]))
    other_wins = other_ready & (~cat_ready | (exam_df["_OTHER_EAS"] > exam_df["_CAT_EAS"]))

    exam_df.loc[cat_wins, "_Winning_Exam"] = "CAT"
    exam_df.loc[cat_wins, "_Winning_Percentile"] = exam_df.loc[cat_wins, "Percentile CAT"]

    exam_df.loc[other_wins, "_Winning_Exam"] = exam_df.loc[other_wins, "Entrance Exam"]
    exam_df.loc[other_wins, "_Winning_Percentile"] = exam_df.loc[other_wins, "Percentile score"]

    # Safety fallback: if EAS is blank but only one exam has a valid percentile,
    # keep that student's available exam data instead of dropping the record.
    unresolved = exam_df["_Winning_Exam"].eq("")
    only_cat = unresolved & exam_df["Percentile CAT"].notna() & ~valid_other_exam
    exam_df.loc[only_cat, "_Winning_Exam"] = "CAT"
    exam_df.loc[only_cat, "_Winning_Percentile"] = exam_df.loc[only_cat, "Percentile CAT"]

    unresolved = exam_df["_Winning_Exam"].eq("")
    only_other = unresolved & valid_other_exam & exam_df["Percentile score"].notna() & exam_df["Percentile CAT"].isna()
    exam_df.loc[only_other, "_Winning_Exam"] = exam_df.loc[only_other, "Entrance Exam"]
    exam_df.loc[only_other, "_Winning_Percentile"] = exam_df.loc[only_other, "Percentile score"]

    batch_order=["2024-26","2025-27","2026-28"]
    exam_list=["CAT","CMAT","MAT","XAT","ATMA","GMAT"]

    # TOP ROW — SELECT BATCH + NOTE (exact reference layout)
    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div><div class="jaipuria-filter-area">', unsafe_allow_html=True)
    filter_col,note_col=st.columns([1.05,2.95],gap="small")
    with filter_col:
        selected_batch=st.selectbox("Select Batch",["All Batches"]+batch_order,key="entrance_batch_filter_exact")
    with note_col:
        st.markdown('<div class="batch-note">ℹ️ &nbsp; Note: PGDM-SM is not available for the 2026-28 batch.</div>',unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    display_df=exam_df.copy() if selected_batch=="All Batches" else exam_df[exam_df["Batch"]==selected_batch].copy()

    def get_exam_data(source_df, exam):
        # EAS has already selected the winning exam.
        # The winning exam's PERCENTILE is used for all table ranges.
        result = source_df[
            (source_df["_Winning_Exam"] == exam)
            & (pd.to_numeric(source_df["_Winning_Percentile"], errors="coerce").notna())
        ].copy()

        result["_Winning_Percentile"] = pd.to_numeric(
            result["_Winning_Percentile"], errors="coerce"
        )
        return result, "_Winning_Percentile"

    def programmes_for(batch):
        return ["PGDM-N","PGDM-M"] if batch=="2026-28" else ["PGDM-N","PGDM-M","PGDM-SM"]

    # KPI CARDS
    counts={}
    for exam in exam_list:
        t,c=get_exam_data(display_df,exam)
        counts[exam]=int(t[c].notna().sum())
    total_students=sum(counts.values())

    cards=[
        ("👤","Total Students",total_students,"#F0EAFE"),("📖","CAT",counts["CAT"],"#EAF2FF"),
        ("🟩","CMAT",counts["CMAT"],"#EAF8F2"),("📘","MAT",counts["MAT"],"#F4EAFE"),
        ("👥","XAT",counts["XAT"],"#FDEEEE"),("🔶","ATMA",counts["ATMA"],"#FFF3E3"),
        ("📄","GMAT",counts["GMAT"],"#EAF8F6")]
    st.markdown('<span class="kpi-tab-marker kpi-scope-entrance"></span>', unsafe_allow_html=True)
    kcols=st.columns(7,gap="small")
    for col,(icon,label,value,bg) in zip(kcols,cards):
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-icon" style="background:{bg};">{icon}</div><div><div class="kpi-label">{label}</div><div class="kpi-value">{value:,}</div></div></div>',unsafe_allow_html=True)

    # MODERN GRAPH — directly below cards (no summary table, exactly like image)
    graph_title="📊 Entrance Exam Wise Student Comparison (Year Wise)" if selected_batch=="All Batches" else f"📊 Entrance Exam Wise Student Comparison ({selected_batch})"
    st.markdown(f'<div class="section-heading">{graph_title}</div>',unsafe_allow_html=True)

    if selected_batch=="All Batches":
        rows=[]
        for exam in exam_list:
            t,_=get_exam_data(display_df,exam)
            for batch in batch_order:
                rows.append({"Entrance Exam":exam,"Batch":batch,"Students":int((t["Batch"]==batch).sum())})
        graph_df=pd.DataFrame(rows)
        fig=px.bar(graph_df,x="Entrance Exam",y="Students",color="Batch",barmode="group",text="Students",category_orders={"Entrance Exam":exam_list,"Batch":batch_order},color_discrete_map={"2024-26":"#2457B2","2025-27":"#169B62","2026-28":"#F21D2F"})
    else:
        rows=[]
        for exam in exam_list:
            t,_=get_exam_data(display_df,exam); rows.append({"Entrance Exam":exam,"Students":len(t)})
        graph_df=pd.DataFrame(rows)
        fig=px.bar(graph_df,x="Entrance Exam",y="Students",color="Entrance Exam",text="Students",category_orders={"Entrance Exam":exam_list},color_discrete_map={"CAT":"#1D3F91","CMAT":"#0E6B2D","MAT":"#563B78","XAT":"#E31C23","ATMA":"#E87400","GMAT":"#148C8C"})
    fig.update_traces(textposition="outside",cliponaxis=False,marker_line_width=0)
    fig.update_layout(template="plotly_white",height=350,margin=dict(l=35,r=20,t=15,b=35),plot_bgcolor="white",paper_bgcolor="white",hovermode="x unified",legend_title_text="Batch" if selected_batch=="All Batches" else "",font=dict(size=12,color="#334155"),xaxis_title="Entrance Exam",yaxis_title="Students",showlegend=(selected_batch=="All Batches"))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3",zeroline=False)
    st.plotly_chart(fig,use_container_width=True)

    # PROGRAMME-WISE SCORE RANGE SUMMARY
    section_title="🎯 Programme Wise Score Range Summary (Year Wise)" if selected_batch=="All Batches" else f"🎯 Programme Wise Score Range Summary ({selected_batch})"
    st.markdown(f'<div class="section-heading">{section_title}</div>',unsafe_allow_html=True)

    score_ranges=[("90 & Above",90,float("inf")),("80–89.99",80,89.999999),("70–79.99",70,79.999999),("60–69.99",60,69.999999),("50–59.99",50,59.999999),("40–49.99",40,49.999999)]
    exam_colors={"CAT":"#173A8A","CMAT":"#075D1D","MAT":"#4D2A70","XAT":"#E51B23","ATMA":"#E87000","GMAT":"#148B8B"}

    def build_exam_table(exam,source_df,score_col):
        color=exam_colors[exam]
        html=f'<div class="exam-box"><div class="exam-name" style="background:{color};">{exam}</div><table class="score-table"><thead>'
        if selected_batch=="All Batches":
            html+='<tr><th class="range-col" rowspan="2">Score Range /<br>Criteria</th>'
            for batch in batch_order:
                html+=f'<th class="year-head" colspan="{len(programmes_for(batch))}">{batch}</th>'
            html+='<th rowspan="2">Total</th></tr><tr>'
            for batch in batch_order:
                for programme in programmes_for(batch): html+=f'<th class="program-head">{programme}</th>'
            html+='</tr>'
        else:
            ps=programmes_for(selected_batch)
            html+='<tr><th class="range-col">Score Range /<br>Criteria</th>'+''.join(f'<th>{p}</th>' for p in ps)+'<th>Total</th></tr>'
        html+='</thead><tbody>'
        totals={}
        for label,low,high in score_ranges:
            ranged=source_df[source_df[score_col].notna()&(source_df[score_col]>=low)&(source_df[score_col]<=high)]
            html+=f'<tr><td class="range-col">{label}</td>'
            if selected_batch=="All Batches":
                for batch in batch_order:
                    bd=ranged[ranged["Batch"]==batch]
                    for p in programmes_for(batch):
                        v=int((bd["Final Course Selected"]==p).sum()); totals[f"{batch}|{p}"]=totals.get(f"{batch}|{p}",0)+v; html+=f'<td>{v}</td>'
            else:
                for p in programmes_for(selected_batch):
                    v=int((ranged["Final Course Selected"]==p).sum()); totals[p]=totals.get(p,0)+v; html+=f'<td>{v}</td>'
            rt=int(len(ranged)); totals["Total"]=totals.get("Total",0)+rt; html+=f'<td>{rt}</td></tr>'
        html+=f'<tr class="grand-row" style="background:{color};"><td class="grand-label">Grand Total</td>'
        if selected_batch=="All Batches":
            for batch in batch_order:
                for p in programmes_for(batch): html+=f'<td>{totals.get(f"{batch}|{p}",0)}</td>'
        else:
            for p in programmes_for(selected_batch): html+=f'<td>{totals.get(p,0)}</td>'
        html+=f'<td>{totals.get("Total",0)}</td></tr></tbody></table></div>'
        return html

    # EXACT IMAGE ARRANGEMENT: 3 + 3
    table_html='<div class="exam-grid">'
    for exam in exam_list:
        ed,sc=get_exam_data(display_df,exam)
        table_html+=build_exam_table(exam,ed,sc)
    table_html+='</div>'
    st.markdown(table_html,unsafe_allow_html=True)


elif page == "📍 State & City":

    show_page_heading("📍 State & City Analysis")
    admitted_status=["FULL FEE","PARTIAL FEE","WAITLIST FEE"]
    state_df=df[df["Final Status"].isin(admitted_status)].copy()
    state_col="Correspondence State"
    city_col="Correspondence city"
    state_df[state_col]=state_df[state_col].fillna("Not Available").astype(str).str.strip().replace("","Not Available")
    state_df[city_col]=state_df[city_col].fillna("Not Available").astype(str).str.strip().replace("","Not Available")

    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div><div class="jaipuria-filter-area">', unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    states=sorted(state_df[state_col].unique())
    cities=sorted(state_df[city_col].unique())
    with f1: cbatch_filter=st.selectbox("Batch",["All Batches","2024-26","2025-27","2026-28"],key="geo_batch")
    with f2: state_filter_geo=st.selectbox("State",["All States"]+states,key="geo_state")
    with f3: city_filter_geo=st.selectbox("City",["All Cities"]+cities,key="geo_city")
    st.markdown("</div>", unsafe_allow_html=True)

    geo=state_df.copy()
    if cbatch_filter != "All Batches": geo=geo[geo["Batch"]==cbatch_filter]
    if state_filter_geo != "All States": geo=geo[geo[state_col]==state_filter_geo]
    if city_filter_geo != "All Cities": geo=geo[geo[city_col]==city_filter_geo]

    state_total=geo.groupby(state_col).size().sort_values(ascending=False)
    city_total=geo.groupby(city_col).size().sort_values(ascending=False)
    show_colour_kpi_cards([
        ("👨‍🎓 Total Students", len(geo)),
        ("📍 States Covered", geo[state_col].nunique()),
        ("🏙️ Cities Covered", geo[city_col].nunique()),
        ("🏆 Top State", state_total.index[0] if not state_total.empty else "—")
    ], "geo")

    c1,c2=st.columns(2,gap="large")
    with c1:
        st.subheader("📊 Top States")
        ss=state_total.head(12).sort_values().reset_index(name="Students")
        if not ss.empty:
            fig=px.bar(ss,x="Students",y=state_col,orientation="h",text="Students",color="Students",color_continuous_scale="Teal")
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=500,coloraxis_showscale=False)
            st.plotly_chart(fig,use_container_width=True)
    with c2:
        st.subheader("🏙️ Top Cities")
        cs=city_total.head(12).sort_values().reset_index(name="Students")
        if not cs.empty:
            fig=px.bar(cs,x="Students",y=city_col,orientation="h",text="Students",color="Students",color_continuous_scale="Blues")
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=500,coloraxis_showscale=False)
            st.plotly_chart(fig,use_container_width=True)

    st.subheader("📈 State-wise Admission Comparison")
    state_year=geo.groupby([state_col,"Batch"]).size().reset_index(name="Students")
    if not state_year.empty:
        top_states=state_total.head(15).index
        state_year=state_year[state_year[state_col].isin(top_states)]
        fig=px.bar(state_year,x=state_col,y="Students",color="Batch",barmode="group",text="Students",category_orders={"Batch":["2024-26","2025-27","2026-28"]})
        fig.update_layout(template="plotly_white",height=600,xaxis_tickangle=-35)
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("📋 State & City Summary")
    tab1,tab2=st.tabs(["📍 State Summary","🏙️ City Summary"])
    with tab1:
        state_summary=geo.groupby([state_col,"Batch"]).size().unstack(fill_value=0).reindex(columns=["2024-26","2025-27","2026-28"],fill_value=0)
        state_summary["Total"]=state_summary.sum(axis=1)
        st.dataframe(state_summary.sort_values("Total",ascending=False),use_container_width=True)
    with tab2:
        city_summary=geo.groupby([city_col,"Batch"]).size().unstack(fill_value=0).reindex(columns=["2024-26","2025-27","2026-28"],fill_value=0)
        city_summary["Total"]=city_summary.sum(axis=1)
        st.dataframe(city_summary.sort_values("Total",ascending=False),use_container_width=True)

elif page == "👤 Owner Analysis":


    # =========================================================
    # OWNER ANALYSIS — LIVE MANAGEMENT DASHBOARD
    # =========================================================

    st.markdown("""
    <style>
    .owner-title{font-size:32px!important;font-weight:850!important;color:#243447;margin:0 0 4px 0}
    .owner-subtitle{color:#64748B;font-size:15px!important;margin-bottom:16px}
    .filter-panel{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:14px 16px 6px 16px;margin:8px 0 14px 0}
    .owner-card{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:15px 17px;min-height:105px;box-shadow:0 3px 12px rgba(15,23,42,.06)}
    .owner-card-label{color:#64748B;font-size:13px!important;font-weight:750}
    .owner-card-value{color:#1E293B;font-size:28px!important;font-weight:850;margin-top:7px;line-height:1.05}
    .owner-card-note{color:#94A3B8;font-size:11px!important;margin-top:6px}
    .owner-section{color:#26384B;font-size:20px!important;font-weight:850;margin:22px 0 10px 0}
    .insight-good,.insight-watch{border-radius:12px;padding:13px 16px;margin:7px 0;font-size:14px!important;font-weight:600}
    .insight-good{background:#ECFDF5;border-left:4px solid #10B981;color:#065F46}
    .insight-watch{background:#FFF7ED;border-left:4px solid #F97316;color:#9A3412}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="owner-title">👑 Owner Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="owner-subtitle">Live management view with individual Owner-wise performance and smart filters</div>', unsafe_allow_html=True)

    admitted_status = ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
    owner_df = df[df["Final Status"].isin(admitted_status)].copy()

    def _norm_col(x):
        return "".join(ch.lower() for ch in str(x) if ch.isalnum())

    def find_matching_column(columns, candidates):
        lookup = {_norm_col(c): c for c in columns}
        for candidate in candidates:
            if _norm_col(candidate) in lookup:
                return lookup[_norm_col(candidate)]
        for candidate in candidates:
            key = _norm_col(candidate)
            for norm, original in lookup.items():
                if key in norm or norm in key:
                    return original
        return None

    owner_col = find_matching_column(owner_df.columns, [
        "Owner Name", "Owner", "Counsellor Name", "Counselor Name",
        "Admission Owner", "Sales Owner", "Assigned To",
        "Relationship Manager", "RM Name", "Executive Name"
    ])

    programme_col = "Final Course Selected" if "Final Course Selected" in owner_df.columns else None
    gender_col = "Gender" if "Gender" in owner_df.columns else None
    stream_col = "Graduation Stream" if "Graduation Stream" in owner_df.columns else None
    state_col = "Correspondence State" if "Correspondence State" in owner_df.columns else None
    city_col = "Correspondence city" if "Correspondence city" in owner_df.columns else None

    for col in [programme_col, stream_col, state_col, city_col]:
        if col:
            owner_df[col] = owner_df[col].fillna("Not Available").astype(str).str.strip()

    if gender_col:
        owner_df[gender_col] = owner_df[gender_col].fillna("Not Available").astype(str).str.upper().str.strip().replace({"M":"MALE","F":"FEMALE"})

    owner_found = owner_col is not None
    if owner_found:
        owner_df[owner_col] = owner_df[owner_col].fillna("Unassigned").astype(str).str.strip()
    else:
        owner_df["_Owner_Display"] = "Owner column not found"
        owner_col = "_Owner_Display"

    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div>', unsafe_allow_html=True)
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    f1, f2, f3, f4, f5, f6 = st.columns(6)

    with f1:
        batch_filter = st.selectbox("📅 Batch", ["All Batches","2024-26","2025-27","2026-28"], key="owner_batch_filter")
    with f2:
        opts = ["All Programmes"] + sorted(owner_df[programme_col].dropna().unique().tolist()) if programme_col else ["All Programmes"]
        programme_filter = st.selectbox("🎓 Programme", opts, key="owner_programme_filter")
    with f3:
        opts = ["All Owners"] + sorted(owner_df[owner_col].dropna().unique().tolist())
        owner_filter = st.selectbox("👤 Owner Name", opts, key="owner_name_filter")
    with f4:
        opts = ["All Genders"] + sorted(owner_df[gender_col].dropna().unique().tolist()) if gender_col else ["All Genders"]
        gender_filter = st.selectbox("👥 Gender", opts, key="owner_gender_filter")
    with f5:
        opts = ["All Streams"] + sorted(owner_df[stream_col].dropna().unique().tolist()) if stream_col else ["All Streams"]
        stream_filter = st.selectbox("📚 Stream", opts, key="owner_stream_filter")
    with f6:
        opts = ["All States"] + sorted(owner_df[state_col].dropna().unique().tolist()) if state_col else ["All States"]
        state_filter = st.selectbox("📍 State", opts, key="owner_state_filter")

    st.markdown("</div>", unsafe_allow_html=True)

    if not owner_found:
        st.warning("⚠️ Owner Name column automatically detect nahi hua. Google Sheet me actual Owner column ka naam confirm hote hi individual Owner filter live data show karega.")

    filtered = owner_df.copy()
    if batch_filter != "All Batches":
        filtered = filtered[filtered["Batch"] == batch_filter]
    if programme_col and programme_filter != "All Programmes":
        filtered = filtered[filtered[programme_col] == programme_filter]
    if owner_filter != "All Owners":
        filtered = filtered[filtered[owner_col] == owner_filter]
    if gender_col and gender_filter != "All Genders":
        filtered = filtered[filtered[gender_col] == gender_filter]
    if stream_col and stream_filter != "All Streams":
        filtered = filtered[filtered[stream_col] == stream_filter]
    if state_col and state_filter != "All States":
        filtered = filtered[filtered[state_col] == state_filter]

    total_students = len(filtered)
    batch_counts = filtered.groupby("Batch").size().reindex(["2024-26","2025-27","2026-28"], fill_value=0)
    best_batch = batch_counts.idxmax() if batch_counts.max() > 0 else "—"
    top_programme = filtered[programme_col].value_counts().idxmax() if programme_col and not filtered.empty else "—"
    top_state = filtered[state_col].value_counts().idxmax() if state_col and not filtered.empty else "—"

    if owner_found and not filtered.empty:
        owner_value = filtered[owner_col].replace("Unassigned", pd.NA).nunique() if owner_filter == "All Owners" else total_students
        owner_label = "Active Owners" if owner_filter == "All Owners" else "Selected Owner Students"
    else:
        owner_value, owner_label = "—", "Owner Performance"

    st.markdown('<span class="kpi-tab-marker kpi-scope-owner"></span>', unsafe_allow_html=True)
    k1,k2,k3,k4,k5 = st.columns(5)
    cards = [
        (k1,"👥 Total Admissions",f"{total_students:,}","Current filtered data"),
        (k2,f"👤 {owner_label}",str(owner_value),"Live Owner-wise view"),
        (k3,"🏆 Best Batch",best_batch,"Highest admissions"),
        (k4,"🎓 Top Programme",top_programme,"Most selected programme"),
        (k5,"📍 Top State",top_state,"Highest contribution")
    ]
    for col,label,value,note in cards:
        with col:
            st.markdown(f'<div class="owner-card"><div class="owner-card-label">{label}</div><div class="owner-card-value" style="font-size:{"21px" if len(str(value))>12 else "28px"}!important;">{value}</div><div class="owner-card-note">{note}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="owner-section">📈 Year-wise Admission Performance</div>', unsafe_allow_html=True)
    year_summary = batch_counts.reset_index()
    year_summary.columns = ["Batch","Students"]
    fig = px.bar(year_summary, x="Batch", y="Students", text="Students", color="Batch",
                 category_orders={"Batch":["2024-26","2025-27","2026-28"]},
                 color_discrete_map={"2024-26":"#2457B2","2025-27":"#169B62","2026-28":"#F21D2F"})
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(template="plotly_white",height=390,margin=dict(l=35,r=20,t=20,b=30),showlegend=False,
                      plot_bgcolor="white",paper_bgcolor="white",xaxis_title="Batch",yaxis_title="Admissions")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3",zeroline=False)
    st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2,gap="large")

    with c1:
        st.markdown('<div class="owner-section">👤 Owner-wise Performance</div>', unsafe_allow_html=True)
        if owner_found and not filtered.empty:
            os = (filtered[filtered[owner_col]!="Unassigned"].groupby(owner_col).size()
                  .reset_index(name="Students").sort_values("Students",ascending=False).head(15))
            if not os.empty:
                fig = px.bar(os.sort_values("Students"),x="Students",y=owner_col,orientation="h",text="Students",
                             color="Students",color_continuous_scale="Blues")
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=470,margin=dict(l=20,r=30,t=15,b=20),
                                  coloraxis_showscale=False,xaxis_title="Students",yaxis_title="")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Selected filters ke liye Owner-wise data available nahi hai.")
        else:
            st.info("Owner column detect hote hi yahan Top Owners ka live comparison show hoga.")

    with c2:
        st.markdown('<div class="owner-section">🎓 Programme Performance</div>', unsafe_allow_html=True)
        if programme_col and not filtered.empty:
            ps = filtered.groupby([programme_col,"Batch"]).size().reset_index(name="Students")
            fig = px.bar(ps,x=programme_col,y="Students",color="Batch",barmode="group",text="Students",
                         category_orders={"Batch":["2024-26","2025-27","2026-28"]},
                         color_discrete_map={"2024-26":"#2457B2","2025-27":"#169B62","2026-28":"#F21D2F"})
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=470,margin=dict(l=20,r=20,t=15,b=60),
                              legend_title="Batch",xaxis_title="Programme",yaxis_title="Students")
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Selected filters ke liye Programme data available nahi hai.")

    # =========================================================
    # REFERENCE LAYOUT: STUDENT QUALITY + STREAM + ENTRANCE
    # =========================================================
    quality = filtered.copy()
    academic_cols = ["10th Percentage", "12th Percentage", "Graduation Percentage"]
    for col in academic_cols:
        if col in quality.columns:
            quality[col] = pd.to_numeric(quality[col], errors="coerce")

    # Students scoring 60% or above in 10th, 12th and Graduation
    quality_available = all(col in quality.columns for col in academic_cols)
    if quality_available:
        all60 = int(((quality["10th Percentage"] >= 60) &
                     (quality["12th Percentage"] >= 60) &
                     (quality["Graduation Percentage"] >= 60)).sum())
    else:
        all60 = 0

    r1, r2, r3 = st.columns([1.05, 1.0, 1.25], gap="small")

    with r1:
        st.markdown('<div class="owner-section">🏆 Student Quality Index (Average %)</div>', unsafe_allow_html=True)
        rows=[]
        for batch in ["2024-26", "2025-27", "2026-28"]:
            bq=quality[quality["Batch"]==batch]
            rows.append({
                "Batch":batch,
                "10th %":round(bq["10th Percentage"].mean(),2) if "10th Percentage" in bq.columns else 0,
                "12th %":round(bq["12th Percentage"].mean(),2) if "12th Percentage" in bq.columns else 0,
                "Graduation %":round(bq["Graduation Percentage"].mean(),2) if "Graduation Percentage" in bq.columns else 0
            })
        if batch_filter == "All Batches":
            rows.append({
                "Batch":"All Batches",
                "10th %":round(quality["10th Percentage"].mean(),2) if "10th Percentage" in quality.columns else 0,
                "12th %":round(quality["12th Percentage"].mean(),2) if "12th Percentage" in quality.columns else 0,
                "Graduation %":round(quality["Graduation Percentage"].mean(),2) if "Graduation Percentage" in quality.columns else 0
            })
        quality_table=pd.DataFrame(rows)
        if batch_filter != "All Batches":
            quality_table=quality_table[quality_table["Batch"]==batch_filter]
        st.dataframe(
            quality_table.style.format({"10th %":"{:.2f}","12th %":"{:.2f}","Graduation %":"{:.2f}"}),
            use_container_width=True, hide_index=True
        )

    with r2:
        st.markdown('<div class="owner-section">🎓 Graduation Stream Analysis</div>', unsafe_allow_html=True)
        if stream_col and not filtered.empty:
            stream_summary=(filtered[stream_col].fillna("Not Available").astype(str).str.strip()
                            .replace("", "Not Available").value_counts().head(6).reset_index())
            stream_summary.columns=["Graduation Stream","Students"]
            fig=px.pie(stream_summary,names="Graduation Stream",values="Students",hole=0.52)
            fig.update_traces(textinfo="percent",textposition="inside")
            fig.update_layout(
                template="plotly_white",height=330,margin=dict(l=5,r=5,t=5,b=5),
                legend=dict(orientation="v",x=1.0,y=0.5),
                annotations=[dict(text=f"<b>{total_students:,}</b><br>Total",x=0.5,y=0.5,showarrow=False,font=dict(size=16))]
            )
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Graduation Stream data available nahi hai.")

    with r3:
        st.markdown('<div class="owner-section">📝 Entrance Exam Analysis</div>', unsafe_allow_html=True)
        exam_rows=[]
        temp=filtered.copy()
        if "Percentile CAT" in temp.columns:
            exam_rows.append({"Entrance Exam":"CAT","Students":int(pd.to_numeric(temp["Percentile CAT"],errors="coerce").notna().sum())})
        if "Entrance Exam" in temp.columns and "Percentile score" in temp.columns:
            temp["_exam"]=temp["Entrance Exam"].fillna("").astype(str).str.upper().str.strip()
            temp["_score"]=pd.to_numeric(temp["Percentile score"],errors="coerce")
            for exam in ["MAT","CMAT","XAT","ATMA","GMAT"]:
                exam_rows.append({"Entrance Exam":exam,"Students":int(((temp["_exam"]==exam)&temp["_score"].notna()).sum())})
        er=pd.DataFrame(exam_rows)
        if not er.empty:
            er=er.sort_values("Students",ascending=False)
            fig=px.bar(er,x="Students",y="Entrance Exam",orientation="h",text="Students",
                       color="Entrance Exam",
                       color_discrete_map={"CAT":"#1D4ED8","CMAT":"#6B3FA0","MAT":"#0F766E","XAT":"#DC2626","ATMA":"#D97706","GMAT":"#0891B2"})
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=330,showlegend=False,
                              margin=dict(l=10,r=35,t=5,b=5),xaxis_title="",yaxis_title="")
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(autorange="reversed",showgrid=False)
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Entrance Exam data available nahi hai.")

    g1,g2 = st.columns(2,gap="large")
    with g1:
        st.markdown('<div class="owner-section">📍 Top States</div>', unsafe_allow_html=True)
        if state_col and not filtered.empty:
            gs=(filtered.groupby(state_col).size().reset_index(name="Students")
                .sort_values("Students",ascending=False).head(8).sort_values("Students"))
            fig=px.bar(gs,x="Students",y=state_col,orientation="h",text="Students",color="Students",color_continuous_scale="Teal")
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=390,coloraxis_showscale=False,margin=dict(l=20,r=25,t=10,b=20),xaxis_title="Students",yaxis_title="")
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("State data available nahi hai.")

    with g2:
        st.markdown('<div class="owner-section">📍 Geographic Performance</div>', unsafe_allow_html=True)
        if city_col and not filtered.empty:
            cs_geo=(filtered.groupby(city_col).size().reset_index(name="Students")
                    .sort_values("Students",ascending=False).head(8).sort_values("Students"))
            fig=px.bar(cs_geo,x="Students",y=city_col,orientation="h",text="Students",color="Students",color_continuous_scale="Blues")
            fig.update_traces(textposition="outside",cliponaxis=False)
            fig.update_layout(template="plotly_white",height=390,coloraxis_showscale=False,margin=dict(l=20,r=25,t=10,b=20),xaxis_title="Students",yaxis_title="")
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("City data available nahi hai.")

    if city_col and not filtered.empty:
        st.markdown('<div class="owner-section">🏙️ Top Cities</div>', unsafe_allow_html=True)
        cs=(filtered.groupby(city_col).size().reset_index(name="Students").sort_values("Students",ascending=False).head(12))
        fig=px.bar(cs,x=city_col,y="Students",text="Students",color="Students",color_continuous_scale="Viridis")
        fig.update_traces(textposition="outside",cliponaxis=False)
        fig.update_layout(template="plotly_white",height=420,coloraxis_showscale=False,margin=dict(l=35,r=20,t=20,b=80),xaxis_title="City",yaxis_title="Students")
        fig.update_xaxes(tickangle=-35,showgrid=False)
        fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
        st.plotly_chart(fig,use_container_width=True)

    st.markdown('<div class="owner-section">💡 Owner Key Insights</div>', unsafe_allow_html=True)
    i1,i2,i3=st.columns(3,gap="small")
    with i1:
        growth=[]
        if batch_counts.max()>0:
            growth.append(f"✓ {batch_counts.idxmax()} batch has highest admissions.")
        if owner_found and not filtered.empty:
            top_owner=(filtered[filtered[owner_col]!="Unassigned"][owner_col].value_counts().index[0]
                       if not filtered[filtered[owner_col]!="Unassigned"].empty else "—")
            growth.append(f"✓ {top_owner} has the strongest owner contribution.")
        growth.append(f"✓ Admissions growth is {((batch_counts.max()/max(batch_counts.min(),1)-1)*100):.1f}% between highest and lowest batch.")
        st.markdown('<div style="border:1px solid #A7E3C2;border-radius:12px;padding:14px;min-height:170px;background:#F5FCF7;"><b style="color:#15803D;">GROWTH OPPORTUNITIES</b><br><br>'+"<br>".join(growth[:3])+'</div>',unsafe_allow_html=True)
    with i2:
        watch=[]
        if quality_available and all60 < total_students:
            watch.append(f"⚠ Focus on academic quality: only {all60:,} students are 60%+ throughout.")
        if stream_col and not filtered.empty:
            watch.append("⚠ Review lower-contributing graduation streams for targeted counselling.")
        watch.append("⚠ Track low-volume entrance exams for conversion improvement.")
        st.markdown('<div style="border:1px solid #F2C56B;border-radius:12px;padding:14px;min-height:170px;background:#FFFDF8;"><b style="color:#B45309;">ATTENTION REQUIRED</b><br><br>'+"<br>".join(watch[:3])+'</div>',unsafe_allow_html=True)
    with i3:
        best=[]
        if programme_col:
            best.append(f"★ {top_programme} is the leading programme.")
        if state_col:
            best.append(f"★ {top_state} has the highest geographic contribution.")
        if owner_filter != "All Owners":
            best.append(f"★ Individual owner view active: {owner_filter}.")
        else:
            best.append("★ Live filters can drill down by Batch, Programme, Owner, Gender, Stream and State.")
        st.markdown('<div style="border:1px solid #A9C7F5;border-radius:12px;padding:14px;min-height:170px;background:#F8FBFF;"><b style="color:#1D4ED8;">BEST PERFORMING AREAS</b><br><br>'+"<br>".join(best[:3])+'</div>',unsafe_allow_html=True)

    with st.expander("📋 View Filtered Student Records"):
        show_cols=[c for c in ["Batch",owner_col,programme_col,gender_col,stream_col,state_col,city_col,"Final Status"] if c and c in filtered.columns and c!="_Owner_Display"]
        st.dataframe(filtered[show_cols] if show_cols else filtered,use_container_width=True)

elif page == "🚀 Command Center":
    show_page_heading("🚀 Command Center")
    st.caption("Complete Admission Intelligence Dashboard")

    admitted_status = ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
    cc = df[df["Final Status"].isin(admitted_status)].copy()

    def cc_find(candidates):
        for c in cc.columns:
            name = str(c).strip().lower()
            if any(x.lower() == name or x.lower() in name for x in candidates):
                return c
        return None

    programme_col = cc_find(["Final Course Selected", "Programme", "Program", "Course"])
    owner_col = cc_find(["Owner", "Counsellor"])
    exam_col = cc_find(["Entrance Exam", "Exam"])
    gender_col = cc_find(["Gender"])
    state_col = cc_find(["Correspondence State", "State"])

    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        batch_filter = st.selectbox("📅 Batch", ["All Batches", "2024-26", "2025-27", "2026-28"], key="cc_batch")
    with f2:
        p_opts = ["All Programmes"] + (sorted(cc[programme_col].dropna().astype(str).unique().tolist()) if programme_col else [])
        programme_filter = st.selectbox("🎓 Programme", p_opts, key="cc_programme")
    with f3:
        s_opts = ["All States"] + (sorted(cc[state_col].dropna().astype(str).unique().tolist()) if state_col else [])
        state_filter = st.selectbox("📍 State", s_opts, key="cc_state")

    if batch_filter != "All Batches":
        cc = cc[cc["Batch"].astype(str) == batch_filter]
    if programme_col and programme_filter != "All Programmes":
        cc = cc[cc[programme_col].astype(str) == programme_filter]
    if state_col and state_filter != "All States":
        cc = cc[cc[state_col].astype(str) == state_filter]

    def top_item(col):
        if not col or cc.empty:
            return "—"
        x = cc[col].dropna().astype(str)
        x = x[(x != "") & (x.str.lower() != "nan")]
        return x.value_counts().index[0] if not x.empty else "—"

    total = len(cc)
    top_programme = top_item(programme_col)
    top_owner = top_item(owner_col)
    top_exam = top_item(exam_col)
    top_state = top_item(state_col)

    show_command_center_kpi_cards([
        ("👥 Total Admissions", f"{total:,}"),
        ("🎓 Top Programme", str(top_programme)),
        ("📝 Top Exam", str(top_exam)),
        ("👤 Top Owner", str(top_owner)),
        ("📍 Top State", str(top_state)),
    ])

    st.divider()

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("📈 Admission Trend")
        trend = cc.groupby("Batch").size().reindex(["2024-26", "2025-27", "2026-28"], fill_value=0).reset_index()
        trend.columns = ["Batch", "Students"]
        fig = px.bar(trend, x="Batch", y="Students", text="Students", color="Batch",
                     category_orders={"Batch": ["2024-26", "2025-27", "2026-28"]})
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(template="plotly_white", height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🎓 Programme Performance")
        if programme_col:
            p = cc.groupby(programme_col).size().reset_index(name="Students").sort_values("Students", ascending=False).head(10)
            if not p.empty:
                fig = px.bar(p, x=programme_col, y="Students", text="Students", color="Students")
                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(template="plotly_white", height=420, coloraxis_showscale=False)
                fig.update_xaxes(tickangle=-25)
                st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2, gap="large")
    with c3:
        st.subheader("👤 Owner Performance")
        if owner_col:
            o = cc.groupby(owner_col).size().reset_index(name="Students").sort_values("Students", ascending=False).head(10)
            if not o.empty:
                fig = px.bar(o, x="Students", y=owner_col, orientation="h", text="Students", color="Students")
                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(template="plotly_white", height=420, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.subheader("📝 Entrance Exam Intelligence")
        if exam_col:
            e = cc.groupby(exam_col).size().reset_index(name="Students").sort_values("Students", ascending=False).head(10)
            if not e.empty:
                fig = px.pie(e, names=exam_col, values="Students", hole=0.55)
                fig.update_layout(template="plotly_white", height=420)
                st.plotly_chart(fig, use_container_width=True)

    c5, c6 = st.columns(2, gap="large")
    with c5:
        st.subheader("📍 Top States")
        if state_col:
            s = cc.groupby(state_col).size().reset_index(name="Students").sort_values("Students", ascending=False).head(10)
            if not s.empty:
                fig = px.bar(s, x="Students", y=state_col, orientation="h", text="Students", color="Students")
                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(template="plotly_white", height=420, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.subheader("👥 Student Profile")
        if gender_col:
            g = cc.groupby(gender_col).size().reset_index(name="Students")
            if not g.empty:
                fig = px.pie(g, names=gender_col, values="Students", hole=0.5)
                fig.update_layout(template="plotly_white", height=420)
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("💡 Command Center Insights")
    i1, i2, i3, i4 = st.columns(4)
    i1.success("🏆 Top Programme: " + str(top_programme))
    i2.info("👤 Top Owner: " + str(top_owner))
    i3.warning("📝 Leading Exam: " + str(top_exam))
    i4.success("📍 Top State: " + str(top_state))

elif page == "💰 Scholarship":

    # =========================================================
    # SCHOLARSHIP ANALYSIS — NOIDA LIVE DASHBOARD
    # =========================================================
    st.markdown("""
    <style>
    .sch-title{font-size:32px!important;font-weight:850!important;color:#243447;margin:0 0 4px 0}
    .sch-subtitle{color:#64748B;font-size:15px!important;margin-bottom:14px}
    .sch-filter{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:14px;padding:12px 14px 4px 14px;margin:6px 0 14px 0}
    .sch-card{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:15px 17px;min-height:104px;box-shadow:0 3px 12px rgba(15,23,42,.06)}
    .sch-label{color:#64748B;font-size:13px!important;font-weight:750}
    .sch-value{color:#1E293B;font-size:27px!important;font-weight:850;margin-top:7px;line-height:1.05}
    .sch-note{color:#94A3B8;font-size:11px!important;margin-top:7px}
    .sch-section{color:#26384B;font-size:20px!important;font-weight:850;margin:20px 0 9px 0}
    .sch-insight{border-radius:12px;padding:14px 16px;margin:7px 0;font-size:14px!important;font-weight:600;min-height:150px}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sch-title">💰 Scholarship Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sch-subtitle">Noida admissions — live scholarship performance, amount analysis and key insights</div>', unsafe_allow_html=True)

    admitted_status = ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
    sch_df = df[df["Final Status"].isin(admitted_status)].copy()

    def _sch_norm(x):
        return "".join(ch.lower() for ch in str(x) if ch.isalnum())

    def _sch_find(columns, candidates):
        lookup = {_sch_norm(c): c for c in columns}
        for candidate in candidates:
            key = _sch_norm(candidate)
            if key in lookup:
                return lookup[key]
        for candidate in candidates:
            key = _sch_norm(candidate)
            for norm, original in lookup.items():
                if key and (key in norm or norm in key):
                    return original
        return None

    # Auto-detect columns so the dashboard continues working if headers have
    # minor spelling/spacing differences in Google Sheets.
    programme_col = _sch_find(sch_df.columns, ["Final Course Selected", "Programme", "Program", "Course Selected"])
    owner_col = _sch_find(sch_df.columns, ["Owner Name", "Owner", "Counsellor Name", "Counselor Name", "Admission Owner", "Assigned To"])
    city_col = _sch_find(sch_df.columns, ["Correspondence city", "City", "Correspondence City"])
    state_col = _sch_find(sch_df.columns, ["Correspondence State", "State", "Correspondence state"])
    category_col = _sch_find(sch_df.columns, [
        "Scholarship Category", "Scholarship Criteria", "Scholarship Type",
        "Scholarship", "Criteria", "Scholarship Slab"
    ])
    amount_col = _sch_find(sch_df.columns, [
        "Scholarship Amount", "Scholarship Amt", "Scholarship Value",
        "Scholarship Amount INR", "Amount", "Scholarship"
    ])

    # Prefer a column containing both scholarship/concession + amount/value.
    for c in sch_df.columns:
        n = _sch_norm(c)
        if ("scholarship" in n or "concession" in n or "waiver" in n) and any(k in n for k in ["amount","amt","value","inr","rs"]):
            amount_col = c
            break

    # If the initially detected "Scholarship" column is not numeric, search
    # for another numeric-looking scholarship/concession column.
    if amount_col:
        probe = pd.to_numeric(
            sch_df[amount_col].astype(str).str.replace(r"[₹,]", "", regex=True),
            errors="coerce"
        )
        if probe.notna().sum() == 0:
            for c in sch_df.columns:
                n = _sch_norm(c)
                if any(k in n for k in ["scholarship","concession","waiver"]) and any(k in n for k in ["amount","amt","value","discount"]):
                    amount_col = c
                    break

    # Prepare clean dimensions.
    for c in [programme_col, owner_col, city_col, state_col, category_col]:
        if c:
            sch_df[c] = sch_df[c].fillna("Not Available").astype(str).str.strip()
            sch_df.loc[sch_df[c].eq(""), c] = "Not Available"

    if amount_col:
        sch_df["_Scholarship_Amount"] = pd.to_numeric(
            sch_df[amount_col].astype(str)
                  .str.replace(r"[₹,]", "", regex=True)
                  .str.replace(r"\s+", "", regex=True),
            errors="coerce"
        )
    else:
        sch_df["_Scholarship_Amount"] = pd.NA

    # Only records with a positive scholarship amount are treated as scholarship records.
    # If the sheet stores scholarship as a category/criteria without amount,
    # non-empty category records are used as fallback.
    if sch_df["_Scholarship_Amount"].notna().any():
        scholarship_df = sch_df[sch_df["_Scholarship_Amount"].fillna(0) > 0].copy()
    elif category_col:
        scholarship_df = sch_df[
            ~sch_df[category_col].isin(["", "Not Available", "NONE", "NO", "N/A", "0"])
        ].copy()
    else:
        scholarship_df = sch_df.iloc[0:0].copy()

    # ---------------- Filters ----------------
    st.markdown('<div class="jaipuria-filter-title">🎛️ Filters</div>', unsafe_allow_html=True)
    st.markdown('<div class="sch-filter">', unsafe_allow_html=True)
    f1,f2,f3,f4,f5,f6 = st.columns(6)

    with f1:
        sch_batch = st.selectbox(
            "📅 Batch",
            ["All Batches","2024-26","2025-27","2026-28"],
            key="sch_batch_filter"
        )

    with f2:
        prog_opts = ["All Programmes"] + sorted(scholarship_df[programme_col].dropna().unique().tolist()) if programme_col and not scholarship_df.empty else ["All Programmes"]
        sch_programme = st.selectbox("🎓 Programme", prog_opts, key="sch_programme_filter")

    with f3:
        owner_opts = ["All Owners"] + sorted(scholarship_df[owner_col].dropna().unique().tolist()) if owner_col and not scholarship_df.empty else ["All Owners"]
        sch_owner = st.selectbox("👤 Owner", owner_opts, key="sch_owner_filter")

    with f4:
        city_opts = ["All Cities"] + sorted(scholarship_df[city_col].dropna().unique().tolist()) if city_col and not scholarship_df.empty else ["All Cities"]
        sch_city = st.selectbox("🏙️ City", city_opts, key="sch_city_filter")

    with f5:
        state_opts = ["All States"] + sorted(scholarship_df[state_col].dropna().unique().tolist()) if state_col and not scholarship_df.empty else ["All States"]
        sch_state = st.selectbox("📍 State", state_opts, key="sch_state_filter")

    with f6:
        if scholarship_df["_Scholarship_Amount"].notna().any():
            a_min = float(scholarship_df["_Scholarship_Amount"].min())
            a_max = float(scholarship_df["_Scholarship_Amount"].max())
            if a_min == a_max:
                sch_amount_range = (a_min, a_max)
                st.number_input("💰 Scholarship Amount", value=a_min, disabled=True, key="sch_amount_single")
            else:
                sch_amount_range = st.slider(
                    "💰 Scholarship Amount Range",
                    min_value=a_min, max_value=a_max,
                    value=(a_min, a_max),
                    key="sch_amount_filter"
                )
        else:
            sch_amount_range = None
            st.selectbox("💰 Scholarship Amount", ["Amount data not available"], disabled=True, key="sch_amount_na")

    st.markdown("</div>", unsafe_allow_html=True)

    filtered_sch = scholarship_df.copy()
    if sch_batch != "All Batches":
        filtered_sch = filtered_sch[filtered_sch["Batch"] == sch_batch]
    if programme_col and sch_programme != "All Programmes":
        filtered_sch = filtered_sch[filtered_sch[programme_col] == sch_programme]
    if owner_col and sch_owner != "All Owners":
        filtered_sch = filtered_sch[filtered_sch[owner_col] == sch_owner]
    if city_col and sch_city != "All Cities":
        filtered_sch = filtered_sch[filtered_sch[city_col] == sch_city]
    if state_col and sch_state != "All States":
        filtered_sch = filtered_sch[filtered_sch[state_col] == sch_state]
    if sch_amount_range is not None:
        filtered_sch = filtered_sch[
            filtered_sch["_Scholarship_Amount"].between(sch_amount_range[0], sch_amount_range[1], inclusive="both")
        ]

    # ---------------- KPIs ----------------
    total_students = len(filtered_sch)
    total_amount = float(filtered_sch["_Scholarship_Amount"].sum()) if filtered_sch["_Scholarship_Amount"].notna().any() else 0.0
    avg_amount = float(filtered_sch["_Scholarship_Amount"].mean()) if filtered_sch["_Scholarship_Amount"].notna().any() else 0.0

    batch_sch = filtered_sch.groupby("Batch").size().reindex(["2024-26","2025-27","2026-28"], fill_value=0)
    best_batch = batch_sch.idxmax() if batch_sch.max() > 0 else "—"

    top_programme = (
        filtered_sch[programme_col].value_counts().idxmax()
        if programme_col and not filtered_sch.empty else "—"
    )
    top_category = (
        filtered_sch[category_col].value_counts().idxmax()
        if category_col and not filtered_sch.empty else "—"
    )

    st.markdown('<span class="kpi-tab-marker kpi-scope-scholarship"></span>', unsafe_allow_html=True)
    k1,k2,k3,k4,k5 = st.columns(5)
    cards = [
        (k1,"🎓 Total Scholarship Students",f"{total_students:,}","Current filtered data"),
        (k2,"💰 Total Scholarship Amount",f"₹{total_amount:,.0f}","Filtered scholarship value"),
        (k3,"📊 Average Scholarship",f"₹{avg_amount:,.0f}","Average per student"),
        (k4,"🏆 Best Batch",best_batch,"Highest scholarship students"),
        (k5,"🏅 Top Criteria / Category",top_category,"Most frequent scholarship basis")
    ]
    for col,label,value,note in cards:
        with col:
            size = "19px" if len(str(value)) > 14 else "27px"
            st.markdown(
                f'<div class="sch-card"><div class="sch-label">{label}</div>'
                f'<div class="sch-value" style="font-size:{size}!important;">{value}</div>'
                f'<div class="sch-note">{note}</div></div>',
                unsafe_allow_html=True
            )

    if scholarship_df.empty:
        st.warning(
            "⚠️ Scholarship records detect nahi hue. Please Google Sheet me Scholarship Amount / Scholarship Category / Criteria column ka header check karein."
        )
    else:
        # =========================================================
        # SCHOLARSHIP EXAM SCORE RANGE ANALYSIS
        # EAS decides the winning exam; percentile/score decides the range.
        # Only scholarship recipients are included, therefore only ranges
        # actually eligible/used for scholarship appear in the tables/charts.
        # =========================================================
        def _safe_num(series):
            return pd.to_numeric(series, errors="coerce")

        def _find_eas_after(source, percentile_header):
            try:
                pos = source.columns.get_loc(percentile_header)
                if isinstance(pos, slice):
                    pos = pos.start
                if isinstance(pos, int) and pos + 1 < len(source.columns):
                    return source.columns[pos + 1]
            except Exception:
                return None
            return None

        range_df = filtered_sch.copy()
        range_df["_Scholarship_Exam"] = ""
        range_df["_Scholarship_Score"] = pd.NA

        cat_pct_col = _sch_find(range_df.columns, ["Percentile CAT"])
        other_exam_col = _sch_find(range_df.columns, ["Entrance Exam"])
        other_pct_col = _sch_find(range_df.columns, ["Percentile score"])
        cat_eas_col = _find_eas_after(range_df, cat_pct_col) if cat_pct_col else None
        other_eas_col = _find_eas_after(range_df, other_pct_col) if other_pct_col else None

        valid_other = ["CMAT", "MAT", "XAT", "ATMA", "GMAT"]
        if cat_pct_col:
            range_df["_CAT_PCT"] = _safe_num(range_df[cat_pct_col])
        else:
            range_df["_CAT_PCT"] = pd.NA
        if other_pct_col:
            range_df["_OTHER_PCT"] = _safe_num(range_df[other_pct_col])
        else:
            range_df["_OTHER_PCT"] = pd.NA
        if other_exam_col:
            range_df["_OTHER_EXAM"] = range_df[other_exam_col].fillna("").astype(str).str.upper().str.strip()
        else:
            range_df["_OTHER_EXAM"] = ""

        range_df["_CAT_EAS"] = _safe_num(range_df[cat_eas_col]) if cat_eas_col in range_df.columns else pd.NA
        range_df["_OTHER_EAS"] = _safe_num(range_df[other_eas_col]) if other_eas_col in range_df.columns else pd.NA

        cat_ready = range_df["_CAT_PCT"].notna() & range_df["_CAT_EAS"].notna()
        other_ready = (
            range_df["_OTHER_EXAM"].isin(valid_other)
            & range_df["_OTHER_PCT"].notna()
            & range_df["_OTHER_EAS"].notna()
        )
        cat_wins = cat_ready & (~other_ready | (range_df["_CAT_EAS"] >= range_df["_OTHER_EAS"]))
        other_wins = other_ready & (~cat_ready | (range_df["_OTHER_EAS"] > range_df["_CAT_EAS"]))

        range_df.loc[cat_wins, "_Scholarship_Exam"] = "CAT"
        range_df.loc[cat_wins, "_Scholarship_Score"] = range_df.loc[cat_wins, "_CAT_PCT"]
        range_df.loc[other_wins, "_Scholarship_Exam"] = range_df.loc[other_wins, "_OTHER_EXAM"]
        range_df.loc[other_wins, "_Scholarship_Score"] = range_df.loc[other_wins, "_OTHER_PCT"]

        # Fallback for scholarship records where EAS is blank: use the available
        # exam score, but never double count a student.
        unresolved = range_df["_Scholarship_Exam"].eq("")
        only_cat = unresolved & range_df["_CAT_PCT"].notna() & ~range_df["_OTHER_EXAM"].isin(valid_other)
        range_df.loc[only_cat, "_Scholarship_Exam"] = "CAT"
        range_df.loc[only_cat, "_Scholarship_Score"] = range_df.loc[only_cat, "_CAT_PCT"]

        unresolved = range_df["_Scholarship_Exam"].eq("")
        only_other = unresolved & range_df["_OTHER_EXAM"].isin(valid_other) & range_df["_OTHER_PCT"].notna() & range_df["_CAT_PCT"].isna()
        range_df.loc[only_other, "_Scholarship_Exam"] = range_df.loc[only_other, "_OTHER_EXAM"]
        range_df.loc[only_other, "_Scholarship_Score"] = range_df.loc[only_other, "_OTHER_PCT"]

        range_df["_Scholarship_Score"] = _safe_num(range_df["_Scholarship_Score"])
        range_df = range_df[
            range_df["_Scholarship_Exam"].ne("") & range_df["_Scholarship_Score"].notna()
        ].copy()

        def _score_band(exam, score):
            score = float(score)
            # 10-point bands, with the top band ending at 100.
            low = int(score // 10) * 10
            if score >= 90:
                return f"{exam} {low}-100"
            return f"{exam} {low}-{low+9.99:.2f}"

        if not range_df.empty:
            range_df["Exam Range"] = [
                _score_band(exam, score)
                for exam, score in zip(range_df["_Scholarship_Exam"], range_df["_Scholarship_Score"])
            ]

        # ---------------- Batch + Programme ----------------
        c1,c2 = st.columns(2, gap="large")

        with c1:
            st.markdown('<div class="sch-section">📊 Batch-wise Scholarship</div>', unsafe_allow_html=True)
            batch_amount = (
                filtered_sch.groupby("Batch")
                .agg(Students=("Batch","size"), Amount=("_Scholarship_Amount","sum"))
                .reindex(["2024-26","2025-27","2026-28"], fill_value=0)
                .reset_index()
            )
            fig = px.bar(
                batch_amount, x="Batch", y="Students", text="Students",
                color="Batch",
                category_orders={"Batch":["2024-26","2025-27","2026-28"]},
                color_discrete_map={"2024-26":"#2457B2","2025-27":"#169B62","2026-28":"#F21D2F"}
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(template="plotly_white",height=410,showlegend=False,
                              margin=dict(l=30,r=20,t=10,b=35),
                              xaxis_title="Batch",yaxis_title="Scholarship Students")
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            st.markdown('<div class="sch-section">📚 Programme-wise Scholarship</div>', unsafe_allow_html=True)
            if programme_col and not filtered_sch.empty:
                ps = (
                    filtered_sch.groupby(programme_col)
                    .agg(Students=(programme_col,"size"), Amount=("_Scholarship_Amount","sum"))
                    .reset_index().sort_values("Students",ascending=False)
                )
                fig = px.bar(ps, x=programme_col, y="Students", text="Students",
                             color="Students", color_continuous_scale="Blues")
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=410,coloraxis_showscale=False,
                                  margin=dict(l=25,r=20,t=10,b=55),
                                  xaxis_title="Programme",yaxis_title="Scholarship Students")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Programme data available nahi hai.")

        # ---------------- Amount + Owner ----------------
        c3,c4 = st.columns(2, gap="large")

        with c3:
            st.markdown('<div class="sch-section">💰 Scholarship Amount Analysis</div>', unsafe_allow_html=True)
            if filtered_sch["_Scholarship_Amount"].notna().any():
                bins = [-1, 25000, 50000, 100000, 200000, float("inf")]
                labels = ["Up to ₹25K","₹25K–₹50K","₹50K–₹1L","₹1L–₹2L","Above ₹2L"]
                amt = filtered_sch.copy()
                amt["Amount Range"] = pd.cut(
                    amt["_Scholarship_Amount"], bins=bins, labels=labels
                )
                amt_summary = amt.groupby("Amount Range", observed=False).size().reset_index(name="Students")
                fig = px.bar(amt_summary,x="Amount Range",y="Students",text="Students",
                             color="Amount Range",color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=410,showlegend=False,
                                  margin=dict(l=25,r=20,t=10,b=45),
                                  xaxis_title="Scholarship Amount Range",yaxis_title="Students")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Scholarship Amount numeric data available nahi hai.")

        with c4:
            st.markdown('<div class="sch-section">👤 Owner-wise Scholarship</div>', unsafe_allow_html=True)
            if owner_col and not filtered_sch.empty:
                os = (
                    filtered_sch.groupby(owner_col)
                    .agg(Students=(owner_col,"size"), Amount=("_Scholarship_Amount","sum"))
                    .reset_index().sort_values("Students",ascending=False).head(12)
                    .sort_values("Students")
                )
                fig = px.bar(os,x="Students",y=owner_col,orientation="h",text="Students",
                             color="Students",color_continuous_scale="Teal")
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=410,coloraxis_showscale=False,
                                  margin=dict(l=25,r=35,t=10,b=30),
                                  xaxis_title="Scholarship Students",yaxis_title="")
                fig.update_yaxes(showgrid=False)
                fig.update_xaxes(showgrid=True,gridcolor="#E8EDF3")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Owner data available nahi hai.")

        # ---------------- Trend + Category ----------------
        c5,c6 = st.columns(2, gap="large")

        with c5:
            st.markdown('<div class="sch-section">📈 Year-wise Scholarship Trend</div>', unsafe_allow_html=True)
            trend = (
                filtered_sch.groupby("Batch")
                .agg(Students=("Batch","size"), Amount=("_Scholarship_Amount","sum"))
                .reindex(["2024-26","2025-27","2026-28"], fill_value=0)
                .reset_index()
            )
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend["Batch"],y=trend["Students"],mode="lines+markers+text",
                text=trend["Students"],textposition="top center",
                name="Scholarship Students",line=dict(width=3,color="#2457B2")
            ))
            fig.update_layout(template="plotly_white",height=410,showlegend=False,
                              margin=dict(l=30,r=20,t=15,b=35),
                              xaxis_title="Batch",yaxis_title="Students")
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True,gridcolor="#E8EDF3")
            st.plotly_chart(fig,use_container_width=True)

        with c6:
            st.markdown('<div class="sch-section">🏆 Top Scholarship Categories / Criteria</div>', unsafe_allow_html=True)
            if category_col and not filtered_sch.empty:
                cs = filtered_sch[category_col].value_counts().head(10).reset_index()
                cs.columns=["Category / Criteria","Students"]
                fig = px.bar(cs.sort_values("Students"),x="Students",y="Category / Criteria",
                             orientation="h",text="Students",color="Students",
                             color_continuous_scale="Purples")
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=410,coloraxis_showscale=False,
                                  margin=dict(l=25,r=35,t=10,b=30),
                                  xaxis_title="Students",yaxis_title="")
                fig.update_yaxes(showgrid=False)
                fig.update_xaxes(showgrid=True,gridcolor="#E8EDF3")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Scholarship Category / Criteria data available nahi hai.")

        # ---------------- State Map + Detailed Table ----------------
        state_col = _sch_find(filtered_sch.columns, ["Correspondence State", "State"])
        c7,c8 = st.columns([1.05,1.45], gap="large")

        with c7:
            st.markdown('<div class="sch-section">📍 State-wise Scholarship Analysis</div>', unsafe_allow_html=True)
            if state_col and not filtered_sch.empty:
                ss = (
                    filtered_sch.groupby(state_col).size().reset_index(name="Students")
                    .sort_values("Students",ascending=False).head(10).sort_values("Students")
                )
                fig = px.bar(ss,x="Students",y=state_col,orientation="h",text="Students",
                             color="Students",color_continuous_scale="Blues")
                fig.update_traces(textposition="outside",cliponaxis=False)
                fig.update_layout(template="plotly_white",height=400,coloraxis_showscale=False,
                                  margin=dict(l=25,r=35,t=10,b=30),
                                  xaxis_title="Students",yaxis_title="")
                fig.update_yaxes(showgrid=False)
                fig.update_xaxes(showgrid=True,gridcolor="#E8EDF3")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("State data available nahi hai.")

        st.markdown('<div class="sch-section">🗺️ Geographic Scholarship Map</div>', unsafe_allow_html=True)
        india_state_coords = {
            "ANDHRA PRADESH":(15.9129,79.7400), "ASSAM":(26.2006,92.9376),
            "BIHAR":(25.0961,85.3131), "CHHATTISGARH":(21.2787,81.8661),
            "DELHI":(28.7041,77.1025), "GOA":(15.2993,74.1240),
            "GUJARAT":(22.2587,71.1924), "HARYANA":(29.0588,76.0856),
            "JHARKHAND":(23.6102,85.2799), "KARNATAKA":(15.3173,75.7139),
            "KERALA":(10.8505,76.2711), "MADHYA PRADESH":(22.9734,78.6569),
            "MAHARASHTRA":(19.7515,75.7139), "ODISHA":(20.9517,85.0985),
            "PUNJAB":(31.1471,75.3412), "RAJASTHAN":(27.0238,74.2179),
            "TAMIL NADU":(11.1271,78.6569), "TELANGANA":(18.1124,79.0193),
            "UTTAR PRADESH":(26.8467,80.9462), "UTTARAKHAND":(30.0668,79.0193),
            "WEST BENGAL":(22.9868,87.8550), "JAMMU AND KASHMIR":(33.7782,76.5762),
            "HIMACHAL PRADESH":(31.1048,77.1734), "CHANDIGARH":(30.7333,76.7794)
        }
        if state_col and not filtered_sch.empty:
            map_state = filtered_sch.copy()
            map_state["_MAP_STATE"] = map_state[state_col].fillna("").astype(str).str.upper().str.strip()
            map_state["_MAP_STATE"] = map_state["_MAP_STATE"].str.replace("&", "AND", regex=False)
            geo_rows=[]
            for state_name, grp in map_state.groupby("_MAP_STATE"):
                if state_name in india_state_coords:
                    lat, lon = india_state_coords[state_name]
                    geo_rows.append({
                        "State":state_name.title(), "Latitude":lat, "Longitude":lon,
                        "Students":len(grp),
                        "Amount":float(grp["_Scholarship_Amount"].sum())
                    })
            geo_df=pd.DataFrame(geo_rows)
            if not geo_df.empty:
                fig = px.scatter_geo(
                    geo_df, lat="Latitude", lon="Longitude", size="Students", color="Students",
                    hover_name="State",
                    hover_data={"Amount":":,.0f", "Latitude":False, "Longitude":False},
                    projection="natural earth", scope="asia", size_max=48,
                    color_continuous_scale="Blues"
                )
                fig.update_geos(
                    center=dict(lat=22.5, lon=80.0), projection_scale=4.2,
                    showcountries=True, countrycolor="#CBD5E1",
                    showland=True, landcolor="#F8FAFC",
                    showocean=True, oceancolor="#EAF4FF",
                    showlakes=True, lakecolor="#EAF4FF"
                )
                fig.update_layout(template="plotly_white", height=520,
                                  margin=dict(l=0,r=0,t=10,b=0), coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Map ke liye recognized Indian State names detect nahi hue. State-wise bar chart above available hai.")
        else:
            st.info("Map ke liye State data available nahi hai.")

        with c8:
            st.markdown('<div class="sch-section">📋 Detailed Scholarship Summary</div>', unsafe_allow_html=True)
            detail_cols = ["Batch"]
            for c in [programme_col, owner_col, city_col, category_col, amount_col]:
                if c and c in filtered_sch.columns and c not in detail_cols:
                    detail_cols.append(c)

            detail = filtered_sch[detail_cols].copy() if detail_cols else filtered_sch.copy()
            if amount_col and amount_col in detail.columns:
                detail = detail.rename(columns={amount_col:"Scholarship Amount"})
            elif "_Scholarship_Amount" in filtered_sch.columns:
                detail["Scholarship Amount"] = filtered_sch["_Scholarship_Amount"].values

            st.dataframe(detail, use_container_width=True, hide_index=True, height=365)

        # ---------------- Key Insights ----------------
        st.markdown('<div class="sch-section">💡 Scholarship Key Insights</div>', unsafe_allow_html=True)
        i1,i2,i3 = st.columns(3,gap="small")

        with i1:
            insights = []
            if total_students:
                insights.append(f"✓ {best_batch} batch has the highest scholarship participation.")
                insights.append(f"✓ {total_students:,} scholarship students in the current filtered view.")
                if total_amount > 0:
                    insights.append(f"✓ Total scholarship value is ₹{total_amount:,.0f}.")
            else:
                insights.append("✓ Current filters me scholarship record available nahi hai.")
            st.markdown(
                '<div class="sch-insight" style="border:1px solid #A7E3C2;background:#F5FCF7;">'
                '<b style="color:#15803D;">GROWTH OPPORTUNITIES</b><br><br>'
                + "<br>".join(insights[:3]) + '</div>',
                unsafe_allow_html=True
            )

        with i2:
            watch = []
            if total_students and avg_amount > 0:
                watch.append(f"⚠ Average scholarship is ₹{avg_amount:,.0f}; amount distribution should be monitored.")
            if category_col:
                watch.append("⚠ Review low-volume scholarship categories for awareness and utilisation.")
            watch.append("⚠ Use Batch, City and Amount filters to identify focused opportunities.")
            st.markdown(
                '<div class="sch-insight" style="border:1px solid #F2C56B;background:#FFFDF8;">'
                '<b style="color:#B45309;">ATTENTION REQUIRED</b><br><br>'
                + "<br>".join(watch[:3]) + '</div>',
                unsafe_allow_html=True
            )

        with i3:
            best = []
            if programme_col:
                best.append(f"★ {top_programme} is the leading programme for scholarships.")
            if category_col:
                best.append(f"★ {top_category} is the top scholarship category / criteria.")
            if city_col and sch_city != "All Cities":
                best.append(f"★ City drill-down active: {sch_city}.")
            else:
                best.append("★ City and Amount slicers are available for individual analysis.")
            st.markdown(
                '<div class="sch-insight" style="border:1px solid #A9C7F5;background:#F8FBFF;">'
                '<b style="color:#1D4ED8;">BEST PERFORMING AREAS</b><br><br>'
                + "<br>".join(best[:3]) + '</div>',
                unsafe_allow_html=True
            )

        # =====================================================
        # SCORE RANGE ANALYSIS - KEPT LAST AS REQUESTED
        # =====================================================
        st.markdown('<div class="sch-section">🎯 Scholarship Exam Score Range Analysis</div>', unsafe_allow_html=True)
        st.caption("Only scholarship recipients are included. Exam selection is based on EAS, while the displayed range is based on the corresponding percentile / entrance score.")

        if not range_df.empty:
            def _range_summary(source):
                out = (
                    source.groupby("Exam Range", as_index=False)
                    .agg(
                        Count=("Exam Range", "size"),
                        Amount=("_Scholarship_Amount", "mean"),
                        Total=("_Scholarship_Amount", "sum")
                    )
                )
                order = {e:i for i,e in enumerate(["CAT","MAT","CMAT","XAT","ATMA","GMAT"])}
                out["_exam_order"] = out["Exam Range"].str.split().str[0].map(order).fillna(99)
                out["_range_low"] = out["Exam Range"].str.extract(r"(\d+(?:\.\d+)?)")[0].astype(float)
                out = out.sort_values(["_exam_order","_range_low"]).drop(columns=["_exam_order","_range_low"])
                return out

            combined_range = _range_summary(range_df)

            # =====================================================
            # YEAR-WISE SCHOLARSHIP SCORE RANGE TABLE
            # All Batches + 2024-26 + 2025-27 + 2026-28
            # Table and ranges change when a batch tab is selected.
            # Only scholarship recipients / eligible score ranges appear.
            # =====================================================
            st.markdown('<div class="sch-section">🗓️ Year-wise Scholarship Score Range Summary</div>', unsafe_allow_html=True)
            range_tabs = st.tabs(["All Batches", "2024-26", "2025-27", "2026-28"])

            def _show_range_table(source, empty_message):
                if source.empty:
                    st.info(empty_message)
                    return
                tbl = _range_summary(source).copy()
                tbl["Amount"] = tbl["Amount"].round(0).astype(int)
                tbl["Total"] = tbl["Total"].round(0).astype(int)
                tbl = tbl.rename(columns={
                    "Exam Range": "Exam Range",
                    "Count": "Count",
                    "Amount": "Scholarship Amount (₹)",
                    "Total": "Total (₹)"
                })
                total_row = pd.DataFrame({
                    "Exam Range": ["Total"],
                    "Count": [int(tbl["Count"].sum())],
                    "Scholarship Amount (₹)": [int(tbl["Scholarship Amount (₹)"].sum())],
                    "Total (₹)": [int(tbl["Total (₹)"].sum())]
                })
                st.dataframe(
                    pd.concat([tbl, total_row], ignore_index=True),
                    use_container_width=True, hide_index=True
                )

            with range_tabs[0]:
                _show_range_table(range_df, "All Batches me scholarship exam-score data available nahi hai.")
            for tab, batch_name in zip(range_tabs[1:], ["2024-26", "2025-27", "2026-28"]):
                with tab:
                    _show_range_table(
                        range_df[range_df["Batch"] == batch_name],
                        f"{batch_name} me scholarship exam-score data available nahi hai."
                    )

            rc1, rc2 = st.columns(2, gap="large")
            with rc1:
                st.markdown('<div class="sch-section">📊 Scholarship Students by Score Range</div>', unsafe_allow_html=True)
                fig = px.bar(
                    combined_range,
                    x="Exam Range", y="Count", text="Count", color="Exam Range",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_traces(textposition="outside", cliponaxis=False)
                fig.update_layout(template="plotly_white", height=430, showlegend=False,
                                  xaxis_title="Scholarship Eligible Score Range", yaxis_title="Students",
                                  margin=dict(l=30,r=20,t=15,b=75))
                fig.update_xaxes(tickangle=-35, showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor="#E8EDF3")
                st.plotly_chart(fig, use_container_width=True)

            with rc2:
                st.markdown('<div class="sch-section">💰 Scholarship Amount by Score Range</div>', unsafe_allow_html=True)
                fig = px.bar(
                    combined_range,
                    x="Exam Range", y="Total", text="Total", color="Exam Range",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside", cliponaxis=False)
                fig.update_layout(template="plotly_white", height=430, showlegend=False,
                                  xaxis_title="Scholarship Eligible Score Range", yaxis_title="Total Scholarship Amount",
                                  margin=dict(l=30,r=20,t=15,b=75))
                fig.update_xaxes(tickangle=-35, showgrid=False)
                fig.update_yaxes(showgrid=True, gridcolor="#E8EDF3")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Scholarship recipients ke liye CAT / MAT / CMAT / XAT / ATMA / GMAT score data detect nahi hua.")


elif page == "📥 Download Report":
    show_page_heading("📥 Download Report")
# Test GitHub
