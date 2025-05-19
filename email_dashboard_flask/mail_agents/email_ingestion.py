import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime, parseaddr
from collections import defaultdict

EMAIL = "ssaemailagentai@gmail.com"
PASSWORD = "jews kwwa axmz yztx"
IMAP_SERVER = "imap.gmail.com"

def decode_mime_words(s):
    try:
        dh = decode_header(s)
        return ''.join(
            str(t[0], t[1] or "utf-8") if isinstance(t[0], bytes) else t[0]
            for t in dh
        )
    except:
        return s

def get_body_from_msg(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                try:
                    return part.get_payload(decode=True).decode(errors="ignore").strip()
                except:
                    return ""
    else:
        try:
            return msg.get_payload(decode=True).decode(errors="ignore").strip()
        except:
            return ""
    return ""

def fetch_support_threads(limit):
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")

    status, messages = imap.search(None, 'ALL')
    if status != "OK":
        imap.logout()
        return []

    email_ids = messages[0].split()
    latest_ids = list(reversed(email_ids))  # newest first

    support_keywords = ["support", "help", "issue", "problem", "error", "bug", "request", "assistance"]
    seen_message_ids = set()
    thread_map = defaultdict(list)  # thread_id -> list of emails

    for num in latest_ids:
        if sum(len(v) for v in thread_map.values()) >= limit:
            break

        status, msg_data = imap.fetch(num, "(BODY.PEEK[])")
        if status != "OK":
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                message_id = msg.get("Message-ID", "").strip()
                if not message_id or message_id in seen_message_ids:
                    continue

                subject = decode_mime_words(msg.get("Subject", "") or "")
                from_name, from_email = parseaddr(msg.get("From", "") or "")
                date_str = msg.get("Date", "")
                try:
                    sent_at = parsedate_to_datetime(date_str)
                except:
                    sent_at = None
                body = get_body_from_msg(msg)

                content = (subject + body + from_email).lower()
                if not (
                    any(keyword in content for keyword in support_keywords) or 
                    "support@" in from_email.lower() or 
                    "help@" in from_email.lower()
                ):
                    continue

                references = msg.get("References", "").split()
                in_reply_to = msg.get("In-Reply-To", "").strip()
                thread_id = references[0] if references else in_reply_to or message_id

                email_data = {
                    "from": from_email,
                    "subject": subject,
                    "body": body,
                    "date": date_str,
                    "message_id": message_id,
                    "in_reply_to": in_reply_to,
                    "references": msg.get("References", "").strip()
                }

                thread_map[thread_id].append(email_data)
                seen_message_ids.add(message_id)

    imap.logout()

    # Sort messages inside threads by date
    threads = []
    for thread_id, emails in thread_map.items():
        sorted_emails = sorted(emails, key=lambda x: x["date"] or "")
        threads.append({
            "thread_id": thread_id,
            "messages": sorted_emails
        })

    print(f"Fetched {sum(len(t['messages']) for t in threads)} support-related emails in {len(threads)} threads")

    return threads
