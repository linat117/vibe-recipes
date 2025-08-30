from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    CUISINE_CHOICES = [
        ('italian', 'Italian'),
        ('indian', 'Indian'),
        ('ethiopian', 'Ethiopian'),
        ('mexican', 'Mexican'),
        ('chinese', 'Chinese'),
        ('japanese', 'Japanese'),
        ('french', 'French'),
        ('mediterranean', 'Mediterranean'),
        ('american', 'American'),
        ('thai', 'Thai'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField()
    cooking_time = models.IntegerField(help_text="Cooking time in minutes", blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_generated = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.name}"


class UserRecipeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    selected_ingredients = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Recipe Histories"
