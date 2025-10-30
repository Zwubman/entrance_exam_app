
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# ---------- CONFIG ----------
COLLECTION_NAME = "pdf_content"
VECTOR_SIZE = 384
TEXT_EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
IMAGE_EMBEDDING_MODEL = SentenceTransformer("clip-ViT-B-32")

# Qdrant connection (local or cloud)
# For Qdrant Cloud: replace with url + api_key
# qdrant = QdrantClient(url="https://YOUR_CLUSTER.qdrant.tech", api_key="YOUR_API_KEY")
qdrant = QdrantClient(host="localhost", port=6333)


qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)