#!/usr/bin/env python3

"""
A Python script to query a SQLite database using a context manager.
The script demonstrates how to manage database connections and execute
queries securely and efficiently.
"""

import sqlite3


class ExecuteQuery:
    """
    A reusable context manager to manage SQLite database connections.
    It takes a query and parameters as input, executes the query, and
    ensures the connection is safely opened and closed.
    """

    def __init__(self, query, age):
        """
        Initialize the ExecuteQuery context manager with a query
        and parameters.

        :param query: The SQL query to execute.
        :param age: Parameters for the SQL query
        (in this case, the age threshold).
        """
        self.query = query  # Store the SQL query
        self.age = age  # Store the query parameter (age)

    def __enter__(self):
        """
        Establish a connection to the SQLite database
        and return the connection object.

        :return: A connection object to the database.
        """
        self.conn = sqlite3.connect(
            'users.db')  # Connect to the SQLite database file
        return self.conn  # Return the connection object

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Commit changes, close the database connection,
        and handle any exceptions that occurred during execution.

        :param exc_type: The exception type (if any).
        :param exc_val: The exception value (if any).
        :param exc_tb: The traceback object (if any).
        :return: False if an exception occurred, True otherwise.
        """
        if self.conn:  # Ensure the connection exists
            self.conn.commit()  # Commit any changes made during the context
            self.conn.close()  # Close the database connection
        if exc_type:  # If an exception occurred
            print(f"Error: {exc_type}, {exc_val}")  # Log the error details
            return False  # Indicate the exception was not handled
        return True  # Indicate successful execution


# Define the SQL query to execute
query = "SELECT * FROM users WHERE age > ?"

# Define the query parameter (age threshold)
age = 25

# Use the ExecuteQuery context manager to execute the query
with ExecuteQuery(query, age) as connection:
    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    # Execute the SQL query with the age parameter
    cursor.execute(query, (age,))
    for row in cursor:  # Iterate through the query results
        print(row)  # Print each row returned by the query
