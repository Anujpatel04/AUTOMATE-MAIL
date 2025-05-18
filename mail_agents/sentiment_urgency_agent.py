from data_store.db_connector import get_db_connection


def store_emails_in_db(emails):
    print("Emails to insert:", emails)

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO emails (sender, subject, body, processed)
    VALUES (%s, %s, %s, 0)
    """

    for mail in emails:
        cursor.execute(insert_query, (mail["from"], mail["subject"], mail["body"]))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"📥 Stored {len(emails)} emails into the database.")
