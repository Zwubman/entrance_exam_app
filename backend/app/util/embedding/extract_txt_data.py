import textwrap
from app.config.setting import settings

def extract_txt_data(file_bytes: bytes):
    text = file_bytes.decode('utf-8')
    extracted_payloads = []
    text_segments = []
    image_paths = []

    if text:
        sentences = textwrap.wrap(text, width=settings.CHUNK_LENGTH)
        text_segments.extend(sentences)

    extracted_payloads.append({
        "texts": text_segments,
        "images": image_paths
    })

    return extracted_payloads