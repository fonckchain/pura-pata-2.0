from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
import uuid
from pathlib import Path

from ...core.config import settings
from ...models.user import User
from ...services.storage import storage_service
from .auth import get_current_user

router = APIRouter()


ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
ALLOWED_DOCUMENT_EXTENSIONS = {'.pdf'}


def validate_file_size(file: UploadFile, max_size: int):
    """Validate file size"""
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()  # Get position (file size)
    file.file.seek(0)  # Reset to beginning

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size / (1024 * 1024)}MB"
        )


def validate_image_file(file: UploadFile):
    """Validate image file type and size"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )

    # Check content type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid content type. Must be an image."
        )

    # Check file size
    validate_file_size(file, settings.MAX_UPLOAD_SIZE)


def validate_pdf_file(file: UploadFile):
    """Validate PDF file type and size"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Must be PDF."
        )

    # Check content type
    if file.content_type != 'application/pdf':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content type. Must be a PDF document."
        )

    # Check file size (10MB for PDFs)
    validate_file_size(file, 10 * 1024 * 1024)


@router.post("/photo", response_model=dict)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload a dog photo"""
    validate_image_file(file)

    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"

    # Read file content
    file_content = await file.read()

    # Upload to Supabase Storage
    file_url = await storage_service.upload_file(
        file_content=file_content,
        file_name=unique_filename,
        content_type=file.content_type,
        folder="dogs/photos"
    )

    if not file_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file"
        )

    return {
        "url": file_url,
        "filename": unique_filename
    }


@router.post("/photos", response_model=dict)
async def upload_multiple_photos(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload multiple dog photos (max 5)"""
    if len(files) > settings.MAX_PHOTOS_PER_DOG:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {settings.MAX_PHOTOS_PER_DOG} photos allowed"
        )

    uploaded_urls = []

    for file in files:
        validate_image_file(file)

        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"

        # Read file content
        file_content = await file.read()

        # Upload to Supabase Storage
        file_url = await storage_service.upload_file(
            file_content=file_content,
            file_name=unique_filename,
            content_type=file.content_type,
            folder="dogs/photos"
        )

        if file_url:
            uploaded_urls.append(file_url)

    if len(uploaded_urls) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload files"
        )

    return {
        "urls": uploaded_urls,
        "count": len(uploaded_urls)
    }


@router.post("/certificate", response_model=dict)
async def upload_certificate(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload veterinary certificate (PDF)"""
    validate_pdf_file(file)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.pdf"

    # Read file content
    file_content = await file.read()

    # Upload to Supabase Storage
    file_url = await storage_service.upload_file(
        file_content=file_content,
        file_name=unique_filename,
        content_type=file.content_type,
        folder="dogs/certificates"
    )

    if not file_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload certificate"
        )

    return {
        "url": file_url,
        "filename": unique_filename
    }


@router.delete("/file")
async def delete_file(
    file_url: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a file from storage"""
    success = await storage_service.delete_file(file_url)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )

    return {"message": "File deleted successfully"}
