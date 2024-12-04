#!/usr/bin/env python3

import os
import pymysql
from pymysql.err import Error
from dotenv import load_dotenv


"""generator that streams rows from an SQL database"""

# Load environment variables from .env file
load_dotenv()


def stream_users():
    """generator function to fetch rows
    one by one from the user_data table. """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )

        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM user_data")

                for x in cursor:
                    yield x

            except Error as e:
                print(f"Error fetching data: {e}")

            finally:
                cursor.close()

        return connection

    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None
