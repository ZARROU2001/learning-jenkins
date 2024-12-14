from providers.sse_provider import SSEProvider

sse_provider = SSEProvider()


async def send_transaction_success_notification(user_id: str, transaction_details: str):
    """Send transaction success notification to the user."""
    notification_message = f"Transaction successful: {transaction_details}"
    await sse_provider.send_to_client(user_id, notification_message)


async def send_transaction_failed_notification(user_id: str, error_message: str):
    """Send transaction failed notification to the user."""
    notification_message = f"Transaction failed: {error_message}"
    await sse_provider.send_to_client(user_id, notification_message)
