#!/usr/bin/env python3

import os
import pymysql
from pymysql.err import Error
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def lazy_paginate(page_size):
    """
    Lazily paginate user data in batches.

    This generator function retrieves user data in chunks of the specified size,
    starting from the first batch and continuing until there is no more data to fetch.

    Args:
        page_size (int): The number of rows to fetch per batch.

    Yields:
        list: A list of user data rows as dictionaries for the current batch.
    """
    offset = 0  # Start offset for the first batch
    while True:
        # Fetch a batch of user data using the current offset
        users = paginate_users(page_size, offset)

        if not users:
            break  # Stop iteration if no more data is available

        offset += page_size  # Increment offset for the next batch
        yield users


def paginate_users(page_size, offset):
    """
    Fetch a batch of user data from the database.

    Executes an SQL query to retrieve a specific number of rows (`page_size`) 
    starting from a given `offset`.

    Args:
        page_size (int): The number of rows to fetch.
        offset (int): The starting position for fetching rows.

    Returns:
        list: A list of user data rows as dictionaries, or None if an error occurs.
    """
    try:
        # Establish a connection to the database
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),          # Database host
            user=os.getenv('DB_USER'),          # Database username
            password=os.getenv('DB_PASSWORD'),  # Database password
            database=os.getenv('DB_DATABASE'),  # Database name
            cursorclass=pymysql.cursors.DictCursor  # Return rows as dictionaries
        )

        # Create a cursor object to execute queries
        with connection.cursor() as cursor:
            # Execute the query with LIMIT and OFFSET for pagination
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
            users = cursor.fetchall()  # Fetch the result set for the current batch
            return users

    except Error as e:
        # Print an error message if there is a database connection or query issue
        print(f"Error connecting to the database: {e}")
        return None
    finally:
        # Ensure the database connection is closed properly
        if connection:
            connection.close()
