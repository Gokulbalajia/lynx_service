from pydantic import BaseModel

class UploadResponse(BaseModel):
    image_url: str
