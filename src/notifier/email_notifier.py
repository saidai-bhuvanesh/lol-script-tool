import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

class EmailNotifier:
    def __init__(self):
        self.sender = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("SENDER_PASSWORD")
        self.receiver = os.getenv("RECEIVER_EMAIL")

    def send_report(self, excel_path: str):
        if not self.sender or not self.password:
            print("WARNING: Email credentials missing. Skipping email notification.")
            return

        if not excel_path or not os.path.exists(excel_path):
            print("No report found to send.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = f"Today's Abroad Job List – 50 Verified Opportunities ({os.path.basename(excel_path).split('_')[-1].split('.')[0]})"

        body = "Hello,\n\nPlease find attached your daily curated list of abroad job opportunities with visa sponsorship potential.\n\nBest regards,\nYour AI Job Assistant"
        msg.attach(MIMEText(body, 'plain'))

        with open(excel_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(excel_path)}")
            msg.attach(part)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender, self.password)
            text = msg.as_string()
            server.sendmail(self.sender, self.receiver, text)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
