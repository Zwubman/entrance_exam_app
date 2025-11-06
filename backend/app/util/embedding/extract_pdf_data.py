import io
import os
import uuid
import textwrap
from PyPDF2 import PdfReader
from PIL import Image
from app.config.setting import settings

def extract_pdf_data(file_bytes: bytes):
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_payloads = []

        for page_num, page in enumerate(reader.pages, start=1):
            page_texts, page_images = [], []

            # Extract text
            text = page.extract_text()
            if text and text.strip():
                sentences = textwrap.wrap(text.strip(), width=settings.CHUNK_LENGTH)
                page_texts.extend(sentences)

            # Extract images - simplified approach
            if '/Resources' in page and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                
                for obj_name, obj in xObject.items():
                    if obj.get('/Subtype') == '/Image':
                        try:
                            # Get image data
                            if '/Filter' in obj:
                                if obj['/Filter'] == '/FlateDecode':
                                    data = obj.get_data()
                                else:
                                    data = obj._data
                            else:
                                data = obj.get_data()

                            if not data:
                                continue

                            # Try to open and save image
                            img = Image.open(io.BytesIO(data))
                            image_name = f"page_{page_num}_{uuid.uuid4().hex}.png"
                            image_path = os.path.join(settings.UPLOADS_DIR, image_name)
                            img.save(image_path, "PNG")
                            page_images.append(image_path)
                            
                        except Exception as e:
                            print(f"Failed to extract image from page {page_num}: {e}")
                            continue

            extracted_payloads.append({
                'texts': page_texts,
                'images': page_images
            })

        return extracted_payloads
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []