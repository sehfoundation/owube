from fastapi import FastAPI
from db import database, Base
from users import engine, get_auth_router, get_register_router, get_users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpenWebUI API with Auth",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None
)

# CORS налаштування
origins = [
    "https://open-webui-production-5be5.up.railway.app",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup / Shutdown
@app.on_event("startup")
async def on_startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

# Роутери аутентифікації/реєстрації/користувачів
app.include_router(get_auth_router, prefix="/api/auth/jwt", tags=["auth"])
app.include_router(get_register_router, prefix="/api/auth", tags=["auth"])
app.include_router(get_users_router, prefix="/api/users", tags=["users"])

# Кореневий ендпоінт
@app.get("/api/")
async def api_root():
    return {"message": "Welcome to the OpenWebUI API with Auth!"}
