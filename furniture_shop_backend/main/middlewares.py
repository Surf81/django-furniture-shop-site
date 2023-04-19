from .models import SubCategory
from django.db.models import Count
from furniture_shop import settings

def furniture_shop_context_processor(request):
    context = {}
    context['categories'] = (SubCategory.objects
                             .select_related('super_category')
                             .annotate(product_count=Count('product'))
                             .filter(product_count__gt=0)
                             .order_by(*SubCategory._meta.ordering)
    )
    context['image_stub'] = settings.IMAGE_STUB_URL
    return context