from celery import shared_task
from .models import Document

@shared_task
def process_document(document_id):
    doc = Document.objects.get(id=document_id)
    doc.status = "processing"
    doc.save()

    # Fake AI processing (replace later)
    extracted = {
        "text": "Sample extracted content",
        "amount": "5000",
    }

    doc.extracted_data = extracted
    doc.status = "completed"
    doc.save()

#Trigger task on upload
def perform_create(self, serializer):
    doc = serializer.save(user=self.request.user)
    from .tasks import process_document
    process_document.delay(doc.id)