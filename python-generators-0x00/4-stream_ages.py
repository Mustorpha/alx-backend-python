#!/usr/bin/env python3

from seed import connect_to_prodev

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """Uses the generator to calculate average age without loading all data."""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
