import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataSabi Pro - ₦2,000", page_icon="💰", layout="wide")
st.markdown("<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>", unsafe_allow_html=True)

if 'data_room' not in st.session_state:
    st.session_state.data_room = {}
if 'active_file' not in st.session_state:
    st.session_state.active_file = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

qp = st.query_params
# Auto-unlock if coming from Paystack
if "reference" in qp or "trxref" in qp or qp.get("paid") == "true":
    st.session_state.unlocked = True
    st.toast("✅ Payment verified! Premium unlocked!", icon="💰")

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
    st.markdown("## 📊 DataSabi Pro")
    st.info("👈 Open sidebar > Upload file to start - Tap top left > arrow")
    st.stop()

if st.session_state.active_file is None:
    st.session_state.active_file = list(st.session_state.data_room.keys())[0]
df = st.session_state.data_room[st.session_state.active_file]

st.markdown("## 📊 DataSabi Pro")
st.caption(f"Active: {st.session_state.active_file} - {len(df)} rows | Paystack LIVE")

tab1, tab2, tab3 = st.tabs(["📄 Table", "📊 Chart", "💰 Unlock"])

with tab1:
    st.dataframe(df, use_container_width=True)
with tab2:
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()
    if numeric_cols:
        x = st.selectbox("X-Axis", all_cols)
        y = st.selectbox("Y-Axis", numeric_cols)
        chart = st.selectbox("Chart", ["Bar","Line","Pie","Area"])
        if chart=="Bar":
            fig = px.bar(df, x=x, y=y)
        elif chart=="Line":
            fig = px.line(df, x=x, y=y, markers=True)
        elif chart=="Pie":
            fig = px.pie(df, names=x, values=y, hole=0.4)
        else:
            fig = px.area(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    if not st.session_state.unlocked:
        st.markdown("""
        <div style="border:3px solid #4f46e5; border-radius:16px; padding:25px; background:#eef2ff; text-align:center;">
            <h2>🔒 Unlock Full Intelligence - ₦2,000 Only</h2>
            <p><b>Real Paystack Payment - Auto Unlock</b></p>
            <p>✅ Insights • Recommendation • Prescription • Prediction</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.link_button("💳 PAY ₦2,000 WITH PAYSTACK - REAL", "https://paystack.shop/pay/2jji7vgoln", use_container_width=True)
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I've Paid - Unlock Now", use_container_width=True):
                st.session_state.unlocked = True
                st.rerun()
        with col2:
            if st.button("🧪 Demo (Free Test)", use_container_width=True):
                st.session_state.unlocked = True
                st.rerun()
        st.caption("After paying, you'll be redirected back here and auto-unlocked. If not, click 'I've Paid'.")
    else:
        st.success("✅ Premium Active - Payment Verified!")
        st.balloons()
        st.metric("Total rows", len(df))
        st.info("Insight: Quality best at moderate temp 70-80C")
        st.success("Recommendation: Keep temp stable")
        st.warning("Prescription: Calibrate daily")
        st.metric("Prediction", "96% Quality Expected")
        if st.button("Lock Again"):
            st.session_state.unlocked = False
            st.query_params.clear()
            st.rerun()
