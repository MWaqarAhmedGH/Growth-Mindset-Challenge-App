# 📁 File: Growth_Mindset_Challenge.py

import streamlit as st
import json
import os
from datetime import datetime


# ---------------------- Helper Functions ------------------------

# Load or create reflections storage
def load_reflections():
    if not os.path.exists("data"):
        os.makedirs("data")
    filepath = "data/reflections.json"
    if not os.path.isfile(filepath):
        with open(filepath, "w") as f:
            json.dump({}, f)
    with open(filepath, "r") as f:
        return json.load(f)

# Save user reflections
def save_reflection(date_str, reflection):
    data = load_reflections()
    data[date_str] = reflection
    with open("data/reflections.json", "w") as f:
        json.dump(data, f, indent=4)

# AI-style mood check using simple keyword detection
def detect_mood(text):
    positive_words = ["happy", "grateful", "excited", "progress", "growth"]
    negative_words = ["stuck", "sad", "angry", "frustrated", "tired"]
    score = sum(word in text.lower() for word in positive_words) - \
            sum(word in text.lower() for word in negative_words)
    
    if score > 1:
        return "🌟 You sound really motivated today! Keep it up!"
    elif score < 0:
        return "💡 It’s okay to feel low sometimes. Growth takes time."
    else:
        return "🧠 Keep reflecting — every thought counts!"


# ---------------------- App UI Starts ---------------------------

st.set_page_config(page_title="Growth Mindset Challenge App", layout="centered")
st.title("🌱 Growth Mindset Challenge App")

# Load today's date
today = datetime.now().strftime("%Y-%m-%d")
reflections = load_reflections()

# Daily Challenges (AI-feel rotation)
challenges = [
    "Think of a recent failure — what did you learn from it?",
    "What’s one thing you’re proud of this week?",
    "Write down a fear you want to overcome.",
    "What habit do you want to build, and why?",
    "Describe a time when you turned a challenge into an opportunity."
]
challenge_of_the_day = challenges[hash(today) % len(challenges)]
st.subheader("📝 Today's Challenge")
st.info(challenge_of_the_day)

# Motivational Quotes
quotes = [
    "“Mistakes are proof that you are trying.” – Unknown",
    "“I am not afraid of storms, for I am learning how to sail my ship.” – Louisa May Alcott",
    "“Every expert was once a beginner.” – Helen Hayes",
    "“The only limit to our realization of tomorrow is our doubts of today.” – FDR",
    "“Progress, not perfection.” – Unknown"
]
quote_of_the_day = quotes[hash(today[::-1]) % len(quotes)]
st.subheader("💬 Quote of the Day")
st.success(quote_of_the_day)

# Reflection Input
st.subheader("💭 Your Reflection")
user_input = st.text_area("Write your thoughts here...", height=200)

if st.button("Submit Reflection"):
    if user_input.strip():
        save_reflection(today, user_input.strip())
        st.success("✅ Reflection saved!")
        st.markdown(detect_mood(user_input))
    else:
        st.warning("Please write something before submitting.")

# Display Past Reflections
st.subheader("📅 Past Reflections")
for date, entry in sorted(reflections.items(), reverse=True):
    with st.expander(f"Reflection on {date}"):
        st.write(entry)

# Show streak
st.sidebar.title("📈 Progress")
st.sidebar.success(f"Total Reflections: {len(reflections)} days")
