#!/usr/bin/env python3

import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class DatabaseConnection:
    """
    A class-based context manager to handle database connections.
    Automatically opens and closes connections to ensure safe
    resource management.
    """

    def __init__(self, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE):
        """
        Initializes the context manager.
        No arguments are required since the connection details are
        retrieved from environment variables.
        """
        self.DB_HOST = DB_HOST
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_DATABASE = DB_DATABASE

    def __enter__(self):
        """
        Opens the database connection when entering the context.

        :return: An active database connection object.
        """
        # Establish a database connection using environment variables.
        self.conn = pymysql.connect(
            host=self.DB_HOST,  # Database host (e.g., localhost)
            user=self.DB_USER,  # Database user
            password=self.DB_PASSWORD,  # User's password
            database=self.DB_DATABASE,  # Target database name

            # Return rows as dictionaries
            cursorclass=pymysql.cursors.DictCursor
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection when exiting the context.

        :param exc_type: Exception type, if any occurred.
        :param exc_val: Exception value, if any occurred.
        :param exc_tb: Traceback object, if any occurred.
        :return: False if an exception occurred, True otherwise.
        """
        # Ensure the connection is closed
        if self.conn:
            self.conn.close()

        # Print error details if an exception occurred
        if exc_type:
            print(f"Error: {exc_type}, {exc_val}")
            return False  # Propagate the exception

        return True  # Suppress exceptions if none occurred


# Using the DatabaseConnection context manager
# to safely handle database interactions
with DatabaseConnection(DB_HOST=os.getenv('DB_HOST'),
                        DB_USER=os.getenv('DB_USER'),
                        DB_PASSWORD=os.getenv('DB_PASSWORD'),
                        DB_DATABASE=os.getenv('DB_DATABASE')) as connection:
    # Create a cursor object to execute queries
    cursor = connection.cursor()

    # Execute a query to fetch all rows from the 'user_data' table
    cursor.execute("SELECT * FROM user_data")

    # Iterate through the results and print each row
    for row in cursor:
        print(row)
