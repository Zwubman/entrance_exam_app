import textwrap
import easyocr
from app.config.setting import settings

reader = easyocr.Reader(['en'], gpu=False)

def extract_img_data(file_bytes: bytes):
    results = reader.readtext(file_bytes)
    text = " ".join(text for (_, text, _) in results).strip()
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