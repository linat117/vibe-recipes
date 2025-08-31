from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CommunityPost
from apps.recipes.models import Recipe


def community_feed(request):
    """Display the public community feed"""
    # Get all community posts, newest first
    posts = CommunityPost.objects.select_related('user', 'recipe').order_by('-created_at')
    
    # Search/filter functionality
    search_query = request.GET.get('search', '')
    cuisine_filter = request.GET.get('cuisine', '')
    
    if search_query:
        posts = posts.filter(
            Q(recipe__title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(recipe__ingredients__name__icontains=search_query)
        ).distinct()
    
    if cuisine_filter:
        posts = posts.filter(recipe__cuisine=cuisine_filter)
    
    # Pagination
    paginator = Paginator(posts, 12)  # 12 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique cuisines for filter dropdown
    cuisines = Recipe.objects.values_list('cuisine', flat=True).distinct().order_by('cuisine')
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'search_query': search_query,
        'cuisine_filter': cuisine_filter,
        'cuisines': cuisines,
    }
    
    return render(request, 'community/feed.html', context)


@login_required
def share_recipe(request, recipe_id):
    """Share a recipe to the community"""
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        description = request.POST.get('description', '').strip()
        
        if not description:
            messages.error(request, 'Please provide a description for your post.')
            return redirect('recipes:recipe_detail', recipe_id=recipe_id)
        
        # Check if user already shared this recipe
        existing_post = CommunityPost.objects.filter(user=request.user, recipe=recipe).first()
        if existing_post:
            messages.warning(request, 'You have already shared this recipe to the community.')
            return redirect('recipes:recipe_detail', recipe_id=recipe_id)
        
        # Create the community post
        CommunityPost.objects.create(
            user=request.user,
            recipe=recipe,
            description=description
        )
        
        messages.success(request, 'Recipe shared to community successfully!')
        return redirect('community:feed')
    
    # GET request - show share form
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'community/share_recipe.html', context)


@login_required
def delete_post(request, post_id):
    """Delete a community post (only by the author)"""
    if request.method == 'POST':
        post = get_object_or_404(CommunityPost, id=post_id, user=request.user)
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('community:feed')
    
    return redirect('community:feed')
