# Spoonacular API Setup

## Getting Your API Key

1. **Visit**: https://spoonacular.com/food-api
2. **Sign up** for a free account
3. **Get your API key** from your dashboard
4. **Free tier**: 150 requests/day

## Configuration

### Option 1: Environment Variable (Recommended)
Add to your `.env` file:
```
SPOONACULAR_API_KEY=your-api-key-here
```

### Option 2: Direct in Settings (Not recommended for production)
Add to `vibe_recipes/settings.py`:
```python
SPOONACULAR_API_KEY = 'your-api-key-here'
```

## How It Works

1. **User selects ingredients** and cuisine
2. **System calls Spoonacular API** to find real recipes
3. **If API returns results**: Uses the best recipe with image
4. **If no API results**: Falls back to local recipe generation
5. **Recipe is saved** to user's history

## Features

- ✅ **Real recipes** from Spoonacular database
- ✅ **High-quality food images**
- ✅ **Detailed instructions**
- ✅ **Cooking times and servings**
- ✅ **Source attribution**
- ✅ **Fallback to local generation**

## Testing

1. **Get your API key** from Spoonacular
2. **Add it to your environment**
3. **Generate a recipe** with common ingredients
4. **Check for real recipe with image**

## API Limits

- **Free tier**: 150 requests/day
- **Rate limiting**: 1 request/second
- **Timeout**: 10 seconds per request

## Troubleshooting

- **No recipes found**: Check API key and ingredient names
- **API errors**: Check network connection and API status
- **Fallback works**: System will use local generation if API fails
