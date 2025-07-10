from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet, BaseModelFormSet

from catalog.models import Product, Version


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'modificated_at', 'user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        restricted_words = ['казино', 'криптовалюта', 'крипта', 'биржа',
                            'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in restricted_words:
            if word.lower() in cleaned_data:
                raise forms.ValidationError('Недопустимое имя продукта')
        return cleaned_data


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
        widgets = {'product': forms.HiddenInput()}


class VersionFormSet(BaseModelFormSet):

    def clean(self):
        is_currency = False
        for form in self.forms:
            if form.cleaned_data.get('is_currency'):
                if is_currency:
                    raise ValidationError("только одна версия может быть текущей")
                else:
                    is_currency = True


class VersionInlineFormSet(BaseInlineFormSet):

    def clean(self):
        is_currency = False
        for form in self.forms:
            if form.cleaned_data.get('is_currency'):
                if is_currency:
                    raise ValidationError("только одна версия может быть текущей")
                else:
                    is_currency = True
