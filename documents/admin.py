from django.contrib import admin
from .models import Document

# Register your models here.
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("status", "extracted_data", "created_at")