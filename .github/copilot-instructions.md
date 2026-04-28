# Expense Tracker - AI Coding Agent Instructions

## Project Overview
A Django 5.1-based personal expense tracker with automated categorization, forecasting, goal tracking, and reporting. Multi-tenant (per-user data isolation) with REST API and ML-powered features.

## Architecture Patterns

### App Structure & Responsibilities
- **expenses**: Core expense CRUD, NLTK-based auto-categorization, expense limits
- **authentication**: Email verification, user registration/login (class-based views pattern)
- **api**: REST endpoints with DRF, ML model endpoints for category prediction
- **expense_forecast**: ARIMA time-series forecasting of future expenses
- **userincome**: Income tracking (parallel to expenses), sources management
- **userpreferences**: User currency settings (OneToOneField pattern)
- **goals**: Savings goal tracking with progress calculation
- **report_generation**: Celery async tasks for weekly/monthly Excel reports
- **userprofile**: User profile management

### Data Flow
1. **User Authentication** → Email verification token → Profile/Preferences created
2. **Expense Entry** → ML prediction endpoint suggests category → Manual override possible
3. **Auto-Categorization**: TF-IDF + RandomForest on `dataset.csv` (not in git, loaded at import)
4. **Forecasting**: 30-day ARIMA forecast from last 30 expenses per user
5. **Reporting**: Celery task triggers on schedule, generates Excel, emails via Django mail backend

### Critical Data Models
- **Expense**: `amount`, `date`, `description`, `category`, `owner` (FK to User)
- **UserIncome**: Parallel structure to Expense, with `source` instead of `category`
- **Goal**: Date range, target amount, progress tracking via `calculate_progress()`
- **ExpenseLimit**: Daily limit enforcement per user
- **UserPreference**: Currency preference (OneToOne with User)

## Key Conventions

### ML/Data Processing
- **Dataset Loading**: Global `dataset.csv` loaded at app startup in views (lines 29-36 in expenses/views.py)
- **Model Retraining**: No persistence layer - RandomForest/TF-IDF retrained per request
- **Text Preprocessing**: NLTK tokenization + stopword removal (reused function across files)
- **No Caching**: ML models are ephemeral; consider caching for production

### Authentication & Permissions
- **Login Decorator**: `@login_required(login_url='/authentication/login')` on all user-specific views
- **Multi-tenant**: Filter all queries with `owner=request.user`
- **Email Activation**: Tokens via Django's `PasswordResetTokenGenerator` pattern (utils.py)

### Async Tasks
- **Celery Config**: [celery_config.py](celery_config.py) has Redis fallback (eager mode if Redis unavailable)
- **Report Tasks**: `generate_report_and_send_email()` runs weekly/monthly (checks `today.day`)
- **Error Handling**: Tasks have 30min time limit with 25min soft limit

### View Patterns
- **Class-based**: Authentication views (RegistrationView, LoginView); transaction.atomic() for atomic operations
- **Function-based**: Expense management (search, index); use Paginator for large datasets
- **API Views**: DRF APIView with `permission_classes = [IsAuthenticated]`
- **Messages Framework**: Use `messages.error/success()` for user feedback, not exceptions

## Developer Workflows

### Local Setup
```bash
conda activate fyp  # Project env (see start_server.bat)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Database Migrations
- New models: `python manage.py makemigrations <app_name>` then `migrate`
- Migrations stored in `<app>/migrations/`

### Testing
- Unit tests in each app's `tests.py` (currently minimal)
- Run: `python manage.py test`

### Static Files
- CSS: Bootstrap + custom styles in [static/css/](static/css/)
- Images: Generated plots saved to `static/img/forecast_plot.png`
- Collect: `python manage.py collectstatic` (for production)

## External Dependencies
- **Data Science**: pandas, scikit-learn, statsmodels (ARIMA), matplotlib
- **NLTK**: punkt, stopwords (auto-downloaded on first use)
- **Email**: Django's EmailMessage with SMTP backend
- **REST**: djangorestframework 3.15.2
- **PDF/Excel**: reportlab, openpyxl (not currently used but in requirements)

## Common Pitfalls & Solutions

| Issue | Solution |
|-------|----------|
| "Model not found" when categorizing | Ensure `dataset.csv` exists in project root; models are reloaded each request |
| User sees expenses from other users | Always filter with `owner=request.user` |
| Celery tasks fail silently | Check [celery_config.py](celery_config.py) - Redis must be running or tasks use eager mode |
| Forecast returns empty | Need ≥10 expenses in user history (hardcoded check in views) |
| Email not sending | Verify Django email backend in settings.py; hardcoded sender is `hemantshirsath24@gmail.com` |

## File Organization Rules
- **Models**: Define in `models.py` with `owner=models.ForeignKey(to=User, on_delete=models.CASCADE)` for user isolation
- **Views**: Keep business logic in views (no separate services layer yet)
- **URLs**: Pattern is `path('route/', view_name, name='route_name')`
- **Templates**: In `templates/<app_name>/` directories
- **Static**: App-specific static files in `<app>/static/` (not used; centralized in top-level `static/`)

## When Adding Features
1. **User-facing data**: Add `owner` FK to model, filter views with `owner=request.user`
2. **Async work**: Use Celery task in `report_generation/tasks.py`
3. **API endpoint**: Use DRF APIView, add to `api/views.py` + `api/urls.py`
4. **Category prediction**: Leverage existing ML pipeline in `api/views.py` (PredictCategory)
5. **Tests**: Add to app's `tests.py` before marking complete

## Debug Commands
```bash
python manage.py shell  # Django shell with models loaded
python manage.py dbshell  # Direct DB access
python -m pytest --tb=short  # If pytest installed
```

---
**Last Updated**: April 2026 | **Django Version**: 5.1.1 | **Python**: 3.x (conda env)
