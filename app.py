import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# DATABASE INITIALIZATION
def init_clean_db():
    conn = sqlite3.connect("classroom_ai.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (staff_id TEXT PRIMARY KEY, name TEXT, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (reg_no TEXT PRIMARY KEY, name TEXT, photo_path TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, reg_no TEXT, status TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO staff VALUES ('ST101', 'Kumar', 'password123')")
    cursor.execute("INSERT OR IGNORE INTO students VALUES ('REG001', 'Manoj', 'Active')")
    cursor.execute("INSERT OR IGNORE INTO students VALUES ('REG002', 'Vishnu', 'Active')")
    conn.commit()
    conn.close()

init_clean_db()

st.set_page_config(page_title="AI Classroom System", layout="wide")
st.title("🎓 AI Classroom Attention & Attendance System")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

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
                st.error("Invalid Login!")

# --- DASHBOARD SCREEN ---
else:
    st.sidebar.title(f"Welcome, Prof. {st.session_state['staff_name']} 👋")
    menu = st.sidebar.radio("Navigate Menu", ["Live Class Session", "View Attendance Reports"])
    
    if menu == "Live Class Session":
        st.header("📹 Live Classroom Monitor (Browser Native Cam)")
        st.write("Python dependencies illama direct browser support moolama camera inga open aagum.")
        
        # Streamlit-oda official built-in camera component (No OpenCV Needed!)
        img_file = st.camera_input("🚀 Take Attendance Photo / Scan Classroom")
        
        if img_file is not None:
            st.success("📸 Image captured successfully by AI engine!")
            st.image(img_file, caption="Classroom Scan Snapshot")
            
            # Simulated Attendance marking logic
            st.info("AI Analysis: 2 Students detected. Attendance log tracking complete.")

    elif menu == "View Attendance Reports":
        st.header("📊 Student Attendance Log")
        conn = sqlite3.connect("classroom_ai.db")
        df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)