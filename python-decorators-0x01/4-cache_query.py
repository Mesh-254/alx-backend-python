import time
import sqlite3
import functools


def with_db_connection(func):
    """
    A decorator that manages the SQLite database connection by:
    - Opening a connection before executing the wrapped function
    - Committing the transaction if the function succeeds
    - Rolling back the transaction if an exception occurs
    - Closing the connection after the function completes or
    raises an exception

    Args:
        func (function): The function that requires a
        database connection as the first argument.

    Returns:
        function: A wrapped function that handles the connection
        lifecycle automatically.
    """
    def wrapper(*args, **kwargs):
        # Open a connection to the SQLite database
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function
            # with the database connection as the first argument
            result = func(conn, *args, **kwargs)

            # Commit the transaction if the function completes successfully
            conn.commit()
            return result
        except sqlite3.Error as e:
            # Rollback the transaction if an error occurs
            conn.rollback()
            raise e
        finally:
            # Ensure that the connection is
            # closed regardless of success or failure
            conn.close()

    return wrapper


# A global dictionary to store cached query results
query_cache = {}


def cache_query(func):
    """
    A decorator that caches the results of a function based on a query.

    If the query is found in the cache, the cached result is returned
    instead of executing the function.
    Otherwise, the function is executed, and the result is stored in the cache.

    Args:
        func (function): The function to be wrapped and cached.

    Returns:
        function: A wrapped function with caching functionality.
    """
    def wrapper(*args, **kwargs):
        # Extract the query from the keyword arguments
        query = kwargs.get('query')

        # Check if the query is already cached
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]

        # If not cached, execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result

        # Log that the query has been cached
        print(f"Query cached: {query}")
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
