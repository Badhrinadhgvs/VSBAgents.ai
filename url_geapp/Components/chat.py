from url_geapp.models import DynamicPage
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from phi.agent import Agent
from phi.model.groq import Groq as GroqPhi

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
            instructions=["Provide concise and helpful responses.", "Use markdown for formatting.","Provide code examples when necessary.","Use bullet points for lists.", "Be polite and professional.", "Avoid unnecessary jargon.", "Be concise and to the point.", "Use emojis to enhance communication.", "Use headings and subheadings for clarity.", "Use tables for data representation when necessary.", "Use code blocks for code examples.", "Use lists for enumerating items.", "Use links for references and further reading.", "Use images for visual representation when necessary.", "Use quotes for citing sources.", "Use footnotes for additional information.", "Use bold and italics for emphasis.", "Use colors for highlighting important information.", "Use animations for engaging content.", "Use audio for auditory learners.", "Use video for visual learners.", "Use interactive elements for engagement.", "Use gamification for motivation.", "Use storytelling for relatability.", "Use humor for light-heartedness.", "Use empathy for understanding.", "Use encouragement for support.", "Use feedback for improvement.", "Use praise for motivation.", "Use criticism for growth.", "Use questions for engagement.", "Use answers for clarity.", "Use examples for illustration.", "Use analogies for understanding.", "Use metaphors for creativity.", "Use similes for comparison.", "Use personification for relatability.", "Use hyperbole for exaggeration.", "Use understatement for subtlety.", "Use irony for humor.", "Use sarcasm for wit.", "Use puns for playfulness.", "Use alliteration for rhythm.", "Use assonance for harmony.", "Use consonance for balance.", "Use onomatopoeia for sound effects.", "Use symbolism for deeper meaning.", "Use imagery for visualization.", "Use foreshadowing for suspense.", "Use flashbacks for context.", "Use cliffhangers for intrigue."],
            
        )
        # Get response from the agent
        response = agent.run(user_message)
        return JsonResponse({'response': response.content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)