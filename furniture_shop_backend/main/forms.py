from django import forms
from captcha.fields import CaptchaField

from main.models import (Product, AdditionalImage,
                         SuperCategory, SubCategory, 
                         CharacteristicGroup, CharacteristicItem, CharacteristicProduct,
                         Comment)


class SubCategoryForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=SuperCategory.objects.all(),
                                   empty_label=None,
                                   label='группа категорий',
                                   required=True)
    
    class Meta:
        model = SubCategory
        fields = '__all__'


class CharacteristicItemForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=CharacteristicGroup.objects.all(),
                                   empty_label=None,
                                   label='группа характеристик',
                                   required=True)
    
    class Meta:
        model = CharacteristicItem
        fields = '__all__'


class UserCommentBaseForm(forms.ModelForm):
    # author = forms.CharField(label='Автор', disabled=True)
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'product': forms.HiddenInput,
                   'author': forms.TextInput(attrs={'readonly': True})}
        help_texts = {'is_claim': "Сообщения, содержащие жалобы, направляются в службу контроля качества"}

    def clean(self):
        author_name = self.cleaned_data['author']
        if self.cleaned_data.get('is_anonimous'):
            self.cleaned_data['author'] = self._meta.model.ANONIMOUS_NAME


class UserCommentForm(UserCommentBaseForm):
    pass
        
class GuestCommentForm(UserCommentBaseForm):
    captcha = CaptchaField(label='введите код с картинки',
                           error_messages = {'invalid': 'Неправильный текст'})

    class Meta(UserCommentBaseForm.Meta):
        exclude = ('is_active', 'is_anonimous')


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'count', 'price', 'image')

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'count', 'price', 'is_active', 'image')


class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = '__all__'
        widgets = {'product': forms.HiddenInput}

    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data['image'] and not self.cleaned_data['product'].image:
            errors['image'] = forms.ValidationError("Не выбрано основное изображение")
        if errors:
            raise forms.ValidationError(errors)

AdditionalImageFormSet = forms.inlineformset_factory(Product, AdditionalImage, form=AdditionalImageForm, extra=3, can_delete=False)

class SelectCharacteristicForm(forms.ModelForm):
    class Meta:
        model = CharacteristicProduct
        fields = ('characteristic', 'value', 'product')
        widgets = {'product': forms.HiddenInput}

SelectCharacteristicFormSet = forms.inlineformset_factory(Product, CharacteristicProduct, form=SelectCharacteristicForm, extra=3, can_delete=False)
