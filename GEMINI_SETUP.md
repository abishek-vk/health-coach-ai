# Gemini API Configuration Guide

## Current Status

Your Health Coach AI app is configured to use the **latest Gemini 2.5 models** with intelligent fallback:

### Model Priority Order (Auto-selected):
1. **gemini-2.5-flash** (Preferred) - Latest, fastest, cost-efficient
2. **gemini-2.5-pro** (Fallback) - Latest, more capable
3. **gemini-2.0-flash** (Fallback) - Stable, proven
4. **gemini-flash-latest** (Fallback) - Always points to latest

---

## Common Issues & Solutions

### ❌ Error 429: "You exceeded your current quota"
**Cause:** Your API key has hit rate limits or quota

**Solutions:**
1. Check your quota at [Google AI Studio](https://aistudio.google.com/)
2. Verify billing is active and up-to-date
3. Wait 60 seconds and retry
4. Consider upgrading your plan if using free tier

### ❌ Error 404: "Model not found"
**Cause:** The model name is incorrect or not available on your API tier

**Solution:** This is automatically handled. The app tries newer models first and falls back to older ones.

### ✅ Active Model Detection
Run this to check which model is currently active:
```bash
python -c "from modules.gemini_integration import get_active_model_name; print(f'Active Model: {get_active_model_name()}')"
```

---

## Files Modified

- **modules/gemini_integration.py**
  - Centralized `PREFERRED_MODELS` configuration
  - Intelligent model fallback logic
  - Better error messages
  - `get_active_model_name()` function

- **main.py**
  - Enhanced error messaging for users
  - Displays specific diagnostic information
  - Links to Google AI Studio

---

## How It Works

1. **Initialization:** When the app starts, it tries each model in the PREFERRED_MODELS list
2. **Testing:** Each model is tested with a simple request to verify accessibility
3. **Auto-selection:** First working model is selected and used
4. **Fallback:** If a model fails, moves to the next in the list
5. **Graceful Degradation:** If all fail, app works without AI features but shows helpful error

---

## Verify Everything Works

```bash
# 1. Check available models
python check_models.py

# 2. Verify Gemini initialization
python -c "from modules.gemini_integration import get_gemini_advisor, get_active_model_name; print(f'Model: {get_active_model_name()}'); print(f'Enabled: {get_gemini_advisor().enabled}')"

# 3. Start the app
python -m streamlit run main.py
```

---

## Environment Setup

Required in `.env`:
```
GEMINI_API_KEY=your_api_key_here
ENABLE_GEMINI_ENHANCEMENTS=true
```

Get your API key: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## Model Capabilities

| Model | Speed | Cost | Capability | Best For |
|-------|-------|------|------------|----------|
| gemini-2.5-flash | Very Fast | Low | Excellent | Recommendations, Health Insights |
| gemini-2.5-pro | Moderate | Medium | Outstanding | Complex analysis, Personalized plans |
| gemini-2.0-flash | Fast | Low | Very Good | General purpose |

---

**Last Updated:** February 7, 2026
**Configuration Version:** 2.0 (Gemini 2.5 Ready)
