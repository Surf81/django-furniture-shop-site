from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http.response import HttpResponseNotFound
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.query import Prefetch
from django.db.models.functions import Concat
from django.db.models import F, Q

from .models import Product, CharacteristicItem, Category




class IndexPageView(ListView):
    prefetch = Prefetch('characteristics',
                        queryset=(CharacteristicItem.objects
                                  .annotate(value=F('characteristicproduct__value'))
                                  .select_related('group',)
                                  ),
                        to_attr="characts_to_public"
                        )

    queryset = (Product.objects
                .select_related('category')
                .filter(is_active__exact=True)
                .prefetch_related(prefetch)
    )
    template_name = "main/index.html"
    context_object_name = 'store'
    paginate_by = 2


class CategoryPageView(IndexPageView):
    def get_queryset(self):
        category_id = self.kwargs['pk']
        return super().get_queryset().filter(Q(category_id=category_id) | Q(category__super_category_id=category_id))
                                             
    def get_context_data(self, **kwargs):
        category_queryset = Category.objects.filter(id__exact=self.kwargs['pk'])
        if category_queryset.exists():
            kwargs['category'] = category_queryset.get().title
        else:
            raise Http404

        return super().get_context_data(**kwargs)
   

class DetailPageView(DetailView):
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
    context_object_name = "item"
    template_name = "main/detail.html"


def any_page(request, url):
    try:
        template = get_template(f'main/{url}.html')
        return HttpResponse(template.render(request=request))
    except TemplateDoesNotExist:
        return HttpResponseNotFound(request)


