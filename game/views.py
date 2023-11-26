from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json
import time
# Import the necessary function from threads.py
from .services.threads import run_autogen_chat, run_stable_diffusion

def game_view(request):
    # Start the game when the page loads
    combined_game_text = run_autogen_chat()  # Get the combined text from the chat
    timestamp = int(time.time())  # Current timestamp for cache busting
    context = {'game_text': combined_game_text, 'timestamp': timestamp}
    return render(request, 'game.html', context)

def game_api(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        data = json.loads(request.body)
        user_input = data.get('user_input')

        # Check if user_input is provided
        if not user_input:
            return HttpResponseBadRequest("User input is missing.")

        # Run threads.py functions with user_input
        combined_game_text = run_autogen_chat(user_input)  # You might need to modify the function to accept and process user_input
        
        return JsonResponse({'game_text': combined_game_text})
    else:
        return HttpResponseBadRequest("Invalid request method.")
