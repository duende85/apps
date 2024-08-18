import streamlit as st
import soundfile as sf
from pathlib import Path

# Define the notes and their corresponding files
NOTE_FILES = {
    'C3': 'notes/c3.wav',
    'C#3': 'notes/c_sharp_3.wav',
    'D3': 'notes/d3.wav',
    'D#3': 'notes/d_sharp_3.wav',
    'E3': 'notes/e3.wav',
    'F3': 'notes/f3.wav',
    'F#3': 'notes/f_sharp_3.wav',
    'G3': 'notes/g3.wav',
    'G#3': 'notes/g_sharp_3.wav',
    'A3': 'notes/a3.wav',
    'A#3': 'notes/a_sharp_3.wav',
    'B3': 'notes/b3.wav',
    'C4': 'notes/c4.wav',
    'C#4': 'notes/c_sharp_4.wav',
    'D4': 'notes/d4.wav',
    'D#4': 'notes/d_sharp_4.wav',
    'E4': 'notes/e4.wav',
    'F4': 'notes/f4.wav',
    'F#4': 'notes/f_sharp_4.wav',
    'G4': 'notes/g4.wav',
    'G#4': 'notes/g_sharp_4.wav',
    'A4': 'notes/a4.wav',
    'A#4': 'notes/a_sharp_4.wav',
    'B4': 'notes/b4.wav',
    'C5': 'notes/c5.wav',
    'C#5': 'notes/c_sharp_5.wav',
    'D5': 'notes/d5.wav',
    'D#5': 'notes/d_sharp_5.wav',
    'E5': 'notes/e5.wav',
    'F5': 'notes/f5.wav',
    'F#5': 'notes/f_sharp_5.wav',
    'G5': 'notes/g5.wav',
    'G#5': 'notes/g_sharp_5.wav',
    'A5': 'notes/a5.wav',
    'A#5': 'notes/a_sharp_5.wav',
    'B5': 'notes/b5.wav',
    'C6': 'notes/c6.wav',
    'C#6': 'notes/c_sharp_6.wav',
    'D6': 'notes/d6.wav',
    'D#6': 'notes/d_sharp_6.wav',
    'E6': 'notes/e6.wav',
    'F6': 'notes/f6.wav',
    'F#6': 'notes/f_sharp_6.wav',
    'G6': 'notes/g6.wav',
    'G#6': 'notes/g_sharp_6.wav',
    'A6': 'notes/a6.wav',
    'A#6': 'notes/a_sharp_6.wav',
    'B6': 'notes/b6.wav'
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
