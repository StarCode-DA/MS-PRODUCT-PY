from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.products import router as products_router

app = FastAPI(title="MS PRODUCTS")

# Orígenes permitidos (tu frontend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],      # dominios que pueden hacer requests
    allow_credentials=True,     # cookies y credenciales
    allow_methods=["*"],        # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # headers permitidos
)

# Routers
app.include_router(products_router)
