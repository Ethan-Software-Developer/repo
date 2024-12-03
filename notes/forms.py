from django import forms
from .models import StickyNote

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your note here...',
                'rows': 5
            }),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
