import streamlit as st
import pandas as pd
import smtplib
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# ========================== CONFIGURE PAGE ===========================
st.set_page_config(page_title="Phone Repair Doctor", layout="wide")

# ========================== CONNECT TO GOOGLE SHEETS ===========================
def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Repair Pricing").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# ========================== DEVICE IMAGE MAPPING ===========================
image_folder = "images"
device_images = {
    "Phone": os.path.join(image_folder, "phone.png"),
    "Tablet": os.path.join(image_folder, "tablet.png"),
    "Laptop": os.path.join(image_folder, "laptop.png"),
    "Console": os.path.join(image_folder, "console.png")
}

# ========================== REPAIR BOOKING SYSTEM ===========================
def send_confirmation(email, repair_date, repair_time, total_cost):
    message = f"Your repair is scheduled for {repair_date} at {repair_time}. Total cost: £{total_cost}."
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your-email@gmail.com", "your-password")
    server.sendmail("your-email@gmail.com", email, message)
    server.quit()

# ========================== SAVE CUSTOMER REPAIR HISTORY ===========================
def save_repair_request(name, device, issue, cost):
    with open("repair_history.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, device, issue, cost])

# ========================== STREAMLIT INTERFACE ===========================
def repair_inquiry_web_interface():
    st.title("Phone Repair Doctor")
    st.write("Welcome to the repair process!")

    # Step 1: Device Details
    st.header("Device Information")
    device_type = st.radio("What type of device do you need repaired?", list(device_images.keys()))
... 
...     # Show selected device image
...     if device_type in device_images and os.path.exists(device_images[device_type]):
...         st.image(device_images[device_type], caption=device_type, width=200)
...     else:
...         st.warning("Image not found for this device.")
... 
...     device_model = st.selectbox("What is the model of the device?", [
...         "iPhone 7", "iPhone 8", "iPhone X", "iPhone XS", "iPhone 12", "iPhone 12 Pro",
...         "iPhone 12 Pro Max", "iPhone 13", "iPhone 13 Pro", "iPhone 13 Pro Max",
...         "iPhone 14", "iPhone 14 Pro", "iPhone 14 Pro Max", "iPhone 15", "iPhone 15 Pro", "iPhone 15 Pro Max"
...     ])
... 
...     # Step 2: Select Issues
...     st.header("Select Issues")
...     issues = st.multiselect("What issues are you experiencing?", ["Screen", "Battery", "Charging Port"])
... 
...     # Load Repair Pricing Data
...     data = load_data()
... 
...     # Step 3: Match Issues to Price List and Calculate Total Cost
...     total_cost = 0
...     unmatched_issues = []
... 
...     if st.button("Calculate Repair Costs"):
...         for issue in issues:
...             fault_row = data[(data["Device Model"] == device_model) & (data["Issue"].str.contains(issue, case=False, na=False))]
...             if not fault_row.empty:
...                 matched_price = fault_row["Price"].values[0]
...                 total_cost += matched_price
...                 st.write(f"{issue} Repair: £{matched_price}")
...             else:
...                 unmatched_issues.append(issue)
... 
        # Handle unmatched issues
        if unmatched_issues:
            st.warning(f"The following issues couldn't be matched: {', '.join(unmatched_issues)}.")

        # Optional Services
        st.header("Optional Services")
        screen_protector = st.checkbox("Add Screen Protector (£10)")
        expedited_repair = st.checkbox("Add Expedited Repair (£25)")

        if screen_protector:
            total_cost += 10
        if expedited_repair:
            total_cost += 25

        # Display Final Cost
        st.success(f"Total Estimated Cost: £{total_cost}")

    # Step 4: Booking System
    st.header("Schedule Your Repair")

    repair_date = st.date_input("Select a Repair Date")
    repair_time = st.time_input("Select a Repair Time")
    customer_email = st.text_input("Enter your email for confirmation")

    if st.button("Confirm Repair"):
        send_confirmation(customer_email, repair_date, repair_time, total_cost)
        save_repair_request(customer_email, device_model, issues, total_cost)
        st.success("Your repair has been booked! A confirmation email has been sent.")

# Run the app
if __name__ == "__main__":
