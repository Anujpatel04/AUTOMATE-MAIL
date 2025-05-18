import imaplib
import email
from email.header import decode_header

# Your email credentials
EMAIL = "ssaemailagentai@gmail.com"
PASSWORD = "jews kwwa axmz yztx"  # Use App Password for Gmail if 2FA is on
IMAP_SERVER = "imap.gmail.com"

def fetch_emails(limit=10):
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")

    # Search for all emails (use 'UNSEEN' if you want only unread)
    status, messages = imap.search(None, 'ALL')
    email_ids = messages[0].split()
    latest_ids = reversed(email_ids[-limit:])  # Check latest emails first

    keywords = ["support"]
    emails = []

    for num in latest_ids:
        status, msg_data = imap.fetch(num, "(BODY.PEEK[])")
        if status != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["Subject"] or ""
                from_email = msg["From"] or ""
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                content = (subject + body + from_email).lower()

                if any(keyword in content for keyword in keywords):
                    emails.append({
                        "from": from_email,
                        "subject": subject,
                        "body": body,
                    })
                    imap.logout()
                    return emails  # Return immediately after first match

    imap.logout()
    return emails  # Empty if no match
