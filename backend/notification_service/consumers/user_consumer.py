import json
from aiokafka import AIOKafkaConsumer

from config import Config
from logger import logger
from services.email_service import send_forgot_password_email, send_update_password_email, send_welcome_email


async def consume_user_events():
    consumer = AIOKafkaConsumer(
        Config.KAFKA_USER_TOPIC,
        bootstrap_servers=Config.KAFKA_BROKER,
        group_id="notification-service-group"
    )
    await consumer.start()
    print("consumer started")
    try:
        async for message in consumer:
            event = message.value
            print(event)
            logger.info(f"Received event: {event}")
            await process_message(event)
    finally:
        await consumer.stop()




async def process_message(message):
    """
    Process incoming Kafka message and call the appropriate email sending function.
    """
    try:
        # Parse the message
        data = json.loads(message)

        # Extract message details
        email_type = data.get("email_type")
        to_email = data.get("to_email")

        if email_type == "forgot_password":
            reset_token = data.get("reset_token")
            send_forgot_password_email(to_email=to_email, reset_token=reset_token)
        elif email_type == "update_password":
            user_name = data.get("user_name")
            await send_update_password_email(to_email=to_email, user_name=user_name)
        elif email_type == "welcome":
            user_name = data.get("user_name")
            send_welcome_email(to_email=to_email, user_name=user_name)
        else:
            logger.error(f"Unknown email type: {email_type}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
