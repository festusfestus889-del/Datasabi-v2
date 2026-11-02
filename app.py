import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

st.set_page_config(page_title="DataSabi - Data Room", page_icon="📊", layout="wide")

if 'data_room' not in st.session_state:
    st.session_state.data_room = {}
if 'active_file' not in st.session_state:
    st.session_state.active_file = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

st.markdown("## 📊 DataSabi Pro")
st.caption("Data Room • Upload Files + Links • Table + One Chart")
st.divider()

# --- SIDEBAR DATA ROOM ---
with st.sidebar:
    st.title("📁 Data Room")
    
    # 1. FILE UPLOAD
    st.subheader("1. Upload File")
    uploaded_files = st.file_uploader(
        "CSV, Excel, TXT", 
        type=["csv","xlsx","xls","txt"], 
        accept_multiple_files=True
    )
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.name.endswith('.csv') or file.name.endswith('.txt'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                st.session_state.data_room[file.name] = df
                st.session_state.active_file = file.name
                st.success(f"Added {file.name}")
            except Exception as e:
                st.error(f"Failed {file.name}: {e}")

    st.divider()
    
    # 2. LINK UPLOAD - NEW!
    st.subheader("2. Upload by Link 🔗")
    st.caption("Paste link to CSV, Excel, Google Sheet")
    
    link = st.text_input("Paste data link here:", placeholder="https://.../data.csv")
    link_name = st.text_input("Name for this data:", placeholder="e.g. sales_data.csv")
    
    if st.button("🌐 Load Data from Link"):
        if not link:
            st.warning("Please paste a link")
        else:
            try:
                with st.spinner("Loading from link..."):
                    # Handle Google Sheets link conversion
                    if "docs.google.com/spreadsheets" in link:
                        # Convert to export csv link
                        if "/edit" in link:
                            link = link.split("/edit")[0] + "/export?format=csv"
                    
                    if link.endswith('.csv') or 'csv' in link or 'docs.google' in link:
                        df = pd.read_csv(link)
                    else:
                        df = pd.read_excel(link)
                    
                    name = link_name if link_name else f"link_data_{len(st.session_state.data_room)+1}.csv"
                    if not name.endswith(('.csv','.xlsx')):
                        name += ".csv"
                    
                    st.session_state.data_room[name] = df
                    st.session_state.active_file = name
                    st.success(f"Loaded {name} - {len(df)} rows")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to load link: {e}")
                st.info("Tip: For Google Sheets, make it 'Anyone with link can view' then paste link")

    st.divider()
    st.subheader(f"Files in Room ({len(st.session_state.data_room)})")
    
    if st.session_state.data_room:
        for name in list(st.session_state.data_room.keys()):
            col1, col2 = st.columns([4,1])
            is_active = st.session_state.active_file == name
            if col1.button(f"{'🟢 ' if is_active else '📄 '}{name}", key=f"sel_{name}", use_container_width=True):
                st.session_state.active_file = name
                st.rerun()
            if col2.button("❌", key=f"del_{name}"):
                del st.session_state.data_room[name]
                if st.session_state.active_file == name:
                    st.session_state.active_file = None
                st.rerun()
        
        if st.button("Clear Entire Room"):
            st.session_state.data_room = {}
            st.session_state.active_file = None
            st.rerun()
    else:
        st.info("Room empty")
        if st.button("Load Demo Data"):
            demo = pd.DataFrame({
                "Date": pd.date_range("2026-10-20", periods=12),
                "Sales": [45000,52000,38000,62000,58000,71000,49000,68000,72000,65000,80000,82000],
                "Expenses": [20000,22000,18000,25000,23000,28000,21000,27000,30000,26000,32000,35000],
                "Customers": [20,25,18,30,28,35,22,32,34,31,38,40],
                "Source_Link": ["https://example.com/data.csv"]*12
            })
            st.session_state.data_room["demo_business.csv"] = demo
            st.session_state.active_file = "demo_business.csv"
            st.rerun()

# --- MAIN ---
if not st.session_state.data_room:
    st.info("👈 Go to Data Room: Upload file OR paste link to CSV/Excel/Google Sheet")
    st.markdown("""
    **How to use Link:**
    - Direct CSV link: `https://example.com/sales.csv`
    - Google Sheets: Share > Anyone with link > Paste link here
    - Excel link: `https://example.com/data.xlsx`
    """)
    st.stop()

if st.session_state.active_file is None:
    st.session_state.active_file = list(st.session_state.data_room.keys())[0]

df = st.session_state.data_room[st.session_state.active_file]

st.subheader(f"📄 Active: {st.session_state.active_file}")
st.caption(f"{len(df)} rows × {len(df.columns)} columns | Source includes link if uploaded by link")

# 1. TABLE - SHOW RAW DATA WITH LINK COLUMN
st.markdown("### 1. Raw Data Table (with source link if any)")
st.dataframe(df, use_container_width=True, height=380)

# Show download + link info
c1, c2 = st.columns(2)
with c1:
    st.download_button("📥 Download CSV", df.to_csv(index=False), f"{st.session_state.active_file}.csv")
with c2:
    if st.button("🔗 Copy Data Room Link"):
        st.info("Share your Streamlit app link - Data Room keeps files in session")

st.divider()

# 2. ONE CHART ONLY
st.markdown("### 2. Visualization (One Chart)")
numeric_cols = df.select_dtypes(include='number').columns.tolist()
all_cols = df.columns.tolist()

if numeric_cols:
    c1, c2, c3 = st.columns(3)
    x_axis = c1.selectbox("X-Axis", all_cols, index=0)
    y_axis = c2.selectbox("Y-Axis", numeric_cols, index=0)
    chart_type = c3.selectbox("Chart Type", ["Bar", "Line", "Pie", "Scatter", "Area"])
    
    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis, markers=True)
    elif chart_type == "Pie":
        fig = px.pie(df, names=x_axis, values=y_axis, hole=0.4)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    else:
        fig = px.area(df, x=x_axis, y=y_axis)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No numeric columns for chart")

st.divider()
st.caption("DataSabi • Data Room supports File Upload + Link Upload • Raw data always includes source")
