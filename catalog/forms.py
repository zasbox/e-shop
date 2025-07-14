from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet, BaseModelFormSet, CheckboxInput

from catalog.models import Product, Version


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'modificated_at', 'user')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        user_id = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if type(field.widget) != CheckboxInput:
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
        custom_perms: tuple = (
            'catalog.set_published_status',
            'catalog.change_category',
            'catalog.change_description',
        )
        if request is not None:
            auth_user = request.user
            if auth_user != user_id and not auth_user.is_superuser:
                self.fields['name'].disabled = True
                self.fields['preview'].disabled = True
                self.fields['price'].disabled = True
            if not auth_user.has_perm('catalog.set_published_status'):
                self.fields['is_published'].disabled = True
        else:
            self.fields.pop('is_published')

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
