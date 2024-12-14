import logging
from decimal import Decimal

import requests
import web3
from sqlalchemy.ext.asyncio import AsyncSession
from web3 import Web3
from web3.exceptions import ContractLogicError, TimeExhausted, BadFunctionCallOutput

from blockchain_interaction.kafka_producer import send_notification
from blockchain_interaction.model import TransactionHistory
from blockchain_interaction.repository import TransactionRepository
from blockchain_interaction.transaction_type import TransactionType
from config import Config
from errors import BlockchainException, InsufficientFundsException, UnauthorizedException

# Set up logging for debugging purposes
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BlockchainService:
    def __init__(self, transaction_repo: TransactionRepository):
        """
        Initializes the BlockchainService with web3 provider and contract instance.
        """
        self.web3 = Web3(Web3.HTTPProvider(Config.INFURA_URL))
        contract_address = Web3.to_checksum_address(Config.CONTRACT_ADDRESS)
        self.contract = self.web3.eth.contract(address=contract_address, abi=Config.CONTRACT_ABI)
        self.transaction_repo = transaction_repo
        self.private_key = Config.PRIVATE_KEY

    def _get_account_from_private_key(self):
        """
        Returns the account address derived from the private key.
        """
        account = self.web3.eth.account.privateKeyToAccount(self.private_key)
        return account

    def is_owner(self, account: str):
        """
        Checks if the account is the owner of the contract.
        """
        owner_address = self.contract.functions.owner().call()
        return owner_address.lower() == Web3.to_checksum_address(account).lower()

    def get_gold_price(self):
        """
        Fetches the current gold price from the smart contract.
        """
        try:
            print(self.web3.eth.block_number)
            # Correct way to access the public variable goldPrice
            gold_price = self.contract.functions.getTokenPrice().call()
            # Convert to Ether if needed
            gold_price_in_ether = self.web3.from_wei(gold_price, 'ether')
            logger.info(f"Gold price fetched: {gold_price_in_ether}")
            return gold_price_in_ether
        except BadFunctionCallOutput as e:
            logger.error(f"Error calling goldPrice function: {e}")
            raise BlockchainException(detail="Failed to retrieve gold price.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise BlockchainException(detail="An unexpected error occurred while fetching the gold price.")

    async def buy_tokens(self, account: str, value: float, db: AsyncSession):
        """
        Allows the user to buy tokens by sending ETH.
        """
        try:
            logger.info(f"Buying tokens for account: {account} with value: {value}")

            # Convert value to Wei (since ETH is a floating-point number, Web3 works with Wei)
            value_in_wei = Web3.to_wei(value, 'ether')

            act = web3.Web3.to_checksum_address(account)
            print(act)
            # Check if the buyer has enough ETH
            balance_in_wei = self.web3.eth.get_balance(act)  # This is synchronous; no need for await
            print(balance_in_wei)
            if balance_in_wei < value_in_wei:
                raise InsufficientFundsException(detail="You do not have enough ETH to complete this transaction.")

            # Estimate gas price and gas limit
            gas_price = self.web3.eth.gas_price  # Current gas price in Wei
            gas_estimate = self.contract.functions.buyToken().estimate_gas({'from': account, 'value': value_in_wei})

            # Calculate gas fee
            estimated_gas_cost = gas_estimate * gas_price
            logger.info(f"Estimated gas cost: {estimated_gas_cost} Wei")

            # Get current nonce for transaction ordering
            nonce = self.web3.eth.get_transaction_count(act)

            # Build transaction data
            tx = {
                'from': account,
                'to': self.contract.address,
                'data': self.contract.functions.buyToken().build_transaction({'from': account, 'value': value_in_wei})['data'],
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': nonce,
                'value': value_in_wei
            }

            # Sign the transaction using the private key
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)

            # Send the signed transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for transaction receipt (confirmation)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # 2-minute timeout
            if receipt.get("status") != 1:
                raise BlockchainException(detail="Transaction failed. Please try again.")

            # Record transaction in DB
            transaction = TransactionHistory(user_id=account, amount=value, tx_type=TransactionType.BUY,
                                             tx_hash=tx_hash.hex())
            await self.transaction_repo.add_transaction(transaction, db)

            logger.info(f"Tokens purchased successfully. Transaction hash: {tx_hash.hex()}")

            kafka_message = {
                "user_id": account,
                "transaction_id": tx_hash.hex(),
                "transaction_status": "success",
                "transaction_type": TransactionType.BUY,
                "transaction_amount": value,
                "notification_message": f"Your purchase of {value} ETH was successful.",
            }
            await send_notification(kafka_message)
            return tx_hash.hex()

        except InsufficientFundsException as e:
            logger.error(f"Insufficient funds: {e}")
            failure_message = {
                "user_id": account,
                "transaction_id": None,
                "transaction_status": "failure",
                "transaction_amount": value,
                "notification_message": f"Transaction failed: {e}",
            }
            await send_notification(failure_message)
            raise e
        except (ContractLogicError, TimeExhausted) as e:
            logger.error(f"Blockchain transaction failed: {e}")
            failure_message = {
                "user_id": account,
                "transaction_id": None,
                "transaction_status": "failure",
                "transaction_amount": value,
                "notification_message": f"Transaction failed: {e}",
            }
            await send_notification(failure_message)
            raise BlockchainException(detail=f"Failed to buy tokens: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during buy tokens: {e}")
            failure_message = {
                "user_id": account,
                "transaction_id": None,
                "transaction_status": "failure",
                "transaction_amount": value,
                "notification_message": f"Transaction failed: {e}",
            }
            await send_notification(failure_message)
            raise BlockchainException(detail="Failed to buy tokens due to an unexpected error.")

    async def sell_tokens(self, amount: float, account: str, db: AsyncSession):
        """
        Allows the user to sell tokens and receive ETH.
        """
        try:
            logger.info(f"Selling {amount} tokens for account: {account}")

            # Estimate gas and gas price for selling tokens
            gas_price = self.web3.eth.gas_price
            gas_estimate = self.contract.functions.sellToken(amount).estimate_gas({'from': account})

            # Calculate gas fee
            estimated_gas_cost = gas_estimate * gas_price
            logger.info(f"Estimated gas cost: {estimated_gas_cost} Wei")

            # Ensure the user has enough tokens to sell
            balance = await self.get_user_balance(account)
            if balance < amount:
                raise InsufficientFundsException(detail="Not enough tokens to sell.")

            # Get current nonce for transaction
            nonce = self.web3.eth.get_transaction_count(Web3.to_checksum_address(account))

            # Create transaction data
            tx = {
                'from': account,
                'to': self.contract.address,
                'data': self.contract.functions.sellToken(amount).build_transaction({'from': account})['data'],
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': nonce
            }
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)

            # Send the signed transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for the transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # 2-minute timeout

            # Send transaction
            #tx_hash = self.web3.eth.send_transaction(tx)

            # Wait for receipt with a timeout
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # 2-minute timeout
            if receipt.get("status") != 1:
                raise BlockchainException(detail="Transaction failed. Please try again.")

            # Record transaction in DB
            transaction = TransactionHistory(user_id=account, amount=amount, tx_type=TransactionType.SELL,
                                             tx_hash=tx_hash.hex())
            await self.transaction_repo.add_transaction(transaction, db)

            logger.info(f"Tokens sold successfully. Transaction hash: {tx_hash.hex()}")

            kafka_message = {
                "user_id": account,
                "transaction_id": tx_hash.hex(),
                "transaction_status": "success",
                "transaction_type": TransactionType.SELL,
                "transaction_amount": amount,
                "notification_message": f"Your Selling of {amount} ETH was successful.",
            }
            await send_notification(kafka_message)

            return tx_hash.hex()

        except (ContractLogicError, TimeExhausted) as e:
            logger.error(f"Blockchain transaction failed: {e}")
            failure_message = {
                "user_id": account,
                "transaction_id": None,
                "transaction_status": "failure",
                "transaction_amount": amount,
                "notification_message": f"Transaction failed: {e}",
            }
            await send_notification(failure_message)
            raise BlockchainException(detail=f"Failed to sell tokens: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during sell tokens: {e}")
            failure_message = {
                "user_id": account,
                "transaction_id": None,
                "transaction_status": "failure",
                "transaction_amount": amount,
                "notification_message": f"Transaction failed: {e}",
            }
            await send_notification(failure_message)
            raise BlockchainException(detail="Failed to sell tokens due to an unexpected error.")

    async def update_gold_price(self, new_price: float, account: str):
        """
        Updates the gold price in the smart contract. Only callable by the owner.
        """
        try:
            logger.info(f"Updating gold price to {new_price} by account: {account}")

            # Fetch ETH/USD price (example from an API like CoinGecko)
            eth_to_usd = await self.get_eth_to_usd_price()
            new_price_in_eth = Decimal(new_price) / Decimal(eth_to_usd)
            new_price_in_wei = int(new_price_in_eth * (10 ** 18))  # Convert to Wei

            logger.info(
                f"Gold price in USD: {new_price}, Gold price in ETH: {new_price_in_eth}, Gold price in Wei: {new_price_in_wei}")

            # Ensure the account is authorized (could be the contract owner, for example)
            if not self.is_owner(account):
                raise UnauthorizedException(detail="Only the contract owner can update the gold price.")

            # Estimate gas for the update
            gas_price = self.web3.eth.gas_price
            gas_estimate = self.contract.functions.updateGoldPrice(new_price_in_wei).estimate_gas({'from': account})

            # Create and send the transaction
            tx = self.contract.functions.updateGoldPrice(new_price_in_wei).build_transaction({
                'from': account,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': self.web3.eth.get_transaction_count(Web3.to_checksum_address(account)),
            })

            # Sign the transaction with the private key
            private_key = Config.PRIVATE_KEY  # Replace with the private key of the account
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)

            # Send the signed transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for the transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # 2-minute timeout
            if receipt.get("status") != 1:
                raise BlockchainException(detail="Failed to update gold price.")

            logger.info(f"Gold price updated successfully. Transaction hash: {tx_hash.hex()}")
            return tx_hash.hex()

        except (ContractLogicError, TimeExhausted) as e:
            logger.error(f"Blockchain transaction failed: {e}")
            if "revert" in str(e):
                raise UnauthorizedException(detail="Only the contract owner can update the gold price.")
            raise BlockchainException(detail=f"Failed to update gold price: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during gold price update: {e}")
            raise BlockchainException(detail="Failed to update gold price due to an unexpected error.")

    async def get_eth_to_usd_price(self):
        """
        Fetches the current ETH/USD price from an API or oracle.
        """
        # Example: Fetch ETH/USD price from a public API (could be a Chainlink oracle in a real case)
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        data = response.json()
        eth_to_usd = data['ethereum']['usd']
        logger.info(f"ETH/USD price fetched: {eth_to_usd}")
        return eth_to_usd

    async def get_transaction_history(self, user_id: str, db: AsyncSession):
        """
        Retrieves the transaction history of a user from the database.
        """
        try:
            transaction_history = await self.transaction_repo.get_transaction_history(user_id, db)
            logger.info(f"Transaction history fetched for user {user_id}.")
            return transaction_history
        except Exception as e:
            logger.error(f"Error retrieving transaction history: {e}")
            raise BlockchainException(detail="Failed to retrieve transaction history.")

    async def get_user_balance(self, account: str):
        """
        Fetches the balance of the user for gGOLD tokens.
        """
        try:
            Web3.to_checksum_address(account)
            balance = self.contract.functions.balanceOf(account).call()
            logger.info(f"Balance for {account}: {balance}")
            return balance
        except Exception as e:
            logger.error(f"Error fetching balance for {account}: {e}")
            raise BlockchainException(detail="Failed to fetch user balance.")

    async def calculate_gas_fee(self, account: str, eth_amount: float, action: str):
        """
        Estimate gas cost for either the buy or sell transaction.

        :param account: The user's Ethereum address.
        :param eth_amount: The amount of ETH to be used for the buy or sell.
        :param action: Either 'buy' or 'sell' to determine the transaction type.
        :return: Gas cost in ETH for the selected action.
        """
        try:
            # Get the current gas price (in Wei)
            gas_price = self.web3.eth.gas_price  # This is the current gas price in Wei

            # Convert the ETH amount to Wei
            eth_amount_in_wei = self.web3.to_wei(eth_amount, 'ether')  # Convert ETH to Wei

            # Estimate gas cost based on the action (either 'buy' or 'sell')
            if action == 'buy':
                # Estimate gas for the buyToken transaction
                gas_estimate = self.contract.functions.buyToken().estimate_gas(
                    {'from': account, 'value': eth_amount_in_wei})  # Pass the ETH in Wei for 'buy'
            elif action == 'sell':
                # Estimate gas for the sellToken transaction (ensure the amount is correct)
                gas_estimate = self.contract.functions.sellToken(eth_amount_in_wei).estimate_gas({'from': account})
            else:
                raise ValueError("Invalid action. Must be 'buy' or 'sell'.")

            # Calculate the gas cost in Wei (gas_estimate is in gas units, gas_price in Wei)
            gas_cost_in_wei = gas_estimate * gas_price

            # Convert the gas cost to ETH (since gas_cost_in_wei is in Wei)
            gas_cost_in_eth = self.web3.from_wei(gas_cost_in_wei, 'ether')

            return gas_cost_in_eth

        except Exception as e:
            logger.error(f"Error calculating gas fee: {e}")
            raise BlockchainException(detail="Failed to calculate gas fee.")

