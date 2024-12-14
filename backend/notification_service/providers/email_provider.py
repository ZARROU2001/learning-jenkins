import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_validator import validate_email, EmailNotValidError
from jinja2 import Environment, FileSystemLoader

from config import Config
from logger import logger

env = Environment(loader=FileSystemLoader('templates'))


async def send_email(to_email: str, subject: str, template_name: str, context: dict, content_type: str = "html"):
    """
    Generalized email-sending function using SMTP.

    Args:
        to_email (str): Recipient's email address.
        subject (str): Subject of the email.
        template_name (str): The name of the template to render (e.g., forgot_password_template.html).
        context (dict): The dynamic content to pass to the template for rendering.
        content_type (str): Content type of the email body (e.g., 'plain' for text, 'html' for HTML content).
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Validate recipient email address
        try:
            validate_email(to_email)
        except EmailNotValidError as e:
            logger.error(f"Invalid email address {to_email}: {e}")
            return False

        # Load the email template
        template = env.get_template(template_name)

        # Render the email body with dynamic context
        body = template.render(context)

        # Set up the SMTP server and login credentials
        smtp_server = Config.SMTP_SERVER
        smtp_port = Config.SMTP_PORT
        smtp_password = Config.SMTP_CODE
        sender_email = Config.SMTP_EMAIL

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body content
        msg.attach(MIMEText(body, content_type))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, to_email, msg.as_string())

        logger.info(f"Email successfully sent to {to_email}")
        return True
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
