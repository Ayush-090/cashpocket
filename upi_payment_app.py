import streamlit as st
import qrcode
from PIL import Image
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CashPocket 💼", page_icon="💰")

# Title and logo
st.image("cashpocket_logo.png", width=150)
st.title("💼 CashPocket – UPI-based Loan Approval")

# Generate QR code for UPI
upi_id = "ayushbhradwaj009-1@okicici"
upi_name = "Ayush Bhardwaj"
qr_data = f"upi://pay?pa={upi_id}&pn={upi_name}"
qr_img = qrcode.make(qr_data)
qr_img.save("upi_qr.png")
st.image("upi_qr.png", caption="Scan to Pay", width=250)

# Admin confirms payment received
st.subheader("🔐 Step 1: Verify Payment")
payment_verified = st.checkbox("✅ Payment received and verified by admin")

if payment_verified:
    st.subheader("📝 Step 2: Fill Loan Request Form")

    name = st.text_input("Full Name")
    contact = st.text_input("Contact Number")
    email = st.text_input("Email (optional)")
    loan_amount = st.number_input("Desired Loan Amount (₹)", min_value=1000.0, step=500.0)
    reason = st.text_area("Reason for Loan")

    if st.button("📩 Submit Loan Request"):
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_data = pd.DataFrame([[name, contact, email, loan_amount, reason, submission_time]],
                                    columns=["Name", "Contact", "Email", "Amount (₹)", "Reason", "Timestamp"])

        if os.path.exists("loan_requests.csv"):
            df_loan = pd.read_csv("loan_requests.csv")
            df_loan = pd.concat([df_loan, request_data], ignore_index=True)
        else:
            df_loan = request_data

        df_loan.to_csv("loan_requests.csv", index=False)
        st.success("✅ Loan request submitted! You will be contacted soon.")

# Admin can optionally view loan history
if os.path.exists("loan_requests.csv"):
    with st.expander("📜 View Submitted Loan Requests"):
        df = pd.read_csv("loan_requests.csv")
        st.dataframe(df)
