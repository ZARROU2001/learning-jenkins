from aiokafka import AIOKafkaConsumer

from config import Config
from logger import logger


async def consume_user_events():
    consumer = AIOKafkaConsumer(
        Config.KAFKA_TRANSACTION_TOPIC,
        bootstrap_servers=Config.KAFKA_BROKER,
        group_id="notification-service-group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            event = message.value
            logger.info(f"Received event: {event}")
            #process_message(event)
    finally:
        await consumer.stop()