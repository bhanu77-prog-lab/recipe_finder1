import requests
from django.conf import settings
from django.shortcuts import render

def recipe_finder_view(request):
    recipes = []
    error_message = None
    if request.method == 'POST':
        query = request.POST.get('query')
        api_key = settings.RAPID_API_KEY
        url = f"https://tasty.p.rapidapi.com/recipes/list?q={query}&from=0&size=10"
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "tasty.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "results" in data:
                for item in data["results"]:
                    try:
                        recipe = {
                            'title': item.get('name', 'Untitled Recipe'),
                            'ingredients': [
                                component.get('ingredient', {}).get('name', '')
                                for section in item.get('sections', [])
                                for component in section.get('components', [])
                                if component.get('ingredient') and component['ingredient'].get('name')
                            ],
                            'instructions': [
                                step.get('display_text', '') 
                                for step in item.get('instructions', [])
                            ],
                            'image': item.get('thumbnail_url', '')
                        }
                        if recipe['ingredients'] and recipe['instructions']:
                            recipes.append(recipe)
                    except Exception as e:
                        continue
            else:
                error_message = "No recipes found. Please try a different search term."
        except requests.RequestException as e:
            error_message = f"Error fetching recipes: {str(e)}"

    return render(request, 'recipes/index.html', {
        'recipes': recipes,
        'error_message': error_message
    })