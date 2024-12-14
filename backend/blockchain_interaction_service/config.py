import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./transactions.db")
    INFURA_URL = os.getenv("INFURA_URL")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    KAFKA_TRANSACTION_TOPIC = os.getenv("KAFKA_TRANSACTION_TOPIC")
    OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")
    ETH_NODE_URL =os.getenv("ETH_NODE_URL")
    with open("./contract/gGOLDToken.json", "r") as abi_file:
        CONTRACT_ABI = json.load(abi_file)["abi"]

    @staticmethod
    def is_configured():
        return all([Config.INFURA_URL, Config.PRIVATE_KEY, Config.CONTRACT_ADDRESS])