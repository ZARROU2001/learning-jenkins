import asyncio
import json

from aiokafka import AIOKafkaProducer

from config import Config


async def send_notification(kafka_message, is_successful=True):
    """
    Send a notification message to the Kafka topic.
    This is an asynchronous function that sends a message to Kafka for triggering email notifications.
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        loop=asyncio.get_event_loop(),
    )

    # Convert the message dictionary to JSON string before sending
    message_json = json.dumps(kafka_message).encode('utf-8')

    try:
        # Start the producer
        await producer.start()

        # Send the message to the Kafka topic
        await producer.send_and_wait(Config.KAFKA_TRANSACTION_TOPIC, message_json)

        # Ensure the message is sent before exiting
        await producer.flush()

        print(f"Sent message to Kafka: {kafka_message}")

    except Exception as e:
        # Handle any exceptions that occur during sending
        print(f"Failed to send message to Kafka: {e}")

    finally:
        # Stop the producer
        await producer.stop()
