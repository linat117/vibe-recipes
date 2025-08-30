from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.recipes.models import Ingredient, Recipe, RecipeIngredient


class Command(BaseCommand):
    help = 'Seed the database with sample ingredients and recipes'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create ingredients
        ingredients_data = [
            # Vegetables
            ('tomato', 'vegetable'),
            ('onion', 'vegetable'),
            ('garlic', 'vegetable'),
            ('bell pepper', 'vegetable'),
            ('carrot', 'vegetable'),
            ('spinach', 'vegetable'),
            ('mushroom', 'vegetable'),
            ('potato', 'vegetable'),
            ('broccoli', 'vegetable'),
            ('cauliflower', 'vegetable'),
            
            # Proteins
            ('chicken', 'protein'),
            ('beef', 'protein'),
            ('fish', 'protein'),
            ('eggs', 'protein'),
            ('tofu', 'protein'),
            ('lentils', 'protein'),
            ('chickpeas', 'protein'),
            
            # Grains
            ('rice', 'grain'),
            ('pasta', 'grain'),
            ('bread', 'grain'),
            ('quinoa', 'grain'),
            ('couscous', 'grain'),
            
            # Dairy
            ('milk', 'dairy'),
            ('cheese', 'dairy'),
            ('butter', 'dairy'),
            ('yogurt', 'dairy'),
            ('cream', 'dairy'),
            
            # Herbs & Spices
            ('basil', 'herb'),
            ('oregano', 'herb'),
            ('thyme', 'herb'),
            ('rosemary', 'herb'),
            ('cumin', 'spice'),
            ('paprika', 'spice'),
            ('black pepper', 'spice'),
            ('salt', 'spice'),
            ('cinnamon', 'spice'),
            ('ginger', 'spice'),
            
            # Others
            ('olive oil', 'other'),
            ('vegetable oil', 'other'),
            ('honey', 'other'),
            ('sugar', 'other'),
            ('flour', 'other'),
            ('lemon', 'other'),
            ('lime', 'other'),
        ]
        
        ingredients = {}
        for name, category in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={'category': category}
            )
            ingredients[name] = ingredient
            if created:
                self.stdout.write(f'Created ingredient: {name}')
        
        # Create sample recipes
        recipes_data = [
            {
                'title': 'Classic Spaghetti Carbonara',
                'cuisine': 'italian',
                'description': 'A traditional Italian pasta dish with eggs, cheese, and pancetta',
                'instructions': '''1. Cook spaghetti according to package directions
2. In a large pan, cook pancetta until crispy
3. Beat eggs with grated cheese and black pepper
4. Drain pasta and immediately toss with egg mixture
5. Add pancetta and serve immediately''',
                'cooking_time': 20,
                'difficulty': 'medium',
                'ingredients': ['pasta', 'eggs', 'cheese', 'black pepper', 'salt']
            },
            {
                'title': 'Chicken Tikka Masala',
                'cuisine': 'indian',
                'description': 'Creamy and flavorful Indian curry with tender chicken',
                'instructions': '''1. Marinate chicken in yogurt and spices for 30 minutes
2. Grill or bake chicken until cooked through
3. In a pan, sauté onions and garlic
4. Add tomatoes and spices, cook until thickened
5. Add chicken and cream, simmer for 10 minutes''',
                'cooking_time': 45,
                'difficulty': 'medium',
                'ingredients': ['chicken', 'yogurt', 'onion', 'garlic', 'tomato', 'cream', 'cumin', 'paprika']
            },
            {
                'title': 'Ethiopian Doro Wat',
                'cuisine': 'ethiopian',
                'description': 'Spicy Ethiopian chicken stew with berbere spice',
                'instructions': '''1. Sauté onions and garlic in oil
2. Add berbere spice and cook until fragrant
3. Add chicken pieces and cook until browned
4. Add water and simmer until chicken is tender
5. Serve with injera bread''',
                'cooking_time': 60,
                'difficulty': 'hard',
                'ingredients': ['chicken', 'onion', 'garlic', 'paprika', 'black pepper', 'salt']
            },
            {
                'title': 'Simple Vegetable Stir Fry',
                'cuisine': 'chinese',
                'description': 'Quick and healthy vegetable stir fry with soy sauce',
                'instructions': '''1. Heat oil in a wok or large pan
2. Add garlic and ginger, stir fry for 30 seconds
3. Add vegetables and stir fry for 3-4 minutes
4. Add soy sauce and seasonings
5. Serve hot with rice''',
                'cooking_time': 15,
                'difficulty': 'easy',
                'ingredients': ['broccoli', 'carrot', 'bell pepper', 'garlic', 'ginger', 'soy sauce', 'vegetable oil']
            },
            {
                'title': 'Mediterranean Quinoa Salad',
                'cuisine': 'mediterranean',
                'description': 'Fresh and healthy quinoa salad with Mediterranean flavors',
                'instructions': '''1. Cook quinoa according to package directions
2. Chop vegetables and herbs
3. Mix quinoa with vegetables, olives, and feta
4. Dress with olive oil, lemon juice, and herbs
5. Chill for 30 minutes before serving''',
                'cooking_time': 25,
                'difficulty': 'easy',
                'ingredients': ['quinoa', 'tomato', 'cucumber', 'olive oil', 'lemon', 'basil', 'salt']
            }
        ]
        
        for recipe_data in recipes_data:
            ingredients_list = recipe_data.pop('ingredients')
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults=recipe_data
            )
            
            if created:
                # Add ingredients to recipe
                for ingredient_name in ingredients_list:
                    if ingredient_name in ingredients:
                        RecipeIngredient.objects.create(
                            recipe=recipe,
                            ingredient=ingredients[ingredient_name]
                        )
                
                self.stdout.write(f'Created recipe: {recipe.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database!')
        )
