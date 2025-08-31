import requests
import logging
from typing import List, Dict, Optional
from django.conf import settings
from apps.recipes.models import Ingredient, Recipe, RecipeIngredient

logger = logging.getLogger(__name__)


class SpoonacularAPI:
    """Service class for interacting with Spoonacular API"""
    
    def __init__(self):
        self.api_key = settings.SPOONACULAR_API_KEY
        self.base_url = settings.SPOONACULAR_BASE_URL
        
    def search_recipes_by_ingredients(self, ingredient_names: List[str], cuisine: str = None, max_results: int = 5) -> List[Dict]:
        """
        Search for recipes using the selected ingredients
        """
        if not self.api_key:
            logger.warning("Spoonacular API key not configured")
            return []
            
        try:
            # Prepare ingredients string (comma-separated)
            ingredients_str = ','.join(ingredient_names)
            
            # Build API parameters
            params = {
                'apiKey': self.api_key,
                'ingredients': ingredients_str,
                'number': max_results,
                'ranking': 2,  # Maximize used ingredients
                'ignorePantry': True,  # Ignore common pantry items
            }
            
            # Add cuisine filter if specified
            if cuisine and cuisine != 'other':
                params['cuisine'] = cuisine
            
            # Make API request
            url = f"{self.base_url}/findByIngredients"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            recipes_data = response.json()
            
            # Get detailed recipe information for each recipe
            detailed_recipes = []
            for recipe in recipes_data[:3]:  # Limit to top 3 results
                detailed_recipe = self.get_recipe_details(recipe['id'])
                if detailed_recipe:
                    detailed_recipes.append(detailed_recipe)
            
            return detailed_recipes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching recipes from Spoonacular: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Spoonacular API: {str(e)}")
            return []
    
    def get_recipe_details(self, recipe_id: int) -> Optional[Dict]:
        """
        Get detailed recipe information including instructions and image
        """
        try:
            params = {
                'apiKey': self.api_key,
            }
            
            url = f"{self.base_url}/{recipe_id}/information"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            recipe_data = response.json()
            
            # Extract relevant information
            return {
                'id': recipe_data.get('id'),
                'title': recipe_data.get('title'),
                'image': recipe_data.get('image'),
                'instructions': recipe_data.get('instructions', ''),
                'ready_in_minutes': recipe_data.get('readyInMinutes', 30),
                'servings': recipe_data.get('servings', 4),
                'cuisine': self._extract_cuisine(recipe_data),
                'ingredients': self._extract_ingredients(recipe_data),
                'source_url': recipe_data.get('sourceUrl', ''),
                'source_name': recipe_data.get('sourceName', ''),
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching recipe details for ID {recipe_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting recipe details: {str(e)}")
            return None
    
    def _extract_cuisine(self, recipe_data: Dict) -> str:
        """Extract cuisine from recipe data"""
        cuisines = recipe_data.get('cuisines', [])
        if cuisines:
            # Map Spoonacular cuisines to our cuisine choices
            cuisine_mapping = {
                'italian': 'italian',
                'indian': 'indian',
                'mexican': 'mexican',
                'chinese': 'chinese',
                'japanese': 'japanese',
                'french': 'french',
                'mediterranean': 'mediterranean',
                'american': 'american',
                'thai': 'thai',
            }
            
            for cuisine in cuisines:
                if cuisine.lower() in cuisine_mapping:
                    return cuisine_mapping[cuisine.lower()]
        
        return 'other'
    
    def _extract_ingredients(self, recipe_data: Dict) -> List[Dict]:
        """Extract ingredients from recipe data"""
        ingredients = []
        for ingredient in recipe_data.get('extendedIngredients', []):
            ingredients.append({
                'name': ingredient.get('name', '').lower(),
                'amount': ingredient.get('amount'),
                'unit': ingredient.get('unit'),
                'original': ingredient.get('original', ''),
            })
        return ingredients


def create_recipe_from_spoonacular(recipe_data: Dict, selected_ingredients: List[int], user=None) -> Recipe:
    """
    Create a Recipe object from Spoonacular data
    """
    # Determine difficulty based on cooking time
    cooking_time = recipe_data.get('ready_in_minutes', 30)
    if cooking_time <= 30:
        difficulty = 'easy'
    elif cooking_time <= 60:
        difficulty = 'medium'
    else:
        difficulty = 'hard'
    
    # Create the recipe
    recipe = Recipe.objects.create(
        title=recipe_data.get('title', 'Unknown Recipe'),
        cuisine=recipe_data.get('cuisine', 'other'),
        description=f"A delicious recipe from {recipe_data.get('source_name', 'Spoonacular')}",
        instructions=recipe_data.get('instructions', ''),
        cooking_time=cooking_time,
        difficulty=difficulty,
        image_url=recipe_data.get('image', ''),
        is_generated=True
    )
    
    # Add ingredients to recipe
    for ingredient_info in recipe_data.get('ingredients', []):
        ingredient_name = ingredient_info.get('name', '').lower()
        
        # Try to find existing ingredient or create new one
        ingredient, created = Ingredient.objects.get_or_create(
            name=ingredient_name,
            defaults={'category': 'other'}
        )
        
        # Create recipe ingredient relationship
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=str(ingredient_info.get('amount', '')),
            unit=ingredient_info.get('unit', '')
        )
    
    return recipe


def get_spoonacular_recipes(selected_ingredients: List[int], cuisine: str) -> List[Dict]:
    """
    Main function to get recipes from Spoonacular API
    """
    api = SpoonacularAPI()
    
    # Get ingredient names
    ingredients = Ingredient.objects.filter(id__in=selected_ingredients)
    ingredient_names = [ing.name for ing in ingredients]
    
    # Search for recipes
    recipes = api.search_recipes_by_ingredients(ingredient_names, cuisine)
    
    return recipes
