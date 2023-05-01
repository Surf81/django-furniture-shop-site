from django.db import models
from django.db.models.functions import Lower
from django.forms import ValidationError
from django.db.models.signals import post_save

from main.utilities import get_timestamp_path, send_claim_notification
from advuser.models import AdvancedUser


class Category(models.Model):
    title = models.CharField("категория", max_length=150, db_index=True, unique=True)
    order = models.SmallIntegerField('порядок', default=0, db_index=True)
    super_category = models.ForeignKey("SuperCategory", 
                                     on_delete=models.PROTECT, 
                                     null=True, 
                                     blank=True, 
                                     verbose_name='надрубрика')


class SuperCatogoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)
    
class SuperCategory(Category):
    objects = SuperCatogoryManager()

    def __str__(self):
        return self.title

    class Meta:
        proxy = True
        ordering = ('order', 'title')
        verbose_name = 'группа гатегорий'
        verbose_name_plural = 'группы категорий'


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)
    
class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return "{} - {}".format(self.super_category.title, self.title)
    
    class Meta:
        proxy = True
        ordering = ('super_category__order', 'super_category__title', 'order', 'title')
        verbose_name = 'категория'
        verbose_name_plural = 'категории'



def is_nul_validator(value):
    if value is None:
        raise ValidationError(
            "Выберите тип параметра", code="invalid", params={"value": value}
        )    

class Characteristic(models.Model):
    class Types(models.IntegerChoices):
        SELECT = (1, "Элемент списка")
        VALUE = (2, "Измерение")

    title = models.CharField("характеристика", max_length=100, db_index=True)
    order = models.SmallIntegerField('порядок', default=0, db_index=True)
    type = models.IntegerField('тип', choices=Types.choices, 
                               null=True, 
                               validators=[is_nul_validator])
    group = models.ForeignKey('CharacteristicGroup', 
                                     on_delete=models.PROTECT, 
                                     null=True, 
                                     blank=True, 
                                     verbose_name='группа характеристик')
    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('title').desc(), 'group', name='unique_lower_name_category')
        ]

class CharacteristicGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group__isnull=True)
        
    
class CharacteristicGroup(Characteristic):
    objects = CharacteristicGroupManager()

    def __str__(self):
        return self.title
    
    class Meta:
        proxy = True
        ordering = ('order', 'title')
        verbose_name = 'группа характеристик'
        verbose_name_plural = 'группы характеристик'


class CharacteristicItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group__isnull=False)
        
    
class CharacteristicItem(Characteristic):
    objects = CharacteristicItemManager()

    def __str__(self):
        return "{} - {}".format(self.group.title, self.title)
    
    class Meta:
        proxy = True
        ordering = ('group__order', 'group__title', 'order', 'title')
        verbose_name = 'характеристика'
        verbose_name_plural = 'характеристики'


class Product(models.Model):
    title = models.CharField("модель", max_length=150)
    description = models.TextField('описание')
    count = models.PositiveIntegerField("количество")
    price = models.PositiveIntegerField("цена")
    image = models.ImageField('основное изображение', blank=True, upload_to=get_timestamp_path)
    is_active = models.BooleanField('модель доступна?', default=True, db_index=True)
    created_at = models.DateTimeField('опубликовано', auto_now_add=True, db_index=True)    
    changed_at = models.DateTimeField('опубликовано', auto_now=True, db_index=True)    
    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=False, verbose_name="категория")
    characteristics = models.ManyToManyField(CharacteristicItem, through="CharacteristicProductRelated")
    buyers = models.ManyToManyField(AdvancedUser, through="UserProductRelated")

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'товары'
        verbose_name = 'товар'

    def __str__(self):
        return self.title


class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='модель')
    image = models.ImageField('дополнительное изображение', upload_to=get_timestamp_path)

    class Meta:
        verbose_name_plural = 'дополнительные изображения'
        verbose_name = 'дополнительное изображение'


class CharacteristicProductRelated(models.Model):
    value = models.IntegerField('значение', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    characteristic = models.ForeignKey(CharacteristicItem, on_delete=models.CASCADE, null=False, verbose_name="характеристика")

    class Meta:
        verbose_name_plural = 'характеристики модели'
        verbose_name = 'характеристика модели'
        constraints = [
            models.UniqueConstraint('product', 'characteristic', name='unique_product_characteristic')
        ]

    def __str__(self):
        return str(self.characteristic)


class UserProductRelated(models.Model):
    user = models.ForeignKey(AdvancedUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count_on_cart = models.PositiveIntegerField("в корзине", default=0, null=False)
    is_favorit = models.BooleanField('избранное', default=False, null=False)

    class Meta:
        verbose_name_plural = 'действия пользователей с товарами'
        verbose_name = 'пользователь - товар'

    def __str__(self):
        return f"{self.user} : {self.product}"
    

class Comment(models.Model):
    ANONIMOUS_NAME = 'аноним'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар")
    author = models.CharField('автор', max_length=150)
    is_anonimous = models.BooleanField('оставаться анонимным?', default=False)
    content = models.TextField('содержание')
    is_active = models.BooleanField('выводить на экран?', default=True, db_index=True)
    is_claim = models.BooleanField('жалоба', default=False, db_index=True)
    created_at = models.DateTimeField('опубликован', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = 'комментарии'
        verbose_name = 'комментарий'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    if kwargs['created'] and kwargs['instance'].is_claim:
        send_claim_notification(kwargs['instance'])

post_save.connect(post_save_dispatcher, sender=Comment)