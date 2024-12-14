from fastapi import HTTPException, status


# Base class for custom HTTP exceptions
class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


# Specific error for database-related issues
class DatabaseException(CustomHTTPException):
    def __init__(self, detail: str = "A database error occurred. Please try again later."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# Specific error for blockchain-related issues (e.g., contract transactions, state issues)
class BlockchainException(CustomHTTPException):
    def __init__(self, detail: str = "Blockchain transaction failed. Please try again later."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# Specific error for unauthorized access (e.g., owner-only functions)
class UnauthorizedException(CustomHTTPException):
    def __init__(self, detail: str = "You are not authorized to perform this action."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


# Specific error when a resource is not found (e.g., contract, data)
class NotFoundException(CustomHTTPException):
    def __init__(self, detail: str = "The requested resource was not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


# Specific error for validation failures (e.g., bad input or parameter validation)
class ValidationException(CustomHTTPException):
    def __init__(self, detail: str = "Invalid input. Please check your data and try again."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


# Specific error for conflicts (e.g., resource already exists)
class ConflictException(CustomHTTPException):
    def __init__(self, detail: str = "The request could not be completed due to a conflict."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


# Specific exception for insufficient funds or gas errors when interacting with the blockchain
class InsufficientFundsException(BlockchainException):
    def __init__(self, detail: str = "Insufficient funds to complete the transaction."):
        super().__init__( detail=detail)


# Specific exception for "out of gas" errors when calling smart contract functions
class OutOfGasException(BlockchainException):
    def __init__(self, detail: str = "Transaction failed due to insufficient gas. Please try again with more gas."):
        super().__init__( detail=detail)


# Specific exception for invalid Ethereum addresses
class InvalidAddressException(BlockchainException):
    def __init__(self, detail: str = "The provided Ethereum address is invalid. Please check the address format."):
        super().__init__( detail=detail)


# Specific exception for contract not being found or deployed
class ContractNotFoundException(BlockchainException):
    def __init__(self, detail: str = "Contract not found at the specified address."):
        super().__init__( detail=detail)


# Specific exception for contract logic errors or transaction reverts
class ContractLogicException(BlockchainException):
    def __init__(self, detail: str = "Contract logic failure. Transaction reverted."):
        super().__init__( detail=detail)


# Specific exception for network issues, such as connection errors or timeouts
class NetworkException(CustomHTTPException):
    def __init__(self, detail: str = "Network error occurred. Please check your connection and try again."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


# Example for a generic internal server error (could be for unexpected issues)
class InternalServerErrorException(CustomHTTPException):
    def __init__(self, detail: str = "An unexpected error occurred. Please try again later."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
