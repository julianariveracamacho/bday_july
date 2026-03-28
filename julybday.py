import streamlit as st
import sqlite3
import random
import socket
from datetime import datetime

st.set_page_config(page_title="July's B-Day Challenge", page_icon="🎉", layout="centered")

# Access instructions: run Streamlit with network options instead of setting them on the fly
# Example:
# streamlit run julybday.py --server.address 0.0.0.0 --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false

# Note: set_option for server.address/port is not allowed at runtime in Streamlit.

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

local_ip = get_local_ip()

st.info(f"Access this app from your phone browser at: http://{local_ip}:8501")

# Custom CSS for styling - Pink Theme
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ffb6c1 0%, #ff69b4 50%, #ffc0cb 100%);
    color: #333333;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 20px;
}
.stApp {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(255, 105, 180, 0.3);
    border: 2px solid rgba(255, 105, 180, 0.2);
}
h1, h2, h3 {
    color: #ff1493; /* Pink headings */
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    font-weight: bold;
}
.stButton>button {
    background: linear-gradient(45deg, #ff69b4, #ffb6c1);
    color: white;
    border: 2px solid #ff1493;
    border-radius: 10px;
    font-size: 16px;
    padding: 10px 20px;
}
.stTextInput>div>div>input {
    border-radius: 10px;
    border: 2px solid #ff69b4;
    background-color: white;
}
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px;
    border: 2px solid #ff1493;
    background-color: rgba(255, 255, 255, 0.9);
}
.stDivider {
    border-color: #ff69b4;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("birthday_game.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_name TEXT UNIQUE,
    number INTEGER,
    assigned_at TEXT
)
""")
conn.commit()


def get_existing_assignment(guest_name):
    cursor.execute("SELECT number FROM assignments WHERE guest_name = ?", (guest_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_available_numbers():
    # numbers 0-16, each allowed exactly twice
    all_numbers = list(range(17))
    available = []

    for number in all_numbers:
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE number = ?", (number,))
        count = cursor.fetchone()[0]

        if count < 2:
            available.extend([number] * (2 - count))

    random.shuffle(available)
    return available


def assign_number(guest_name):
    existing = get_existing_assignment(guest_name)
    if existing is not None:
        return existing, False  # already had a number

    available_numbers = get_available_numbers()

    if not available_numbers:
        return None, None  # no numbers left

    assigned_number = random.choice(available_numbers)
    assigned_at = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO assignments (guest_name, number, assigned_at) VALUES (?, ?, ?)",
        (guest_name, assigned_number, assigned_at)
    )
    conn.commit()

    return assigned_number, True


# ---------- UI ----------
st.markdown("<h1 style='text-align: center; color: #ff1493;'>✨🎉 Hello and welcome to my B-day 💖✨</h1>", unsafe_allow_html=True)
st.write("I am so happy to have the opportunity to share this day with youuuuuuuu 💖✨")
st.write("I hope you enjoy yourself and have a great time!! 🌈")

st.divider()

# Display local images if available, otherwise use web fallback to ensure visibility
import os

img_paths = ["IMG_9277.jpeg", "IMG_9276.jpeg"]
any_image_shown = False
# smaller width for mobile/device friendliness
image_width = 350
for img_path in img_paths:
    if os.path.exists(img_path):
        st.image(img_path, width=image_width, caption=f"Image: {img_path}")
        any_image_shown = True

if not any_image_shown:
    st.warning("No local image files found. Showing placeholder images instead.")
    st.image("https://images.unsplash.com/photo-1524169358669-1a97c3aa6e96?auto=format&fit=crop&w=1200&q=80", width=image_width, caption="Birthday celebration")
    st.image("https://images.unsplash.com/photo-1533723159674-7f83f5e8af69?auto=format&fit=crop&w=1200&q=80", width=image_width, caption="Party fun")

st.divider()

name = st.text_input("Your name:")

st.write(
    "If you want and feel good to, you can be part of a mini challenge. "
    "If you are successful, you get a shot from me! 🥃"
)

st.markdown(
    "The task is the following: click the button below and you will get a number. "
    "The game starts at **23:00**!"
)

st.write(
    "In this room, there is another person with the same number. "
    "You need to find them!"
)

st.write(
    "Discuss one of the following topics with them or make a selfie together. "
    "After this, come to me to claim your shot with some kind of evidence 📸"
)

topics = [
    "Comunism",
    "Worst date ever",
    "Who is the person in this party that makes you curious and why?",
    "New year's resolution",
    "A surprising talent of yours",
    "A kindness you witnessed recently",
    "Can a woman and a man be just friends?",
    "Why do men belong to jail?"
]

st.markdown("""
<div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; border: 2px solid #ff69b4; margin: 10px 0;'>
<h3 style='color: #ff1493; text-align: center;'>💬 Conversation Topics</h3>
<ul style='color: #333;'>
""" + "".join(f"<li>{topic}</li>" for topic in topics) + """
</ul>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; border: 2px solid #ff69b4; margin: 10px 0;'>
<h3 style='color: #ff1493; text-align: center;'>📋 Additional Information</h3>
<p>📸 This is the menu of the bar:</p>
<p><a href='https://drive.google.com/file/d/17ZlbYJ5aj_-LTZ8C_DR-YL0UKHJyB7OQ/view?usp=sharing' target='_blank' style='color: #ff1493; font-weight: bold;'>🍹 Open the bar menu 🍹</a></p>
<p>📸 You can take pictures and upload them here:</p>
<p><a href='https://drive.google.com/drive/folders/12YeXZR7BmuNqyPIFRPfniFeXop5KCO6N?usp=sharing' target='_blank' style='color: #ff1493; font-weight: bold;'>📤 Upload your pictures 📤</a></p>
<p>💖 I love you all so much and I am happy that you are part of this special night! 🌟</p>
<p><strong>Bestitos, July 💕✨</strong></p>
</div>
""", unsafe_allow_html=True)

st.divider()

# in case local IMG_9276.png is needed here as well
if os.path.exists("IMG_9276.png"):
    st.image("IMG_9276.png", width=image_width, caption="Image: IMG_9276.png")

st.divider()

st.markdown("<h3 style='text-align: center; color: #ff1493; text-shadow: 2px 2px 4px rgba(255, 215, 0, 0.5);'>🎲✨ Get your challenge number ✨🎲</h3>", unsafe_allow_html=True)

if st.button("🎲✨ Give me my number ✨🎲"):
    guest_name = name.strip().lower()

    if not guest_name:
        st.warning("Please enter your name first.")
    else:
        assigned_number, is_new = assign_number(guest_name)

        if assigned_number is None:
            st.error("Sorry, all numbers have already been assigned.")
        elif is_new:
            st.success(f"{name}, your number is: **{assigned_number}**")
        else:
            st.info(f"{name}, your saved number is: **{assigned_number}**")

# Add a note for proper execution
if __name__ == "__main__":
    print("To run this Streamlit app, use: streamlit run julybday.py")