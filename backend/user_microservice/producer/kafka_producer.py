import asyncio
import json

from aiokafka import AIOKafkaProducer

from config import Config


async def send_email_notification(email_type, to_email, user_name=None, reset_token=None):
    """
    Send a notification message to the Kafka topic.
    This is an asynchronous function that sends a message to Kafka for triggering email notifications.
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=Config.KAFKA_BROKER,
        loop=asyncio.get_event_loop(),
    )

    message = {
        "email_type": email_type,
        "to_email": to_email,
        "user_name": user_name,
        "reset_token": reset_token
    }

    # Convert the message dictionary to JSON string before sending
    message_json = json.dumps(message).encode('utf-8')

    try:
        # Start the producer
        await producer.start()

        # Send the message to the Kafka topic
        await producer.send_and_wait(Config.KAFKA_USER_TOPIC, message_json)

        # Ensure the message is sent before exiting
        await producer.flush()

        print(f"Sent message to Kafka: {message}")

    except Exception as e:
        # Handle any exceptions that occur during sending
        print(f"Failed to send message to Kafka: {e}")

    finally:
        # Stop the producer
        await producer.stop()
