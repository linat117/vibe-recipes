# 🚀 Recipe Generator - Deployment Guide

## 📋 Prerequisites

- Python 3.11+
- MySQL database (local or cloud)
- Git repository
- Spoonacular API key

## 🌐 Deployment Options

### Option 1: Render.com (Recommended - Free Tier)

#### Step 1: Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"

#### Step 3: Connect Repository
1. Connect your GitHub repository
2. Choose the repository: `The-recipe`
3. Select branch: `main`

#### Step 4: Configure Web Service
- **Name**: `recipe-generator` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn vibe_recipes.wsgi:application --bind 0.0.0.0:$PORT`

#### Step 5: Set Environment Variables
Add these in Render dashboard:
```
SECRET_KEY=your-long-random-secret-key-here
DEBUG=False
ALLOWED_HOST=your-app-name.onrender.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
SPOONACULAR_API_KEY=your-spoonacular-api-key
DJANGO_SETTINGS_MODULE=vibe_recipes.production
```

#### Step 6: Deploy
1. Click "Create Web Service"
2. Wait for build to complete
3. Your app will be available at: `https://your-app-name.onrender.com`

---

### Option 2: Railway.com (Alternative - Free Tier)

#### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

#### Step 2: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Select your repository
3. Railway will auto-detect Django

#### Step 3: Set Environment Variables
Add the same environment variables as Render

#### Step 4: Deploy
1. Railway will automatically build and deploy
2. Your app will be available at: `https://your-app-name.railway.app`

---

### Option 3: Vercel.com (Alternative)

#### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

#### Step 2: Import Project
1. Click "New Project"
2. Import your GitHub repository
3. Select Django framework

#### Step 3: Configure
- **Framework Preset**: Django
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Output Directory**: `staticfiles`
- **Install Command**: `pip install -r requirements.txt`

#### Step 4: Deploy
1. Click "Deploy"
2. Your app will be available at: `https://your-app-name.vercel.app`

---

## 🗄️ Database Setup

### Option 1: Use Render's MySQL (Free Tier)
1. In Render dashboard, create a new MySQL service
2. Use the connection details in your environment variables

### Option 2: Use PlanetScale (Free Tier)
1. Go to [planetscale.com](https://planetscale.com)
2. Create free account
3. Create new database
4. Use connection details in environment variables

### Option 3: Use Railway's MySQL
1. In Railway dashboard, create MySQL service
2. Use connection details in environment variables

---

## 🔧 Post-Deployment Steps

### Step 1: Run Migrations
```bash
# In your deployment platform's shell or via Django admin
python manage.py migrate
```

### Step 2: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 3: Test Your App
1. Visit your deployed URL
2. Test all features:
   - User registration/login
   - Recipe generation
   - Community features
   - PWA functionality

---

## 🚨 Troubleshooting

### Common Issues:

#### 1. Build Fails
- Check `requirements.txt` has all dependencies
- Ensure Python version matches `runtime.txt`
- Check build logs for specific errors

#### 2. Database Connection Issues
- Verify environment variables are correct
- Check database is accessible from deployment platform
- Ensure database user has proper permissions

#### 3. Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings
- Verify WhiteNoise is properly configured

#### 4. 500 Errors
- Check deployment logs
- Verify `DEBUG=False` in production
- Check database migrations are applied

---

## 📱 PWA Deployment Notes

Your app includes PWA features:
- ✅ Service Worker for offline support
- ✅ Manifest.json for app installation
- ✅ Responsive design for mobile
- ✅ Offline recipe access

These will work automatically in production!

---

## 🎯 Success Checklist

- [ ] Repository is pushed to GitHub
- [ ] Environment variables are set
- [ ] Database is connected and accessible
- [ ] Build completes successfully
- [ ] App is accessible via URL
- [ ] All features work correctly
- [ ] PWA installs properly
- [ ] Database migrations are applied
- [ ] Superuser account is created

---

## 🆘 Need Help?

If you encounter issues:
1. Check deployment platform logs
2. Verify environment variables
3. Test database connection
4. Check Django error logs
5. Ensure all files are committed

Your Recipe Generator is ready for deployment! 🎉
