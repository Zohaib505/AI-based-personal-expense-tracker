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

nltk.download('punkt')
nltk.download('stopwords')

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
    """Extract currency code and return symbol. 
    Expected format: 'PKR - Pakistani Rupee' or just 'PKR'"""
    if not currency_str:
        return currency_str
    
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
    
    # Return symbol from mapping, or currency code if not found
    return CURRENCY_SYMBOLS.get(currency_code, currency_code)

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

# Preprocessing
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return ' '.join(tokens)

# Apply preprocessing and train model if data exists
if len(data) > 0:
    data['clean_description'] = data['description'].apply(preprocess_text)
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(data['clean_description'])
    model = RandomForestClassifier()
    model.fit(X, data['category'])
else:
    tfidf_vectorizer = None
    model = None
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
        'values': request.POST
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
    