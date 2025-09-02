from django.core.management.base import BaseCommand
from apps.recipes.models import Ingredient, Recipe

class Command(BaseCommand):
    help = 'Load sample data for the recipe generator'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Loading sample data...')
        
        # Create sample ingredients with categories
        ingredients_data = [
            # Meat & Protein
            ('Chicken', 'meat'), ('Beef', 'meat'), ('Pork', 'meat'), ('Fish', 'meat'), 
            ('Shrimp', 'meat'), ('Eggs', 'protein'),
            
            # Dairy
            ('Milk', 'dairy'), ('Cheese', 'dairy'), ('Butter', 'dairy'),
            
            # Vegetables
            ('Onion', 'vegetable'), ('Garlic', 'vegetable'), ('Tomato', 'vegetable'), 
            ('Bell Pepper', 'vegetable'), ('Carrot', 'vegetable'), ('Broccoli', 'vegetable'), 
            ('Spinach', 'vegetable'), ('Potato', 'vegetable'), ('Sweet Potato', 'vegetable'), 
            ('Mushroom', 'vegetable'), ('Avocado', 'vegetable'), ('Cucumber', 'vegetable'), 
            ('Lettuce', 'vegetable'), ('Cabbage', 'vegetable'), ('Corn', 'vegetable'),
            
            # Grains & Starches
            ('Rice', 'grain'), ('Pasta', 'grain'), ('Bread', 'grain'), ('Quinoa', 'grain'), 
            ('Oats', 'grain'), ('Beans', 'grain'), ('Lentils', 'grain'),
            
            # Fruits
            ('Lemon', 'fruit'), ('Banana', 'fruit'), ('Apple', 'fruit'), ('Orange', 'fruit'),
            
            # Oils & Fats
            ('Olive Oil', 'oil'),
            
            # Seasonings & Spices
            ('Salt', 'seasoning'), ('Black Pepper', 'seasoning'), ('Basil', 'herb'), 
            ('Oregano', 'herb'), ('Thyme', 'herb'), ('Chili Powder', 'spice'), 
            ('Cumin', 'spice'), ('Paprika', 'spice'), ('Ginger', 'spice'), 
            ('Cinnamon', 'spice'), ('Vanilla', 'flavoring'),
            
            # Sweeteners
            ('Honey', 'sweetener'), ('Sugar', 'sweetener'),
            
            # Baking
            ('Flour', 'baking'), ('Baking Powder', 'baking'), ('Baking Soda', 'baking'),
            
            # Other
            ('Chocolate', 'other'), ('Nuts', 'other'), ('Seeds', 'other'), 
            ('Peas', 'vegetable'), ('Soy Sauce', 'condiment'), ('Vinegar', 'condiment'), 
            ('Mustard', 'condiment'), ('Ketchup', 'condiment'), ('Mayonnaise', 'condiment'), 
            ('Hot Sauce', 'condiment'), ('Coconut Milk', 'other')
        ]
        
        for ingredient_name, category in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={'category': category}
            )
            if created:
                self.stdout.write(f'✅ Created ingredient: {ingredient_name} ({category})')
            else:
                # Update existing ingredient with category
                ingredient.category = category
                ingredient.save()
                self.stdout.write(f'🔄 Updated ingredient: {ingredient_name} ({category})')
        
        # Create sample recipes
        sample_recipes = [
            {
                'title': 'Simple Pasta with Tomato Sauce',
                'description': 'A classic Italian pasta dish with rich tomato sauce',
                'instructions': '1. Cook pasta according to package directions\n2. Heat olive oil and sauté garlic\n3. Add tomatoes and simmer\n4. Toss with pasta and serve',
                'cooking_time': 20,
                'difficulty': 'easy',
                'cuisine': 'italian',
                'ingredients': ['Pasta', 'Tomato', 'Garlic', 'Olive Oil', 'Basil', 'Salt', 'Black Pepper']
            },
            {
                'title': 'Chicken Stir Fry',
                'description': 'Quick and healthy chicken stir fry with vegetables',
                'instructions': '1. Cut chicken into pieces\n2. Stir fry chicken until golden\n3. Add vegetables and stir fry\n4. Season with soy sauce and serve',
                'cooking_time': 25,
                'difficulty': 'medium',
                'cuisine': 'chinese',
                'ingredients': ['Chicken', 'Bell Pepper', 'Broccoli', 'Carrot', 'Garlic', 'Soy Sauce', 'Olive Oil']
            },
            {
                'title': 'Scrambled Eggs with Herbs',
                'description': 'Fluffy scrambled eggs with fresh herbs and cheese',
                'instructions': '1. Beat eggs in a bowl\n2. Heat butter in pan\n3. Add eggs and stir gently\n4. Add cheese and herbs\n5. Serve immediately',
                'cooking_time': 10,
                'difficulty': 'easy',
                'cuisine': 'american',
                'ingredients': ['Eggs', 'Butter', 'Cheese', 'Basil', 'Salt', 'Black Pepper']
            },
            {
                'title': 'Vegetable Curry',
                'description': 'Spicy vegetable curry with rice',
                'instructions': '1. Sauté onions and garlic\n2. Add vegetables and spices\n3. Simmer with coconut milk\n4. Serve over rice',
                'cooking_time': 30,
                'difficulty': 'medium',
                'cuisine': 'indian',
                'ingredients': ['Onion', 'Garlic', 'Carrot', 'Broccoli', 'Rice', 'Cumin', 'Chili Powder', 'Coconut Milk']
            }
        ]
        
        for recipe_data in sample_recipes:
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults={
                    'description': recipe_data['description'],
                    'instructions': recipe_data['instructions'],
                    'cooking_time': recipe_data['cooking_time'],
                    'difficulty': recipe_data['difficulty'],
                    'cuisine': recipe_data['cuisine']
                }
            )
            
            if created:
                # Add ingredients to recipe
                for ingredient_name in recipe_data['ingredients']:
                    try:
                        ingredient = Ingredient.objects.get(name=ingredient_name)
                        recipe.ingredients.add(ingredient)
                    except Ingredient.DoesNotExist:
                        self.stdout.write(f'⚠️ Ingredient not found: {ingredient_name}')
                
                self.stdout.write(f'✅ Created recipe: {recipe_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('🎉 Sample data loaded successfully!'))
        self.stdout.write(f'📊 Created {Ingredient.objects.count()} ingredients with categories')
        self.stdout.write(f'📊 Created {Recipe.objects.count()} recipes')
        
        # Show category breakdown
        from django.db.models import Count
        category_counts = Ingredient.objects.values('category').annotate(count=Count('id')).order_by('category')
        self.stdout.write('📊 Category breakdown:')
        for cat in category_counts:
            self.stdout.write(f'   {cat["category"]}: {cat["count"]} ingredients')
