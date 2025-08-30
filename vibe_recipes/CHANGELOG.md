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
