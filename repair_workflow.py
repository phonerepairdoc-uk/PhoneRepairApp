import streamlit as st
import pandas as pd

# Load the cleaned dataset
def load_data():
    data = {
        "Fault": ["Cracked, Broken, Glass, Screen", "Battery isn't lasting", "Wont Charge, Won't turn On"],
        "Part": ["Screen", "Battery", "Charging Port"],
        "iPhone 8": [11, 22, 32],
        "iPhone X": [12, 23, 33],
    }
    return pd.DataFrame(data)

# Define the repair workflow
def repair_inquiry_web_interface():
    st.title("Phone Repair Doctor")
    st.write("Welcome to the repair process!")

    # Step 1: Device Details
    st.header("Device Information")
    device_type = st.selectbox("What type of device do you need repaired?", ["Phone", "Tablet", "Laptop", "Console"])
    device_brand = st.selectbox("What is the brand of the device?", ["Apple", "Samsung", "Other"])
    device_model = st.selectbox("What is the model of the device?", [
        "iPhone 7", "iPhone 8", "iPhone X", "iPhone XS", "iPhone 12"
    ])

    # Step 2: Select Issues
    st.header("Select Issues")
    issues = st.multiselect("What issues are you experiencing?", ["Screen", "Battery", "Charging Port"])

    # Step 3: Match Issues to Price List and Calculate Total Cost
    data = load_data()
    total_cost = 0
    unmatched_issues = []
    if st.button("Calculate Repair Costs"):
        for issue in issues:
            fault_row = data[data['Part'].str.contains(issue, case=False, na=False)]
            if not fault_row.empty and device_model in data.columns:
                matched_price = fault_row[device_model].values[0]
                total_cost += matched_price
                st.write(f"{issue} Repair: £{matched_price}")
            else:
                unmatched_issues.append(issue)

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

        # Confirm Repair Process
        if st.button("Confirm Repair"):
            st.success("Thank you! We’ll start processing your repair request.")

# Run the app
if __name__ == "__main__":
    repair_inquiry_web_interface()