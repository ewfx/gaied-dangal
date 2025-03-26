import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from EmailClassification  import process_emails# Keep this as a single entry point

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

class RequestModel(BaseModel):
    model: str  # Specify the model
    folder_path: str

@app.post("/process-emails")
def process_emails_api(request: RequestModel):
    """API endpoint to process emails using the specified model."""
    results = process_emails(request.folder_path, request.model)
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
