from django.contrib import admin

from .forms import SubCategoryForm, CharacteristicItemForm
from .models import (SuperCategory, SubCategory, 
                     CharacteristicItem, CharacteristicGroup, 
                     Product, AdditionalImage, 
                     CharacteristicProduct,
                     UserProductRelated)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class CharacteristicItemInline(admin.TabularInline):
    model = CharacteristicItem


@admin.register(CharacteristicGroup)
class CharacteristicGroupAdmin(admin.ModelAdmin):
    exclude = ('group', 'type')
    inlines = (CharacteristicItemInline,)

    def save_model(self, request, obj, form, change):
        obj.type = 0
        return super().save_model(request, obj, form, change)    


@admin.register(CharacteristicItem)
class CharacteristicItemAdmin(admin.ModelAdmin):
    form = CharacteristicItemForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

class CharacteristicsInline(admin.TabularInline):
    model = CharacteristicProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    fields = ('category', 'title', ('price', 'count'), 'description', 'image', 'is_active', 'created_at', 'changed_at')
    readonly_fields = ('created_at', 'changed_at')
    inlines = (AdditionalImageInline, CharacteristicsInline)


@admin.register(UserProductRelated)
class UserProductRelatedAdmin(admin.ModelAdmin):
    pass

@admin.register(CharacteristicProduct)
class CharacteristicProductAdmin(admin.ModelAdmin):
    pass
