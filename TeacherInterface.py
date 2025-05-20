import streamlit as st
import requests

WEB_APP_URL = "YOUR_APPS_SCRIPT_WEB_APP_URL"  # replace with your deployed URL

st.title("Teacher Attendance Dashboard")

teacher_email = st.text_input("Enter your teacher email to continue:")

if teacher_email:
    # Fetch all pending rows from Apps Script Web App (GET)
    try:
        resp = requests.get(WEB_APP_URL)
        resp.raise_for_status()
        all_data = resp.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.stop()

    # Filter rows for this teacher email (CI)
    teacher_rows = [row for row in all_data if row["CI"].lower() == teacher_email.lower()]

    if not teacher_rows:
        st.info("No pending records found for your email.")
    else:
        st.write(f"Found {len(teacher_rows)} pending entries.")

        # Example work done options (replace with your actual dropdown options)
        work_done_options = [
            "PictureA : Drawing A",
            "PictureB : Drawing B",
            "PictureC : Drawing C"
        ]

        updates = []

        with st.form("update_form"):
            for i, row in enumerate(teacher_rows):
                st.markdown(f"---\n**RowKey:** {row['RowKey']}")
                st.write(f"CI: {row['CI']}")

                work_done = st.selectbox(
                    "Select Work Done",
                    options=work_done_options,
                    key=f"work_done_{i}"
                )

                remarks = st.text_area(
                    "Enter remarks",
                    key=f"remarks_{i}"
                )

                updates.append({
                    "RowKey": row["RowKey"],
                    "workDone": work_done.split(" : ")[0],  # Only ID part
                    "remarks": remarks
                })

            submit = st.form_submit_button("Submit Updates")

        if submit:
            success_count = 0
            for update in updates:
                try:
                    post_resp = requests.post(WEB_APP_URL, json=update)
                    post_resp.raise_for_status()
                    result = post_resp.json()
                    if result.get("status") == "success":
                        success_count += 1
                    else:
                        st.error(f"Failed to update RowKey {update['RowKey']}: {result.get('message')}")
                except Exception as e:
                    st.error(f"Error updating RowKey {update['RowKey']}: {e}")

            st.success(f"Updated {success_count} records successfully!")

else:
    st.info("Please enter your teacher email to continue.")
