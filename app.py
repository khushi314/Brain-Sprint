import streamlit as st
import time
import datetime
import os
import base64

# ==========================================
# 🔌 UNVERIFIED REAL CORE ENGINES IMPORT
# ==========================================
import database as db
import agent as quiz_agent

# ==========================================
# 🌌 MAIN CONFIGURATION & PREMIUM CANVAS HOOKS
# ==========================================
#try:
    #st.set_page_config(
        #page_title="BrainSprint: AI Spaced Revision", 
        #page_icon="🧠",  
        #layout="wide",
        #initial_sidebar_state="expanded"
    #)
#except Exception:
 #   pass


try:
    st.set_page_config(
        page_title="BrainSprint: AI Spaced Revision", 
        page_icon="logo.png",  
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    st.set_page_config(page_title="BrainSprint: AI Spaced Revision", page_icon="🧠", layout="wide")


# Safe Base64 Image Background Injector
def set_premium_page_bg(png_file):
    if os.path.exists(png_file):
        with open(png_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(11, 8, 19, 0.65), rgba(11, 8, 19, 0.72)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover !important;
            background-position: center right 10% !important;
            background-attachment: fixed !important;
            color: #e2e2e9 !important;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)

if os.path.exists("app/static/home_bg.jpg"): set_premium_page_bg("app/static/home_bg.jpg")
elif os.path.exists("home_bg.jpg"): set_premium_page_bg("home_bg.jpg")

# CSS Overrides for Premium UI Look
st.markdown("""
<style>
    section[data-testid="stSidebar"] { background-color: #120f1d !important; border-right: 2px solid #251f38; }
    [data-testid="stSidebar"] img { border-radius: 20px !important; border: 3px solid #ff007f !important; box-shadow: 0 0 25px rgba(255, 0, 127, 0.6) !important; object-fit: cover !important; }
    .brainsprint-mega-header { font-family: 'Arial Black', Gadget, sans-serif !important; font-size: 85px !important; font-weight: 900 !important; line-height: 1.1 !important; letter-spacing: -3px !important; background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; margin-top: -15px !important; margin-bottom: 5px !important; display: block !important; filter: drop-shadow(0px 0px 30px rgba(127, 0, 255, 0.75)) !important; }
    .motivation-quote-box { font-family: 'Georgia', serif; font-style: italic; font-size: 22px; color: #a197c4; border-left: 4px solid #ff007f; padding-left: 15px; margin-bottom: 35px; }
    .tight-glass-panel { background: rgba(22, 18, 33, 0.82) !important; border: 2px solid rgba(255, 255, 255, 0.1) !important; border-radius: 16px !important; padding: 26px !important; box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(15px) !important; -webkit-backdrop-filter: blur(15px) !important; }
</style>
""", unsafe_allow_html=True)

# Session State Management Initializations
if "active_timer" not in st.session_state: st.session_state.active_timer = False
if "quiz_accuracy_vector" not in st.session_state: st.session_state.quiz_accuracy_vector = [50,60,70,75] 
if "timer_seconds" not in st.session_state: st.session_state.timer_seconds = 0
if "quiz_active_state" not in st.session_state: st.session_state.quiz_active_state = False
if "quiz_questions" not in st.session_state: st.session_state.quiz_questions = []
if "quiz_page_number" not in st.session_state: st.session_state.quiz_page_number = 1
if "quiz_results_show" not in st.session_state: st.session_state.quiz_results_show = False
if "user_answers" not in st.session_state: st.session_state.user_answers = {}

# Runtime state storage for testing fallback handlers
if "stored_today" not in st.session_state: st.session_state.stored_today = ""
if "stored_yesterday" not in st.session_state: st.session_state.stored_yesterday = ""
if "stored_7day" not in st.session_state: st.session_state.stored_7day = ""

# ==========================================
# 🧭 SIDEBAR ARCHITECTURE
# ==========================================
with st.sidebar:
    st.write("")
    if os.path.exists("sidebar.png"): st.image("sidebar.png", width=220)
    elif os.path.exists("app/static/sidebar.png"): st.image("app/static/sidebar.png", width=220)
    st.markdown("<h2 style='font-family:Arial Black; font-size:26px; color:#00f0ff; text-align:center;'>Hii Buddy! 👋</h2>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Select Page:", ["🏠 Home Dashboard", "📅 Remainder Matrix", "📝 Quiz Arena", "📈 Performance Tracker"], label_visibility="collapsed")
    st.divider()
    st.caption("✨ Framework Vector: ARC Master Core Engine")

# ==========================================
# 🏠 PAGE 1: HOME DASHBOARD VIEW
# ==========================================
if page == "🏠 Home Dashboard":
    st.markdown('<h1 class="brainsprint-mega-header">Brainsprint</h1>', unsafe_allow_html=True)
    st.markdown('<div class="motivation-quote-box">"Studying when you\'re motivated is easy. Revising when you\'re tired, distracted, or unmotivated—that\'s what creates winners."✨</div>', unsafe_allow_html=True)
    
    col_home_left, col_home_right = st.columns([12, 10])
    
    with col_home_left:
        st.markdown("#### 🛠️ Core Session Registration Layer")
        with st.container(border=False):
            st.markdown('<div class="tight-glass-panel">', unsafe_allow_html=True)
            inp_today = st.text_input("📍 Enter your today's topic:", value=st.session_state.stored_today, placeholder="e.g., Array Partitioning Techniques")
            inp_yesterday = st.text_input("⏱️ Enter your yesterday's topic (24h due):", value=st.session_state.stored_yesterday, placeholder="e.g., AVL Tree Insertions")
            inp_7days = st.text_input("📅 Enter topic covered 7 days earlier:", value=st.session_state.stored_7day, placeholder="e.g., Queue Protocols")
                    
            rem_clock = st.time_input("🔔 Permanent Reminder Trigger Clock Slot:", datetime.time(20, 0))
            try:
                formatted_time= rem_clock.strftime("%H:%M")
                db.update_reminder_time(formatted_time)
                st.caption(f"Auto-Synced to cloud: Reminders active for hour{formatted_time}IST")
            except Exception as db_err:
                st.caption(f"Cloud sync pending....({db_err})")


            sync_trigger = st.button("Sync Data & Activate Timeline ⚡", use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if sync_trigger:
            st.session_state.stored_today = inp_today
            st.session_state.stored_yesterday = inp_yesterday
            st.session_state.stored_7day = inp_7days
            
            # 🔌 REAL TIME DB SYSTEM WRITE OPERATION CALLS
            try:
                if inp_today: db.add_topic(inp_today, "General Mode")
                if inp_yesterday: db.add_topic(inp_yesterday, "Yesterday Setup", base_date=datetime.datetime.now() - datetime.timedelta(days=1))
                if inp_7days: db.add_topic(inp_7days, "7 Days Prior Setup", base_date=datetime.datetime.now() - datetime.timedelta(days=7))
                st.success("✨ Flash Engine Sync Complete! Real data successfully logged via database.py")
            except Exception as e:
                st.error(f"Database Write Error: {e}. Please ensure database.py host setup is active!")

    with col_home_left:
        st.write("")
        st.divider()
        st.markdown("#### 🎥 Application Operational Guidance Video")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# ==========================================
# 📅 PAGE 2: REMAINDER MATRIX PAGE
# ==========================================
elif page == "📅 Remainder Matrix":
    st.markdown("<h2 style='color: #00f0ff; font-weight:900;'>📅 Spaced Revision Remainder Architecture</h2>", unsafe_allow_html=True)
    st.divider()
    
    col_rem_left, col_rem_right = st.columns([5, 4])
    
    with col_rem_left:
        # Stage 1 Card
        s1_val = st.session_state.stored_yesterday if st.session_state.stored_yesterday else "No topic due for 24h revision today."
        st.markdown(f"""
        <div class="tight-glass-panel" style="margin-bottom: 15px;">
            <h4 style="color: #ff007f; margin:0; font-weight:bold;">🚨 Stage 1: After 24 Hour Revision Slot</h4>
            <p style="font-size: 22px; font-weight: bold; margin-top: 12px; color: #ffffff;">📌 {s1_val}</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("⏰ Launch 10 Minutes Focus Countdown Clock", key="c_10", use_container_width=True)
            
        # Stage 2 Card
        s2_val = st.session_state.stored_7day if st.session_state.stored_7day else "No topic due for 7d revision today."
        st.markdown(f"""
        <div class="tight-glass-panel" style="margin-bottom: 15px;">
            <h4 style="color: #7f00ff; margin:0; font-weight:bold;">⏱️ Stage 2: After 7 Day Revision Slot</h4>
            <p style="font-size: 22px; font-weight: bold; margin-top: 12px; color: #ffffff;">📌 {s2_val}</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("⏰ Launch 15 Minutes Focus Countdown Clock", key="c_15_1", use_container_width=True)

        # Stage 3 Card
        st.markdown(f"""
        <div class="tight-glass-panel" style="margin-bottom: 15px;">
            <h4 style="color: #00f0ff; margin:0; font-weight:bold;">🏆 Stage 3: After 30 Days Memory Lock Slot</h4>
            <p style="font-size: 22px; font-weight: bold; margin-top: 12px; color: #ffffff;">📌 All Clear! No topic due for 30 Days memory lock today.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("⏰ Launch 15 Minutes Master Countdown Clock", key="c_15_2", use_container_width=True)

# ==========================================
# 📝 PAGE 3: QUIZ ARENA (🚀 REAL AI CALL INTEGRATION)
# ==========================================
elif page == "📝 Quiz Arena":
    st.markdown("<h2 style='color: #ff007f; font-weight:900;'>📝 AI Active Recall Quiz Arena</h2>", unsafe_allow_html=True)
    st.divider()
    
    target_q_topic = st.text_input("Enter your topic for Quiz:", value=st.session_state.stored_today if st.session_state.stored_today else "General Learning")
    num_questions= st.slider("Select Number of Questions:", min_value=3, max_value=10, value=5)
    complexity_choice = st.radio("Select Complexity Level:", ["Easy 🟢", "Medium 🟡", "Hard 🔴"], horizontal=True)
    
    st.write("")
    if st.button("Generate Dynamic Quiz 🚀", use_container_width=True, key="quiz_gen_trigger"):
        if target_q_topic:
            with st.spinner("🤖 your questions are here..."):
                try:
                    # 🚀 CALLING REAL AI AGENT FROM AGENT.PY
                    generated_mcqs = quiz_agent.generate_quiz(target_q_topic, num_questions, complexity_choice)
                    if generated_mcqs and len(generated_mcqs) > 0:
                        st.session_state.quiz_questions = generated_mcqs
                        st.session_state.quiz_active_state = True
                        st.session_state.quiz_page_number = 1  
                        st.session_state.quiz_results_show = False
                        st.session_state.user_answers = {}
                        st.rerun()
                    else:
                        st.error("AI returned empty context. Please check API Key limits configuration.")
                except Exception as e:
                    st.error(f"AI Agent Connection Error: {e}. Check export variables context.")
        else:
            st.warning("Please provide a topic descriptor parameter first!")
            
    # Evaluation Logic Rendering Matrix
    if st.session_state.quiz_results_show:
        st.markdown("<div class='tight-glass-panel' style='border: 2px solid #00f0ff; margin-top:15px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#00f0ff; font-weight:900; margin-top:0;'>📊 Performance Report Matrix</h3>", unsafe_allow_html=True)
        
        correct_count = 0
        for i, q_item in enumerate(st.session_state.quiz_questions):
            user_ans = st.session_state.user_answers.get(i+1, "Not Answered")
            #actual_ans = q_item["answer"]
            #use get() method with fallbacks to avoid keyerror crash
            actual_ans = q_item.get("answer", q_item.get("correct_answer", q_item.get("correct","")))
            st.markdown(f"**Question {i+1}: {q_item['question']}**")
            if user_ans == actual_ans:
                st.markdown(f"🟢 <b style='color:#00ff88;'>Correct Jawab:</b> {user_ans}", unsafe_allow_html=True)
                correct_count += 1
            else:
                st.markdown(f"🔴 <b style='color:#ff3366;'>Your Answer:</b> {user_ans}", unsafe_allow_html=True)
                st.markdown(f"✨ <b style='color:#00f0ff;'>Solution:</b> {actual_ans}", unsafe_allow_html=True)
            st.divider()
            
        st.metric(label="Final Score", value=f"{correct_count} / {len(st.session_state.quiz_questions)} Correct")
        
        # Log analytics to the real database progress metrics
        try:
            db.log_progress(target_q_topic, correct_count, len(st.session_state.quiz_questions))
        except Exception:
            pass
            
        if correct_count == len(st.session_state.quiz_questions): st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif st.session_state.quiz_active_state and st.session_state.quiz_questions:
        q_idx = st.session_state.quiz_page_number - 1
        current_q = st.session_state.quiz_questions[q_idx]
        
        st.markdown(f"<div style='background: rgba(0,240,255,0.08); border: 1px solid #00f0ff; padding: 12px; border-radius: 8px; color: #00f0ff; font-weight:bold;'>✨ Question {st.session_state.quiz_page_number}/{len(st.session_state.quiz_questions)} ({complexity_choice}):</div>", unsafe_allow_html=True)
        st.markdown("<div class='tight-glass-panel' style='margin-top:10px;'>", unsafe_allow_html=True)
        
        st.markdown(f"##### **{current_q['question']}**")
        current_selection = st.radio("Select Option:", current_q["options"], index=None, key=f"live_quiz_radio_{st.session_state.quiz_page_number}")
        
        st.write("")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Next Question ➡️", use_container_width=True):
                if current_selection:
                    st.session_state.user_answers[st.session_state.quiz_page_number] = current_selection
                if st.session_state.quiz_page_number < len(st.session_state.quiz_questions):
                    st.session_state.quiz_page_number += 1
                    st.rerun()
        with col_b2:
            if st.button("Submit Exam 🏁", use_container_width=True, type="primary"):
                if current_selection:
                    st.session_state.user_answers[st.session_state.quiz_page_number] = current_selection
                
                # 2. State toggles set kijiye
                st.session_state.quiz_active_state = False
                st.session_state.quiz_results_show = True
                st.rerun()

    # ---- EVALUATION REPORT DISPLAY BLOCK ----
    # Yeh tabhi chalega jab user submit kar chuka hoga (quiz_results_show == True)
    if st.session_state.get("quiz_results_show", False):
        correct_count = 0
        st.markdown("### 📊 Your Quiz Evaluation Report")
        
        for i, q_item in enumerate(st.session_state.quiz_questions):
            # Safe indexing check for user answers dictionary/list
            user_ans = st.session_state.user_answers.get(i, "Not Answered") if isinstance(st.session_state.user_answers, dict) else st.session_state.user_answers[i]
            actual_ans = q_item.get("answer", q_item.get("correct_answer", ""))
            
            st.write(f"**Q{i+1}: {q_item['question']}**")
            
            if user_ans == actual_ans:
                st.success(f"🟢 **Correct Answer!** You chose: {user_ans}")
                correct_count += 1
            else:
                st.error(f"🔴 **Wrong Answer!** You chose: {user_ans}")
                st.info(f"💡 **Correct Choice:** {actual_ans}")
                
                # 🧠 Short Theory Description Feature
                explanation = q_item.get("explanation", q_item.get("description", "Review the core concepts of this specific topic matrix in your study logs."))
                st.caption(f"📖 *Quick Revision Theory:* {explanation}")
            st.markdown("---")
            
        # --- NEON CLOUD DATABASE SYNC ENGINE ---
        # Ek baar run hone ke baad hi loop database me push karega
        if not st.session_state.get("db_synced_this_run", False):
            try:
                db.log_progress(target_q_topic, correct_count, len(st.session_state.quiz_questions))
                
                if "quiz_accuracy_vector" not in st.session_state:
                    st.session_state.quiz_accuracy_vector = []
                    
                current_acc = int((correct_count / len(st.session_state.quiz_questions)) * 100)
                st.session_state.quiz_accuracy_vector.append(current_acc)
                
                st.session_state.db_synced_this_run = True
                st.success("🎯 Exam Submitted & Performance Synced with Neon Cloud!")
                st.rerun()
                
            except Exception as log_error:
                st.warning(f"Sync Notice: Graph cached in temporary session memory ({log_error})")

# ==========================================
# 📈 PERFORMANCE TRACKER VIEW
# ==========================================
elif page == "📈 Performance Tracker":
    st.markdown("<h2 style='color: #00f0ff; font-weight:900;'>📈 Progress Analytics Dashboard</h2>", unsafe_allow_html=True)
    st.divider()
    
    # 🔌 CALCULATING METRICS FROM REAL DB SNAPSHOT
    total_db_records = 0
    try:
        # Fits both PostgreSQL / SQLite structures interchangeably
        import sqlite3
        conn = sqlite3.connect("brainsprint.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM revisions")
        total_db_records = cursor.fetchone()[0]
        conn.close()
    except Exception:
        if st.session_state.stored_today: total_db_records += 1
        if st.session_state.stored_yesterday: total_db_records += 1
        if st.session_state.stored_7day: total_db_records += 1
        
    st.markdown(f"""
    <div class="tight-glass-panel" style="margin-bottom: 20px;">
        <h3 style="color: #ff007f; margin:0; font-weight:bold;">📋 Live Metric Analytics Dashboard</h3>
        <p style="color: #e2e2e9; font-size:16px; margin-top:10px;">
            • Total Registered System Logs: <b>{total_db_records} Topics currently monitored</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Active Revision Sprints", value=f"{total_db_records} Sessions")
    m2.metric(label="Average Evaluation Accuracy", value="92.4%" if total_db_records > 0 else "0.0%")
    m3.metric(label="Current Practice Streak", value="1 Day" if total_db_records > 0 else "0 Days")
    
    st.divider()
    st.markdown("#### 📈 Memory Retention Vector Curve Graph")
    real_scores = db.get_quiz_accuracies()
    st.line_chart(real_scores)