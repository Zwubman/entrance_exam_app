from PIL import Image
import io, base64
from . import qdrant, EMBED_TEXT, COLLECTION_NAME

def search_from_vector_db(query: str, limit: int = 5):
    query_vector = EMBED_TEXT.encode(query).tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
    )

    collected = []
    for r in results:
        payload = r.payload
        if payload["type"] == "image":
            img_data = base64.b64decode(payload["content"])
            img = Image.open(io.BytesIO(img_data))
            collected.append({"type": "image", "image_object": img})
        else:
            collected.append({"type": "text", "content": payload["content"]})

    return collected