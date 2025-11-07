import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.globals import set_llm_cache
from app.config.setting import settings
from app.model.ai_cache import SQLAlchemyCache
from app.config.database import db_session_factory

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
set_llm_cache(SQLAlchemyCache(db_session_factory))

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash-lite",
    temperature=0.2,
    max_output_tokens=100,
)