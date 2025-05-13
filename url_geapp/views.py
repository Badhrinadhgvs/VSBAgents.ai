from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import DynamicPage

from url_geapp.Components.verify_key import verify_groq_api_key
from url_geapp.Components.success import success
from url_geapp.Components.dynamic_page import dynamic_page
from url_geapp.Components.chat import chat


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        api_key = request.POST.get('api_key')
        keywords = request.POST.get('keywords')

        # Verify the Groq API key
        if not verify_groq_api_key(api_key):
            messages.error(request, "Invalid Groq API key. Please provide a valid key.")
            return render(request, 'home.html', {
                'name': name,
                'description': description,
                'api_key': api_key,
                'keywords': keywords
            })

        # Create the page if API key is valid
        page = DynamicPage.objects.create(
            name=name,
            description=description,
            api_key=api_key,
            keywords=keywords
        )
        return HttpResponseRedirect(reverse('url_geapp:success', args=[page.slug]))
    return render(request, 'home.html')
