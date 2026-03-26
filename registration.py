import streamlit as st
import mysql.connector
import pandas as pd
import time

def run_query(query, params=None, is_select=False):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="mark_db")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall() if is_select else conn.commit()
    conn.close()
    return result


st.set_page_config(page_title="Student Manager 📋", layout="wide")
st.markdown("""
    <style>
    .stApp { background: url("https://images2.alphacoders.com/261/26102.jpg") center; background-size: cover; } 

    [data-testid="stForm"], .stTabs 
    { background: rgba(50, 50, 50, 0.8)
    center;
    margin-top: 20px;
    padding: 20px; 
    border: 1px solid rgba(255, 255, 255, 0.2); 
    color: white; }

    h3, p { color: white !important;
    font-weight: bold !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    font-size: 1.1rem !important; font-family: Arial !important;} 
    h1 {color: white !important; 
    font-weight: bold !important; 
    font-family: Monospace !important;}
    input { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Information Manager")
tab1, tab2, tab3 = st.tabs(["📝 Add Student", "📊 Student Records", "⚙️ Modify"])

#TAB 1
# --- TAB 1: ADD NEW STUDENT ---
with tab1:
    st.subheader("REGISTER A NEW STUDENT")
    with st.form("reg_form"):
        col1, col2 = st.columns(2)


        s_id = col1.text_input("Student ID (ex. 18-00035)")
        name = col1.text_input("Full Name")
        age = col1.number_input("Age", 1, 100, 18)
        
        gender = col2.selectbox("Gender", ["MALE", "FEMALE"])
        course = col2.selectbox("Course", ["BSIT", "BSED", "BEED", "BSHM", "BSFM"])
        year = col2.selectbox("Year Level", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        
        email = st.text_input("Email")

    

        submit_button = st.form_submit_button("Save Record")
    
    if submit_button:
        if not s_id.strip() or not name.strip():
            st.error("Student ID and Name are required!")
        
        elif not email.strip():
            st.error("Email field cannot be empty.")     
        
        elif "@" not in email:
            st.error("Invalid! Please use an appropriate schools' email.")
            
        elif not email.endswith("@ciccebu.edu.ph"):
            st.warning("Please use your official school email (@ciccebu.edu.ph).")
            
        else:
            
            sql = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)"
            run_query(sql, (s_id, name, age, gender, course, year, email))
            st.success(f"Successfully Added {name}!")
#TAB 2
with tab2:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="mark_db")
    df = pd.read_sql("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()

#TAB 3
with tab3:
    search = st.text_input("Search Student ID or Name")
    if search:
        res = run_query("SELECT * FROM students WHERE student_id = %s OR full_name LIKE %s", (search, f"%{search}%"), True)
        if res:
            student = res[0]
            with st.form("edit_form"):
                cl1, cl2 = st.columns(2)
                u_name = cl1.text_input("Full Name", student['full_name'])
                u_course = cl2.text_input("Course", student['course'])
                u_age = cl1.number_input("Age", student['age'])
                u_email = st.text_input("Email", student['email'])
                u_year = cl2.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"], 
                                    index=["1st Year", "2nd Year", "3rd Year", "4th Year"].index(student['year_level']))
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update"):
                    run_query("UPDATE students SET full_name=%s, course=%s, year_level=%s, age=%s, email=%s WHERE student_id=%s", 
                             (u_name, u_course, u_year, u_age, u_email, student['student_id']))
                    st.success("Updated!")
                    time.sleep(2); 
                    st.rerun()
                
                if c2.form_submit_button("Delete"):
                    run_query("DELETE FROM students WHERE student_id=%s", (student['student_id'],))
                    st.warning("Deleted!")
                    time.sleep(2); 
                    st.rerun()
        else:
            st.error("No student found with that ID or Name.")
