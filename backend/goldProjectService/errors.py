class APIError(Exception):
    """Custom exception for API-related errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
