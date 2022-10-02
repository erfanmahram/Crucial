from core import settings
import uvicorn
from app import create_app

application = create_app()

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run("main:application", host=settings.HOST_URL, port=settings.HOST_PORT, reload=False, workers=4)
