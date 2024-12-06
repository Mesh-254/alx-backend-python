#!/usr/bin/env python3

import pymysql
from pymysql.err import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def calculate_average_age():
    """
    Calculate the average age of users in the database using a generator.

    This function fetches user ages one by one from the database and computes
    the average age without loading all the data into memory at once. The
    average is calculated by summing the ages and dividing by the total count.

    The result is printed with two decimal places.
    """
    total = 0  # Accumulator for the sum of ages
    count = 0  # Counter for the number of users

    # Loop through each age fetched from the generator
    for age in stream_user_ages():
        total += age  # Add the current age to the total
        count += 1  # Increment the count of users

    # Check if there are any users to avoid division by zero
    if count > 0:
        av = total / count  # Calculate the average age
        # Print the average rounded to two decimal places
        print(f"Average age of users: {av:.2f}")
    else:
        # Handle the case with no users
        print("No users found to calculate the average age.")


def stream_user_ages():
    """
    Simulate a stream of user ages from the database.

    This function connects to a MySQL database and retrieves the ages of users
    one by one using a generator. The generator yields one age at a time, making
    the function memory efficient for large datasets.

    Returns:
        generator: A generator that yields user ages from the database.
    """
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'),
        # Ensure rows are returned as dictionaries
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Execute the query to select user ages
            cursor.execute("SELECT age FROM user_data")
            # Yield each age from the result set one at a time
            for row in cursor:
                yield row['age']
    except Error as e:
        # Print an error message if something goes wrong with the database connection or query
        print(f"Error fetching user ages: {e}")
    finally:
        # Ensure the database connection is closed after fetching the data
        connection.close()


if __name__ == "__main__":
    # Start the calculation of average age when the script is executed directly
    calculate_average_age()
