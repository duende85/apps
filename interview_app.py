import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import subprocess

# Define CSV file paths
customers_csv_path = 'customers.csv'
orders_csv_path = 'orders.csv'

# Load data from CSV files
customers_df = pd.read_csv(customers_csv_path)
orders_df = pd.read_csv(orders_csv_path)

# Initialize the in-memory SQLite database
conn = sqlite3.connect(':memory:')
customers_df.to_sql('customers', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# Function to save the DataFrame back to CSV and commit to GitHub
def save_to_csv_and_commit(df, csv_path):
    df.to_csv(csv_path, index=False)
    try:
        subprocess.run(['git', 'add', csv_path], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update {csv_path}'], check=True)
        subprocess.run(['git', 'push'], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f'Error during Git operations: {e}')

# User authentication
def authenticate(username, password):
    # In a real application, you should use a secure method to store and verify passwords
    valid_username = "admin"
    valid_password = "password123"
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
    query = st.text_area('Enter your SQL query here:', 'SELECT * FROM customers')

    # Execute the query and display the result
    if st.button('Run Query'):
        try:
            result = pd.read_sql_query(query, conn)
            st.write(result)
            st.write(query)
            
            # Save changes to the database back to CSV if modifying queries are detected
            if query.strip().lower().startswith(('update', 'delete', 'insert')):
                customers_df_updated = pd.read_sql_query('SELECT * FROM customers', conn)
                orders_df_updated = pd.read_sql_query('SELECT * FROM orders', conn)
                save_to_csv_and_commit(customers_df_updated, customers_csv_path)
                save_to_csv_and_commit(orders_df_updated, orders_csv_path)
        except Exception as e:
            st.error(f'Error: {e}')

    # Logout button
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success('Logged out successfully')

# Close the connection when done
conn.close()
