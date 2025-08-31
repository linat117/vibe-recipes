from typing import List, Dict, Optional, Tuple
from django.db.models import Q, Count
from apps.recipes.models import Ingredient, Recipe, RecipeIngredient, UserRecipeHistory
from .spoonacular import get_spoonacular_recipes, create_recipe_from_spoonacular


# Substitution dictionary for common ingredient replacements
SUBSTITUTIONS = {
    'cream': ['milk', 'butter'],
    'milk': ['cream', 'yogurt'],
    'butter': ['olive oil', 'vegetable oil'],
    'beef': ['mushroom', 'tofu', 'lentils'],
    'chicken': ['tofu', 'mushroom', 'chickpeas'],
    'eggs': ['flax seeds', 'banana'],
    'cheese': ['nutritional yeast', 'tofu'],
    'garlic': ['garlic powder', 'onion'],
    'onion': ['garlic', 'shallot'],
    'tomato': ['bell pepper', 'carrot'],
    'pasta': ['rice', 'quinoa'],
    'rice': ['quinoa', 'couscous'],
    'bread': ['tortilla', 'lettuce'],
}


def get_ingredient_coverage(recipe: Recipe, selected_ingredients: List[int]) -> Tuple[float, int, int]:
    """
    Calculate ingredient coverage for a recipe.
    Returns: (coverage_ratio, matching_ingredients, missing_ingredients)
    """
    if not selected_ingredients:
        return 0.0, 0, 0
    
    recipe_ingredients = set(recipe.ingredients.values_list('id', flat=True))
    selected_set = set(selected_ingredients)
    
    matching = len(recipe_ingredients.intersection(selected_set))
    missing = len(recipe_ingredients - selected_set)
    
    coverage = matching / len(selected_set) if selected_set else 0
    
    return coverage, matching, missing


def find_substitutions(missing_ingredients: List[str], available_ingredients: List[str]) -> Dict[str, List[str]]:
    """
    Find possible substitutions for missing ingredients.
    """
    substitutions = {}
    
    for missing in missing_ingredients:
        missing_lower = missing.lower()
        if missing_lower in SUBSTITUTIONS:
            possible_subs = []
            for sub in SUBSTITUTIONS[missing_lower]:
                if sub in available_ingredients:
                    possible_subs.append(sub)
            if possible_subs:
                substitutions[missing] = possible_subs
    
    return substitutions


def match_recipe(selected_ingredients: List[int], cuisine: Optional[str] = None) -> Optional[Recipe]:
    """
    Find the best matching recipe based on ingredient coverage and cuisine.
    """
    # Get all recipes
    recipes = Recipe.objects.all()
    
    # Filter by cuisine if specified
    if cuisine:
        recipes = recipes.filter(cuisine=cuisine)
    
    best_recipe = None
    best_coverage = 0
    best_missing = float('inf')
    best_cooking_time = float('inf')
    
    for recipe in recipes:
        coverage, matching, missing = get_ingredient_coverage(recipe, selected_ingredients)
        
        # Skip recipes with no matching ingredients
        if matching == 0:
            continue
        
        # Prefer higher coverage, fewer missing ingredients, and lower cooking time
        if (coverage > best_coverage or 
            (coverage == best_coverage and missing < best_missing) or
            (coverage == best_coverage and missing == best_missing and 
             (recipe.cooking_time or 0) < best_cooking_time)):
            
            best_recipe = recipe
            best_coverage = coverage
            best_missing = missing
            best_cooking_time = recipe.cooking_time or 0
    
    return best_recipe


def synthesize_recipe(selected_ingredients: List[int], cuisine: str) -> Recipe:
    """
    Create a new recipe based on ONLY the selected ingredients and cuisine.
    """
    # Get ingredient names
    ingredients = Ingredient.objects.filter(id__in=selected_ingredients)
    ingredient_names = [ing.name.title() for ing in ingredients]
    
    # Create title based on selected ingredients
    if len(ingredient_names) == 1:
        title = f"{cuisine.title()} {ingredient_names[0]} Recipe"
    elif len(ingredient_names) <= 3:
        title = f"{cuisine.title()} {' '.join(ingredient_names)}"
    else:
        # Use key ingredients (first 3) for title
        key_ingredients = ingredient_names[:3]
        title = f"{cuisine.title()} {' '.join(key_ingredients)} Medley"
    
    # Generate instructions template
    instructions = generate_instructions(ingredients, cuisine)
    
    # Estimate cooking time based on number of ingredients
    cooking_time = min(30 + len(ingredients) * 5, 90)  # 30-90 minutes
    
    # Determine difficulty
    if len(ingredients) <= 3:
        difficulty = 'easy'
    elif len(ingredients) <= 6:
        difficulty = 'medium'
    else:
        difficulty = 'hard'
    
    # Create the recipe
    recipe = Recipe.objects.create(
        title=title,
        cuisine=cuisine,
        description=f"A delicious {cuisine} recipe made with {', '.join(ingredient_names).lower()}.",
        instructions=instructions,
        cooking_time=cooking_time,
        difficulty=difficulty,
        is_generated=True
    )
    
    # Add ingredients to recipe
    for ingredient in ingredients:
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient
        )
    
    return recipe


def generate_instructions(ingredients: List[Ingredient], cuisine: str) -> str:
    """
    Generate cooking instructions based on ONLY the selected ingredients and cuisine.
    """
    # Group ingredients by category
    categories = {}
    for ing in ingredients:
        cat = ing.category or 'other'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ing.name)
    
    instructions = []
    
    # Step 1: Preparation
    prep_steps = []
    if 'vegetable' in categories:
        prep_steps.append(f"Wash and chop {', '.join(categories['vegetable'])}")
    if 'protein' in categories:
        prep_steps.append(f"Prepare {', '.join(categories['protein'])}")
    if 'grain' in categories:
        prep_steps.append(f"Cook {', '.join(categories['grain'])} according to package directions")
    if 'dairy' in categories:
        prep_steps.append(f"Prepare {', '.join(categories['dairy'])}")
    if 'spice' in categories:
        prep_steps.append(f"Measure out {', '.join(categories['spice'])}")
    if 'herb' in categories:
        prep_steps.append(f"Wash and chop {', '.join(categories['herb'])}")
    
    if prep_steps:
        instructions.append("1. Preparation:\n   " + "\n   ".join(prep_steps))
    
    # Step 2: Cooking base
    base_steps = []
    # Only mention oil/butter if we have ingredients that need cooking
    has_cookable_ingredients = any(cat in categories for cat in ['vegetable', 'protein', 'grain'])
    
    if has_cookable_ingredients:
        if 'vegetable' in categories and any(name in ['onion', 'garlic'] for name in categories['vegetable']):
            base_steps.append("Heat oil in a pan and sauté onions and garlic until fragrant")
        elif 'protein' in categories:
            base_steps.append(f"Cook {categories['protein'][0]} in oil until done")
        elif 'vegetable' in categories:
            base_steps.append(f"Sauté {categories['vegetable'][0]} in oil until tender")
        else:
            base_steps.append("Heat oil in a pan")
    
    if base_steps:
        instructions.append("2. Cooking:\n   " + "\n   ".join(base_steps))
    
    # Step 3: Combining
    combine_steps = []
    if 'vegetable' in categories and len(categories['vegetable']) > 1:
        # If we have multiple vegetables, add them in sequence
        for veg in categories['vegetable'][1:]:  # Skip the first one if it was already cooked
            combine_steps.append(f"Add {veg} and cook until tender")
    elif 'vegetable' in categories and not any(name in ['onion', 'garlic'] for name in categories['vegetable']):
        combine_steps.append(f"Add {', '.join(categories['vegetable'])} and cook until tender")
    
    if 'dairy' in categories:
        combine_steps.append(f"Stir in {', '.join(categories['dairy'])}")
    
    if 'spice' in categories:
        combine_steps.append(f"Season with {', '.join(categories['spice'])}")
    
    if combine_steps:
        instructions.append("3. Combining:\n   " + "\n   ".join(combine_steps))
    
    # Step 4: Finishing
    finish_steps = []
    if 'herb' in categories:
        finish_steps.append(f"Garnish with {', '.join(categories['herb'])}")
    
    finish_steps.append("Serve hot and enjoy!")
    instructions.append("4. Finishing:\n   " + "\n   ".join(finish_steps))
    
    return "\n\n".join(instructions)


def generate_recipe(selected_ingredients: List[int], cuisine: str, user=None) -> Tuple[Recipe, Dict]:
    """
    Main function to generate a recipe. Returns (recipe, metadata).
    """
    try:
        # Validate inputs
        if not selected_ingredients:
            raise ValueError("No ingredients selected")
        
        if not cuisine:
            raise ValueError("No cuisine selected")
        
        # First, try to get recipes from Spoonacular API
        spoonacular_recipes = get_spoonacular_recipes(selected_ingredients, cuisine)
        
        if spoonacular_recipes:
            # Use the best Spoonacular recipe
            best_recipe_data = spoonacular_recipes[0]
            recipe = create_recipe_from_spoonacular(best_recipe_data, selected_ingredients, user)
            
            metadata = {
                'type': 'spoonacular',
                'source': best_recipe_data.get('source_name', 'Spoonacular'),
                'source_url': best_recipe_data.get('source_url', ''),
                'coverage': 1.0,
                'missing_ingredients': [],
                'substitutions': {},
                'available_recipes': len(spoonacular_recipes)
            }
        else:
            # Fallback to local recipe matching
            matched_recipe = match_recipe(selected_ingredients, cuisine)
            
            if matched_recipe:
                # Use existing recipe
                recipe = matched_recipe
                coverage, matching, missing = get_ingredient_coverage(recipe, selected_ingredients)
                
                # Get missing ingredients
                recipe_ingredients = set(recipe.ingredients.values_list('name', flat=True))
                selected_names = set(Ingredient.objects.filter(id__in=selected_ingredients).values_list('name', flat=True))
                missing_ingredients = list(recipe_ingredients - selected_names)
                
                # Find substitutions
                substitutions = find_substitutions(missing_ingredients, list(selected_names))
                
                metadata = {
                    'type': 'matched',
                    'coverage': coverage,
                    'missing_ingredients': missing_ingredients,
                    'substitutions': substitutions
                }
            else:
                # Create new recipe
                recipe = synthesize_recipe(selected_ingredients, cuisine)
                metadata = {
                    'type': 'generated',
                    'coverage': 1.0,
                    'missing_ingredients': [],
                    'substitutions': {}
                }
        
        # Save to user history if user is logged in
        if user and user.is_authenticated:
            UserRecipeHistory.objects.create(
                user=user,
                recipe=recipe,
                selected_ingredients={
                    'ingredients': selected_ingredients,
                    'cuisine': cuisine,
                    'metadata': metadata
                }
            )
        
        return recipe, metadata
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in generate_recipe: {str(e)}")
        raise
