from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.base import Base
from routes import auth

app = FastAPI()

# Configure CORS
origins = [
    "http://192.168.254.11",  # Replace with your local IP address
    "http://192.168.254.11:8000",  # Replace with your local IP address and port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router
app.include_router(auth.router, prefix="/auth")

Base.metadata.create_all(bind=engine)

# Run the server on all network interfaces
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)