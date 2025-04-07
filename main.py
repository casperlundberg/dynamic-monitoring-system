import threading
import uvicorn
from fastapi import FastAPI
from api.routers.update import router
from UI_dashboard.core.ui import RootApp

api = FastAPI()
api.include_router(router, prefix="/update", tags=["update"])


@api.get("/")
async def root():
    return {"message": "Hello World"}


def run_fastapi():
    uvicorn.run(api, host="127.0.0.1", port=8000)


def run_tkinter():
    ui = RootApp()
    ui.mainloop()


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi)
    tkinter_thread = threading.Thread(target=run_tkinter)

    fastapi_thread.start()
    tkinter_thread.start()

    fastapi_thread.join()
    tkinter_thread.join()
