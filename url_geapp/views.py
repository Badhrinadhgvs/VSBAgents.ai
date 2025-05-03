from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import DynamicPage
from groq import Groq, APIError
from phi.agent import Agent
from phi.model.groq import Groq as GroqPhi
import os

def verify_groq_api_key(api_key):
    """Verify if the Groq API key is valid by making a test request."""
    try:
        client = Groq(api_key=api_key)
        # Make a simple test request
        client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        return True
    except APIError:
        return False

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

def success(request, slug):
    page = get_object_or_404(DynamicPage, slug=slug)
    return render(request, 'success.html', {'page': page})

def dynamic_page(request, slug):
    page = get_object_or_404(DynamicPage, slug=slug)
    return render(request, 'dynamic_page.html', {'page': page})

def chat(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    page = get_object_or_404(DynamicPage, slug=slug)
    user_message = request.POST.get('message')

    if not user_message:
        return JsonResponse({'error': 'No message provided'}, status=400)

    try:
        # Initialize Phidata agent with Groq model
        agent = Agent(
            model=GroqPhi(id="meta-llama/llama-4-scout-17b-16e-instruct", api_key=page.api_key),
            markdown=True,
            instructions=["Provide concise and helpful responses.", "Use markdown for formatting."]
        )
        # Get response from the agent
        response = agent.run(user_message)
        return JsonResponse({'response': response.content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)