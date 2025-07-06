#!/usr/bin/env python3

from mysql.connector import connect, Error
from uuid import uuid4
import logging

# Config
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'ALX_prodev'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_db():
    try:
        return connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    except Error as e:
        logging.error(f"Error connecting to DB server: {e}")


def create_database(connection):
    query = f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            logging.info(f"Database `{DB_NAME}` created or already exists.")
    except Error as e:
        logging.error(f"Error creating database: {e}")


def connect_to_prodev():
    try:
        return connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        logging.error(f"Error connecting to `{DB_NAME}`: {e}")


def create_table(connection):
    query = '''CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(255) PRIMARY KEY, 
                name VARCHAR(255) NOT NULL, 
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )'''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            logging.info("Table `user_data` created or already exists.")
    except Error as e:
        logging.error(f"Error creating table: {e}")


def insert_data(connection, data):
    query = '''
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (data['uuid'], data['name'], data['email'], data['age']))
            connection.commit()
            logging.info(f"Inserted user: {data['name']}")
    except Error as e:
        logging.error(f"Error inserting data: {e}")


def main():
    conn1 = None
    conn2 = None
    try:
        conn1 = connect_db()
        create_database(conn1)
        conn1.close()

        conn2 = connect_to_prodev()
        create_table(conn2)

        # Insert users
        users = [
            {
                "uuid": str(uuid4()),
                "name": "Amina Yusuf",
                "email": "amina@example.com",
                "age": 29
            },
            {
                "uuid": str(uuid4()),
                "name": "Chuka Obi",
                "email": "chuka@example.com",
                "age": 35
            }
        ]
        for user in users:
            insert_data(conn2, user)

    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        if conn1 and conn1.is_connected():
            conn1.close()
        if conn2 and conn2.is_connected():
            conn2.close()
        logging.info("All connections closed.")


if __name__ == '__main__':
    main()
