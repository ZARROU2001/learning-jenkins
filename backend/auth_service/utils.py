import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict

from fastapi import HTTPException, status
import requests
from jose import ExpiredSignatureError, JWTError, jwt

from config import Config

# Secret key for JWT signing (load from environment variable)
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = Config.REFRESH_TOKEN_EXPIRE_DAYS


# Create Access Token (JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create Refresh Token (JWT)
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT Token
def verify_token(token: str) -> Dict:
    """
    Verifies the JWT token and checks its expiration and validity.
    Returns the decoded token payload if valid, otherwise raises an HTTPException.
    """
    try:
        # Decode the token using the secret key and the algorithm
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})

        # Additional validation (you can customize these checks)
        if decoded_token.get("exp") and datetime.fromtimestamp(decoded_token["exp"]) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

        # Optionally, you can check other claims such as 'aud', 'iss' here
        # Example: if decoded_token.get("iss") != "your-app-name":
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid issuer")

        return decoded_token  # Return the payload if the token is valid

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# def create_password_reset_token(email: str) -> str:
#     """
#     Generate a JWT token for password reset.
#     The token will include the user's email and a specific purpose claim.
#     """
#     # Define claims specific to password reset
#     claims = {"sub": email, "purpose": "password_reset"}
#     expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#
#     # Use the existing `create_access_token` to generate the token
#     reset_token = create_access_token(claims, expires_delta=expires_delta)
#     return reset_token


# def verify_password_reset_token(token: str) -> str:
#     """
#     Verify the password reset token and extract the email if valid.
#     """
#     try:
#         # Decode the token using the existing `verify_token` function
#         decoded_token = verify_token(token)
#
#         # Ensure the token is meant for password reset
#         if decoded_token.get("purpose") != "password_reset":
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token purpose")
#
#         # Return the email if the token is valid
#         return decoded_token["sub"]
#
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# def send_password_reset_email(to_email: str, token: str):
#     """
#     Sends a password reset email with a reset token using Gmail's SMTP server.
#     Args:
#         to_email (str): Recipient's email address.
#         token (str): Password reset token to be included in the reset link.
#     Raises:
#         HTTPException: If sending the email fails.
#     """
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     sender_email = "zarrouaz14@gmail.com"  # Replace with your Gmail address
#     sender_password = "wqwg cddj risr qmru"  # Replace with your Gmail app password
#
#     # Construct the reset link
#     reset_link = f"https://localhost:4200/authentication/reset-password?token={token}"
#
#     # Email subject and body content
#     subject = "Password Reset Request"
#     body = f"""
#     <html>
#         <body>
#             <p>Hello,</p>
#             <p>You requested to reset your password. Please click the link below to reset your password:</p>
#             <a href="{reset_link}">Reset Password</a>
#             <p>If you did not request this, please ignore this email or contact support.</p>
#             <p>Thank you,</p>
#             <p>Your Team</p>
#         </body>
#     </html>
#     """
#
#     # Construct the email message
#     msg = MIMEMultipart()
#     msg["From"] = sender_email
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "html"))  # Use "html" for HTML email content
#
#     try:
#         # Establish SMTP connection and send the email
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()  # Start TLS encryption
#         server.login(sender_email, sender_password)
#         server.send_message(msg)
#         server.quit()
#         print("Password reset email sent successfully")
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to send password reset email. Please try again later."
#         )

