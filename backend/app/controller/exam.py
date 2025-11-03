import os
import uuid
from fastapi import Depends, UploadFile, HTTPException, status
from app.config.database import get_db
from app.util.embedding.insert_pdf_to_vector_db import insert_pdf_to_vector_db
from app.util.embedding.search_from_vector_db import search_from_vector_db
from app.util.embedding.extract_pdf_data import extract_pdf_data
from sqlalchemy.orm import Session
from app.model.uploaded_sheet import UploadedSheet
from app.util.embedding import qdrant, COLLECTION_NAME
from app.config.setting import settings
from app.schema.exam import ExamInsert, ExamSearch, ExamSubmit, ExamChat
from app.util.ai_helper.generate_exams import generate_exams
from app.util.ai_helper.evaluate_exam_answer import evaluate_exam_answer
from app.controller import chat
from app.router.chat import get_profile
from app.schema.chat import ChatCreate
from functools import reduce

async def insert_new_exam(year: str, subject: str, extra_data: str, file: UploadFile, db: Session):
    req = ExamInsert(year=year, subject=subject, extra_data=extra_data)
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

    pdf_bytes = await file.read()
    # file_name = f'file_{uuid.uuid1().hex}{os.path.splitext(file.filename)[1]}'
    # file_path = os.path.join(settings.UPLOADS_DIR, file_name)

    # with open(file_path, 'wb') as f:
    #     f.write(pdf_bytes)
        # uploaded_sheet = UploadedSheet(
        #     file_path=file_path
        # )
        # db.add(uploaded_sheet)
        # db.commit()
        # db.refresh(uploaded_sheet)

    extracted_payloads = extract_pdf_data(pdf_bytes)
    summary = insert_pdf_to_vector_db(extracted_payloads, req)

    return summary

def get_all_exams(limit: int, next_page: str):
    scroll_result, next_page_offset = qdrant.scroll(
        collection_name=COLLECTION_NAME,
        limit=limit,
        offset=next_page or None,
        with_payload=True,
        with_vectors=False
    )
    return {
        'points': [{'id': x.id, 'payload': x.payload} for x in scroll_result],
        'next_page': next_page_offset
    }

def get_exam(exam_id: str):
    result = qdrant.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[exam_id],
        with_payload=True,
        with_vectors=False
    )

    if not result:    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Exam not found'
        )
    
    return {
        'id': result[0].id,
        'payload': result[0].payload
    }

def delete_exam(exam_id: str):
    result = qdrant.delete(
        collection_name=COLLECTION_NAME,
        points_selector=[exam_id]
    )

    if not result:    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Exam not found'
        )
    
    return f"delete the exam with ID {exam_id}"

def search_exam(req: ExamSearch):
    search_result = search_from_vector_db(req, 100)
    results = search_result['results']

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Exam not found'
        )
    
    context = list(set([x['payload']['text'] for x in results]))
    generated_exams = generate_exams(context, req.questions_length)

    image_paths = {'images': [x['payload']['images'] for x in results]}
    unique_image_list = list(reduce(lambda acc, sublist: acc.union(set(sublist)), image_paths["images"], set()))

    return {
        'generated_exams': generated_exams,
        'images': unique_image_list,
        'next_page': search_result['next_page']
    }

def submit_exam(req: ExamSubmit):
    result = evaluate_exam_answer(req.questions, req.answers)
    return result

def create_new_chat_from_exam(req: ExamChat, profile = Depends(get_profile), db = Depends(get_db)):
    initial_idea = ChatCreate(initial_idea=f"""
The Student is ask him the following questions:
<questions>
{req.questions}
</questions>

and He answer as follow:
<answers>
{req.answers}
</answers>

and teacher evaluation is:
<evaluation>
{req.evaluations}
</evaluation>
""")
    return chat.create_new_chat(initial_idea, profile, db)