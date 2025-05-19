from mail_agents.email_ingestion import fetch_support_threads

threads = fetch_support_threads(limit=10)

for thread in threads:
    print(f"\n--- Thread ID: {thread['thread_id']} ---")
    for mail in thread["messages"]:
        print(f"[{mail.get('date', '')}] {mail.get('subject', '')} - {mail.get('from', '')}")