mport streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import subprocess

# Initialize the in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create a sample table
cursor.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT
)
''')

# Insert some sample data
employees = [
    (1, 'Alice', 30, 'HR'),
    (2, 'Bob', 24, 'Engineering'),
    (3, 'Charlie', 29, 'Marketing'),
    (4, 'David', 35, 'Engineering'),
    (5, 'Eve', 28, 'HR')
]

cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?)', employees)
conn.commit()

# Define log file path
log_file_path = 'access_log.txt'

# Function to log access to a file
def log_access_to_file(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{timestamp}, {username}\n')

# Function to commit log file to GitHub
def commit_log_to_github():
    try:
        subprocess.run(['git', 'add', log_file_path], check=True)
        subprocess.run(['git', 'commit', '-m', 'Update access log'], check=True)
        subprocess.run(['git', 'push'], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f'Error during Git operations: {e}')

# User authentication
def authenticate(username, password):
    # In a real application, you should use a secure method to store and verify passwords
    valid_username = "cand1"
    valid_password = "1357"
    return username == valid_username and password == valid_password

# Streamlit UI
st.title('SQL Query Emulator with Authentication')

# Login form
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            log_access_to_file(username)
            commit_log_to_github()
            st.success('Logged in successfully')
        else:
            st.error('Invalid username or password')
else:
    st.write(f'Welcome, {st.session_state.username}!')
    
    # Input for SQL query
    query = st.text_area('Enter your SQL query here:', 'SELECT * FROM employees')

    # Execute the query and display the result
    if st.button('Run Query'):
        try:
            result = pd.read_sql_query(query, conn)
            st.write(result)
        except Exception as e:
            st.error(f'Error: {e}')

    # Logout button
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success('Logged out successfully')

# Close the connection when done
conn.close()
