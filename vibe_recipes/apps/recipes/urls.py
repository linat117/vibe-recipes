from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('generate/', views.generate_recipe_view, name='generate'),
    path('search-ingredients/', views.search_ingredients, name='search_ingredients'),
    path('<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
    path('history/', views.history_view, name='history'),
    path('history/delete/<int:history_id>/', views.delete_history_item, name='delete_history_item'),
]
