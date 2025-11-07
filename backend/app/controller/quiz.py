import os
import uuid
import numpy as np
from fastapi import UploadFile, HTTPException, status
from app.util.embedding.extract_file_data import extract_file_data
from sqlalchemy.orm import Session
from app.config.setting import settings
from app.util.ai_helper.generate_exams import generate_exams
from functools import reduce
from app.config.embedding import TEXT_EMBEDDING_MODEL, PointStruct

async def generate_quiz(query: str, questions_length: int, url: str, file: UploadFile, db: Session):
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

    file_extension = None
    if file:
        file_bytes = await file.read()
        file_name = f'file_{uuid.uuid1().hex}{os.path.splitext(file.filename)[1]}'
        file_path = os.path.join(settings.UPLOADS_DIR, file_name)
        file_extension = os.path.splitext(file.filename)[1]

        with open(file_path, 'wb') as f:
            f.write(file_bytes)
            
    elif url:
        if not os.path.exists(url):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='File not found'
            )
        else:
            with open(url, 'rb') as file:
                file_bytes = file.read()
                file_path = url
                file_extension = os.path.splitext(url)[1]

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not specified'
        )
    
    extracted_payloads = extract_file_data(file_bytes, file_extension)
    embedded_texts = text_embedding(extracted_payloads)
    results = text_searching(query or '', embedded_texts)
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

def text_embedding(extracted_payloads: dict):
    points = []

    for extracted_payload in extracted_payloads:
        for text in extracted_payload['texts']:
            vector = TEXT_EMBEDDING_MODEL.encode(text).tolist()
            points.append(
                PointStruct(
                    id=str(uuid.uuid1()),
                    vector=vector,
                    payload={
                        "text": text,
                        "images": extracted_payload['images']
                    }
                )
            )            
    return points

def text_searching(query: str, embedded_texts: list, top_k: int = 5):
    if not embedded_texts or not query:
        return []

    query_vector = np.array(TEXT_EMBEDDING_MODEL.encode(query).tolist())

    similarities = []
    for point in embedded_texts:
        vector = np.array(point.vector)

        sim = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))

        similarities.append({
            "payload": point.payload,
            "similarity": sim
        })

    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    top_results = [item["payload"] for item in similarities[:top_k]]
    return top_results