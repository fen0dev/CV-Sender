import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import argparse
import os

def send_email(sender_email, password, recipient_email, subject, body, cv_filename):
    # Create the email header
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach the email body
    message.attach(MIMEText(body, 'plain'))

    # Attach the CV
    with open(cv_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {cv_filename}",
        )
        message.attach(part)

    # Set up the secure SSL context
    context = ssl.create_default_context()

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.example.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Send CV to multiple email addresses.')
    parser.add_argument('-c', '--cv', required=True, help='Path to the CV file')
    parser.add_argument('-e', '--emails', required=True, help='Path to the text file containing email addresses')
    args = parser.parse_args()

    # Email details
    sender_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    subject = "Subject: Your CV Attached"
    body = "Dear Sir/Madam,\n\nPlease find attached my CV for your review.\n\nBest regards,\nYour Name"

    if not sender_email or not password:
        print("Error: EMAIL_USER and EMAIL_PASS environment variables must be set.")
        return

    # Read the email addresses from the file
    with open(args.emails, 'r') as file:
        recipient_emails = file.read().splitlines()

    # Loop through the email list and send the CV
    for email in recipient_emails:
        send_email(sender_email, password, email, subject, body, args.cv)

if __name__ == "__main__":
    main()
