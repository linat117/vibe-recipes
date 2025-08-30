from django.contrib import admin
from .models import CommunityPost


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'recipe__title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
