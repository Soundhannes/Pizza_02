"""
Database connection management for Pizza Calculator.
"""

import mysql.connector
from mysql.connector import Error
import os
from typing import Optional

def get_connection():
    """
    Create and return a database connection.
    
    Returns:
        mysql.connector.connection: Database connection object
        
    Raises:
        Error: If connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'pizza_calculator'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306)),
            autocommit=True
        )
        return connection
    except Error as e:
        raise Error(f"Error connecting to database: {e}")

def init_database():
    """
    Initialize the database by executing the schema file.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Read and execute schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as file:
            schema_sql = file.read()
        
        # Split and execute each statement
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"Error initializing database: {e}")
        return False
    except FileNotFoundError:
        print("Schema file not found")
        return False