from django import forms
from tinymce.widgets import TinyMCE
from .models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer', )
        widgets = {
            'content': TinyMCE(),
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
