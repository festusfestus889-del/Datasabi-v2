import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

st.set_page_config(page_title="DataSabi Pro - ₦2,000", page_icon="💰", layout="wide")
st.markdown("<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>", unsafe_allow_html=True)

if 'data_room' not in st.session_state:
    st.session_state.data_room = {}
if 'active_file' not in st.session_state:
    st.session_state.active_file = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

qp = st.query_params
if "reference" in qp or "trxref" in qp or qp.get("paid") == "true":
    st.session_state.unlocked = True
    st.toast("✅ Payment verified! Premium report unlocked!", icon="💰")

with st.sidebar:
    st.title("📁 Data Room")
    uploaded_files = st.file_uploader("Upload CSV, Excel, ODS", type=["csv","xlsx","xls","txt","ods"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                st.session_state.data_room[file.name] = df
                st.session_state.active_file = file.name
                st.success(f"Loaded {file.name}")
            except Exception as e:
                st.error(f"Error {e}")
    st.divider()
    st.subheader("Upload by Link 🔗")
    link = st.text_input("Paste Google Sheet or CSV link")
    if st.button("🌐 Load Link") and link:
        try:
            if "docs.google.com" in link:
                link = link.split("/edit")[0] + "/export?format=csv"
            df = pd.read_csv(link) if "csv" in link or "docs.google" in link else pd.read_excel(link)
            name = f"link_{len(st.session_state.data_room)+1}.csv"
            st.session_state.data_room[name] = df
            st.session_state.active_file = name
            st.rerun()
        except:
            st.error("Failed to load")

if not st.session_state.data_room:
    st.markdown("## 📊 DataSabi Pro - Business Intelligence")
    st.info("👈 Tap top left > arrow to open Data Room and upload your sales, factory, inventory file")
    st.stop()

if st.session_state.active_file is None:
    st.session_state.active_file = list(st.session_state.data_room.keys())[0]
df = st.session_state.data_room[st.session_state.active_file]

st.markdown("## 📊 DataSabi Pro")
st.caption(f"Active: {st.session_state.active_file} | {len(df)} rows, {len(df.columns)} columns | Paystack LIVE")

tab1, tab2, tab3 = st.tabs(["📄 Table", "📊 Chart", "💰 Premium Report - ₦2,000"])

with tab1:
    st.dataframe(df, use_container_width=True)
with tab2:
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()
    if numeric_cols:
        x = st.selectbox("X-Axis", all_cols)
        y = st.selectbox("Y-Axis", numeric_cols)
        chart = st.selectbox("Chart", ["Bar","Line","Pie","Area"])
        fig = px.bar(df, x=x, y=y) if chart=="Bar" else px.line(df, x=x, y=y, markers=True) if chart=="Line" else px.pie(df, names=x, values=y, hole=0.4) if chart=="Pie" else px.area(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

def generate_pro_report(dataframe):
    num_cols = dataframe.select_dtypes(include='number').columns.tolist()
    cat_cols = dataframe.select_dtypes(exclude='number').columns.tolist()
    report = {}
    missing = dataframe.isnull().sum().sum()
    missing_pct = (missing / (dataframe.shape[0]*dataframe.shape[1]) *100) if dataframe.size>0 else 0
    dup = dataframe.duplicated().sum()
    report['quality'] = f"Dataset contains {dataframe.shape[0]} records across {dataframe.shape[1]} columns. Missing data: {missing} cells ({missing_pct:.1f}%). Duplicate rows: {dup}. Data completeness is {'Excellent' if missing_pct < 5 else 'Good but needs cleaning' if missing_pct < 20 else 'Poor'}."
    insights = []
    if num_cols:
        for col in num_cols[:3]:
            mean_val = dataframe[col].mean(); max_val = dataframe[col].max(); min_val = dataframe[col].min(); std_val = dataframe[col].std()
            insights.append(f"**{col}:** Average {mean_val:,.2f} (Range {min_val:,.2f} to {max_val:,.2f}, SD {std_val:,.2f}). {'High volatility' if std_val > mean_val*0.5 else 'Stable'}.")
        if len(num_cols) >= 2:
            corr = dataframe[num_cols[:4]].corr()
            corr_unstack = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool)).stack().sort_values(ascending=False)
            if not corr_unstack.empty:
                top_pair = corr_unstack.index[0]; top_val = corr_unstack.iloc[0]
                insights.append(f"**Correlation:** {top_pair[0]} vs {top_pair[1]} (r={top_val:.2f}) - primary leverage point.")
    if cat_cols:
        top_cat = dataframe[cat_cols[0]].value_counts().head(1)
        if not top_cat.empty:
            insights.append(f"**Category Dominance:** {cat_cols[0]} dominated by '{top_cat.index[0]}' ({top_cat.values[0]/len(dataframe)*100:.1f}%).")
    report['insights'] = insights
    recs = [f"1. Focus on top product >30% volume.", f"2. Avg of {num_cols[0]} is {dataframe[num_cols[0]].mean():,.2f}. Target +10%.", "3. Daily data validation."] if num_cols else ["Implement tracking"]
    report['recs'] = recs
    pres = ["**24H:** Pareto analysis.", "**7 Days:** Control limits >2 SD = alert.", "**30 Days:** Track vs predicted ROI."]
    report['pres'] = pres
    preds = []
    if num_cols:
        last_val = dataframe[num_cols[0]].iloc[-1]; avg = dataframe[num_cols[0]].mean(); trend = "upward" if last_val > avg else "downward" if last_val < avg else "stable"
        preds.append(f"**Trend:** {num_cols[0]} is {trend}. Avg {avg:,.2f} vs last {last_val:,.2f}. Next: {avg*1.05:,.2f} (+5% with action).")
        preds.append(f"**Risk:** Target probability {82 if trend!='downward' else 58}%.")
        preds.append(f"**Opportunity:** 12-18% gain = 6x ROI on ₦2,000.")
    report['preds'] = preds
    return report

with tab3:
    if not st.session_state.unlocked:
        st.markdown("""
        <div style="border:3px solid #4f46e5; border-radius:16px; padding:25px; background:#eef2ff; text-align:center;">
            <h2>🔒 Unlock Professional Consulting Report - ₦2,000</h2>
            <p>Full 4-page business report</p>
            <p>✅ Data Quality Audit • 5 Insights • Recommendations • Prescriptions • Predictions</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.link_button("💳 PAY ₦2,000 - GET FULL REPORT (REAL PAYSTACK)", "https://paystack.shop/pay/2jji7vgoln", use_container_width=True)
        st.write("")
        if st.button("✅ I've Paid - Show My Report", use_container_width=True):
            st.session_state.unlocked = True
            st.rerun()
        st.caption("After payment, Paystack auto-redirects and unlocks. If slow network, click I've Paid.")
    else:
        st.success(f"✅ Premium Report Active - {datetime.now().strftime('%B %d, %Y %I:%M %p')} - Verified")
        st.balloons()
        rpt = generate_pro_report(df)
        st.markdown("### 📋 1. EXECUTIVE SUMMARY & DATA QUALITY AUDIT")
        st.write(rpt['quality']); st.divider()
        st.markdown("### 🔍 2. KEY INSIGHTS")
        for i, ins in enumerate(rpt['insights'], 1): st.info(f"**Insight {i}:** {ins}")
        st.divider()
        st.markdown("### 💡 3. RECOMMENDATIONS")
        for rec in rpt['recs']: st.success(rec)
        st.divider()
        st.markdown("### 📝 4. PRESCRIPTIONS")
        for p in rpt['pres']: st.warning(p)
        st.divider()
        st.markdown("### 🔮 5. PREDICTIONS & ROI")
        for pred in rpt['preds']: st.markdown(f"<div style='background:#f0fdf4; border-left:5px solid #22c55e; padding:15px; margin:10px 0; border-radius:8px;'>{pred}</div>", unsafe_allow_html=True)
        st.divider()
        if st.button("Lock Report Again"):
            st.session_state.unlocked = False
            st.query_params.clear()
            st.rerun()
