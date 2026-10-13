from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from userpreferences.models import UserPreference
from .models import Category, Expense, ExpenseLimit
import json
import datetime
import os
import logging
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
from PIL import Image
try:
    import easyocr
except ImportError:
    easyocr = None

# Avoid downloading NLTK resources at import time (can block server startup).
# We'll attempt to use available NLTK data and fall back gracefully if missing.

logger = logging.getLogger(__name__)

# Currency symbol mapping
CURRENCY_SYMBOLS = {
    'PKR': '₨',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'INR': '₹',
    'AUD': 'A$',
    'CAD': 'C$',
    'CHF': 'CHF',
    'CNY': '¥',
    'SEK': 'kr',
    'NZD': 'NZ$',
}

def get_currency_symbol(currency_str):
    """Extract currency code and return as text.
    Always returns the currency code (e.g., 'PKR') instead of symbol.
    Expected format: 'PKR - Pakistani Rupee' or just 'PKR'"""
    if not currency_str:
        return 'PKR'
    
    # Clean the string and extract currency code
    currency_str = str(currency_str).strip()
    
    # Try to extract from format "PKR - Pakistani Rupee"
    if ' - ' in currency_str:
        currency_code = currency_str.split(' - ')[0].strip()
    # Try to extract from format "PKR - ₨"
    elif '-' in currency_str:
        currency_code = currency_str.split('-')[0].strip()
    else:
        # Already just the code
        currency_code = currency_str
    
    # Return currency code as text (not symbol)
    return currency_code.upper() if currency_code else 'PKR'

# Load and prepare dataset
try:
    dataset_path = os.path.join(settings.BASE_DIR, 'dataset.csv')
    if not os.path.exists(dataset_path):
        logger.warning(f"Dataset not found at {dataset_path}. Using empty dataset.")
        data = pd.DataFrame(columns=['description', 'category', 'clean_description'])
    else:
        data = pd.read_csv(dataset_path)
except Exception as e:
    logger.error(f"Failed to load dataset: {e}")
    data = pd.DataFrame(columns=['description', 'category', 'clean_description'])

# Preprocessing (lazy / fault-tolerant)
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    logger.warning("NLTK stopwords not found; continuing with empty stopwords set. Install with: nltk.download('stopwords')")
    stop_words = set()

def preprocess_text(text):
    try:
        tokens = word_tokenize(text.lower())
    except LookupError:
        # punkt tokenizer not available; fall back to simple split
        tokens = re.findall(r"\b\w+\b", text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return ' '.join(tokens)

# Apply preprocessing and train model if data exists
if len(data) > 0:
    try:
        data['clean_description'] = data['description'].apply(preprocess_text)
        tfidf_vectorizer = TfidfVectorizer()
        X = tfidf_vectorizer.fit_transform(data['clean_description'])
        model = RandomForestClassifier()
        model.fit(X, data['category'])
    except LookupError as e:
        # Missing NLTK resources (punkt/stopwords) - skip training for now.
        logger.warning("Skipping ML model training due to missing NLTK resources: %s", e)
        tfidf_vectorizer = None
        model = None
else:
    tfidf_vectorizer = None
    model = None

# ============================================================================
# 📸 RECEIPT SCANNING FUNCTIONALITY (FREE EASYOCR)
# ============================================================================

def extract_amount_from_text(text):
    """Extract amount from receipt text using intelligent pattern matching
    Handles formats: 3,730.90, 3730.90, 3,730, PKR 5000, Total: 2500, etc.
    Prioritizes explicit total keywords over raw numbers."""
    
    def clean_number(num_str):
        """Clean number string: remove commas, keep decimal point"""
        num_str = num_str.replace(',', '')
        try:
            return float(num_str)
        except ValueError:
            return None
    
    amounts_found = {}  # Store amounts with their "confidence" score
    
    # Split text into lines for more intelligent parsing
    lines = text.split('\n')
    
    # STRATEGY 1: Look for explicit keyword patterns across consecutive lines
    # Remove special characters from lines for matching
    for i, line in enumerate(lines):
        # Clean line for keyword matching (remove special chars like |}|
        line_clean = re.sub(r'[^\w\s,.]', '', line).lower().strip()
        
        # Check if this line is a total keyword
        total_keywords = [
            'grand total', 'g total', 'gtotal', 'net total', 
            'final total', 'total amount', 'overall total',
            'payment total', 'amount payable'
        ]
        
        is_total_line = any(keyword in line_clean for keyword in total_keywords)
        
        # Also check for "Total:" pattern
        if re.search(r'\btotal\s*[:=]?\s*', line_clean):
            is_total_line = True
        
        if is_total_line:
            # Look for a number on this line or the next 2 lines
            for j in range(i, min(i+3, len(lines))):
                numbers = re.findall(r'(\d+(?:[.,]\d+)*)', lines[j])
                for num_str in numbers:
                    cleaned = clean_number(num_str)
                    if cleaned and 10 <= cleaned <= 1000000:
                        # Prefer amounts with decimals (confidence 100)
                        if cleaned % 1 != 0:
                            amounts_found[cleaned] = 100
                        else:
                            # Integer amounts get lower confidence (50)
                            if cleaned not in amounts_found or amounts_found[cleaned] < 50:
                                amounts_found[cleaned] = 50
    
    # If we found high-confidence amounts, return the largest
    high_conf = {k: v for k, v in amounts_found.items() if v == 100}
    if high_conf:
        return max(high_conf.keys())
    
    # If we found any amounts, return the largest
    if amounts_found:
        return max(k for k, v in amounts_found.items() if v >= 50)
    
    # FALLBACK: Look for any decimal number in reasonable range
    all_numbers = re.findall(r'(\d+(?:[.,]\d+)*)', text)
    decimal_amounts = []
    for num_str in all_numbers:
        cleaned = clean_number(num_str)
        if cleaned and 10 <= cleaned <= 1000000 and cleaned % 1 != 0:
            decimal_amounts.append(cleaned)
    
    if decimal_amounts:
        return max(decimal_amounts)
    
    return None

def extract_date_from_text(text):
    """Extract date from receipt text"""
    # Patterns: 05/10/2026, 05-10-2026, 10/05/2026, etc.
    date_patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        if matches:
            try:
                match = matches[0]
                if len(match[0]) == 4:  # YYYY first
                    date_obj = datetime.datetime.strptime(f"{match[0]}-{match[1]}-{match[2]}", '%Y-%m-%d').date()
                else:  # DD first
                    date_obj = datetime.datetime.strptime(f"{match[0]}-{match[1]}-{match[2]}", '%d-%m-%Y').date()
                return date_obj
            except ValueError:
                continue
    
    # If no date found, return today's date
    return datetime.date.today()

def extract_vendor_from_text(text):
    """Extract vendor/store name from receipt text"""
    lines = text.split('\n')
    # Usually the first line or a line with store name
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line and len(line) > 3 and not any(char.isdigit() for char in line):
            # Return first non-numeric line that looks like a store name
            return line
    
    return "Receipt Store"

@login_required(login_url='/authentication/login')
def scan_receipt(request):
    """
    API Endpoint: POST /api/scan-receipt/
    Accepts: receipt image file
    Returns: JSON with extracted amount, date, vendor, description
    """
    if not easyocr:
        return JsonResponse({'error': 'EasyOCR not installed'}, status=400)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'receipt_image' not in request.FILES:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    
    try:
        receipt_file = request.FILES['receipt_image']
        
        # Validate file size (max 5MB)
        if receipt_file.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Image too large (max 5MB)'}, status=400)
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/bmp', 'image/gif']
        if receipt_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid image format'}, status=400)
        
        # Save temporary file
        temp_path = os.path.join(settings.MEDIA_ROOT, f'temp_{receipt_file.name}')
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        with open(temp_path, 'wb+') as f:
            for chunk in receipt_file.chunks():
                f.write(chunk)
        
        # Initialize OCR reader (English only for speed)
        reader = easyocr.Reader(['en'], gpu=False)
        
        # Read text from image
        logger.info(f"Scanning receipt for user {request.user}")
        result = reader.readtext(temp_path)
        
        # Extract text
        extracted_text = '\n'.join([detection[1] for detection in result])
        
        # Parse extracted data
        amount = extract_amount_from_text(extracted_text)
        date = extract_date_from_text(extracted_text)
        vendor = extract_vendor_from_text(extracted_text)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if amount is None:
            return JsonResponse({
                'error': 'Could not extract amount from receipt',
                'extracted_text': extracted_text[:200]  # Return partial text for debugging
            }, status=400)
        
        logger.info(f"Receipt scanned: Amount={amount}, Date={date}, Vendor={vendor}")
        
        return JsonResponse({
            'success': True,
            'amount': round(amount, 2),
            'date': date.strftime('%Y-%m-%d'),
            'vendor': vendor,
            'description': f"Receipt from {vendor}",
            'extracted_text': extracted_text[:500]  # For reference
        })
    
    except Exception as e:
        logger.error(f"Receipt scanning error: {str(e)}", exc_info=True)
        # Clean up temp file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return JsonResponse({'error': f'Error processing image: {str(e)}'}, status=500)

# ============================================================================

@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    sort_order = request.GET.get('sort')

    if sort_order == 'amount_asc':
        expenses = expenses.order_by('amount')
    elif sort_order == 'amount_desc':
        expenses = expenses.order_by('-amount')
    elif sort_order == 'date_asc':
        expenses = expenses.order_by('date')
    elif sort_order == 'date_desc':
        expenses = expenses.order_by('-date')

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        user_currency = UserPreference.objects.get(user=request.user).currency
        currency = get_currency_symbol(user_currency)
    except:
        currency = None

    total = page_obj.paginator.num_pages
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'total': total,
        'sort_order': sort_order,

    }
    return render(request, 'expenses/index.html', context)

daily_expense_amounts = {}

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': dict(request.POST) if request.POST else {}
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount_str = request.POST.get('amount', '').strip()
        date_str = request.POST.get('expense_date', '').strip()
        description = request.POST.get('description', '').strip()
        predicted_category = request.POST.get('category', '').strip()
        
        # Validate amount
        if not amount_str:
            messages.error(request, 'Amount is required')
            logger.warning(f"Expense add attempt by {request.user.username}: missing amount")
            return render(request, 'expenses/add_expense.html', context)
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than zero')
                logger.warning(f"Expense add attempt by {request.user.username}: invalid amount {amount}")
                return render(request, 'expenses/add_expense.html', context)
            if amount > 1000000:
                messages.error(request, 'Amount exceeds maximum limit (1,000,000)')
                return render(request, 'expenses/add_expense.html', context)
        except ValueError:
            messages.error(request, 'Amount must be a valid number')
            logger.warning(f"Expense add attempt by {request.user.username}: non-numeric amount")
            return render(request, 'expenses/add_expense.html', context)
        
        # Validate description
        if not description:
            messages.error(request, 'Description is required')
            logger.warning(f"Expense add attempt by {request.user.username}: missing description")
            return render(request, 'expenses/add_expense.html', context)
        
        if len(description) < 3:
            messages.error(request, 'Description must be at least 3 characters')
            return render(request, 'expenses/add_expense.html', context)
        
        if len(description) > 500:
            messages.error(request, 'Description cannot exceed 500 characters')
            return render(request, 'expenses/add_expense.html', context)
        
        # Validate date
        if not date_str:
            messages.error(request, 'Expense date is required')
            logger.warning(f'Expense add attempt by {request.user.username}: missing date')
            return render(request, 'expenses/add_expense.html', context)
        
        # Validate category
        if not predicted_category:
            messages.error(request, 'Category is required')
            logger.warning(f'Expense add attempt by {request.user.username}: missing category')
            return render(request, 'expenses/add_expense.html', context)
        
        initial_predicted_category = request.POST.get('initial_predicted_category')
        if predicted_category != initial_predicted_category:
            new_data = {
            'description': description,
            'category': predicted_category,
        }

        try:
            update_url = request.build_absolute_uri('/api/update-dataset/')
            response = requests.post(update_url, json={'new_data': new_data}, timeout=5)
            if response.status_code != 200:
                logger.warning(f'Dataset update failed: {response.status_code}')
        except requests.RequestException as e:
            logger.error(f'Failed to update dataset: {e}')
            messages.warning(request, 'Could not update ML model with this expense.')

        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.date.today()

            if date > today:
                messages.error(request, 'Date cannot be in the future')
                logger.warning(f'Expense add attempt by {request.user.username}: future date {date}')
                return render(request, 'expenses/add_expense.html', context)
            
            # Also check that date is not too old (optional: older than 10 years)
            ten_years_ago = today.replace(year=today.year - 10)
            if date < ten_years_ago:
                messages.error(request, 'Date cannot be more than 10 years in the past')
                return render(request, 'expenses/add_expense.html', context)
            
            user = request.user
            expense_limits = ExpenseLimit.objects.filter(owner=user)
            if expense_limits.exists():
                daily_expense_limit = expense_limits.first().daily_expense_limit
            else:
                daily_expense_limit = 5000  

            
            total_expenses_today = get_expense_of_day(user) + float(amount)
            if total_expenses_today > daily_expense_limit:
                subject = 'Daily Expense Limit Exceeded'
                message = f'Hello {user.username},\n\nYour expenses for today have exceeded your daily expense limit. Please review your expenses.'
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                messages.warning(request, 'Your expenses for today exceed your daily expense limit')

            Expense.objects.create(owner=request.user, amount=amount, date=date,
                                   category=predicted_category, description=description)
            messages.success(request, 'Expense saved successfully')
            return redirect('expenses')
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        date_str = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        try:
            # Convert the date string to a datetime object and validate the date
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            today = datetime.date.today()

            if date > today:
                messages.error(request, 'Date cannot be in the future')
                return render(request, 'expenses/add_expense.html', context)

            expense.owner = request.user
            expense.amount = amount
            expense. date = date
            expense.category = category
            expense.description = description

            expense.save()
            messages.success(request, 'Expense saved successfully')

            return redirect('expenses')
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'expenses/edit_income.html', context)

        # expense.owner = request.user
        # expense.amount = amount
        # expense. date = date
        # expense.category = category
        # expense.description = description

        # expense.save()

        # messages.success(request, 'Expense updated  successfully')

        # return redirect('expenses')

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

@login_required(login_url='/authentication/login')
def stats_view(request):
    return render(request, 'expenses/stats.html')

def predict_category(description):
    try:
        predict_category_url = 'http://localhost:8000/api/predict-category/'
        data = {'description': description}
        response = requests.post(predict_category_url, data=data, timeout=5)
        
        if response.status_code == 200:
            predicted_category = response.json().get('predicted_category')
            return predicted_category
        else:
            logger.warning(f"Prediction failed with status {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Failed to predict category: {e}")
        return None
    

def set_expense_limit(request):
    if request.method == "POST":
        daily_expense_limit = request.POST.get('daily_expense_limit')
        
        existing_limit = ExpenseLimit.objects.filter(owner=request.user).first()
        
        if existing_limit:
            existing_limit.daily_expense_limit = daily_expense_limit
            existing_limit.save()
        else:
            ExpenseLimit.objects.create(owner=request.user, daily_expense_limit=daily_expense_limit)
        
        messages.success(request, "Daily Expense Limit Updated Successfully!")
        return HttpResponseRedirect('/preferences/')
    else:
        return HttpResponseRedirect('/preferences/')
    
def get_expense_of_day(user):
    current_date = datetime.date.today()
    expenses = Expense.objects.filter(owner=user, date=current_date)
    total_expenses = sum(expense.amount for expense in expenses)
    return total_expenses
    