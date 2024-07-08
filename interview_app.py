import streamlit as st
import pandas as pd
import sqlite3

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

# User authentication
def authenticate(username, password):
    # In a real application, you should use a secure method to store and verify passwords
    valid_username = "user"
    valid_password = "test"
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
