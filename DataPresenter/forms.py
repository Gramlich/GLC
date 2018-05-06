from django import forms
from DataPresenter.models import Document

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('data', )






