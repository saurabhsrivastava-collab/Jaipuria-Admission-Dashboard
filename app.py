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

</style>
""", unsafe_allow_html=True)
# ---------------- Sidebar ----------------

st.sidebar.title("🎓 Jaipuria")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Summary",
        "👨 Gender",
        "🎓 Stream",
        "📝 Entrance Exam",
        "📍 State & City",
        "👤 Owner Analysis",
        "🏢 Campus Analysis",
        "💰 Scholarship",
        "📥 Download Report"
    ]
)

# ---------------- Main Page ----------------

st.title("🎓 Jaipuria Admission Dashboard")
st.subheader("Live Google Sheet Connected 🟢")

st.divider()
SHEET_ID = "1RKLRXNSFxeq4kXEYxA9y0EFuK-5Ozukrr3ejjxm0764"

def load_sheet(gid, batch):

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df["Batch"] = batch

    return df


df2026 = load_sheet(0, "2026-28")

df2025 = load_sheet(1713921462, "2025-27")

df2024 = load_sheet(1951957125, "2024-26")

df = pd.concat(
    [df2026, df2025, df2024],
    ignore_index=True
)
if page == "🏠 Summary":

    admitted_2024 = len(df2024[df2024["Final Status"].isin(["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"])])
    admitted_2025 = len(df2025[df2025["Final Status"].isin(["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"])])
    admitted_2026 = len(df2026[df2026["Final Status"].isin(["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"])])

    st.header("📊 Summary Dashboard")

    st.markdown("### 👨‍🎓 Total Admitted Students")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎓 2024-26", admitted_2024)

    with col2:
        st.metric("🎓 2025-27", admitted_2025)

    with col3:
        st.metric("🎓 2026-28", admitted_2026)

    st.markdown("---")
    
    st.markdown("""
<div style="margin-top:-10px; margin-bottom:20px;">
    <h4 style="color:#1f77b4;">🎯 60% & Above Throughout Academic Records</h4>
    <p style="margin-top:-10px; color:gray;">
        <i>(10th • 12th • Graduation)</i>
    </p>
</div>
""", unsafe_allow_html=True)
    

    # Only admitted students
    summary_df = df[
        df["Final Status"].isin(
            ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
        )
    ]

    # Students having 60% or above in 10th, 12th and Graduation
    eligible_df = summary_df[
        (pd.to_numeric(summary_df["10th Percentage"], errors="coerce") >= 60) &
        (pd.to_numeric(summary_df["12th Percentage"], errors="coerce") >= 60) &
        (pd.to_numeric(summary_df["Graduation Percentage"], errors="coerce") >= 60)
    ]

    total_2024 = len(eligible_df[eligible_df["Batch"] == "2024-26"])
    total_2025 = len(eligible_df[eligible_df["Batch"] == "2025-27"])
    total_2026 = len(eligible_df[eligible_df["Batch"] == "2026-28"])

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎓 2024-26", total_2024)

    with col2:
        st.metric("🎓 2025-27", total_2025)

    with col3:
        st.metric("🎓 2026-28", total_2026)

    st.markdown("---")
    st.subheader("📈 Total Admission Trend")

    admission_chart = pd.DataFrame({
        "Batch": ["2024-26", "2025-27", "2026-28"],
        "Admissions": [admitted_2024, admitted_2025, admitted_2026]
    })

    fig = px.bar(
        admission_chart,
        x="Batch",
        y="Admissions",
        text="Admissions",
        color="Batch"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 60% & Above Throughout Academic Records Trend")

    eligible_chart = pd.DataFrame({
        "Batch": ["2024-26", "2025-27", "2026-28"],
        "Students": [total_2024, total_2025, total_2026]
    })

    fig = px.bar(
        eligible_chart,
        x="Batch",
        y="Students",
        text="Students",
        color="Batch"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

elif page == "👨 Gender":

    st.header("👨 Gender Analysis")

    gender_df = df[df["Final Status"].isin(["FULL FEE","PARTIAL FEE","WAITLIST FEE"])].copy()
    gender_df["Gender"]=(gender_df["Gender"].astype(str).str.upper().replace({"M":"MALE","F":"FEMALE"}))

    summary=(gender_df.groupby(["Batch","Gender"]).size().unstack(fill_value=0).reset_index())
    if "MALE" not in summary.columns: summary["MALE"]=0
    if "FEMALE" not in summary.columns: summary["FEMALE"]=0
    summary["Total"]=summary["MALE"]+summary["FEMALE"]

    st.subheader("📊 Gender Summary")
    c1,c2,c3=st.columns(3)
    for col,batch in zip([c1,c2,c3],["2024-26","2025-27","2026-28"]):
        row=summary[summary["Batch"]==batch]
        if not row.empty:
            total=int(row["Total"].iloc[0]); male=int(row["MALE"].iloc[0]); female=int(row["FEMALE"].iloc[0])
        else:
            total=male=female=0
        col.metric(batch,total,f"👨 {male} | 👩 {female}")

        st.divider()
    st.subheader("📈 Year Wise Gender Comparison")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Male",
        x=summary["Batch"],
        y=summary["MALE"],
        marker_color="#2563EB",
        text=summary["MALE"],
        textposition="outside"
    ))

    fig.add_trace(go.Bar(
        name="Female",
        x=summary["Batch"],
        y=summary["FEMALE"],
        marker_color="#EC4899",
        text=summary["FEMALE"],
        textposition="outside"
    ))

    fig.update_layout(
        template="plotly_white",
        height=550,
        barmode="group",
        title="Year Wise Gender Comparison",
        title_x=0.5,
        xaxis_title="Batch",
        yaxis_title="Number of Students",
        legend_title="Gender",
        font=dict(size=18),
        title_font=dict(size=24),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "🎓 Stream":

    st.header("🎓 Graduation Stream Analysis")

    stream_df = df[
        df["Final Status"].isin(
            ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
        )
    ].copy()

    stream_summary = (
        stream_df.groupby(["Graduation Stream", "Batch"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    total_row = pd.DataFrame({
        "Graduation Stream": ["Total"],
        "2024-26": [stream_summary["2024-26"].sum()],
        "2025-27": [stream_summary["2025-27"].sum()],
        "2026-28": [stream_summary["2026-28"].sum()]
    })

    stream_summary = pd.concat([stream_summary, total_row], ignore_index=True)

    st.subheader("📋 Graduation Stream Summary")
    st.dataframe(stream_summary, use_container_width=True)

    chart_source = stream_summary[
        stream_summary["Graduation Stream"] != "Total"
    ]

    chart_df = chart_source.melt(
        id_vars="Graduation Stream",
        value_vars=["2024-26", "2025-27", "2026-28"],
        var_name="Batch",
        value_name="Students"
    )

    fig = px.bar(
        chart_df,
        x="Graduation Stream",
        y="Students",
        color="Batch",
        barmode="group",
        text="Students"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)

elif page == "📝 Entrance Exam":
    st.header("📝 Entrance Exam Analysis")

    st.header("📍 State & City Analysis")

    state_df = df[
        df["Final Status"].isin(
            ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
        )
    ].copy()

    state_summary = (
        state_df.groupby(["Correspondence State", "Batch"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    total_row = pd.DataFrame({
        "Correspondence State": ["Total"],
        "2024-26": [state_summary["2024-26"].sum()],
        "2025-27": [state_summary["2025-27"].sum()],
        "2026-28": [state_summary["2026-28"].sum()]
    })

    state_summary = pd.concat(
        [state_summary, total_row],
        ignore_index=True
    )

    st.header("📍 State & City Analysis")

    # Admitted Students
    state_df = df[
        df["Final Status"].isin(
            ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
        )
    ].copy()

    # State Summary
    state_summary = (
        state_df.groupby(["Correspondence State", "Batch"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Ensure all batch columns exist
    for col in ["2024-26", "2025-27", "2026-28"]:
        if col not in state_summary.columns:
            state_summary[col] = 0

    # Total Row
    total_row = pd.DataFrame({
        "Correspondence State": ["Total"],
        "2024-26": [state_summary["2024-26"].sum()],
        "2025-27": [state_summary["2025-27"].sum()],
        "2026-28": [state_summary["2026-28"].sum()]
    })

    state_summary = pd.concat(
        [state_summary, total_row],
        ignore_index=True
    )

elif page == "📍 State & City":

    st.header("📍 State & City Analysis")

    state_df = df[
        df["Final Status"].isin(
            ["FULL FEE", "PARTIAL FEE", "WAITLIST FEE"]
        )
    ].copy()

    state_summary = (
        state_df.groupby(["Correspondence State", "Batch"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    for col in ["2024-26", "2025-27", "2026-28"]:
        if col not in state_summary.columns:
            state_summary[col] = 0
    
    total_row = pd.DataFrame({
        "Correspondence State": ["Total"],
        "2024-26": [state_summary["2024-26"].sum()],
        "2025-27": [state_summary["2025-27"].sum()],
        "2026-28": [state_summary["2026-28"].sum()],
    })
    state_summary = pd.concat(
        [state_summary, total_row],
        ignore_index=True
    )

    st.subheader("📍 State Summary")
    st.dataframe(state_summary, use_container_width=True)

    graph_df = state_summary[
        state_summary["Correspondence State"] != "Total"
    ]

    chart_df = graph_df.melt(
        id_vars="Correspondence State",
        value_vars=["2024-26", "2025-27", "2026-28"],
        var_name="Batch",
        value_name="Students"
    )

    st.subheader("📊 State Wise Comparison")

    fig = px.bar(
        chart_df,
        x="Correspondence State",
        y="Students",
        color="Batch",
        barmode="group",
        text="Students"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=650,
        xaxis_title="State",
        yaxis_title="Students"
    )

    st.plotly_chart(fig, use_container_width=True)

    city_summary = (
        state_df.groupby(["Correspondence city", "Batch"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    for col in ["2024-26", "2025-27", "2026-28"]:
        if col not in city_summary.columns:
            city_summary[col] = 0

    total_row = pd.DataFrame({
        "Correspondence city": ["Total"],
        "2024-26": [city_summary["2024-26"].sum()],
        "2025-27": [city_summary["2025-27"].sum()],
        "2026-28": [city_summary["2026-28"].sum()]
    })

    city_summary = pd.concat(
        [city_summary, total_row],
        ignore_index=True
    )

    st.dataframe(city_summary, use_container_width=True)
    # ==========================
    # Top 15 Cities Graph
    # ==========================

    chart_city = city_summary[city_summary["Correspondence city"] != "Total"].copy()

    # Overall Total
    chart_city["Total"] = (
        chart_city["2024-26"] +
        chart_city["2025-27"] +
        chart_city["2026-28"]
    )

    # Top 15 Cities
    top15_city = chart_city.sort_values(
        by="Total",
        ascending=False
    ).head(15)

    fig = px.bar(
        top15_city,
        x="Correspondence city",
        y=["2024-26", "2025-27", "2026-28"],
        barmode="group",
        text_auto=True,
        title="🏙️ Top 15 Cities - Admission Comparison"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=650,
        xaxis_title="City",
        yaxis_title="Students",
        xaxis_tickangle=-45,
        legend_title="Batch"
    )

    st.plotly_chart(fig, use_container_width=True)
elif page == "👤 Owner Analysis":
    st.header("👤 Owner Analysis")

elif page == "🏢 Campus Analysis":
    st.header("🏢 Campus Analysis")

elif page == "💰 Scholarship":
    st.header("💰 Scholarship Analysis")

elif page == "📥 Download Report":
    st.header("📥 Download Report")
# Test GitHub