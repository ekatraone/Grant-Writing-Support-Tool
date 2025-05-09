from django import forms
from .models import GrantDraft

class GrantDraftForm(forms.ModelForm):
    class Meta:
        model = GrantDraft
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Paste your grant draft here...',
                'rows': 10,
            })
        }
