from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import CommunityPost, PostReaction
from apps.recipes.models import Recipe


def test_community(request):
    """Simple test view to debug community feed"""
    try:
        # Get posts directly
        posts = CommunityPost.objects.select_related('user', 'recipe').order_by('-created_at')[:5]
        
        # Simple context
        context = {
            'posts': posts,
            'post_count': posts.count(),
            'debug_info': f"Found {posts.count()} posts"
        }
        
        return render(request, 'community/test.html', context)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'error_type': type(e).__name__
        })


def debug_community(request):
    """Debug view to test community functionality"""
    try:
        posts = CommunityPost.objects.select_related('user', 'recipe').order_by('-created_at')[:5]
        
        # Test adding properties
        for post in posts:
            post.like_count = post.get_like_count()
            if request.user.is_authenticated:
                post.is_liked_by_current_user = post.is_liked_by_user(request.user)
        
        context = {
            'posts': posts,
            'debug_info': {
                'total_posts': CommunityPost.objects.count(),
                'user_authenticated': request.user.is_authenticated,
                'post_properties': [f"{post.recipe.title}: like_count={getattr(post, 'like_count', 'MISSING')}" for post in posts]
            }
        }
        
        return render(request, 'community/debug.html', context)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'error_type': type(e).__name__,
            'traceback': str(e.__traceback__) if hasattr(e, '__traceback__') else 'No traceback'
        })


def community_feed(request):
    """Display the public community feed"""
    try:
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
        
        # Add properties to paginated posts
        for post in page_obj:
            try:
                post.like_count = post.get_like_count()
                if request.user.is_authenticated:
                    post.is_liked_by_current_user = post.is_liked_by_user(request.user)
                else:
                    post.is_liked_by_current_user = False
            except Exception as e:
                # Fallback values if there's an error
                post.like_count = 0
                post.is_liked_by_current_user = False
                print(f"Error processing post {post.id}: {e}")
        
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
        
    except Exception as e:
        # Return error context for debugging
        context = {
            'error': str(e),
            'error_type': type(e).__name__,
            'posts': [],
            'page_obj': None,
            'search_query': '',
            'cuisine_filter': '',
            'cuisines': [],
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


@login_required
def toggle_reaction(request, post_id):
    """Toggle like/unlike reaction on a community post"""
    if request.method == 'POST':
        post = get_object_or_404(CommunityPost, id=post_id)
        reaction_type = request.POST.get('reaction_type', 'like')
        
        # Check if user already has a reaction
        existing_reaction = PostReaction.objects.filter(user=request.user, post=post).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Remove reaction (unlike)
                existing_reaction.delete()
                action = 'removed'
            else:
                # Change reaction type
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                action = 'updated'
        else:
            # Create new reaction
            PostReaction.objects.create(
                user=request.user,
                post=post,
                reaction_type=reaction_type
            )
            action = 'added'
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'action': action,
                'like_count': post.get_like_count(),
                'is_liked': post.is_liked_by_user(request.user),
                'reaction_type': reaction_type if action != 'removed' else None
            })
        
        # Redirect for non-AJAX requests
        messages.success(request, f'Reaction {action} successfully!')
        return redirect('community:feed')
    
    return redirect('community:feed')
