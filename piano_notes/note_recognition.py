import streamlit as st
import soundfile as sf
from pathlib import Path

# Define the notes and their corresponding files
NOTE_FILES = {
    'C3': 'sounds/c3.wav',
    'C#3': 'sounds/c_sharp_3.wav',
    'D3': 'sounds/d3.wav',
    'D#3': 'sounds/d_sharp_3.wav',
    'E3': 'sounds/e3.wav',
    'F3': 'sounds/f3.wav',
    'F#3': 'sounds/f_sharp_3.wav',
    'G3': 'sounds/g3.wav',
    'G#3': 'sounds/g_sharp_3.wav',
    'A3': 'sounds/a3.wav',
    'A#3': 'sounds/a_sharp_3.wav',
    'B3': 'sounds/b3.wav',
    'C4': 'sounds/c4.wav',
    'C#4': 'sounds/c_sharp_4.wav',
    'D4': 'sounds/d4.wav',
    'D#4': 'sounds/d_sharp_4.wav',
    'E4': 'sounds/e4.wav',
    'F4': 'sounds/f4.wav',
    'F#4': 'sounds/f_sharp_4.wav',
    'G4': 'sounds/g4.wav',
    'G#4': 'sounds/g_sharp_4.wav',
    'A4': 'sounds/a4.wav',
    'A#4': 'sounds/a_sharp_4.wav',
    'B4': 'sounds/b4.wav',
    'C5': 'sounds/c5.wav',
    'C#5': 'sounds/c_sharp_5.wav',
    'D5': 'sounds/d5.wav',
    'D#5': 'sounds/d_sharp_5.wav',
    'E5': 'sounds/e5.wav',
    'F5': 'sounds/f5.wav',
    'F#5': 'sounds/f_sharp_5.wav',
    'G5': 'sounds/g5.wav',
    'G#5': 'sounds/g_sharp_5.wav',
    'A5': 'sounds/a5.wav',
    'A#5': 'sounds/a_sharp_5.wav',
    'B5': 'sounds/b5.wav',
    'C6': 'sounds/c6.wav',
    'C#6': 'sounds/c_sharp_6.wav',
    'D6': 'sounds/d6.wav',
    'D#6': 'sounds/d_sharp_6.wav',
    'E6': 'sounds/e6.wav',
    'F6': 'sounds/f6.wav',
    'F#6': 'sounds/f_sharp_6.wav',
    'G6': 'sounds/g6.wav',
    'G#6': 'sounds/g_sharp_6.wav',
    'A6': 'sounds/a6.wav',
    'A#6': 'sounds/a_sharp_6.wav',
    'B6': 'sounds/b6.wav'
}

# Function to play a note
def play_note(note):
    file = NOTE_FILES.get(note)
    if file and Path(file).exists():
        st.audio(file, format='audio/wav')
        st.write(f"Playing: {note}")
    else:
        st.write(f"File not found for note: {note}")

# Create the piano keys
keys = []
for octave in range(3, 7):
    for key in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']:
        keys.append(f'{key}{octave}')

# Create the piano interface
st.title("Piano App")
cols = st.columns(len(keys))
for i, note in enumerate(keys):
    with cols[i]:
        if st.button(note):
            play_note(note)
