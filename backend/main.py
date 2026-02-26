from fastapi import FastAPI
from backend.app.database.connection import Base, engine
from backend.app.routes import user_route, product_route, order_route
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Mini E-Commerce Order Processing System",
    version="1.0.0",
    description="Backend API for Mini E-Commerce Application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


@app.get("/", tags=["Home"], summary="Home")
def home():
    return {"message": "Mini E-Commerce Order processing running."}


app.include_router(user_route.router)
app.include_router(product_route.router)
app.include_router(order_route.router)
