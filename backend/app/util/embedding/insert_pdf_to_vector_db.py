import io
import uuid
import base64
from PIL import Image
from .extract_pdf_data import extract_pdf_data
from . import qdrant, COLLECTION_NAME, TEXT_EMBEDDING_MODEL, IMAGE_EMBEDDING_MODEL, PointStruct

def insert_pdf_to_vector_db(pdf_bytes: bytes):
    """Extract, embed, and insert PDF content (text + images) into Qdrant."""
    text_segments, images = extract_pdf_data(pdf_bytes)
    points = []

    for text in text_segments:
        vector = TEXT_EMBEDDING_MODEL.encode(text).tolist()
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"type": "text", "content": text},
            )
        )

    for img_bytes in images:
        vector = IMAGE_EMBEDDING_MODEL.encode([Image.open(io.BytesIO(img_bytes))])[0].tolist()
        encoded_img = base64.b64encode(img_bytes).decode("utf-8")
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"type": "image", "content": encoded_img},
            )
        )

    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

    return {"text_segments": len(text_segments), "images": len(images)}
