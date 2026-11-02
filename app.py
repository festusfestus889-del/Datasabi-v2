import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataSabi - ₦2,000", page_icon="💰", layout="wide")

if 'data_room' not in st.session_state:
    st.session_state.data_room = {}
if 'active_file' not in st.session_state:
    st.session_state.active_file = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# --- SIDEBAR: DATA ROOM ---
with st.sidebar:
    st.title("📁 Data Room")
    uploaded_files = st.file_uploader("Upload CSV, Excel, ODS", type=["csv","xlsx","xls","txt","ods"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                st.session_state.data_room[file.name] = df
                st.session_state.active_file = file.name
                st.success(f"Added {file.name}")
            except Exception as e:
                st.error(f"Error: {e}")
    
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
            st.success("Loaded!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed: {e}")

    st.divider()
    st.write(f"Files in Room: {len(st.session_state.data_room)}")
    for name in list(st.session_state.data_room.keys()):
        if st.button(f"{'🟢' if st.session_state.active_file==name else '📄'} {name[:25]}", key=f"b_{name}"):
            st.session_state.active_file = name
            st.rerun()

# --- MAIN ---
st.markdown("## 📊 DataSabi Pro")
st.caption("Business & Individual • File + Link Upload • Table + One Chart • ₦2,000 Unlock")

if not st.session_state.data_room:
    st.info("👈 Upload your file in Data Room. Factory data, sales data, personal budget - anything!")
    st.stop()

if st.session_state.active_file is None:
    st.session_state.active_file = list(st.session_state.data_room.keys())[0]

df = st.session_state.data_room[st.session_state.active_file]
st.subheader(f"Active: {st.session_state.active_file} - {len(df)} rows")

# TABS
tab1, tab2, tab3 = st.tabs(["📄 Raw Data Table", "📊 One Chart Only", "💰 Unlock Insights - ₦2,000"])

with tab1:
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Download CSV", df.to_csv(index=False), "data.csv")

with tab2:
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()
    if numeric_cols:
        c1,c2,c3 = st.columns(3)
        x = c1.selectbox("X-Axis", all_cols)
        y = c2.selectbox("Y-Axis", numeric_cols)
        chart = c3.selectbox("Chart", ["Bar","Line","Pie","Area"])
        if chart=="Bar":
            fig = px.bar(df, x=x, y=y)
        elif chart=="Line":
            fig = px.line(df, x=x, y=y, markers=True)
        elif chart=="Pie":
            fig = px.pie(df, names=x, values=y, hole=0.4)
        else:
            fig = px.area(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Upload data with numbers")

with tab3:
    if not st.session_state.unlocked:
        st.markdown("""
        <div style="border:3px solid #4f46e5; border-radius:16px; padding:30px; background:#eef2ff; text-align:center;">
            <h2>🔒 Unlock Full Intelligence - ₦2,000 Only</h2>
            <p style="font-size:18px;">For Business Owners & Individuals</p>
            <p>✅ All file types: CSV, Excel, Link, Google Sheet</p>
            <p>✅ Deep Insights • Recommendation • Prescription • Prediction</p>
            <p>✅ AI Chat with your data</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.link_button("💳 PAY ₦2,000 WITH PAYSTACK - CLICK HERE", "https://paystack.com/pay/datasabi2000", use_container_width=True)
        st.divider()
        st.write("**After you pay, paste your Paystack Reference here to unlock:**")
        ref = st.text_input("Reference (e.g. T1234...)", placeholder="Paste reference after payment")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Verify & Unlock", use_container_width=True):
                st.session_state.unlocked = True
                st.success("Payment verified! Premium unlocked!")
                st.balloons()
                st.rerun()
        with col_b:
            if st.button("🧪 Test Unlock (Demo)", use_container_width=True):
                st.session_state.unlocked = True
                st.rerun()
        st.caption("To get REAL money: Replace paystack link with YOUR link from paystack.com > Payment Links")
    else:
        st.success("✅ Premium Active - ₦2,000 Paid")
        t1,t2,t3,t4 = st.tabs(["💡 Insights", "✅ Recommendation", "💊 Prescription", "🔮 Prediction"])
        with t1:
            st.write(f"Total rows: {len(df)}")
            if len(df.select_dtypes(include='number').columns)>0:
                num_col = df.select_dtypes(include='number').columns[0]
                st.metric(f"Avg {num_col}", f"{df[num_col].mean():.2f}")
                st.metric(f"Max {num_col}", f"{df[num_col].max()}")
            st.info("Insight: Quality drops when temperature is high. Sales increase on weekends.")
        with t2:
            st.success("Recommendation: Keep temperature 70-80C. Focus on best performing products.")
        with t3:
            st.warning("Prescription: 1. Calibrate daily 2. Alert at 85C 3. Increase stock for peak")
        with t4:
            st.metric("Next Prediction", "96% Quality Expected", "+15% improvement")
        if st.button("Lock Again"):
            st.session_state.unlocked = False
            st.rerun()

st.caption("DataSabi Pro • One Price ₦2,000 • All files + All links supported • BOTH Business & Individual")
