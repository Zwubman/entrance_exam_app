import io
import os
import uuid
from PIL import Image
import pytesseract
import textwrap
from app.config.setting import settings

def extract_img_data(file_bytes: bytes):
    extracted_payloads = []

    try:
        img = Image.open(io.BytesIO(file_bytes))
        img = img.convert("RGB")  # Normalize mode

        image_name = f"image_{uuid.uuid1().hex}.png"
        image_path = os.path.join(settings.UPLOADS_DIR, image_name)
        img.save(image_path, "PNG")

        try:
            extracted_text = pytesseract.image_to_string(img)
        except Exception as e:
            print(f"OCR failed: {e}")
            extracted_text = ""

        text_segments = []
        if extracted_text.strip():
            sentences = textwrap.wrap(extracted_text.strip(), width=settings.CHUNK_LENGTH)
            text_segments.extend(sentences)

        extracted_payloads.append({
            "texts": text_segments,
            "images": [image_path]
        })

    except Exception as e:
        print(f"Failed to process image file: {e}")

    return extracted_payloads