import pytesseract
import os
from PIL import Image
from pdf2image import convert_from_path
from celery import shared_task
from .models import Document

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Celery task
@shared_task
def process_document(document_id):
    doc = Document.objects.get(id=document_id)
    doc.status = "processing"
    doc.save()

    try:
        file_path = doc.file.path
        extracted_text = ""

        # 👇 Check if PDF
        if file_path.lower().endswith(".pdf"):
            # Convert PDF to images
            images = convert_from_path(file_path)

            # Extract text from each image
            for image in images:
                text = pytesseract.image_to_string(image)
                extracted_text += text + "\n"
        else:
            # Open image
            image = Image.open(file_path)

            # Extract text
            extracted_text = pytesseract.image_to_string(image)

        doc.extracted_data = {
            "text": extracted_text.strip()
        }

        doc.status = "completed"

    except Exception as e:
        doc.status = "failed"
        doc.extracted_data = {"error": str(e)}

    doc.save()
    

#Trigger task on upload
def perform_create(self, serializer):
    doc = serializer.save(user=self.request.user)
    from .tasks import process_document
    process_document.delay(doc.id)