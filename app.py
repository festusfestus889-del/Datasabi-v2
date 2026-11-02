import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="DataSabi - Business Intelligence", page_icon="📊", layout="wide")

# --- PRO STYLING ---
st.markdown("""
<style>
.metric-card {background: #f8f9ff; padding: 20px; border-radius: 12px; border: 1px solid #e0e7ff;}
.big-title {font-size: 3rem; font-weight: 800; color: #1e293b;}
.subtitle {color: #64748b; font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<p class="big-title">📊 DataSabi</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Professional Intelligence for Business Owners & Individuals in Africa</p>', unsafe_allow_html=True)
with col2:
    st.write("")
    st.caption(f"{datetime.now().strftime('%A, %d %B %Y')}")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1822/1822663.png", width=60)
    st.title("DataSabi Pro")
    user_type = st.radio("Select Workspace", ["🏢 Business Owner", "👤 Individual", "📈 Analytics"])
    st.divider()
    st.info("💡 Tip: Track daily to get smart insights.")

# --- BUSINESS OWNER - PRO DASHBOARD ---
if user_type == "🏢 Business Owner":
    st.subheader("Business Performance Dashboard")
    
    c1, c2, c3, c4 = st.columns(4)
    sales = c1.number_input("Total Sales Today (₦)", value=50000)
    expenses = c2.number_input("Total Expenses (₦)", value=20000)
    customers = c3.number_input("Customers Today", value=25)
    target = c4.number_input("Daily Target (₦)", value=60000)
    
    profit = sales - expenses
    margin = (profit/sales*100) if sales>0 else 0
    progress = min(sales/target*100, 100) if target>0 else 0
    
    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Revenue", f"₦{sales:,}", f"{progress:.0f}% of target")
    k2.metric("Profit", f"₦{profit:,}", f"{margin:.1f}% margin")
    k3.metric("Customers", f"{customers}", "Today")
    k4.metric("Health", "✅ Good" if profit>0 else "⚠️ Review", "Business")

    # Chart
    df = pd.DataFrame({
        "Category": ["Sales", "Expenses", "Profit"],
        "Amount": [sales, expenses, profit]
    })
    fig = px.bar(df, x="Category", y="Amount", color="Category", text_auto=True, color_discrete_map={"Sales":"#4f46e5","Expenses":"#ef4444","Profit":"#10b981"})
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Generate Business Insight →"):
        st.success(f"Insight: Your profit margin is {margin:.1f}%. {'Focus on increasing customers to hit your ₦{target:,} target.' if sales < target else 'Excellent! You exceeded your target.'}")

# --- INDIVIDUAL - PRO ---
elif user_type == "👤 Individual":
    st.subheader("Personal Wealth Dashboard")
    
    c1, c2 = st.columns(2)
    income = c1.number_input("Monthly Income (₦)", value=150000)
    spend = c2.number_input("Total Spending (₦)", value=95000)
    
    savings = income - spend
    rate = (savings/income*100) if income>0 else 0
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Savings", f"₦{savings:,}")
    k2.metric("Savings Rate", f"{rate:.1f}%")
    k3.metric("Status", "💰 Wealth Builder" if rate>30 else "📊 Needs Plan")
    
    df2 = pd.DataFrame({"Type": ["Income", "Spending", "Savings"], "Amount": [income, spend, savings]})
    fig2 = px.pie(df2, values="Amount", names="Type", hole=0.5, color_discrete_sequence=["#4f46e5","#ef4444","#10b981"])
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.subheader("Analytics & Growth")
    st.write("Coming soon: Trends, weekly reports, and export to Excel.")
    st.bar_chart({"Mon": [20], "Tue": [35], "Wed": [30], "Thu": [50], "Fri": [45]})

st.divider()
st.caption("DataSabi Pro • Built for Business Owners & Individuals • Port Harcourt, NG")
