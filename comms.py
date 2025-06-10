import smtplib
from email.mime.text import MIMEText
from json import load

with open('secrets.json', 'r') as file:
    secrets = load(file)

def send_sms_via_email(to_number, message, carrier_gateway, smtp_server, smtp_port, smtp_username, smtp_password):
    to_address = f"{to_number}@{carrier_gateway}"
    msg = MIMEText(message)
    msg["From"] = smtp_username
    msg["To"] = to_address
    msg["Subject"] = "SMS via Email"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [to_address], msg.as_string())

# Example usage
to_number = "15417312952"
message = "Hello, this is a test message."
carrier_gateway = "vtext.com"  # AT&T gateway, change this based on carrier
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = secrets["smtp_email"]
smtp_password = secrets["smtp_password"]

print(smtp_password)

send_sms_via_email(to_number, message, carrier_gateway, smtp_server, smtp_port, smtp_username, smtp_password)
