from django.db import models
from django.conf import settings

class StickyNote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="sticky_notes"
    )
    content = models.TextField()
    attachment = models.FileField(
        upload_to="notes/attachments/", 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sticky Note by {self.user.email} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

