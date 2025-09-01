from django.shortcuts import render
from django.contrib.auth.models import User
from apps.recipes.models import Recipe, Ingredient
from apps.community.models import CommunityPost


def home(request):
    """
    Home page view with real-time statistics from database
    """
    # Get real statistics from database
    recipes_count = Recipe.objects.count()
    ingredients_count = Ingredient.objects.count()
    cuisines_count = Recipe.objects.values('cuisine').distinct().count()
    users_count = User.objects.count()
    
    stats = {
        'recipes_count': recipes_count,
        'ingredients_count': ingredients_count,
        'cuisines_count': cuisines_count,
        'users_count': users_count,
    }
    
    # Get additional statistics for CTA section
    cta_stats = {
        'total_recipes': recipes_count,
        'total_users': users_count,
        'average_rating': 4.9,  # This could be calculated from actual ratings if you have them
        'response_time': 24,  # This could be calculated from actual response times
    }
    
    # Debug output
    print(f"DEBUG - Recipes: {recipes_count}, Ingredients: {ingredients_count}, Cuisines: {cuisines_count}, Users: {users_count}")
    print(f"DEBUG - Context stats: {stats}")
    print(f"DEBUG - Context cta_stats: {cta_stats}")
    
    context = {
        'stats': stats,
        'cta_stats': cta_stats,
        'test_var': 'VIEW_IS_WORKING',
    }
    
    print(f"DEBUG - Final context: {context}")
    
    return render(request, 'home.html', context)
