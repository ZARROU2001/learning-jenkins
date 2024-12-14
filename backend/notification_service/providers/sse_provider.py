import asyncio
from typing import Dict

from fastapi.responses import StreamingResponse

class SSEProvider:
    def __init__(self):
        # Dictionary to store client queues based on user_id
        self.clients: Dict[str, asyncio.Queue] = {}

    async def add_client(self, client_id: str) -> asyncio.Queue:
        """Register a new client with a unique client_id."""
        queue = asyncio.Queue()
        self.clients[client_id] = queue
        return queue

    async def remove_client(self, client_id: str):
        """Remove a client when they disconnect."""
        if client_id in self.clients:
            del self.clients[client_id]

    async def send_to_client(self, client_id: str, message: str):
        """Send a message to a specific client."""
        if client_id in self.clients:
            await self.clients[client_id].put(message)

    def stream(self, client_id: str):
        """Generate the SSE stream for a specific client."""

        async def event_stream():
            queue = await self.add_client(client_id)
            try:
                while True:
                    message = await queue.get()
                    yield f"data: {message}\n\n"
            finally:
                await self.remove_client(client_id)

        return StreamingResponse(event_stream(), media_type="text/event-stream")
