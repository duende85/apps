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

# Streamlit UI
st.title('SQL Query Emulator')

# Input for SQL query
query = st.text_area('Enter your SQL query here:', 'SELECT * FROM employees')

# Execute the query and display the result
if st.button('Run Query'):
    try:
        result = pd.read_sql_query(query, conn)
        st.write(result)
    except Exception as e:
        st.error(f'Error: {e}')

# Close the connection when done
conn.close()
