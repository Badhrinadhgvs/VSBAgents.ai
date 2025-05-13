from django.shortcuts import render, get_object_or_404
from url_geapp.models import DynamicPage



def success(request, slug):
    page = get_object_or_404(DynamicPage, slug=slug)
    return render(request, 'success.html', {'page': page})