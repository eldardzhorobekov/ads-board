from django import forms
from django.forms import BaseInlineFormSet
from django.utils.safestring import mark_safe
from string import Template
from ad.models import Advertisement, AdvertisementImage


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = (  'description', 'price',
                    'currency', 'city', 'category', 'phone_number',
                    'hide_phone_number', 'email')
        labels = {
            'description': 'Описание:',
            'price': 'Цена:',
            'currency': 'Валюта:',
            'city': 'Город:',
            'category': 'Категория:',
            'phone_number': 'Телефон:',
            'hide_phone_number': 'Скрыть номер',
            'email': 'Электронная почта:'
        }
    
    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = None
        self.fields['category'].empty_label = None


class AdvertisementImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisementImage
        fields = ('image', 'is_main')


class AdvertisementImageInlineFormSet(BaseInlineFormSet):
    pass


class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        url = value.url if value is not None else 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D'
        img_html = mark_safe(f'<img src="{url}" width="100px" height="100px" id="{attrs["id"]}"/>')
        delete_btn = mark_safe(f'<button class="delete-image-btn"><i class="fas fa-times"></i></button>')
        input_html = super(PictureWidget, self).render(name, value, attrs=None, **kwargs)
        return f'{input_html}{img_html}{delete_btn}'


AdvertisementImageInlineFormset = forms.inlineformset_factory(
    Advertisement,
    AdvertisementImage,
    formset=AdvertisementImageInlineFormSet,
    fields=('image',),
    widgets={
        'image': PictureWidget
    },
    extra=1,
    # can_order=True,
    can_delete=True
)