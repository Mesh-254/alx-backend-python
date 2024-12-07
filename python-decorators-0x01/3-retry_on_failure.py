import time
import sqlite3
import functools


def with_db_connection(func):
    """
    A decorator that manages the SQLite database connection by:
    - Opening a connection before executing the wrapped function
    - Committing the transaction if the function succeeds
    - Rolling back the transaction if an exception occurs
    - Closing the connection after the function completes
    or raises an exception

    Args:
        func (function): The function that requires
        a database connection as the first argument.

    Returns:
        function: A wrapped function that handles the connection lifecycle.
    """
    def wrapper(*args, **kwargs):
        # Open a connection to the SQLite database 'users.db'
        conn = sqlite3.connect('users.db')
        try:
            # Execute the decorated function with
            # the database connection as the first argument
            result = func(conn, *args, **kwargs)

            # Commit the transaction if the function completes successfully
            conn.commit()
            return result
        except sqlite3.Error as e:
            # Rollback the transaction if a database error occurs
            conn.rollback()
            raise e
        finally:
            # Ensure the database connection is closed
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=1):
    """
    A decorator that retries the wrapped function if it raises an exception.

    Args:
        retries (int): The number of times to retry
        the function (default is 3).
        delay (int): The delay in seconds between
        retries (default is 1 second).

    Returns:
        function: A wrapped function that retries execution on failure.

    Behavior:
        - If the decorated function raises an exception, the retry mechanism
          will execute it again up to the specified number of retries.
        - A delay is applied between each retry attempt.
        - If all retry attempts fail, the exception is re-raised.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0  # Track the number of retry attempts
            while attempts < retries:
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1  # Increment the attempt counter
                    print(f"Attempt {attempts} failed: {e}")
                    if attempts == retries:
                        # Raise the exception if maximum retries are reached
                        raise e
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)  # Wait before retrying
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# attempt to fetch users with automatic retry on failure


users = fetch_users_with_retry()
print(users)
