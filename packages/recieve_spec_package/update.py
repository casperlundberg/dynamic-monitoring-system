import asyncio
from fastapi import FastAPI, APIRouter
from typing import Optional, Dict, Any


class OpenAPIHandlerAPI:
    def __init__(self):
        self._spec: Optional[Dict[str, Any]] = None
        self._spec_queue: asyncio.Queue = asyncio.Queue()
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        router = APIRouter()

        @router.put("/")
        async def put_update(spec: Dict[str, Any]):
            if not spec:
                return {"message": "Spec is empty"}

            self._spec = spec
            await self._spec_queue.put(spec)
            return {"message": "Spec received and stored"}

        self.app.include_router(router)

    def get_spec(self) -> Optional[Dict[str, Any]]:
        """Returns the most recently stored OpenAPI spec (dereferenced)."""
        return self._spec

    async def wait_for_spec(self) -> Dict[str, Any]:
        """Asynchronously waits for the next incoming OpenAPI spec."""
        return await self._spec_queue.get()
