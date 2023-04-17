from django.http import HttpResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http.response import HttpResponseNotFound
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.query import Prefetch
from django.db.models.functions import Concat
from django.db.models import F

from .models import Product, CharacteristicItem, CharacteristicGroup




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


