from django.contrib import admin
from .models import StickyNote

@admin.register(StickyNote)
class StickyNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'updated_at')
    search_fields = ('user__email', 'content')
    list_filter = ('created_at',)
