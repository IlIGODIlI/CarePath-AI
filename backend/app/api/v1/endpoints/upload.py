from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database.connections import get_db
from app.services import upload_service
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/image")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save temp and upload
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    result = upload_service.handle_upload(db, temp_path, "default_user", "image")
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return result

@router.post("/report")
async def upload_report(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    result = upload_service.handle_upload(db, temp_path, "default_user", "report")
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return result

@router.post("/prescription")
async def upload_prescription(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    result = upload_service.handle_upload(db, temp_path, "default_user", "prescription")
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return result
