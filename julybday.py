import streamlit as st
import sqlite3
import random
from datetime import datetime

st.set_page_config(page_title="July's B-Day Challenge", page_icon="🎉", layout="centered")

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
    "Your most embarrassing moment 😂",
    "A secret talent you have 💖",
    "Your favorite travel destination 🌍",
    "Your worst date ever 💀",
    "What you would do with 1 million euros 💸",
    "Your biggest life goal💖",
    "Your favorite moment with me 💖",
    "Why do men belong to jail 💀"
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
<p><a href='https://drive.google.com/file/d/1hiv8T22LzFchES53mo-qTEgLw6AVZbA8/view?usp=sharing' target='_blank' style='color: #ff1493; font-weight: bold;'>🍹 Open the bar menu 🍹</a></p>
<p>📸 You can take pictures and upload them here:</p>
<p><a href='https://drive.google.com/drive/folders/12YeXZR7BmuNqyPIFRPfniFeXop5KCO6N?usp=sharing' target='_blank' style='color: #ff1493; font-weight: bold;'>📤 Upload your pictures 📤</a></p>
<p>💖 I love you all so much and I am happy that you are part of this special night! 🌟</p>
<p><strong>Bestitos, July 💕✨</strong></p>
</div>
""", unsafe_allow_html=True)

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