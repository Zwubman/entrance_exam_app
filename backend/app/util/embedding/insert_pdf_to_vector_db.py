import uuid
from . import qdrant, COLLECTION_NAME, TEXT_EMBEDDING_MODEL, PointStruct
from app.schema.exam import ExamInsert

def insert_pdf_to_vector_db(extracted_payloads: dict, req: ExamInsert):
    """Insert extracted PDF content (text + images) into Qdrant."""
    points = []
    total_points = total_images = 0

    for extracted_payload in extracted_payloads:
        for text in extracted_payload['texts']:
            vector = TEXT_EMBEDDING_MODEL.encode(text).tolist()
            points.append(
                PointStruct(
                    id=str(uuid.uuid1()),
                    vector=vector,
                    payload={
                        "text": text,
                        "images": extracted_payload['images'],
                        'year': req.year,
                        'subject': req.subject,
                        'extra_data': req.extra_data or None
                    }
                )
            )

        if points:
            qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

        total_points += len(extracted_payload['texts'])
        total_images += len(extracted_payload['images'])

    return {
        'total_pages': len(extracted_payloads),
        'total_points': total_points,
        'total_images': total_images
    }