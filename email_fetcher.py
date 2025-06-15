import imaplib, email
from bs4 import BeautifulSoup
#The credentials are fake ones below.
EMAIL = 'username@slngcorp.com'
PASSWORD = 'xxxxxx'
IMAP_SERVER = 'outlook.office365.com'

def fetch_links():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Search from ESGPedia
    result, data = mail.search(None, '(FROM "news@esgpedia.io")')
    email_ids = data[0].split()

    all_links = []

    for eid in email_ids[-5:]:  # Only check the last few for testing
        result, data = mail.fetch(eid, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                soup = BeautifulSoup(part.get_payload(decode=True), "html.parser")
                links = [a['href'] for a in soup.find_all('a', href=True)]
                all_links.extend(links)
    
    return all_links

links = fetch_links()
print("ESG Links:", links)