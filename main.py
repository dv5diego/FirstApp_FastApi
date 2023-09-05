from fastapi import FastAPI
from routers import product, jwt_auth_user
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
app.title="Project with FastApi"
app.version="0.0.1"


origins=[
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200"
]

#CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Routers
app.include_router(product.router)
app.include_router(jwt_auth_user.router)