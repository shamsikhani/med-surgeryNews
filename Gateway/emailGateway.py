import resend
import os
from typing import List
from crewai.tools import BaseTool
from pydantic import Field, BaseModel
import markdown2
import logging

logger = logging.getLogger(__name__)

class EmailSender(BaseModel):
    """Simple email sending class using Resend"""
    api_key: str = Field(description="Resend API key")
    
    def send_email(self, to: List[str], subject: str, html_content: str) -> bool:
        try:
            resend.api_key = self.api_key
            response = resend.Emails.send({
                "from": "Rosetta News <onboarding@resend.dev>",
                "to": to,
                "subject": subject,
                "html": html_content
            })
            logger.info(f"Email sent successfully to {len(to)} recipients")
            return True
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return False

class EmailGateway(BaseTool):
    """CrewAI tool for sending news digests"""
    
    name: str = "Email News Tool"
    description: str = "Sends formatted news digest as markdown email"
    recipients: List[str] = Field(description="List of email recipients")
    sender: EmailSender = Field(description="Email sender instance")

    def __init__(self, api_key: str, recipients: List[str]):
        sender = EmailSender(api_key=api_key)
        super().__init__(recipients=recipients, sender=sender)
        self.recipients = recipients

    def _run(self, markdown_content: str) -> str:
        html_content = self._convert_markdown_to_html(markdown_content)
        success = self.sender.send_email(
            to=self.recipients,
            subject="Today's News Digest",
            html_content=html_content
        )
        return "Email sent successfully" if success else "Failed to send email"

    def send_email(self, markdown_content: str) -> str:
        return self._run(markdown_content)

    def _convert_markdown_to_html(self, markdown_content: str) -> str:
        try:
            html_content = markdown2.markdown(markdown_content)
            return f"""
                <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1 {{ color: #333; }}
                            a {{ color: #0066cc; }}
                        </style>
                    </head>
                    <body>{html_content}</body>
                </html>
            """
        except ImportError:
            return f"<pre>{markdown_content}</pre>" 