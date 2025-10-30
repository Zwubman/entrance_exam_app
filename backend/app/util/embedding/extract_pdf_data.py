import io
from PyPDF2 import PdfReader
from PIL import Image

def extract_pdf_data(pdf_bytes: bytes):
    """Extract text and images from a PDF."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text_segments, image_list = [], []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            text_segments.extend(sentences)

        if "/XObject" in page["/Resources"]:
            xObject = page["/Resources"]["/XObject"].get_object()
            for obj_name, obj in xObject.items():
                if obj["/Subtype"] == "/Image":
                    size = (obj["/Width"], obj["/Height"])
                    data = obj.get_data()
                    mode = "RGB" if obj["/ColorSpace"] == "/DeviceRGB" else "P"
                    img = Image.frombytes(mode, size, data)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    image_list.append(buf.getvalue())

    return text_segments, image_list