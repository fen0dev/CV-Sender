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
    with open(cv_filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {cv_filename}",
        )
        message.attach(part)

        # Set up the secure SSL context
        content = ssl.create_default_context()

        # Send the email
        try:
            with smtplib.SMTP_SSL('gmail.com', 465, context=content) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f'E-mail has been successfully sent to {recipient_email}')
        except Exception as e:
            print(f'Failed to send e-mail to {recipient_email}: {e}')

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Send CV to multiple email addresses.')
    parser.add_argument('-c', '--Cv', required=True, help='Path to the CV file')
    parser.add_argument('-e', '--email', required=True, help='Path to the file containing email addresses.')
    args = parser.parse_args()

    # Email details
    # Optional you can use global variable within your environment (terminal) 
    # and export the following
    # sender_email = os.getenv("EMAIL_USER")    --> (Ex: export EMAIL_USER=youremail@example.com)
    # password = os.getenv("PASS_USER")  --> (Ex: export PASS_USER=youremail@example.com)
    sender_email = 'giusdema99@gmail.com'
    password ='Giuspippo99'
    subject = 'Application to Job interview'
    body = "Dear Frangelico,\n\nThis is a test\n\nBest regards,\nGiuseppe"

    if not sender_email or not password:
        print("Error: EMAIL_USER and EMAIL_PASS environment variables must be set.")
        return
    
    # Read the email addresses from the file
    with open(args.emails, 'r') as file:
        recipient_emails = file.read().splitlines()

    # Loop through the email list and send the CV
    for email in recipient_emails:
        send_email(sender_email, password, email, subject, body, args.cv)

if __name__ == '__main__':
    main()

