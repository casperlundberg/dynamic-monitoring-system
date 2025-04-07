import jsonref
from fastapi import FastAPI, APIRouter
from typing import Optional, Dict, Any


class OpenAPIHandlerAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = APIRouter()
        self._spec: Optional[
            Dict[str, Any]] = None  # Store the dereferenced spec
        self.setup_routes()

    def setup_routes(self):
        @self.router.put("/")
        async def put_update(spec: Dict[str, Any]):
            # deref_spec = jsonref.JsonRef.replace_refs(spec)
            deref_spec = spec

            if deref_spec is None:
                return {"message": "Spec is empty"}

            self._spec = deref_spec
            return {"message": "Spec received and stored"}

        self.include_router(self.router)

    def get_spec(self) -> Optional[Dict[str, Any]]:
        """Returns the most recently stored OpenAPI spec (dereferenced)."""
        return self._spec
