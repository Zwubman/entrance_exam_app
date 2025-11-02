import io
import os
import uuid
from PyPDF2 import PdfReader
from PIL import Image
from app.config.setting import settings
import textwrap

def extract_pdf_data(pdf_bytes: bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text_segments, image_paths = [], []
    extracted_payloads = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            sentences = textwrap.wrap(text, width=settings.CHUNK_LENGTH)
            text_segments.extend(sentences)

        resources = page.get("/Resources")
        if hasattr(resources, "get_object"):
            resources = resources.get_object()

        if resources and "/XObject" in resources:
            xObject = resources["/XObject"]
            if hasattr(xObject, "get_object"):
                xObject = xObject.get_object()

            for obj_name, obj in xObject.items():
                if hasattr(obj, "get_object"):
                    obj = obj.get_object()

                if obj.get("/Subtype") == "/Image":
                    width, height = obj.get("/Width"), obj.get("/Height")
                    color_space = obj.get("/ColorSpace", "/DeviceRGB")
                    mode = "RGB" if color_space == "/DeviceRGB" else "P"

                    data = obj.get_data()
                    filters = obj.get("/Filter")

                    try:
                        if filters == "/DCTDecode" or filters == "/JPXDecode":
                            img = Image.open(io.BytesIO(data))
                        elif filters == "/FlateDecode":
                            img = Image.frombytes(mode, (width, height), data)
                        else:
                            img = Image.frombytes(mode, (width, height), data)
                    except Exception:
                        continue

                    image_name = f"{uuid.uuid1().hex}.png"
                    image_path = os.path.join(settings.UPLOADS_DIR, image_name)
                    img.save(image_path, "PNG")
                    image_paths.append(image_path)

        extracted_payloads.append({
            'texts': text_segments,
            'images': image_paths
        })
        image_paths = []

    return extracted_payloads