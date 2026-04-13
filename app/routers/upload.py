from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.core.supabase_client import get_supabase_admin
from supabase import Client
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/upload-image")
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
    
    # Reset file pointer if needed, but we already have 'content' for upload
    
    # 3. Generate Unique Filename to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = f"images/{unique_filename}"
    
    # 4. Upload to Supabase Storage
    try:
        bucket_name = "petshop-images"
        
        # Upload context
        # supabase-py storage upload accepts bytes
        res = db_admin.storage.from_(bucket_name).upload(
            path=file_path,
            file=content,
            file_options={"content-type": file.content_type}
        )
        
        # 5. Generate Public URL
        # get_public_url returns the direct access URL
        public_url = db_admin.storage.from_(bucket_name).get_public_url(file_path)
        
        return {"image_url": public_url}
        
    except Exception as e:
        # Log error if possible
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image to Supabase: {str(e)}"
        )
    finally:
        await file.close()
