import asyncio
from fastapi import FastAPI, APIRouter
from typing import Optional, Dict, Any
import packages.recieve_spec_package.deref_clean as deref_clean


class OpenAPIHandlerAPI:
    def __init__(self):
        self._spec_queue: asyncio.Queue = asyncio.Queue()
        self.app = FastAPI()
        self._setup_routes()

    def _setup_routes(self):
        router = APIRouter()

        @router.put("/")
        async def put_update(spec: Dict[str, Any]):
            if not spec:
                return {"message": "Spec is empty"}

            cleaned_spec = deref_clean.clean_dereference(spec)

            await self._spec_queue.put(cleaned_spec)
            return {"message": "Spec received and stored"}

        self.app.include_router(router)

    async def wait_for_spec(self) -> Dict[str, Any]:
        """Asynchronously waits for the next incoming OpenAPI spec."""
        return await self._spec_queue.get()
