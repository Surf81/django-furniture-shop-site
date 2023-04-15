from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http.response import HttpResponseNotFound

def index(request):
    return render(request, "main/index.html")


def any_page(request, url):
    try:
        template = get_template(f'main/{url}')
        return render(request, template)
    except TemplateDoesNotExist:
        return HttpResponseNotFound(request)