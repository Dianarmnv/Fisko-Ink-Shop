from PIL import Image
from django.utils.safestring import mark_safe
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin

from .models import *


# Sprawdzanie rozmiaru zdjęcia
# class NotebookAdminForm(ModelForm):
#
#     # help_text for upload images
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = mark_safe(
#             """<span style="color:red; font-size: 14px;">If you upload an image with a higher resolution {}x{}, it will
#             be cropped!</span>
#             """.format(
#                 *Product.MAX_RESOLUTION
#             )
#         )

# def clean_image(self):
#     image = self.cleaned_data['image']
#     img = Image.open(image)
#     min_height, min_width = Product.MIN_RESOLUTION
#     max_height, max_width = Product.MAX_RESOLUTION
#     if image.size > Product.MAX_IMAGE_SIZE:
#         raise ValidationError('Image size should not exceed 3MB!')
#     if img.height < min_height or img.width < min_width:
#         raise ValidationError('Your image resolution is less than the minimum!')
#     if img.height > max_height or img.width > max_width:
#         raise ValidationError('Your image resolution is more than the maximum!')
#     return image


# zabroniamy wprowadzania liczby obsługiwanych gigabajtów karty SD
# po naciśnięciu tego pola wyboru
class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # super() daje nam dostęp do metod w nadklasie z podklasy, która po niej dziedziczy.
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray;'
            })

    # clen pozwala nam pracować z polami, czyli clean dotyczy całego formularza,
    # ale jeśli musimy pracować z jakimś konkretnym obiektem, to do clean dodajemy nazwe pola naprzyklad 'clean_sd'
    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


class NotebookAdmin(admin.ModelAdmin):

    # form = NotebookAdminForm - połączenie weryfikacji obrazu

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
