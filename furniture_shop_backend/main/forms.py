from django import forms

from main.models import (SuperCategory, SubCategory, CharacteristicGroup, CharacteristicItem)


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