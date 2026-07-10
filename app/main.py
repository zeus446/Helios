from fastapi import FastAPI
from app.api.routes import auth, users, resume as resume_routes
from app.database import engine, Base
from app.models import user, resume as resume_models
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title = "HELIOS",version = "0.1.0" )




@app.on_event("startup")
async def startup():
    try:
        logger.info("Starting up...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(resume_routes.router)


@app.get("/")
def get_root():
    return {"message":"root initialized"}

