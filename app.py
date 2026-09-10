import streamlit as st
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
    padding-top:0.5rem;
    padding-left:2rem;
    padding-right:2rem;
    max-width:100%;
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
}

h2{
    font-size:34px !important;
}

h3{
    font-size:26px !important;
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

st.sidebar.title("🎓 Jaipuria")

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
    margin: 4px 0 8px 0;
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
