from supabase import create_client, Client
from ..core.config import settings
from typing import Optional
import os


class StorageService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_STORAGE_BUCKET

    async def upload_file(
        self,
        file_content: bytes,
        file_name: str,
        content_type: str,
        folder: str = "dogs"
    ) -> Optional[str]:
        """Upload a file to Supabase Storage"""
        try:
            file_path = f"{folder}/{file_name}"

            result = self.supabase.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}
            )

            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket).get_public_url(file_path)
            return public_url

        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    async def delete_file(self, file_url: str) -> bool:
        """Delete a file from Supabase Storage"""
        try:
            # Extract path from URL
            file_path = file_url.split(f"{self.bucket}/")[-1]

            self.supabase.storage.from_(self.bucket).remove([file_path])
            return True

        except Exception as e:
            print(f"Error deleting file: {e}")
            return False


storage_service = StorageService()
