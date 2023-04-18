from .models import SubCategory
from django.db.models import Count

def furniture_shop_context_processor(request):
    context = {}
    context['categories'] = (SubCategory.objects
                             .select_related('super_category')
                             .annotate(products=Count('product'))
                             .filter(products__gt=0)
                             .order_by(*SubCategory._meta.ordering)
    )
    return context