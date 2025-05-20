import streamlit as st
import pandas as pd
import requests

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzgx96l-aK3d55jnVLxaFTwp8wTObnwQxg27M9cg_jVTbT0CSaeeq65NBN_0rB50dsD/exec"

st.title("🎨 Update Classwork & Remarks")

# Simulate login (Replace this with real Google Auth in production)
teacher_email = st.text_input("Enter your registered teacher email to continue:")

if teacher_email:
    # Step 1: Fetch data from Google Apps Script
    try:
        response = requests.get(WEB_APP_URL)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["data"])
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        st.stop()

    # Step 2: Filter data based on teacher email and PENDING remarks
    filtered_df = df[(df["CI"] == teacher_email) & (df["REMARKS"] == "PENDING")]

    if filtered_df.empty:
        st.info("✅ No pending entries for you.")
    else:
        st.subheader("📝 Pending Entries")
        updated_entries = []

        for idx, row in filtered_df.iterrows():
            st.markdown(f"#### 👩‍🎓 {row['STUDENT NAME']} ({row['DATE']})")

            # Work Done dropdown
            current_value = row.get("WORK DONE IN THE CLASS", "")
            work_done = st.selectbox(
                f"Select Work Done for {row['STUDENT NAME']}",
                options=[""] + list(picture_options.values()),
                index=[""] + list(picture_options.values()).index(current_value) if current_value in picture_options.values() else 0,
                key=f"work_{idx}"
            )

            # Remarks textarea
            remarks = st.text_area(
                f"Add Remark for {row['STUDENT NAME']}",
                value="",
                key=f"remark_{idx}"
            )

            # Collect for submission
            if st.button(f"✅ Submit for {row['STUDENT NAME']}", key=f"submit_{idx}"):
                updated_entries.append({
                    "RowKey": row["RowKey"],
                    "WORK DONE IN THE CLASS": work_done,
                    "REMARKS": remarks
                })
                st.success(f"Submitted for {row['STUDENT NAME']}")

        # Step 3: Send updated entries to Apps Script
        if updated_entries:
            try:
                update_response = requests.post(WEB_APP_URL, json={"updates": updated_entries})
                if update_response.status_code == 200:
                    st.success("🎉 All updates submitted successfully.")
                else:
                    st.error("Failed to update entries.")
            except Exception as e:
                st.error(f"Update failed: {e}")
else:
    st.warning("👤 Please enter your email to view your pending entries.")
