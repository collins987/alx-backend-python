# 4-stream_ages.py
import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield float(age)
    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No data available.")

if __name__ == "__main__":
    calculate_average_age()
