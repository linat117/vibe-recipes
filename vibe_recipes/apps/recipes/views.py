from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Ingredient, Recipe, RecipeIngredient, UserRecipeHistory
from .services.generator import generate_recipe


def generate_recipe_view(request):
    if request.method == 'POST':
        selected_ingredients = request.POST.getlist('ingredients')
        selected_cuisine = request.POST.get('cuisine')
        
        if not selected_ingredients:
            messages.error(request, 'Please select at least one ingredient.')
            return redirect('recipes:generate')
        
        try:
            # Convert ingredient IDs to integers
            ingredient_ids = [int(ing_id) for ing_id in selected_ingredients]
            
            # Generate recipe using the service
            recipe, metadata = generate_recipe(ingredient_ids, selected_cuisine, request.user)
            
            # Redirect to recipe detail page
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
            
        except Exception as e:
            messages.error(request, f'Error generating recipe: {str(e)}')
            return redirect('recipes:generate')
    
    # GET request - show ingredient selection form
    ingredients = Ingredient.objects.all().order_by('category', 'name')
    
    # Group ingredients by category
    ingredients_by_category = {}
    for ingredient in ingredients:
        category = ingredient.category or 'Other'
        if category not in ingredients_by_category:
            ingredients_by_category[category] = []
        ingredients_by_category[category].append(ingredient)
    
    context = {
        'ingredients_by_category': ingredients_by_category,
        'cuisine_choices': Recipe.CUISINE_CHOICES,
    }
    
    return render(request, 'recipes/generate.html', context)


def search_ingredients(request):
    """AJAX endpoint for ingredient search"""
    query = request.GET.get('q', '').lower()
    category = request.GET.get('category', '')
    
    ingredients = Ingredient.objects.all()
    
    if query:
        ingredients = ingredients.filter(name__icontains=query)
    
    if category:
        ingredients = ingredients.filter(category=category)
    
    ingredients = ingredients.order_by('name')[:20]  # Limit results
    
    data = [{'id': ing.id, 'name': ing.name, 'category': ing.category} for ing in ingredients]
    return JsonResponse({'ingredients': data})


def recipe_detail_view(request, recipe_id):
    """Display recipe details"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Get recipe ingredients with quantities
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient')
    
    # Get cuisine display name
    cuisine_display = dict(Recipe.CUISINE_CHOICES).get(recipe.cuisine, recipe.cuisine.title())
    
    # Get difficulty display name
    difficulty_display = dict(Recipe.DIFFICULTY_CHOICES).get(recipe.difficulty, recipe.difficulty.title())
    
    context = {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients,
        'cuisine_display': cuisine_display,
        'difficulty_display': difficulty_display,
    }
    
    return render(request, 'recipes/recipe_detail.html', context)
