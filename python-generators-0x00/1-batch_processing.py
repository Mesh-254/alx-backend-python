#!/usr/bin/env python3

import pymysql
from pymysql.err import Error
import os
from dotenv import load_dotenv

load_dotenv()


def stream_users_in_batches(batch_size):
    """
    Stream users in batches of a specified size from the database.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A batch of user data rows as dictionaries.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            cursorclass=pymysql.cursors.DictCursor  # Ensure rows are returned as dictionaries
        )

        with connection.cursor() as cursor:

            offset = 0
            while True:
                cursor.execute("SELECT * FROM user_data ORDER BY user_id  LIMIT %s OFFSET %s", (batch_size, offset))

                batch = cursor.fetchall()
              
                if not batch:
                    break  # No more rows to fetch

                offset += batch_size
                yield batch
    
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Process users in batches, filtering users over the age of 25.

    Args:
        batch_size (int): The number of rows to fetch in each batch.
    """
    try:
        for batch in stream_users_in_batches(batch_size):
            # Filter users with age > 25
            filtered_users = [user for user in batch if user['age'] > 25]
            for user in filtered_users:
                print(user)  # Replace with actual processing logic
    except Exception as e:
        print(f"Error processing users: {e}")
