#!/usr/bin/env python3

from mysql.connector import Error
from seed import connect_to_prodev  # adjust if needed

def stream_users_in_batches(batch_size):
    """Yields users in batches of size `batch_size` from the user_data table."""
    try:
        conn = connect_to_prodev()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM user_data")
        total = cursor.fetchone()["total"]

        for offset in range(0, total, batch_size):
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
            )
            users = cursor.fetchall()
            yield users

    except Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()


def batch_processing(batch_size):
    """Processes each batch and prints users with age > 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
