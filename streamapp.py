import streamlit as st
import json
from datetime import datetime

with open("subsci.json", "r", encoding="utf-8") as file:
    data = json.load(file)

st.title("Subject Management App - Add or Edit Subject")

subject_codes = [subject['subject_code'] for subject in data]
selected_subject_code = st.selectbox("Select Subject Code to Edit or Create New", ["Create New"] + subject_codes)

if selected_subject_code != "Create New":
    subject_to_edit = next((subject for subject in data if subject['subject_code'] == selected_subject_code), None)
    subject_id = st.text_input("Subject ID", value=subject_to_edit['subject_id'])
    subject_name = st.text_input("Subject Name", value=subject_to_edit['subject_name'])
    subject_code = selected_subject_code  
    subject_department = st.text_input("Subject Department", value=subject_to_edit['subject_department'])
    final_date = st.date_input("Final Exam Date", value=datetime.strptime(subject_to_edit['final']['date'], "%Y-%m-%d"))
    final_period = st.number_input("Final Exam Period", value=subject_to_edit['final']['period'], min_value=1)

    group_codes = subject_to_edit['groups']
else:
    # Fields for a new subject
    subject_id = st.text_input("Subject ID")
    subject_name = st.text_input("Subject Name")
    subject_code = st.text_input("Subject Code")
    subject_department = st.text_input("Subject Department")
    final_date = st.date_input("Final Exam Date")
    final_period = st.number_input("Final Exam Period", min_value=1)

    group_codes = []

st.subheader("Add/Edit Groups and Lectures")
group_code = st.text_input("Group Code")
professor = st.text_input("Professor")
day = st.text_input("Lecture Day")
start_time = st.time_input("Lecture Start Time")
end_time = st.time_input("Lecture End Time")
room = st.text_input("Lecture Room")

if 'lectures' not in st.session_state:
    st.session_state.lectures = []

if st.button("Add Lecture"):
    if day and start_time and end_time and room:
        st.session_state.lectures.append({
            "day": day,
            "start_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M"),
            "room": room
        })
        st.success("Lecture added successfully!")
    else:
        st.error("Please fill in all lecture details.")

if st.button("Add Group"):
    if group_code and professor:
        group_codes.append({
            "group_code": group_code,
            "professor": professor,
            "lectures": st.session_state.lectures
        })
        st.session_state.lectures = []  
        st.success("Group added successfully!")
    else:
        st.error("Please enter both group code and professor details.")


if st.button("Save Subject"):
    new_subject = {
        "subject_id": subject_id,
        "subject_name": subject_name,
        "subject_code": subject_code,
        "subject_department": subject_department,
        "final": {
            "date": final_date.strftime("%Y-%m-%d"),
            "period": final_period
        },
        "groups": group_codes
    }

    if selected_subject_code == "Create New":
        data.append(new_subject)
        st.success("New subject added successfully!")
    else:
        index = next((i for i, subject in enumerate(data) if subject['subject_code'] == selected_subject_code), None)
        if index is not None:
            data[index] = new_subject
            st.success("Subject updated successfully!")
        else:
            st.error("Subject not found. Please try again.")

    with open("subsci.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

st.subheader("Current Subjects")
st.json(data)

st.download_button(
    label="Download JSON",
    data=json.dumps(data, indent=4, ensure_ascii=False),
    file_name="updated_subsci.json",
    mime="application/json"
)
