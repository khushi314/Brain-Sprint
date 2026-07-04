import os
import pytz
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import database as db

def check_and_send_email_reminders():
    # 1. Timezone configurations (IST Check)
    ist = pytz.timezone('Asia/Kolkata')
    current_hour = datetime.now(ist).strftime("%H") # Jaise "08", "14" etc.
    today_str = datetime.now(ist).strftime("%Y-%m-%d")
    
    # 2. Database se aapka set kiya hua time lekar aao
    user_set_time = db.get_reminder_time()
    user_hour = user_set_time.split(":")[0] 
    
    if current_hour != user_hour:
        print(f"😴 Current hour ({current_hour}:00 IST) doesn't match User Slot ({user_hour}:00 IST). Skipping.")
        return
        
    print(f"⏰ Hour Match Found! Checking due revisions for today...")
    
    # 3. Connect to Neon Database to find due tasks
    conn = db.get_connection()
    cursor = conn.cursor()
    query = """
        SELECT topic_name, stage FROM revisions 
        WHERE ((date_1_day = %s) OR (date_7_day = %s) OR (date_30_day = %s)) 
        AND current_status = 'Active';
    """
    cursor.execute(query, (today_str, today_str, today_str))
    due_topics = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not due_topics:
        print("✅ No revisions scheduled for today.")
        return
        
    # 4. Craft Beautiful Email HTML/Text Body
    email_sender = os.getenv("SENDER_EMAIL")       
    email_receiver = os.getenv("RECEIVER_EMAIL")   
    app_password = os.getenv("GMAIL_APP_PASSWORD") 
    
    if not all([email_sender, email_receiver, app_password]):
        print("❌ Error: Email credentials missing in GitHub Secrets.")
        return

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "🧠 BrainSprint: Daily Spaced Revision Alert!"
    
    body = "🧠 BrainSprint Daily Spaced Revision Alert! 🧠\n\n"
    for topic, stage in due_topics:
        body += f"📌 Topic: {topic}\n⏳ Stage: {stage}\n\n"
    body += "🚀 Log in to your app dashboard, complete the quiz arena and smash your daily target, Buddy!"
    
    msg.attach(MIMEText(body, 'plain'))
    
    # 5. Connect to Gmail Server and Send
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Ekdam sahi spelling (l hai, 1 nahi)
        server.login(email_sender, app_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print("🔥 Revision Reminder Email Triggered Successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    check_and_send_email_reminders()