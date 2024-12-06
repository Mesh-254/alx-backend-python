import sqlite3
import functools


def with_db_connection(func):
    """
    A decorator that manages the SQLite database connection by:
    - Opening a connection before executing the wrapped function
    - Closing the connection after the function completes or raises
    an exception

    Args:
        func (function): The function that requires a database
        connection as the first argument.

    Returns:
        function: A wrapped function that handles the
        connection lifecycle automatically.
    """
    def wrapper(*args, **kwargs):
        # Open a connection to the SQLite database
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with the connection
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is closed after the function completes
            conn.close()
    return wrapper


def transactional(func):
    """
    A decorator that wraps a function to ensure that
    the database transaction is handled automatically.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: A wrapped function that handles the transaction.
    """
    def wrapper(conn, *args, **kwargs):
        try:
            # Call the original function with the connection
            result = func(conn, *args, **kwargs)

            # Commit the transaction if the function completes successfully
            conn.commit()
            return result
        except sqlite3.Error as e:
            # Rollback the transaction if an error occurs
            conn.rollback()
            raise e

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email in the database.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
        user_id (int): The ID of the user whose email will be updated.
        new_email (str): The new email to update in the database.

    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))


# Example usage: Update user with ID 1 to a new email
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
