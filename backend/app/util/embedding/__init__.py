from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from app.config.setting import settings

# ---------- CONFIG ----------
COLLECTION_NAME = "pdf_content"
TEXT_VECTOR_SIZE = 384
IMAGE_VECTOR_SIZE = 512
TEXT_EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
IMAGE_EMBEDDING_MODEL = SentenceTransformer("clip-ViT-B-32")

# qdrant = QdrantClient(
#     url=settings.QDRANT_URL,
#     api_key=settings.QDRANT_API_KEY,
# )

# qdrant = QdrantClient(host="localhost", port=6333)

qdrant = QdrantClient(":memory:")

try:
    qdrant.get_collection(COLLECTION_NAME)
except:
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=TEXT_VECTOR_SIZE,
            distance=Distance.COSINE
        ),
    )

# qdrant.recreate_collection(
#     collection_name=COLLECTION_NAME,
#     vectors_config=VectorParams(
#         size=TEXT_VECTOR_SIZE,
#         distance=Distance.COSINE
#     )
# )