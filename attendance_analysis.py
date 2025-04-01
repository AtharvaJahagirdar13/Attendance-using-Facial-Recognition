import streamlit as st
import pandas as pd
import MySQLdb


# Function to load attendance data from MySQL into a DataFrame
@st.cache_data
def load_attendance_data():
    # Update connection credentials if needed
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Anj@130206", db="attendance_db")
    query = "SELECT * FROM attendance"  # Ensure your table name and column names match
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def main():
    st.title("Attendance Analysis Dashboard")

    # Load attendance data
    data = load_attendance_data()

    # Display the raw data
    st.header("Raw Attendance Data")
    st.dataframe(data)

    # Convert the attendance_date column to datetime (if stored as a DATE or string)
    if 'attendance_date' in data.columns:
        data['attendance_date'] = pd.to_datetime(data['attendance_date'])

    # Attendance trend: Group data by date and count the number of records
    st.header("Daily Attendance Trend")
    if not data.empty:
        daily_attendance = data.groupby(data['attendance_date'].dt.date).size()
        st.line_chart(daily_attendance)
    else:
        st.write("No attendance data available.")

    # Filter attendance by student name
    st.header("Filter Attendance by Student")
    if 'name' in data.columns:
        student_names = data['name'].unique()
        selected_student = st.selectbox("Select a student", student_names)
        if selected_student:
            student_data = data[data['name'] == selected_student]
            st.subheader(f"Attendance records for {selected_student}")
            st.dataframe(student_data)
    else:
        st.write("No student data available.")


if __name__ == "__main__":
    main()
