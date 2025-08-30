from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, UserRecipeHistory


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'cuisine', 'difficulty', 'cooking_time', 'is_generated', 'created_at']
    list_filter = ['cuisine', 'difficulty', 'is_generated', 'created_at']
    search_fields = ['title', 'description', 'instructions']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RecipeIngredientInline]
    ordering = ['-created_at']


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'quantity', 'unit']
    list_filter = ['ingredient__category']
    search_fields = ['recipe__title', 'ingredient__name']


@admin.register(UserRecipeHistory)
class UserRecipeHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'recipe__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
