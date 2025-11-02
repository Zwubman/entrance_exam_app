import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.uploaded_sheet import UploadedSheet
from app.util.embedding.insert_pdf_to_vector_db import insert_pdf_to_vector_db
from app.util.embedding.extract_pdf_data import extract_pdf_data
from app.schema.exam import ExamInsert
from app.config.setting import settings

def get_all_uploaded_sheet(limit: int, page: int, src: str | None, db: Session):
    limit = 1 if limit < 1 else limit
    page = 1 if page < 1 else page
    offset = (page - 1) * limit
    total = db.query(UploadedSheet).count()
    src = src.lower() if src else None

    uploaded_sheets = db.query(UploadedSheet).limit(limit).offset(offset).all()
    db_files = [x.file_path for x in uploaded_sheets]

    files_in_dir = os.listdir(settings.UPLOADS_DIR)
    dir_files = [os.path.join(settings.UPLOADS_DIR, f) for f in files_in_dir if os.path.isfile(os.path.join(settings.UPLOADS_DIR, f))]

    if src == 'db' or src == 'database':
        return {
        'files': db_files,
        'page': page,
        'limit': limit,
        'total': total,
        'source': src or 'all'
    }

    if src == 'file' or src == 'dir':
        return {
        'files': dir_files,
        'page': page,
        'limit': limit,
        'total': total,
        'source': src or 'all'
    }

    file_paths = set(db_files + dir_files)
    return {
        'files': file_paths,
        'page': page,
        'limit': limit,
        'total': total,
        'source': src or 'all'
    }

def get_uploaded_sheet(file_path: str, db: Session):
    file = db.query(UploadedSheet).filter(UploadedSheet.file_path == file_path).first()
    return {
        'file': file
    }

def insert_exam_from_sheet(url: str, req: ExamInsert):
    print(os.path.exists(url))
    if not os.path.exists(url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found'
        )

    with open(url, 'rb') as file:
        pdf_bytes = file.read()
    extracted_payloads = extract_pdf_data(pdf_bytes)
    summary = insert_pdf_to_vector_db(extracted_payloads, req)

    return summary

def delete_uploaded_sheet(file_path: str, db: Session):
    file = db.query(UploadedSheet).filter((UploadedSheet.file_path == file_path) & (UploadedSheet.is_deleted == False)).first()
    if not file:
        return 'This file are not stored in database'
    
    file.soft_delete()
    db.commit()
    return f'Soft delete the file with path {file_path}'

def force_delete_uploaded_sheet(file_path: str, db: Session):
    delete_uploaded_sheet(file_path, db)
    if os.path.exists(file_path):
        os.remove(file_path)
    return f'Force delete the file with path {file_path}'