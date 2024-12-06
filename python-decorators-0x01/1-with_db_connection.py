import sqlite3
import functools

# Decorator to automatically manage SQLite database connections


def with_db_connection(func):
    """
    A decorator that manages the SQLite database connection by:
    - Opening a connection before executing the wrapped function
    - Committing the transaction if the function succeeds
    - Rolling back the transaction if an exception occurs
    - Closing the connection after the function completes or raises an exception

    Args:
        func (function): The function that requires a database connection as the first argument.

    Returns:
        function: A wrapped function that handles the connection lifecycle automatically.
    """
    def wrapper(*args, **kwargs):
        # Open a connection to the SQLite database
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the database connection as the first argument
            result = func(conn, *args, **kwargs)

            # Commit the transaction if the function completes successfully
            conn.commit()
            return result
        except sqlite3.Error as e:
            # Rollback the transaction if an error occurs
            conn.rollback()
            raise e
        finally:
            # Ensure that the connection is closed regardless of success or failure
            conn.close()

    return wrapper

# Function to fetch a user by their ID, with automatic database connection handling


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the database by their unique ID.

    This function executes a SQL SELECT query to find a user by their ID and returns the result.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
        user_id (int): The unique ID of the user to fetch.

    Returns:
        tuple: A tuple containing the user's data, or None if the user is not found.
    """
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Execute the SELECT query to fetch the user with the given ID
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

    # Return the result of the query (fetch one user)
    return cursor.fetchone()


# Fetch a user by their ID with automatic connection handling
user = get_user_by_id(user_id=1)

# Print the fetched user information (or None if not found)
print(user)
