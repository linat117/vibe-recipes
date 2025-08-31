from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_feed, name='feed'),
    path('share/<int:recipe_id>/', views.share_recipe, name='share_recipe'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
