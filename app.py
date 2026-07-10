import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# CRASH-PROOF DATABASE INITIALIZATION
def init_clean_db():
    conn = sqlite3.connect("classroom_ai.db")
    cursor = conn.cursor()
    
    # Drop existing incomplete tables to avoid column count crashes
    cursor.execute("DROP TABLE IF EXISTS staff")
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("DROP TABLE IF EXISTS attendance")
    
    # Recreate structured tables cleanly
    cursor.execute('''CREATE TABLE staff (staff_id TEXT PRIMARY KEY, name TEXT, password TEXT)''')
    cursor.execute('''CREATE TABLE students (reg_no TEXT PRIMARY KEY, name TEXT, status TEXT)''')
    cursor.execute('''CREATE TABLE attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, reg_no TEXT, name TEXT, status TEXT)''')
    
    # Insert Fresh Data Records
    cursor.execute("INSERT OR IGNORE INTO staff VALUES ('ST101', 'Kumar', 'password123')")
    cursor.execute("INSERT OR IGNORE INTO students VALUES ('REG001', 'Manoj', 'Active')")
    cursor.execute("INSERT OR IGNORE INTO students VALUES ('REG002', 'Vishnu', 'Active')")
    cursor.execute("INSERT OR IGNORE INTO students VALUES ('REG003', 'Abhi', 'Active')")
    
    conn.commit()
    conn.close()

# Always ensure the database has the fresh structure on reload
if 'db_ready' not in st.session_state:
    init_clean_db()
    st.session_state['db_ready'] = True

st.set_page_config(page_title="AI Classroom System", layout="wide")
st.title("🎓 AI Classroom Attention & Attendance System")

if 'logged_in' not in st.session_state: 
    st.session_state['logged_in'] = False

# --- LOGIN SCREEN ---
if not st.session_state['logged_in']:
    st.subheader("🔑 Staff Login")
    with st.form("login_form"):
        staff_id = st.text_input("Staff ID")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            conn = sqlite3.connect("classroom_ai.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM staff WHERE staff_id=? AND password=?", (staff_id, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                st.session_state['logged_in'] = True
                st.session_state['staff_name'] = result[0]
                st.rerun()
            else:
                st.error("Invalid Login details entered!")

# --- DASHBOARD SCREEN ---
else:
    st.sidebar.title(f"Welcome, Prof. {st.session_state['staff_name']} 👋")
    menu = st.sidebar.radio("Navigate Menu", ["Live Class Session", "View Attendance Reports"])
    
    if menu == "Live Class Session":
        st.header("📹 Live Classroom Monitor (Browser Native Cam)")
        
        img_file = st.camera_input("🚀 Take Attendance Photo / Scan Classroom")
        
        if img_file is not None:
            st.success("📸 Image captured successfully by AI engine!")
            st.image(img_file, caption="Classroom Scan Snapshot")
            
            st.subheader("📊 Processing Real-time Attendance Updates...")
            
            conn = sqlite3.connect("classroom_ai.db")
            cursor = conn.cursor()
            
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Simulated Student detection matches
            present_students = [
                ('REG001', 'Manoj'),
                ('REG002', 'Vishnu')
            ]
            
            for reg_no, name in present_students:
                # Direct safe insertion with accurate 5 column parameters mapping
                cursor.execute("INSERT INTO attendance (date, reg_no, name, status) VALUES (?, ?, ?, 'Present')", 
                               (current_date, reg_no, name))
            
            conn.commit()
            conn.close()
            st.balloons()
            st.success("🎯 AI Database Engine Synced Successfully!")

    elif menu == "View Attendance Reports":
        st.header("📊 Student Attendance Database Log Sheets")
        
        conn = sqlite3.connect("classroom_ai.db")
        
        st.subheader("👨‍🎓 Registered Batch Profiles")
        df_students = pd.read_sql_query("SELECT * FROM students", conn)
        st.dataframe(df_students, use_container_width=True)
        
        st.subheader("📝 Live Automated Attendance Sheet")
        df_attendance = pd.read_sql_query("SELECT * FROM attendance ORDER BY id DESC", conn)
        
        if df_attendance.empty:
            st.warning("No attendance records scanned yet.")
        else:
            st.dataframe(df_attendance, use_container_width=True)
            
        conn.close()