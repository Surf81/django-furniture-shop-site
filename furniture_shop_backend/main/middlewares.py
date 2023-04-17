from .models import SubCategory

def furniture_shop_context_processor(request):
    context = {}
    context['categories'] = SubCategory.objects.select_related('super_category').all()
    return context