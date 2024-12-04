from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(title="Library Management System")
app.include_router(api_router, prefix="/api/v1")