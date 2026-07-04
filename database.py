import psycopg2
import streamlit as st
import datetime

def get_connection():
    """
    Neon PostgreSQL Cloud Database se secure connection leta hai.
    Streamlit secrets (.streamlit/secrets.toml) se URL string padhega.
    """
    # Streamlit .io aur GitHub Actions dono jagah se 'DB_CONNECT_STRING' environment variable ban kar read hoga
    if"DB_CONNNECT_STRING" in st.secrets:
        return psycopg2.connect(st.secrets["DB_CONNECT_STRING"])
    else:
        import os
        return psycopg2.connect(os.getenv("DB_CONNECT_STRING","YOUR_FALLING_STRING_IF_NEEDED"))
    

def init_db():
    """
    PostgreSQL ke tables create karne ke liye initialization function.
    Iska schema GitHub Actions ke WhatsApp scheduler ke sath perfectly sync karega.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Spaced Revisions Data Table (PostgreSQL standard data types)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revisions (
            id SERIAL PRIMARY KEY,
            topic_name VARCHAR(255) NOT NULL,
            stage VARCHAR(100),
            current_status VARCHAR(50) DEFAULT 'Active',
            date_created TIMESTAMP NOT NULL,
            date_1_day DATE NOT NULL,
            date_7_day DATE NOT NULL,
            date_30_day DATE NOT NULL
        );
    """)
    
    # Table 2: Quiz & Progress Analytics Performance Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_performance (
            id SERIAL PRIMARY KEY,
            quiz_date TIMESTAMP NOT NULL,
            topic_name VARCHAR(255),
            score INT NOT NULL,
            total_questions INT NOT NULL,
            accuracy_percentage INT NOT NULL
        );
    """)
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings(
                   id SERIAL PRIMARY KEY,
                   remainder_time VARCHAR(10) NOT NULL DEFAULT '06:00'
                   );


""")
    conn.commit()
    cursor.close()
    conn.close()

def add_topic(topic_name, stage, base_date=None):
    """
    Frontend (app.py) se naye topics ko timeline dates generate karke PostgreSQL me save karta hai.
    """
    if base_date is None:
        base_date = datetime.datetime.now()
        
    # Mathematical spaced intervals calculations
    date_1 = (base_date + datetime.timedelta(days=1)).date()
    date_7 = (base_date + datetime.timedelta(days=7)).date()
    date_30 = (base_date + datetime.timedelta(days=30)).date()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Standard PostgreSQL tuple formatting using %s placeholders
    query = """
        INSERT INTO revisions (topic_name, stage, date_created, date_1_day, date_7_day, date_30_day)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (topic_name, stage, base_date, date_1, date_7, date_30))
    
    conn.commit()
    cursor.close()
    conn.close()

def log_progress(topic_name, score, total_qs):
    """
    Quiz complete hone par score statistics analytics table me log karta hai.
    """
    accuracy = int((score / total_qs) * 100) if total_qs > 0 else 0
    now = datetime.datetime.now()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO quiz_performance (quiz_date, topic_name, score, total_questions, accuracy_percentage)
        VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (now, topic_name, score, total_qs, accuracy))
    
    conn.commit()
    cursor.close()
    conn.close()

# Automatic startup script wrapper to create tables instantly if they don't exist
try:
    init_db()
except Exception as e:
    print(f"Database Init Alert/Fallback: {e}")


def get_quiz_accuracies():
    """
    Performance Tracker ke real graph ke liye database se saari accuracies fetch karta hai.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Sabse purane se lekar naye quiz tak ki accuracy select karega
        cursor.execute("SELECT accuracy_percentage FROM quiz_performance ORDER BY id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Data ko simple python list [80, 90, 70] me convert karega
        accuracies = [row[0] for row in rows]
        return accuracies if accuracies else [0] # Agar data na ho to [0] return karega
    except Exception:
        return [0]   
    

def update_reminder_time(new_time_str):
    conn = get_connection
    cursor = conn.cursor
    cursor.execute("SELECT id FROM user_settings LIMIT 1;")
    row = cursor.fetchone()

    if row:
        cursor.execute("UPDATE user_settings SET reminder_time = %s WHERE id = %s;", (new_time_str,row[0]))
    else:
        cursor.execute("INSERT INTO user_settings(reminder_time) VALUES (%S);", (new_time_str,))    

        conn.commit()
        cursor.close()
        conn.close()   


def get_reminder_time():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT reminder_time  FROM user_settings LIMIT 1;") 
    row = cursor.fetchone
    cursor.close()
    conn.close()
    return row[0] if row else"06:00"
        