# CHANGELOG

## [0.1.0] - 2024-01-XX
### Added
- Initial Django project setup with `vibe_recipes` project
- Created app structure: `accounts`, `recipes`, `community` under `apps/` package
- Added `core/` directory for global templates and static files
- Configured MySQL database connection with environment variables
- Set up Bootstrap 5 via CDN in base template
- Created responsive navigation with Home, Generate, History, Community, Login/Logout
- Added basic home page with three main feature cards
- Configured Django settings for templates, static files, and authentication
- Added requirements.txt with Django, mysqlclient, python-dotenv, Pillow, whitenoise, pytest-django
- Created env.example for environment configuration

## [0.2.0] - 2024-01-XX
### Added
- Complete authentication system with user registration and login
- Created UserRegistrationForm and UserLoginForm with Bootstrap styling
- Added authentication views: register, login, logout, profile
- Created authentication templates: register.html, login.html, profile.html
- Updated navigation to show conditional login/logout and profile links
- Added flash messages for user feedback
- Configured URL routing for authentication endpoints
- Protected profile view with login_required decorator
- Switched to MySQL database configuration
- Added mysqlclient package for MySQL connectivity

## [0.3.0] - 2024-01-XX
### Added
- Complete data models: Ingredient, Recipe, RecipeIngredient, UserRecipeHistory, CommunityPost
- Admin interface with proper list displays, filters, and search functionality
- Django management command for seeding sample data
- Sample ingredients across categories (vegetables, proteins, grains, dairy, herbs & spices)
- Sample recipes from multiple cuisines (Italian, Indian, Ethiopian, Chinese, Mediterranean)
- Many-to-many relationship between recipes and ingredients with quantities
- User recipe history tracking with JSON field for selected ingredients
- Community post model for recipe sharing
- Created superuser account for admin access

## [0.4.0] - 2024-01-XX
### Added
- Complete ingredient selection interface with responsive grid layout
- Search functionality for ingredients with real-time filtering
- Category-based filtering (vegetables, proteins, grains, dairy, herbs, spices, others)
- Cuisine selection dropdown with all available cuisine options
- Interactive ingredient cards with checkboxes and hover effects
- Real-time selection counter showing number of selected ingredients
- Form validation ensuring at least one ingredient and cuisine are selected
- User recipe history tracking for selected ingredients and cuisine preferences
- Updated navigation to link to generate page
- Responsive design with Bootstrap 5 styling

## [0.5.0] - 2024-01-XX
### Added
- **Community Post Reactions System** - Users can now like community recipe posts
- New `PostReaction` model with support for multiple reaction types (like, love, wow, yum)
- Real-time like counting with AJAX-powered interaction
- Interactive like buttons that show current state (liked/not liked)
- Visual feedback with heart icons and color changes
- Loading states and smooth animations for better UX
- Mobile-responsive reaction interface
- CSRF protection for secure reaction handling
- Database migrations for the new reaction system
- Comprehensive testing of reaction functionality
