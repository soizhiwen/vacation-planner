from fastapi import FastAPI

from api.routers import plans

app = FastAPI()
app.include_router(plans.router)
