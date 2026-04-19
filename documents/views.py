from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from documents.tasks import process_document
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    #Replace delay() with direct task call
    def perform_create(self, serializer):
        doc = serializer.save(user=self.request.user)

        from .tasks import process_document
        process_document(doc.id) 