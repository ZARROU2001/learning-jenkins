from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from db.main import get_session
from nonce_metamask.schema import TokenResponse, LoginRequest, VerifySignatureRequest
from nonce_metamask.service import NonceService
from user_token.dependecy import check_user_exists, create_user
from user_token.schemas import LoginResponse, UserLoginModel, UserCreateModel
from user_token.services import authenticate_user, oauth
from utils import verify_token, create_access_token, create_refresh_token
from fastapi.responses import RedirectResponse

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/auth/login", response_model=LoginResponse)
async def login(login_request: UserLoginModel):
    # Call the authentication service
    access_token, refresh_token = await authenticate_user(login_request)

    # Return the tokens in the response
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.get("/auth/logout", dependencies=[Depends(oauth2_scheme)])
async def logout():
    return "working"


@auth_router.post("/auth/refresh_token", response_model=LoginResponse)
async def refresh_token(token: str):
    # Verify and refresh the JWT token
    try:
        payload = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Create a new access token using the user information in the payload
    new_access_token = create_access_token(data={"sub": payload['sub']})

    return LoginResponse(access_token=new_access_token, refresh_token=token)


@auth_router.post("/metamask/login", response_model=TokenResponse)
async def login_with_metamask(request: LoginRequest, db: AsyncSession = Depends(get_session)):
    try:
        nonce_entry = await NonceService.generate_nonce(db, request.wallet_address)
        return {"access_token": nonce_entry.nonce, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get("/google/login")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, Config.GOOGLE_REDIRECT_URI)

@auth_router.get("/callback/google")
async def auth_google(request: Request):
    try:
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user_info = user_response.get("userinfo")

    print(user_info)

    user_create_data = {
        'first_name': user_info.get('given_name'),
        'last_name': user_info.get('family_name'),
        'username': user_info.get('name'),
        # Create username by combining first and last name
        'email': user_info.get('email'),
    }

    user = UserCreateModel(**user_create_data)

    existing_user = await check_user_exists(user.email)

    if existing_user:
        print("Existing user")
        user = existing_user
    else:
        print("Creating user")
        user = await create_user(user)

    print(user)

    access_token = create_access_token(data={"sub": user["uid"]})
    refresh_token1 = create_refresh_token(data={"sub": user["uid"]})

    return RedirectResponse(f"{Config.FRONTEND_URL}/authentication/auth-callback?access_token={access_token}&refresh_token={refresh_token1}")


@auth_router.post("/metamask/verify-signature", response_model=TokenResponse)
async def verify_signature(request: VerifySignatureRequest, db: AsyncSession = Depends(get_session)):
    try:
        token = await NonceService.verify_signature(db, request.wallet_address, request.signed_message)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @auth_router.post("/auth/forget-password")
# async def forget_password(email: PasswordResetRequestModel):
#     # Check if user exists
#     await check_user_exists(email.email)
#
#     # Generate reset token and send email (existing logic)
#     reset_token = create_password_reset_token(email.email)  # Replace with your token generation logic
#     # Call the email sending function
#     send_password_reset_email(to_email=email.email, token=reset_token)
#
#     return {"message": "Password reset email sent successfully"}
#
#
# # Main endpoint function
# @auth_router.post("/auth/reset-password", status_code=status.HTTP_200_OK)
# async def change_password(password: PasswordResetConfirmModel):
#     # Step 1: Validate that the new password and confirm password match
#     validate_passwords_match(password.new_password, password.confirm_new_password)
#
#     # Step 2: Validate the JWT token and retrieve the user ID
#     user_id = verify_password_reset_token(password.token)
#
#     # Step 3: Call the User Service to reset the password
#     await reset_password_in_user_service(user_id=user_id, new_password=password.new_password)
#
#     return {"message": "Password updated successfully"}
#
#
# @auth_router.put("/users/changePassword", status_code=status.HTTP_200_OK)
# async def change_password(password: PasswordUpdateModel,tokens: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         await update_password(password,token=tokens)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Route to handle password change
# @auth_router.post("/auth/reset-password", status_code=status.HTTP_201_CREATED)
# async def change_password(password: PasswordResetConfirmModel):
#     # Step 1: Check if new_password and confirm_password match
#     if password.new_password != password.confirm_new_password:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="The new password and confirmation password do not match"
#         )
#
#     # Step 2: Verify the JWT token (you can add additional verification if needed)
#     try:
#         # If token is valid, the decoded token is returned
#         decoded_token = verify_token(password.token)
#         user_id : str = decoded_token["sub"]  # Assuming 'sub' is the user ID in the token
#     except HTTPException as e:
#         raise e  # If the token is invalid, an error is raised
#     # Step 3: Call the User Service to reset the user's password
#     try:
#         # Call the UserService to change the password
#         response = await _update_password_in_user_service(user_id=user_id, new_password=password.new_password)
#         return response  # Return success response
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @auth_router.get("/logout")
# async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
#     jti = token_details["jti"]
#
#     await add_jti_to_blocklist(jti)
#
#     return JSONResponse(
#         content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
#     )
#
#
# @auth_router.post("/password-reset-request")
# async def password_reset_request(email_data: PasswordResetRequestModel):
#     email = email_data.email
#
#     token = create_url_safe_token({"email": email})
#
#     link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
#
#     html_message = f"""
#     <h1>Reset Your Password</h1>
#     <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
#     """
#     subject = "Reset Your Password"
#
#     send_email.delay([email], subject, html_message)
#     return JSONResponse(
#         content={
#             "message": "Please check your email for instructions to reset your password",
#         },
#         status_code=status.HTTP_200_OK,
#     )
#
#
# @auth_router.post("/password-reset-confirm/{token}")
# async def reset_account_password(
#     token: str,
#     passwords: PasswordResetConfirmModel,
#     session: AsyncSession = Depends(get_session),
# ):
#     new_password = passwords.new_password
#     confirm_password = passwords.confirm_new_password
#
#     if new_password != confirm_password:
#         raise HTTPException(
#             detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
#         )
#
#     token_data = decode_url_safe_token(token)
#
#     user_email = token_data.get("email")
#
#     if user_email:
#         user = await user_service.get_user_by_email(user_email, session)
#
#         if not user:
#             raise UserNotFound()
#
#         passwd_hash = generate_passwd_hash(new_password)
#         await user_service.update_user(user, {"password_hash": passwd_hash}, session)
#
#         return JSONResponse(
#             content={"message": "Password reset Successfully"},
#             status_code=status.HTTP_200_OK,
#         )
#
#     return JSONResponse(
#         content={"message": "Error occured during password reset."},
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     )
#
#
# @auth_router.post("/send_mail")
# async def send_mail(emails: EmailModel):
#     emails = emails.addresses
#
#     html = "<h1>Welcome to the app</h1>"
#     subject = "Welcome to our app"
#
#     send_email.delay(emails, subject, html)
#
#     return {"message": "Email sent successfully"}
