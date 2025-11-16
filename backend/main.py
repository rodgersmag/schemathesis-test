from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

from endpoints import users


app = FastAPI(
    title=os.getenv("NAME"),
    description=os.getenv("DESCRIPTION"),
    version=os.getenv("FASTAPI_VERSION")
)

# Include routers
app.include_router(users.router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for Docker and load balancers"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"}
    )

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)