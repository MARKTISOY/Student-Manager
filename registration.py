import streamlit as st
import time
import mysql.connector
import pandas as pd


# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mark_db"
    )

st.set_page_config(page_title="Student Manager 📋", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images2.alphacoders.com/261/26102.jpg");
        background-size: cover;
        background-position: center;
        height: 1000px; /* Adjust this height as you like */
        width: 100%;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #ddd;

        
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: rgba(240, 242, 246, 0.95); /* Light gray with 95% opacity */
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #d1d1d1;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    }

    label p {
        color: #1f1f1f !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: light-grey !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    }

    button[data-testid="stBaseButton-tertiary"] p {
        color: white !important;
        font-weight: bold !important;
    }

    input, select, textarea {
        color: black !important;
        text-shadow: none !important;
    }

    /* 4. Fix the Form background so the white text is readable */
    [data-testid="stForm"] {
        background-color: rgba(50, 50, 50, 0.8); /* Semi-transparent dark gray */
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)



st.title("🎓 Student Information Manager")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Add Student", "📊 View Records", "⚙️ Manage"])

#TAB 1
with tab1:
    st.subheader("Registration Form")
    with st.form("reg_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_id = st.text_input("Student ID (ex. 18-00035)")
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=100)
            gender = st.selectbox("Gender", ["MALE", "FEMALE"])
        with col2:
            course = st.text_input("Course")
            year = st.selectbox("Year Level", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
            email = st.text_input("Email")
        
        if st.form_submit_button("Save Record"):
            conn =get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO students (student_id, full_name, age, gender, course, year_level, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (s_id, name, age, gender, course, year, email))
            conn.commit()
            st.success("Successfully Added!")
            conn.close()

#TAB 2
with tab2:
    st.subheader("Student List")
    conn = get_db_connection()
    # Read the database table into a professional-looking table
    df = pd.read_sql("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()

#TAB 3
with tab3:
    st.subheader("Manage Records (Update or Delete)")
    
    search_query = st.text_input("Enter Student ID or Full Name to Manage")
    
    if search_query:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM students WHERE student_id = %s OR full_name LIKE %s"
        name_pogi = f"%{search_query}%"
        cursor.execute(sql, (search_query, name_pogi))
        student = cursor.fetchone()
        conn.close()

        if student:
            st.write("### Edit Information")
            # Create a form pre-filled with existing data
            with st.form("update_form"):
                new_name = st.text_input("Full Name", value=student['full_name'])
                new_course = st.text_input("Course", value=student['course'])
                new_year = st.selectbox("Year Level", 
                                      ["1st Year", "2nd Year", "3rd Year", "4th Year"],
                                      index=["1st Year", "2nd Year", "3rd Year", "4th Year"].index(student['year_level']))
                
                col_update, col_delete = st.columns(2)
                
                # UPDATE BUTTON
                if col_update.form_submit_button("Update Student Details"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    sql = "UPDATE students SET full_name=%s, course=%s, year_level=%s WHERE student_id=%s"
                    cursor.execute(sql, (new_name, new_course, new_year, search_id))                 
                    conn.commit()
                    conn.close()
                    st.success("Information Updated!")
                    time.sleep(5)
                    st.rerun()

                # DELETE BUTTON (Inside the same flow)
                if col_delete.form_submit_button("Delete This Student"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM students WHERE student_id = %s", (search_id,))
                    conn.commit()
                    conn.close()
                    st.warning("Student Deleted!")
                    time.sleep(2)
                    st.rerun()
        else:
            st.error("Student ID not found.")
