from django.db import models
from django.contrib.auth.models import User
from apps.recipes.models import Recipe


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"
    
    class Meta:
        ordering = ['-created_at']
