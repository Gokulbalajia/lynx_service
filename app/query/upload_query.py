from supabase import Client
from typing import Optional
import uuid

class UploadQuery:
    def __init__(self, client: Client):
        self.client = client

    async def upload_file(self, content: bytes, filename: str, content_type: str) -> Optional[str]:
        # Generate Unique Filename
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = f"images/{unique_filename}"
        bucket_name = "petshop-images"

        try:
            # Upload to Supabase Storage
            self.client.storage.from_(bucket_name).upload(
                path=file_path,
                file=content,
                file_options={"content-type": content_type}
            )
            
            # Generate Public URL
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_path)
            return public_url
        except Exception:
            return None
