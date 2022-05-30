from django import forms
from django.conf import settings
from tinymce.widgets import TinyMCE
from .models import BookReview, BookInstance


class DateInput(forms.DateInput):
    input_type = 'date'


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer', )
        widgets = {
            'content': TinyMCE(mce_attrs=settings.TINYMCE_USER_CONFIG),
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class UserBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'reader', 'due_back')
        widgets = {
            'reader': forms.HiddenInput(),
            'due_back': DateInput(),
        }
