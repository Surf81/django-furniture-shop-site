from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http.response import HttpResponseNotFound
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.query import Prefetch
from django.db.models import F, Q, Case, When, BooleanField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from main.utilities import user_is_staff, user_permission_test

from .models import (Product, 
                     CharacteristicItem, 
                     Category, 
                     AdditionalImage, 
                     UserProductRelated, 
                     Comment)
from .forms import (UserCommentForm, 
                    GuestCommentForm, 
                    CreateProductForm, 
                    EditProductForm, 
                    AdditionalImageFormSet, 
                    SelectCharacteristicFormSet)


class IndexPageView(ListView):
    prefetch_characteristics = Prefetch('characteristics',
                        queryset=(CharacteristicItem.objects
                                  .annotate(value=F('characteristicproductrelated__value'))
                                  .select_related('group',)
                                  .distinct()
                                  ),
                        to_attr="characts_to_public"
                        )

    queryset = (Product.objects
                .select_related('category')
                .filter(is_active__exact=True)
                .prefetch_related(prefetch_characteristics)
    )
    template_name = "main/index.html"
    context_object_name = 'store'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (super().get_queryset()
                          .annotate(favorite=Case(
                            When(id__in=self.request.user.userproductrelated_set.filter(is_favorit__exact=True).values('product__id'), then=True),
                            default=False,
                            output_field=BooleanField()
                          ))
            )
        return super().get_queryset()


class CategoryPageView(IndexPageView):
    def get_queryset(self):
        cat_id = self.kwargs['pk']
        return super().get_queryset().filter(Q(category_id__exact=cat_id) | Q(category__super_category_id__exact=cat_id))
                                             
    def get_context_data(self, **kwargs):
        category_queryset = Category.objects.filter(id__exact=self.kwargs['pk'])
        if category_queryset.exists():
            kwargs['category'] = category_queryset.get().title
        else:
            raise Http404

        return super().get_context_data(**kwargs)
   

class DetailPageView(DetailView):
    CONTEXT_OBJECT_NAME = 'item'
    prefetch = Prefetch('characteristics',
                        queryset=(CharacteristicItem.objects
                                  .annotate(value=F('characteristicproductrelated__value'))
                                  .select_related('group',)
                                  .distinct()
                                  ),
                        to_attr="characts_to_public"
                        )
    queryset =   queryset = (Product.objects
                .select_related('category')
                .filter(is_active__exact=True)
                .prefetch_related(prefetch)
    )
    context_object_name = CONTEXT_OBJECT_NAME
    template_name = "main/detail.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (super().get_queryset()
                          .annotate(favorite=Case(
                            When(id__in=self.request.user.userproductrelated_set.filter(is_favorit__exact=True).values('product__id'), then=True),
                            default=False,
                            output_field=BooleanField()
                          ))
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = AdditionalImage.objects.filter(product=context[self.CONTEXT_OBJECT_NAME].pk)
        context['additional_images'] = images

        comments = Comment.objects.filter(product=context[self.CONTEXT_OBJECT_NAME].pk, is_active=True)
        initial = {'product': context[self.CONTEXT_OBJECT_NAME].pk}
        if self.request.user.is_authenticated:
            initial['author'] = self.request.user.username
            initial['is_anonimous'] = False
            form_class = UserCommentForm
        else:
            initial['author'] = Comment.ANONIMOUS_NAME
            initial['is_anonimous'] = True
            form_class = GuestCommentForm

        form = form_class(initial=initial)
        if self.request.method == 'POST':
            c_form = form_class(self.request.POST)
            if c_form.is_valid():
                c_form.save()
                messages.add_message(self.request, messages.SUCCESS, 'Комментарий добавлен')
                if c_form.cleaned_data['is_claim']:
                    messages.add_message(self.request, messages.INFO, 'Информация с Вашей жалобой отправлена в службу контроля качества')

            else:
                form = c_form
                messages.add_message(self.request, messages.WARNING, 'Комментарий не добавлен')

        context.update({'comments': comments, 'comment_form': form})
        return context

    post = DetailView.get


def any_page(request, url):
    try:
        template = get_template(f'main/{url}.html')
        return HttpResponse(template.render(request=request))
    except TemplateDoesNotExist:
        return HttpResponseNotFound(request)


@login_required
def favorite_toggle(request, pk):
    product = Product.objects.get(pk=pk)
    productrelated, _ = UserProductRelated.objects.get_or_create(product=product, user=request.user)
    productrelated.is_favorit = not productrelated.is_favorit
    productrelated.save()

    if (next := request.GET.get('next')):
        return redirect(next)
    elif (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('main:index')
    

class FavoriteProductsView(LoginRequiredMixin, ListView):
    template_name = 'main/favorite_products.html'
    context_object_name = 'favorite_products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(userproductrelated__user=self.request.user.pk, userproductrelated__is_favorit__exact=True)
        return queryset


@user_permission_test(user_is_staff)
def product_create_view(request):
    if request.method == 'POST':
        product_form = CreateProductForm(data=request.POST, files=request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            image_form = AdditionalImageFormSet(data=request.POST, files=request.FILES, instance=product)
            characteristic_form = SelectCharacteristicFormSet(data=request.POST, instance=product)
            if characteristic_form.is_valid():
                characteristic_form.save()
            if image_form.is_valid():
                image_form.save()
                messages.add_message(request, messages.SUCCESS, 'Товар добавлен')
            else:
                messages.add_message(request, messages.SUCCESS, 'Товар добавлен без изображений поскольку основное изображение не выбрано')
            return redirect('main:detail', pk=product.pk)

        messages.add_message(request, messages.WARNING, 'Товар не добавлен')
    else:
        product_form = CreateProductForm()
        image_form = AdditionalImageFormSet()
        characteristic_form = SelectCharacteristicFormSet()

    context = {
        'product_form': product_form,
        'image_form': image_form,
        'characteristic_form': characteristic_form,
    }

    return render(request, 'main/product_create.html', context)


@user_permission_test(user_is_staff)
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = EditProductForm(data=request.POST, files=request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            image_form = AdditionalImageFormSet(data=request.POST, files=request.FILES, instance=product)
            characteristic_form = SelectCharacteristicFormSet(data=request.POST, instance=product)
            if characteristic_form.is_valid():
                characteristic_form.save()
            if image_form.is_valid():
                image_form.save()
                messages.add_message(request, messages.SUCCESS, 'Товар изменен')
            else:
                messages.add_message(request, messages.SUCCESS, 'Товар добавлен без изображений поскольку основное изображение не выбрано')
            return redirect('main:detail', pk=product.pk)

        messages.add_message(request, messages.WARNING, 'Товар не изменен')
    else:
        product_form = EditProductForm(instance=product)
        image_form = AdditionalImageFormSet(instance=product)
        characteristic_form = SelectCharacteristicFormSet(instance=product)

    context = {
        'product_form': product_form,
        'image_form': image_form,
        'characteristic_form': characteristic_form,
    }

    return render(request, 'main/product_edit.html', context)


@user_permission_test(user_is_staff)
def product_del_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.add_message(request, messages.SUCCESS, 'Товар удален')

    return redirect('main:index')

