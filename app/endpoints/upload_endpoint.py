from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.db.connection import get_supabase_admin
from app.models.upload_model import UploadResponse
from app.query.upload_query import UploadQuery
from supabase import Client

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/upload-image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    db_admin: Client = Depends(get_supabase_admin)
):
    # 1. Validate File Type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only images (JPEG, PNG, GIF, WEBP) are allowed."
        )
    
    # 2. Validate File Size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5MB limit."
        )
    
    query = UploadQuery(db_admin)
    public_url = await query.upload_file(content, file.filename, file.content_type)
    
    if not public_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image to Supabase"
        )
        
    return {"image_url": public_url}
