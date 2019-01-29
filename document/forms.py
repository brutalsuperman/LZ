from django import forms
from .models import Document, Source
from django_select2.forms import ModelSelect2Widget


class DocumentModelForm(forms.ModelForm):

    source = forms.ModelChoiceField(
        queryset=Source.objects.all(),
        label=u"source",
        widget=ModelSelect2Widget(
            model=Source,
            search_fields=['name__icontains'],
        )
    )

    class Meta:
        model = Document
        fields = [
            'title', 'text', 'url', 'source'
        ]
