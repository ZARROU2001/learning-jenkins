from aiokafka import AIOKafkaConsumer
import json
from logger import logger
from providers.sse_provider import SSEProvider


class TransactionConsumer:
    def __init__(self, kafka_broker: str, kafka_topic: str):
        self.kafka_broker = kafka_broker
        self.kafka_topic = kafka_topic
        self.consumer = AIOKafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_broker,
            group_id="transaction-group"
        )
        self.sse_manager = SSEProvider()

    async def start(self):
        """
        Start consuming Kafka messages for transaction notifications.
        """
        await self.consumer.start()
        try:
            print("tets")
            async for msg in self.consumer:
                event = json.loads(msg.value.decode())
                await self.process_transaction_notification(event)
        except Exception as e:
            logger.error(f"Error consuming Kafka message: {e}")
        finally:
            await self.consumer.stop()

    async def process_transaction_notification(self, event: dict):
        """
        Process transaction notifications and handle success/failure accordingly.
        """
        user_id = event['user_id']
        transaction_status = event['transaction_status']
        notification_message = event['notification_message']
        transaction_id = event.get('transaction_id', None)

        try:
            if transaction_status == "success":
                # Handle success notification
                logger.info(
                    f"Transaction successful for user {user_id}, tx_id: {transaction_id}. Message: {notification_message}")
                # You can send a notification to the frontend via SSE or other channels here
                await self.send_sse_notification(user_id, notification_message, "success")

            elif transaction_status == "failure":
                # Handle failure notification
                logger.error(f"Transaction failed for user {user_id}. Message: {notification_message}")
                # Send failure notification to the frontend
                await self.send_sse_notification(user_id, notification_message, "failure")

            else:
                logger.warning(f"Unknown transaction status: {transaction_status} for user {user_id}")
        except Exception as e:
            logger.error(f"Error processing Kafka message for user {user_id}: {e}")

    async def send_sse_notification(self, user_id: str, message: str, status: str):
        """
        Send notification to the frontend (could be via SSE, WebSocket, etc.)
        """
        try:
            # Here you would integrate with your frontend notification system (e.g., SSE, WebSocket)
            logger.info(f"Sending {status} notification to user {user_id}: {message}")
            # Assuming you have a method like `SSEManager.send_message` for this
            await self.sse_manager.send_to_client(client_id=user_id, message=message)
        except Exception as e:
            logger.error(f"Error sending SSE notification to user {user_id}: {e}")
