import smtplib
import uuid
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict

from fastapi import HTTPException, status
from fastapi.logger import logger
from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt

from config import Config
from errors import PasswordTooShort, PasswordTooWeak, InvalidCredentials

passwd_context = CryptContext(schemes=['bcrypt'])



def validate_passwords_match(new_password: str, confirm_password: str) -> bool:
    """Validate that the new password and confirm password match."""
    if new_password != confirm_password:
        return False
    return True

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passwd_context.verify(plain_password, hashed_password)

def validate_password(password: str):
    if len(password) < 8:
        raise PasswordTooShort()
    if not any(char.isdigit() for char in password):
        raise PasswordTooWeak()
    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        raise PasswordTooWeak()


# Create Access Token (JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

# Verify JWT Token
def verify_token(token: str) -> Dict:
    """
    Verifies the JWT token and checks its expiration and validity.
    Returns the decoded token payload if valid, otherwise raises an HTTPException.
    """
    try:
        # Decode the token using the secret key and the algorithm
        decoded_token = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM],
            options={"verify_exp": True}
        )

        # Check if token has expired
        if decoded_token.get("exp") and datetime.fromtimestamp(decoded_token["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your session has expired. Please log in again to continue.",
            )

        # Optionally, check other claims like 'aud' or 'iss'
        # if decoded_token.get("iss") != "your-app-name":
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid issuer")

        return decoded_token  # Return the payload if the token is valid

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token has expired. Please request a new password reset link.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The token is invalid or malformed. Please ensure the token is correct.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="An error occurred while verifying your token. Please try again.",
        )




def create_password_reset_token(user_id : uuid.UUID,email: str) -> str:
    """
    Generate a JWT token for password reset.
    The token will include the user's email and a specific purpose claim.
    """
    # Define claims specific to password reset
    claims = {"sub": email, "purpose": "password_reset","user_id": str(user_id) }
    expires_delta = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Use the existing `create_access_token` to generate the token
    reset_token = create_access_token(claims, expires_delta=expires_delta)
    return reset_token


def verify_password_reset_token(token: str) -> str:
    """
    Verifies the password reset token and extracts the user ID if valid.

    Args:
        token (str): JWT token for password reset.

    Returns:
        str: The user ID extracted from the token.

    Raises:
        InvalidCredentials: If the token is invalid, expired, or not meant for password reset.
    """
    try:
        # Decode the token using the existing `verify_token` function
        decoded_token = verify_token(token)

        # Validate the token's purpose
        if decoded_token.get("purpose") != "password_reset":
            raise InvalidCredentials("Token purpose is not for password reset.")

        # Ensure the user ID is present in the token
        user_id = decoded_token.get("user_id")
        if not user_id:
            raise InvalidCredentials("Token is missing the user ID.")

        return user_id

    except InvalidCredentials as e:
        # Log the failure (optional)
        logger.warning(f"Invalid password reset token: {token} | Error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error in verify_password_reset_token: {e}", exc_info=True)
        raise InvalidCredentials("An error occurred while validating the token.") from e




def send_password_reset_email(to_email: str, token: str):
    """
    Sends a password reset email with a reset token using Gmail's SMTP server.
    Args:
        to_email (str): Recipient's email address.
        token (str): Password reset token to be included in the reset link.
    Raises:
        HTTPException: If sending the email fails.
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = Config.SMTP_EMAIL  # Replace with your Gmail address
    sender_password = Config.SMTP_CODE  # Replace with your Gmail app password

    # Construct the reset link
    reset_link = f"{Config.FRONTEND_URL}?token={token}"

    # Email subject and body content
    subject = "Password Reset Request"
    body = f"""
    <html>
        <body>
            <p>Hello,</p>
            <p>You requested to reset your password. Please click the link below to reset your password:</p>
            <a href="{reset_link}">Reset Password</a>
            <p>If you did not request this, please ignore this email or contact support.</p>
            <p>Thank you,</p>
            <p>Your Team</p>
        </body>
    </html>
    """

    # Construct the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))  # Use "html" for HTML email content

    try:
        # Establish SMTP connection and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Password reset email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email. Please try again later."
        )


