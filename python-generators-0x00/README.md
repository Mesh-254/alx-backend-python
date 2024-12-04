# Python Generators for Efficient Data Handling

## About the Project

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python’s `yield` keyword to implement generators that provide iterative access to data, promoting optimal resource utilization and improving performance in data-driven applications.

## Learning Objectives

By completing this project, you will:

- **Master Python Generators**: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
- **Handle Large Datasets**: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
- **Simulate Real-world Scenarios**: Develop solutions to simulate live data updates and apply them to streaming contexts.
- **Optimize Performance**: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
- **Apply SQL Knowledge**: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

## Requirements

- Proficiency in Python 3.x.
- Understanding of `yield` and Python’s generator functions.
- Familiarity with SQL and database operations (MySQL and SQLite).
- Basic knowledge of database schema design and data seeding.
- Ability to use Git and GitHub for version control and submission.

## Tasks

### 0. Getting Started with Python Generators
**Objective**: Create a generator that streams rows from an SQL database one by one.

**Instructions**:
- Write a Python script `seed.py` to set up the MySQL database, `ALX_prodev`, with the `user_data` table containing the following fields:
    - `user_id` (Primary Key, UUID, Indexed)
    - `name` (VARCHAR, NOT NULL)
    - `email` (VARCHAR, NOT NULL)
    - `age` (DECIMAL, NOT NULL)
- Populate the database with sample data from `user_data.csv`.

**Prototypes**:
```python
def connect_db():  # Connects to the MySQL database server
def create_database(connection):  # Creates the database ALX_prodev if it does not exist
def connect_to_prodev():  # Connects to the ALX_prodev database in MySQL
def create_table(connection):  # Creates the user_data table if it does not exist
def insert_data(connection, data):  # Inserts data into the database
```


---

### 1. Generator that Streams Rows from an SQL Database
**Objective**: Create a generator that streams rows from an SQL database one by one.

**Instructions**:
- In `0-stream_users.py`, write a function that uses a generator to fetch rows one by one from the `user_data` table using the `yield` Python generator.

**Prototype**:
```python
def stream_users():
    # Your generator code here
```

---

### 2. Batch Processing Large Data
**Objective**: Create a generator to fetch and process data in batches from the users database.

**Instructions**:
- Write a function `stream_users_in_batches(batch_size)` that fetches rows in batches.
- Write a function `batch_processing(batch_size)` that processes each batch to filter users over the age of 25.

**Prototypes**:
```python
def stream_users_in_batches(batch_size):
    # Your generator code here
def batch_processing(batch_size):
    # Your batch processing code here
```

---

### 3. Lazy Loading Paginated Data
**Objective**: Simulate fetching paginated data from the users database using a generator to lazily load each page.

**Instructions**:
- Implement a generator function `lazy_paginate(page_size)` that implements `paginate_users(page_size, offset)` to only fetch the next page when needed at an offset of 0.

**Prototype**:
```python
def lazy_paginate(page_size):
    # Your pagination code here
```

---

### 4. Memory-Efficient Aggregation with Generators
**Objective**: Use a generator to compute a memory-efficient aggregate function, e.g., average age for a large dataset.

**Instructions**:
- Implement a generator `stream_user_ages()` that yields user ages one by one.
- Use the generator in a different function to calculate the average age without loading the entire dataset into memory.

**Prototype**:
```python
def stream_user_ages():
    # Your generator code here
```


## How to Run the Project

1. **Set Up the Database**: 
   - Ensure you have MySQL running on your local machine.
   - Run `seed.py` to set up the `ALX_prodev` database and populate the `user_data` table with data from `user_data.csv`.

2. **Execute the Python Scripts**:
   - For each task, execute the respective script (e.g., `0-main.py`, `1-main.py`, `2-main.py`) to test your implementation.
   
3. **Verify the Output**:
   - Check the console outputs to ensure the generator functions work as expected and process the data correctly in each task.

--- 
