from django.core.management.base import BaseCommand
from apps.recipes.models import Ingredient, Cuisine, Recipe
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Load sample data for the recipe generator'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Loading sample data...')
        
        # Create sample ingredients
        ingredients_data = [
            'Chicken', 'Beef', 'Pork', 'Fish', 'Shrimp', 'Eggs', 'Milk', 'Cheese',
            'Onion', 'Garlic', 'Tomato', 'Bell Pepper', 'Carrot', 'Broccoli', 'Spinach',
            'Rice', 'Pasta', 'Bread', 'Potato', 'Sweet Potato', 'Mushroom', 'Lemon',
            'Olive Oil', 'Butter', 'Salt', 'Black Pepper', 'Basil', 'Oregano', 'Thyme',
            'Chili Powder', 'Cumin', 'Paprika', 'Ginger', 'Cinnamon', 'Vanilla',
            'Honey', 'Sugar', 'Flour', 'Baking Powder', 'Baking Soda', 'Chocolate',
            'Nuts', 'Seeds', 'Avocado', 'Cucumber', 'Lettuce', 'Cabbage', 'Corn',
            'Peas', 'Beans', 'Lentils', 'Quinoa', 'Oats', 'Banana', 'Apple', 'Orange'
        ]
        
        for ingredient_name in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            if created:
                self.stdout.write(f'✅ Created ingredient: {ingredient_name}')
        
        # Create sample cuisines
        cuisines_data = [
            'Italian', 'Mexican', 'Chinese', 'Indian', 'Japanese', 'Thai', 'French',
            'Mediterranean', 'American', 'Greek', 'Spanish', 'Korean', 'Vietnamese',
            'Moroccan', 'Turkish', 'Lebanese', 'Persian', 'Russian', 'German', 'British'
        ]
        
        for cuisine_name in cuisines_data:
            cuisine, created = Cuisine.objects.get_or_create(name=cuisine_name)
            if created:
                self.stdout.write(f'✅ Created cuisine: {cuisine_name}')
        
        # Create sample recipes
        sample_recipes = [
            {
                'title': 'Simple Pasta with Tomato Sauce',
                'description': 'A classic Italian pasta dish with rich tomato sauce',
                'instructions': '1. Cook pasta according to package directions\n2. Heat olive oil and sauté garlic\n3. Add tomatoes and simmer\n4. Toss with pasta and serve',
                'cooking_time': 20,
                'difficulty': 'Easy',
                'cuisine': 'Italian',
                'ingredients': ['Pasta', 'Tomato', 'Garlic', 'Olive Oil', 'Basil', 'Salt', 'Black Pepper']
            },
            {
                'title': 'Chicken Stir Fry',
                'description': 'Quick and healthy chicken stir fry with vegetables',
                'instructions': '1. Cut chicken into pieces\n2. Stir fry chicken until golden\n3. Add vegetables and stir fry\n4. Season with soy sauce and serve',
                'cooking_time': 25,
                'difficulty': 'Medium',
                'cuisine': 'Chinese',
                'ingredients': ['Chicken', 'Bell Pepper', 'Broccoli', 'Carrot', 'Garlic', 'Soy Sauce', 'Oil']
            }
        ]
        
        for recipe_data in sample_recipes:
            cuisine = Cuisine.objects.get(name=recipe_data['cuisine'])
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults={
                    'description': recipe_data['description'],
                    'instructions': recipe_data['instructions'],
                    'cooking_time': recipe_data['cooking_time'],
                    'difficulty': recipe_data['difficulty'],
                    'cuisine': cuisine
                }
            )
            
            if created:
                # Add ingredients to recipe
                for ingredient_name in recipe_data['ingredients']:
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    recipe.ingredients.add(ingredient)
                
                self.stdout.write(f'✅ Created recipe: {recipe_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('🎉 Sample data loaded successfully!'))
        self.stdout.write(f'📊 Created {Ingredient.objects.count()} ingredients')
        self.stdout.write(f'📊 Created {Cuisine.objects.count()} cuisines')
        self.stdout.write(f'📊 Created {Recipe.objects.count()} recipes')
