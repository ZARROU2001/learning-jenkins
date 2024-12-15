import logging
from aiokafka import AIOKafkaProducer
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Kafka producer
producer = AIOKafkaProducer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS)

async def start_kafka_producer():
    await producer.start()

async def stop_kafka_producer():
    await producer.stop()

async def send_to_kafka(price: float):
    try:
        logger.info(f"Sending price to Kafka: {price}")
        await producer.send_and_wait(Config.KAFKA_TOPIC, value=str(price).encode('utf-8'))
        logger.info("Price successfully sent to Kafka.")
    except Exception as e:
        logger.error(f"Failed to send price to Kafka: {e}")
