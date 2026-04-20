import pytesseract
import os
from PIL import Image
from celery import shared_task
from .models import Document

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

@shared_task
def process_document(document_id):
    doc = Document.objects.get(id=document_id)
    doc.status = "processing"
    doc.save()

    try:
        file_path = doc.file.path

        # Open image
        image = Image.open(file_path)

        # Extract text
        text = pytesseract.image_to_string(image)

        doc.extracted_data = {
            "text": text.strip()
        }

        doc.status = "completed"

    except Exception as e:
        doc.status = "failed"
        doc.extracted_data = {"error": str(e)}

    doc.save()

    # # Fake AI processing (replace later)
    # extracted = {
    #     "text": "Sample extracted content",
    #     "amount": "5000",
    # }

    # doc.extracted_data = extracted
    # doc.status = "completed"
    # doc.save()

#Trigger task on upload
def perform_create(self, serializer):
    doc = serializer.save(user=self.request.user)
    from .tasks import process_document
    process_document.delay(doc.id)