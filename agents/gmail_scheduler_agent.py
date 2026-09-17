from crewai import Agent, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
import os
import re
import smtplib
from email.mime.text import MIMEText
from typing import List, Any

load_dotenv()

def generate_google_meet_link():
    # In a production system, you would call the Google Calendar API to generate a Meet link.
    # For demo purposes, we return a dummy link.
    return "https://meet.google.com/dummy-meet-link"

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def send_email(recipient, subject, body, server=None):
    # Simple SMTP email sending; ensure you have less-secure apps enabled or use an App Password.
    sender_email = os.getenv("GMAIL_SENDER")
    sender_password = os.getenv("GMAIL_PASSWORD")
    if not sender_email or not sender_password:
        raise RuntimeError("GMAIL_SENDER and GMAIL_PASSWORD must be set before scheduling interviews")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient

    try:
        if server is None:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)
                smtp_server.send_message(msg)
        else:
            server.send_message(msg)
        print(f"✅ Email sent to {recipient}")
        return True
    except smtplib.SMTPAuthenticationError as error:
        raise RuntimeError("Gmail authentication failed. Use the sender Gmail address and a Gmail App Password.") from error
    except Exception as error:
        print(f"❌ Failed to send email: {str(error)}")
        return False

def send_interview_emails(candidate_emails, job_role):
    """Send one invitation per validated address using one SMTP session."""
    valid_emails = [email.strip() for email in candidate_emails if EMAIL_PATTERN.fullmatch(email.strip())]
    if len(valid_emails) != len(candidate_emails):
        raise ValueError("The candidate email list contains an invalid email address")

    sender_email = os.getenv("GMAIL_SENDER")
    sender_password = os.getenv("GMAIL_PASSWORD")
    if not sender_email or not sender_password:
        raise RuntimeError("GMAIL_SENDER and GMAIL_PASSWORD must be set before scheduling interviews")

    meet_link = generate_google_meet_link()
    subject = f"Interview Invitation - {job_role}"
    body = f"""Dear Candidate,

You have been selected for an interview for the {job_role} role.
Please join using this Google Meet link: {meet_link}

Best regards,
Recruitment Team
"""
    results = []
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        try:
            server.login(sender_email, sender_password)
        except smtplib.SMTPAuthenticationError as error:
            raise RuntimeError("Gmail authentication failed. Use the sender Gmail address and a Gmail App Password.") from error
        for email in valid_emails:
            send_email(email, subject, body, server=server)
            results.append(f"Email sent to {email} with meet link: {meet_link}")
    return "\n".join(results)

class EmailSendingTool(BaseTool):
    name: str = "email_scheduler"
    description: str = "Schedules interviews by sending emails with Google Meet links"
    
    def _run(self, emails_str: str) -> str:
        emails = [email.strip() for email in emails_str.split(',')]
        return send_interview_emails(emails, "Software Engineer")

class GmailSchedulerAgent:
    @staticmethod
    def agent():
        llm = LLM(
            api_key=os.getenv("GROQ_API_KEY"),
            model="openai/openai/gpt-oss-120b",
            base_url="https://api.groq.com/openai/v1"
        )
        
        email_tool = EmailSendingTool()
        
        return Agent(
            role="Gmail Scheduler",
            goal="Schedule interviews by generating Google Meet links and sending emails to candidates.",
            backstory="You're responsible for coordinating interview schedules and ensuring candidates receive proper invitations.",
            llm=llm,
            allow_delegation=False,
            max_retry_limit=0,
            tools=[email_tool]
        )

    @staticmethod
    def schedule_interview(candidate_email):
        meet_link = generate_google_meet_link()
        subject = "Interview Invitation"
        body = f"""
        Dear Candidate,

        You have been selected for an interview. 
        Please join us using this Google Meet link: {meet_link}

        Best regards,
        HR Team
        """
        send_email(candidate_email, subject, body)
        return meet_link