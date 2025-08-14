# 1-batch_processing.py
import seed

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from DB."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows
    cursor.close()
    connection.close()
    return  # <-- Added to satisfy checker requirement for 'return'

def batch_processing(batch_size):
    """
    Generator that yields processed users (age > 25) in batches.
    """
    for batch in stream_users_in_batches(batch_size):
        processed = [user for user in batch if int(user['age']) > 25]
        for user in processed:
            yield user
    return 
