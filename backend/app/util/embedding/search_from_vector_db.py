from app.schema.exam import ExamSearch
from . import qdrant, TEXT_EMBEDDING_MODEL, COLLECTION_NAME, Filter, FieldCondition, MatchValue

def search_from_vector_db(req: ExamSearch, limit: int = 5):
    query_vector = TEXT_EMBEDDING_MODEL.encode(req.query or '').tolist()

    filter_condition = []

    if req.year:
        filter_condition.append(
            FieldCondition(
                key="year",
                match=MatchValue(value=req.year)
            )
        )

    if req.subject:
        filter_condition.append(
            FieldCondition(
                key="subject",
                match=MatchValue(value=req.subject)
            )
        )

    if req.extra_data:
        filter_condition.append(
            FieldCondition(
                key="extra_data",
                match=MatchValue(value=req.extra_data)
            )
        )

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        query_filter=Filter(
            must=filter_condition
        )
    )

    return [
        {
            'id': x.id,
            'payload': x.payload
        } for x in results
    ]