import urllib.request
import email, smtplib, ssl
import time
import argparse

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################################################################
def main():

    parser = argparse.ArgumentParser(description='Cmdline parser')
    parser.add_argument("--sender_email", required=True, type=str, help="Email address of sender")
    parser.add_argument("--password", required=True, type=str, help="Password of email sender")
    parser.add_argument("--smtp_server", default="smtp.gmail.com", type=str, help="SMTP mail server")
    parser.add_argument("--port", default=587, type=int, help="SMTP mail server port")
    parser.add_argument("--receiver_email", required=True, type=str, help="Email address of receiver")
    parser.add_argument("--subject", type=str, default="NEW PUBLIC IP", help="Subject line of sent email")

    args = parser.parse_args()

    port = args.port  # For starttls
    smtp_server = args.smtp_server
    sender_email = args.sender_email
    receiver_email = args.receiver_email
    password = args.password
#    password = input("Type your password and press enter:")
    subject = args.subject
    
# Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
#    message["Bcc"] = receiver_email  # Recommended for mass emails

    external_ip = "EMPTY"
        
    while True:
        _ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

        if (_ip != external_ip):
            print(_ip)

            external_ip = _ip
            body = external_ip

            # Add body to email
            message.attach(MIMEText(body, "plain"))
            text = message.as_string()

            # Create a secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
                server.send

        time.sleep(60)

if __name__ == "__main__": #dont run this as a module

    try:
        main()

    except KeyboardInterrupt:
        print("public_ip stopped")
 
    

