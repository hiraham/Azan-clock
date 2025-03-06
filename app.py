import streamlit as st
import pygame
import datetime
import math
import schedule
import time
import threading
import matplotlib.pyplot as plt


# Pygame initialization for playing Azan
pygame.init()

# Azan audio file path
AZAN_AUDIO = "https://www.islamcan.com/audio/adhan/azan1.mp3"  # Ensure this file is in the same directory

# Function to draw the clock dynamically
def draw_clock():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Draw clock circle
    clock_circle = plt.Circle((0, 0), 1, color="black", fill=False, linewidth=3)
    ax.add_patch(clock_circle)

    # Add numbers on the clock
    for i in range(1, 13):
        angle = math.radians(i * 30)
        x, y = 0.85 * math.sin(angle), 0.85 * math.cos(angle)
        ax.text(x, y, str(i), fontsize=16, fontweight="bold", ha="center", va="center", color="black")

    # Get current time
    now = datetime.datetime.now()
    hour = now.hour % 12 + now.minute / 60.0
    minute = now.minute + now.second / 60.0
    second = now.second

    # Clock hands
    hands = [
        (hour * 30, 0.5, 5, "black"),  # Hour hand
        (minute * 6, 0.7, 3, "blue"),   # Minute hand
        (second * 6, 0.9, 2, "red"),    # Second hand
    ]

    # Draw hands
    for angle, length, width, color in hands:
        angle = math.radians(angle)
        x, y = length * math.sin(angle), length * math.cos(angle)
        ax.plot([0, x], [0, y], linewidth=width, color=color)

    return fig

# Function to play Azan
def play_azan():
    pygame.mixer.init()
    pygame.mixer.music.load(AZAN_AUDIO)
    pygame.mixer.music.play()

# Define Azan times (24-hour format)
AZAN_TIMES = [
    "06:55",  # Fajr
    "12:30",  # Dhuhr
    "17:00",  # Asr
    "18:30",  # Maghrib
    "20:00",  # Isha
]

# Schedule Azan times
for azan_time in AZAN_TIMES:
    schedule.every().day.at(azan_time).do(play_azan)

# Function to run scheduler in the background
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

# Run scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Streamlit UI
st.title("🕰️ Islamic Round Clock with Azan Alarm")


# Dynamic clock display
clock_placeholder = st.empty()

while True:
    fig = draw_clock()
    clock_placeholder.pyplot(fig)
    time.sleep(1)
