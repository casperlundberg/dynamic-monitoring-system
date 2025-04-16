import asyncio

import uvicorn

import deifinitions
from monitoring_server.SQL_generator.SQL_generator import generate_sql
from packages.recieve_spec_package.update import OpenAPIHandlerAPI

if __name__ == "__main__":
    openapi_handler = OpenAPIHandlerAPI()


    async def consume_spec():
        while True:
            spec = await openapi_handler.wait_for_spec()
            generate_sql(spec)


    asyncio.create_task(consume_spec())
    uvicorn.run(openapi_handler.app, host="0.0.0.0",
                port=deifinitions.SERVER_UPDATE_ENDPOINT_PORT)
