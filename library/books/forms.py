from django import forms
from django.conf import settings
from tinymce.widgets import TinyMCE
from .models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer', )
        widgets = {
            'content': TinyMCE(mce_attrs=settings.TINYMCE_USER_CONFIG),
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
