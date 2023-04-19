from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http.response import HttpResponseNotFound
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.query import Prefetch
from django.db.models import F, Q, Case, When, BooleanField
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, CharacteristicItem, Category, AdditionalImage, UserProductRelated




class IndexPageView(ListView):
    prefetch_characteristics = Prefetch('characteristics',
                        queryset=(CharacteristicItem.objects
                                  .annotate(value=F('characteristicproduct__value'))
                                  .select_related('group',)
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
                                  .annotate(value=F('characteristicproduct__value'))
                                  .select_related('group',)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = AdditionalImage.objects.filter(product_id=context[self.CONTEXT_OBJECT_NAME].pk)
        context['additional_images'] = images
        return context


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

    if (path := request.META.get('HTTP_REFERER')):
        return redirect(path)
    else:
        return redirect('main:index')
    

class FavoriteProductsView(LoginRequiredMixin, ListView):
    template_name = 'main/favorite_products.html'
    context_object_name = 'favorite_products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(userproductrelated__user=self.request.user.pk, userproductrelated__is_favorit__exact=True)
        return queryset

