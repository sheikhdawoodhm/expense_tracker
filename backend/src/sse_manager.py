import asyncio

class SSEManager:
    def __init__(self):
        self.listeners = {}

    async def event_generator(self, user_id: int):
        if user_id not in self.listeners:
            self.listeners[user_id] = []
            
        queue = asyncio.Queue()
        self.listeners[user_id].append(queue)
        
        try:
            while True:
                data = await queue.get()
                yield f"data: {data}\n\n"
        except asyncio.CancelledError:
            self.listeners[user_id].remove(queue)
            if not self.listeners[user_id]:
                del self.listeners[user_id]

    async def notify(self, user_id: int, message: str):
        if user_id in self.listeners:
            for queue in self.listeners[user_id]:
                await queue.put(message)

sse_manager = SSEManager()
