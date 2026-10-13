# Voice Input Feature - Installation & Setup Guide

## Quick Start (5 minutes)

### Step 1: Run Database Migrations
```bash
python manage.py makemigrations voice_feature
python manage.py makemigrations expenses
python manage.py migrate
```

**Expected Output**:
```
Operations to perform:
  Apply all migrations: ... voice_feature, expenses, ...
Running migrations:
  Applying voice_feature.0001_initial... OK
  Applying expenses.0003_expense_created_from... OK
```

### Step 2: Start Django Server
```bash
python manage.py runserver
```

**Expected Output**:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 3: Navigate to Add Expenses
1. Open http://127.0.0.1:8000 in browser
2. Click "Expenses" → "Add Expense"
3. Scroll to "Voice Input" section
4. Click microphone icon
5. Say: "500 coffee"
6. Verify transcript appears
7. Click "Submit"

**Done!** ✅

---

## Detailed Installation

### Prerequisites
- Python 3.8+
- Django 3.2+
- Browser with Web Speech API support (Chrome, Firefox, Edge)
- Microphone connected to computer

### Installation Steps

#### 1. Install Voice Feature Dependencies
```bash
# Already included in requirements.txt, but verify:
pip install django
pip install djangorestframework
pip install python-docx  # For documentation
```

#### 2. Enable Voice Feature in Django

**File**: `expensetracker/settings.py`
```python
INSTALLED_APPS = [
    # ... existing apps
    'voice_feature',  # ← Add this line
]
```
✅ Already done

**File**: `expensetracker/urls.py`
```python
urlpatterns = [
    # ... existing patterns
    path('voice/', include('voice_feature.urls')),  # ← Add this line
]
```
✅ Already done

#### 3. Run Migrations
```bash
# Step 1: Generate migration files
python manage.py makemigrations voice_feature
python manage.py makemigrations expenses

# Step 2: Apply migrations to database
python manage.py migrate voice_feature
python manage.py migrate expenses
```

**Verify Database Tables Created**:
```bash
python manage.py shell
>>> from voice_feature.models import VoiceInputLog, VoiceCommand
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'voice%'")
>>> cursor.fetchall()
# Should show: voice_feature_voiceinputlog, voice_feature_voicecommand
```

#### 4. Test Voice Feature
```bash
# Run the test suite
python manage.py test voice_feature

# Expected output:
# Ran 12 tests in X.XXXs
# OK
```

#### 5. Access Django Admin (Optional)
```bash
# Create superuser if not already created
python manage.py createsuperuser

# Login at http://127.0.0.1:8000/admin
# Go to Voice Feature → Voice Input Logs
# Should see voice entries created via API
```

---

## Testing Voice Feature

### Test 1: Simple Voice Parsing
**In Browser Console** (`F12` → Console):
```javascript
// Test voice input parsing
fetch('/voice/process/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({transcript: '500 coffee'})
})
.then(r => r.json())
.then(d => console.log(d))
```

**Expected Output**:
```javascript
{
  success: true,
  data: {
    amount: 500,
    description: "coffee",
    category: null,
    date: "2026-05-14",
    type: "expense"
  }
}
```

### Test 2: Save Voice Expense
```javascript
// Test saving expense
fetch('/voice/save-expense/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    amount: 500,
    description: 'Coffee',
    category: 'Food & Dining',
    date: '2026-05-14'
  })
})
.then(r => r.json())
.then(d => console.log(d))
```

**Expected Output**:
```javascript
{
  success: true,
  expense_id: 42,
  message: "Expense saved: 500 PKR for Coffee"
}
```

### Test 3: Get Voice Statistics
```javascript
// Test voice statistics
fetch('/voice/stats/')
.then(r => r.json())
.then(d => console.log(d))
```

**Expected Output**:
```javascript
{
  success: true,
  total_voice_expenses: 1,
  total_voice_income: 0,
  total_entries: 1
}
```

### Test 4: Live Microphone Test
1. Go to "Add Expense" page
2. Click Voice Input button
3. You should hear a beep (voice activated)
4. Say: "one thousand five hundred grocery shopping"
5. Transcript should appear: "one thousand five hundred grocery shopping"
6. Form should auto-fill:
   - Amount: 1500
   - Description: grocery shopping
   - Category: (auto-predicted as "Food")

### Test 5: Database Verification
```bash
python manage.py shell
>>> from voice_feature.models import VoiceInputLog
>>> from expenses.models import Expense
>>> 
>>> # Check voice logs
>>> VoiceInputLog.objects.all().count()  # Should be > 0
>>> 
>>> # Check voice expenses
>>> Expense.objects.filter(created_from='voice_input').count()  # Should be > 0
>>> 
>>> # View latest voice expense
>>> Expense.objects.filter(created_from='voice_input').latest('date')
```

---

## Common Issues & Fixes

### Issue 1: "Module 'voice_feature' not found"
**Cause**: voice_feature not added to INSTALLED_APPS  
**Fix**:
```python
# expensetracker/settings.py
INSTALLED_APPS = [
    ...
    'voice_feature',  # ← Ensure this line exists
]
```

### Issue 2: "Relation 'voice_feature_voiceinputlog' does not exist"
**Cause**: Migrations not applied  
**Fix**:
```bash
python manage.py migrate voice_feature
```

### Issue 3: Microphone Permission Denied
**Cause**: Browser blocked microphone access  
**Fix**:
1. Check browser permissions (URL bar → lock icon)
2. Allow microphone access for `localhost:8000`
3. Refresh page

### Issue 4: Web Speech API Not Available
**Cause**: Using unsupported browser  
**Fix**:
1. Use Chrome, Firefox, or Edge (latest versions)
2. Check browser console for specific error
3. Enable "experimental web features" if available

### Issue 5: Transcript Not Appearing
**Cause**: JavaScript error or voice-input.js not loaded  
**Fix**:
```javascript
// Check if VoiceInputManager is loaded
console.log(typeof VoiceInputManager);  // Should be 'function'
console.log(window.voiceManager);       // Should exist if started
```

### Issue 6: "CSRF token missing"
**Cause**: API request missing CSRF token  
**Fix**: Use Django's `csrftoken` cookie or add to request headers:
```javascript
// Get CSRF token
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

// Include in fetch
fetch('/voice/process/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({...})
})
```

---

## Configuration Options

### voice-input.js Settings
**File**: `static/js/voice-input.js`

```javascript
// At top of file, modify these constants:

const VOICE_CONFIG = {
  language: 'en-US',              // Change to 'ur-PK' for Urdu
  interimResults: true,           // Show partial results
  continuous: false,              // Stop after phrase ends
  maxResults: 1,                  // Best 1 result
  confidence_threshold: 0.5       // Min confidence
};

// Category keywords (for prediction)
const CATEGORY_KEYWORDS = {
  'Food & Dining': ['coffee', 'lunch', 'food', 'restaurant', ...],
  'Transport': ['taxi', 'uber', 'fuel', 'parking', ...],
  'Entertainment': ['movie', 'games', 'concert', ...],
  // Add more categories as needed
};
```

### Django Backend Settings
**File**: `voice_feature/views.py`

```python
# Confidence thresholds
MIN_CONFIDENCE = 0.7            # Minimum for auto-save
HIGH_CONFIDENCE = 0.95          # Recommended confidence

# Category prediction
USE_ML_PREDICTION = True        # Enable ML-based prediction
ML_CONFIDENCE_THRESHOLD = 0.75  # Min ML confidence

# Date handling
SUPPORTED_DATE_WORDS = {
    'today': 0,
    'tomorrow': 1,
    'yesterday': -1,
    'next week': 7,
    'last week': -7,
}
```

---

## Performance Optimization

### For Better Voice Recognition
1. **Use a good microphone** (reduces noise)
2. **Minimize background noise** (quieter environment)
3. **Speak clearly** (distinct pronunciation)
4. **Use consistent phrasing** ("500 coffee" vs "coffee 500")

### For Better Category Prediction
1. **Use descriptive text** ("coffee" vs "c")
2. **Add category** if not auto-predicted
3. **Review misclassifications** (AI learns over time)

### Server Performance
```bash
# Monitor voice endpoint response times
python manage.py shell
>>> from django.test.utils import override_settings
>>> import timeit
>>> 
>>> # Benchmark parsing
>>> import voice_feature.views as v
>>> timeit.timeit(lambda: v.parse_voice_transcript('500 coffee'), number=100)
# Should be < 0.05 seconds for 100 iterations
```

---

## Deployment Checklist

Before deploying to production:

- [ ] All migrations applied successfully
- [ ] Tests passing: `python manage.py test voice_feature`
- [ ] Voice feature working in development
- [ ] HTTPS enabled (required for Web Speech API in production)
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] CORS configured (if separate frontend)
- [ ] Admin interface tested
- [ ] Database backups configured
- [ ] Voice logs retention policy set (optional)
- [ ] User documentation prepared

---

## Uninstall Voice Feature (if needed)

```bash
# 1. Remove from settings
# expensetracker/settings.py: Remove 'voice_feature' from INSTALLED_APPS

# 2. Remove from URLs
# expensetracker/urls.py: Remove voice URL route

# 3. Drop tables (WARNING: Data loss!)
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("DROP TABLE voice_feature_voiceinputlog;")
>>> cursor.execute("DROP TABLE voice_feature_voicecommand;")

# 4. Remove created_from field from Expense (if desired)
# Create reverse migration or manually update
```

---

## Next Steps

1. ✅ **Installation**: Voice feature now installed
2. ⏭️ **Documentation**: Add voice feature to main FYP document
3. ⏭️ **Training**: Teach team how to use voice feature
4. ⏭️ **Monitoring**: Track voice usage in analytics
5. ⏭️ **Improvements**: Gather user feedback for enhancements

---

## Support & Resources

- **Web Speech API Docs**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Repository README**: [README.md](README.md)

---

**Setup Completed**: May 14, 2026  
**Installation Time**: ~5 minutes  
**Status**: Ready for Production ✅
