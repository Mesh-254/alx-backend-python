import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    """
    A decorator that logs the SQL query being executed.
    """
    def wrapper(*args, **kwargs):
        # Extract the query to log it
        query = args[0] if args else kwargs.get('query')
        print(f"SQL query Executing: {query}")
        # Call the original function with the given arguments
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database based on the provided query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list: A list of tuples containing the results from the query.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Execute the provided SQL query
    cursor.execute(query)
    # Fetch all results from the query
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    return results

# Fetch users while logging the query
# This will execute the query to select all users and log the SQL query
users = fetch_all_users(query="SELECT * FROM users")


