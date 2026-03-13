import streamlit as st
import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mark_db"
    )

    st.success("Successfully connected to XAMPP!")

#2. Basic query to test
    cursor = db.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    st.write("You are connected to:", record)

except Exception as e:
    st.error(f"Connection failed: {e}")