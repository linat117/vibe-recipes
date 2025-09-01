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
    
    def get_like_count(self):
        """Get the total number of likes for this post"""
        return self.reactions.filter(reaction_type='like').count()
    
    def is_liked_by_user(self, user):
        """Check if a specific user has liked this post"""
        if not user.is_authenticated:
            return False
        return self.reactions.filter(user=user, reaction_type='like').exists()
    
    class Meta:
        ordering = ['-created_at']


class PostReaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
        ('yum', 'Yum'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # One user can only have one reaction per post
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} {self.reaction_type}d {self.post.recipe.title}"
