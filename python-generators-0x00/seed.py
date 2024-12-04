#!/usr/bin/env python3
import os
import uuid
from dotenv import load_dotenv
import csv
import pymysql
from pymysql import Error


# Load environment variables from .env file
load_dotenv()

# get user data file data
user_data_file = os.getenv('USER_DATA_FILE')


def connect_db():
    """Function to connect to the MySQL database server"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )

        return connection

    except Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return None


def create_database(connection):
    """Function to create the database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_DATABASE')}")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Function to connect to the MySQL database"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )

        return connection

    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """Function to create the table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        cursor.close()
    except Error as e:
        print(f"Error creating user_data table: {e}")


def insert_data(connection, user_data_file):
    """Function to insert data into the table"""
    try:
        cursor = connection.cursor()
        with open(user_data_file, 'r') as file:
            csv_reader = csv.reader(file)  # read csv file
            next(csv_reader)  # Skip header row
            for line in csv_reader:
                if line:

                    # Extract values from the line
                    name, email, age = line

                    # Generate a unique UUID for user_id
                    user_id = str(uuid.uuid4())

                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )

        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
