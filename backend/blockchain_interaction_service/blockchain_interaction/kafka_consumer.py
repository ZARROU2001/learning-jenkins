from aiokafka import AIOKafkaConsumer
from config import Config
KAFKA_TOPIC = Config.KAFKA_TOPIC  # Replace with your Kafka topic
KAFKA_BROKER_URL = Config.KAFKA_BOOTSTRAP_SERVERS # Replace with your Kafka broker URL

async def consume_gold_price(on_price_received):
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="gold-price-consumer-group",
    )

    await consumer.start()
    try:
        async for message in consumer:
            price = message.value.decode("utf-8")
            print(f"Received gold price: {price}")
            await on_price_received(price)  # Call the provided callback function
    finally:
        await consumer.stop()
