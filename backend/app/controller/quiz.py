import os
import uuid
from fastapi import UploadFile, HTTPException, status
from app.util.embedding.insert_pdf_to_vector_db import insert_pdf_to_vector_db
from app.util.embedding.search_from_vector_db import search_from_vector_db
from app.util.embedding.extract_pdf_data import extract_pdf_data
from sqlalchemy.orm import Session
from app.model.uploaded_sheet import UploadedSheet
from app.config.setting import settings
from app.util.ai_helper.generate_exams import generate_exams
from functools import reduce

async def generate_quiz(query: str, questions_length: int, url: str, file: UploadFile, db: Session):
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

    if file:
        pdf_bytes = await file.read()
        file_name = f'file_{uuid.uuid1().hex}{os.path.splitext(file.filename)[1]}'
        file_path = os.path.join(settings.UPLOADS_DIR, file_name)

        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)
            uploaded_sheet = UploadedSheet(
                file_path=file_path
            )
            db.add(uploaded_sheet)
            db.commit()
            db.refresh(uploaded_sheet)
    
    elif url:
        if not os.path.exists(url):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='File not found'
            )
        else:
            with open(url, 'rb') as file:
                pdf_bytes = file.read()
                file_path = url

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not specified'
        )

    extracted_payloads = extract_pdf_data(pdf_bytes)
    results = search_text(extracted_payloads, query or '')

    context = list(set([x['text'] for x in results]))

    if len(context) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Your query is not matched'
        )

    generated_exams = generate_exams(context[:25], questions_length)

    image_paths = [x['images'] for x in results]
    unique_image_list = list(reduce(lambda acc, sublist: acc.union(set(sublist)), image_paths, set()))

    return {
        'generated_exams': generated_exams,
        'images': unique_image_list,
        'file_path': file_path
    }

def search_text(data: list, query: str):
    texts = []
    for item1 in data:
        for item2 in item1['texts']:
            splitted_queries = query.split(' ')
            for splitted_query in splitted_queries:
                if splitted_query.strip() in item2:
                    texts.append({
                        'text': item2,
                        'images': item1['images']
                    })
    return texts