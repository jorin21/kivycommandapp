from dotenv import load_dotenv
from email.header import decode_header
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import os
import imaplib
import email

load_dotenv("./.env")

username = os.getenv('USERNAME1')
password = os.getenv('PASSWORD')
imap_url = os.getenv('IMAPS')
endpoint = os.getenv('ENDPT')
sserv = os.getenv('SMTPS')
port = os.getenv('SMTPPORT')
eFrom = os.getenv('EFROM')


def sendmail(body,subject,attachments = (False, '')):
    message = MIMEMultipart()
    message["From"] = eFrom
    message["To"] = endpoint
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    if attachments[0]:

        filename = attachments[1]

        
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            
        encoders.encode_base64(part)

        
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        
        message.attach(part)
        
        
    strings = message.as_string()

    context = ssl.create_default_context()
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    import certifi
    context.load_verify_locations(
        cafile=os.path.relpath(certifi.where()),
        capath=None,
        cadata=None)

    with smtplib.SMTP_SSL(sserv, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, endpoint, strings)


def readmail():
    #connection
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(username, password)


    # email setup
    status, emails = con.select('INBOX')
    emails = int(emails[0])
    Umail = con.search(None, 'UnSeen')[1][0].split()
    UnSeen = len(Umail)

    # email fetch
    stat, msg = con.fetch(str(emails), "(RFC822)")

    for res in msg:
        if isinstance(res, tuple):
            msg = email.message_from_bytes(res[1])

            
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)

            From = decode_header(msg.get('From'))
            if isinstance(From, bytes):
                From = From.decode(encoding)
                
            From = From[0][0].split('<')
            From = From[1][:-1]
                
            if msg.is_multipart():
                for part in msg.walk():
                    c_type = part.get_content_type()
                    c_dispo = str(part.get('Content-Disposition'))

                    if c_type == 'text/plain':
                        body = part.get_payload(decode=True).decode()

            else:
                body = msg.get_payload(decode=True).decode()
                
            response = [subject.strip(), From, body]
            return response
