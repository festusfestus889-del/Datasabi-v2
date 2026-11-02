import streamlit as st

st.set_page_config(page_title="DataSabi", page_icon="📊", layout="centered")

st.title("📊 DataSabi v2")
st.write("Helping Business Owners & Individuals make smart decisions with data.")

# --- User Type ---
user_type = st.radio("Who are you?", ["Business Owner", "Individual"], horizontal=True)

st.divider()

if user_type == "Business Owner":
    st.subheader("For Business Owners")
    st.write("Track your business quickly.")
    
    business_name = st.text_input("Business Name")
    sales = st.number_input("Today's Sales (₦)", min_value=0)
    expenses = st.number_input("Today's Expenses (₦)", min_value=0)
    
    if st.button("Calculate Profit"):
        profit = sales - expenses
        st.success(f"{business_name} Profit Today: ₦{profit:,.0f}")
        if profit > 0:
            st.write("✅ You are growing! Keep it up.")
        else:
            st.write("⚠️ Watch your spending.")

else:
    st.subheader("For Individuals")
    st.write("Manage your personal money.")
    
    income = st.number_input("Monthly Income (₦)", min_value=0)
    spend = st.number_input("Monthly Spending (₦)", min_value=0)
    
    if st.button("Check Savings"):
        saving = income - spend
        st.success(f"You saved: ₦{saving:,.0f}")
        if saving > 0:
            st.write("💰 Good job saving!")
        else:
            st.write("📉 Try to reduce spending next month.")

st.divider()
st.caption("DataSabi v2 - Clean Build - No errors")
