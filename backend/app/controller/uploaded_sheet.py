import os
from fastapi import HTTPException, status
from app.util.embedding.insert_pdf_to_vector_db import insert_pdf_to_vector_db
from app.util.embedding.extract_pdf_data import extract_pdf_data
from app.schema.exam import ExamInsert
from app.config.setting import settings

def get_all_uploaded_sheet():
    files_in_dir = os.listdir(settings.UPLOADS_DIR)
    dir_files = [os.path.join(settings.UPLOADS_DIR, f) for f in files_in_dir if os.path.isfile(os.path.join(settings.UPLOADS_DIR, f))]
    return dir_files

def insert_exam_from_sheet(url: str, req: ExamInsert):
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

def force_delete_uploaded_sheet(url: str):
    if os.path.exists(url):
        os.remove(url)
    return f'Delete the file with path {url}'