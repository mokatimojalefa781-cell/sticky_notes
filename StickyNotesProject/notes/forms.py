from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Note title',
                'class': 'input-title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'rows': 6,
                'class': 'input-content'
            }),
        }
