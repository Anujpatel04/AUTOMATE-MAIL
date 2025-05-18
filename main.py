from agents.email_ingestion import fetch_emails
from agents.sentiment_urgency_agent import store_emails_in_db
if __name__ == "__main__":
    emails = fetch_emails(limit=10)
    if emails:
        store_emails_in_db(emails)
        print(f"📥 Stored {len(emails)} emails into the database.")
    else:
        print("📭 No new emails to store.")
