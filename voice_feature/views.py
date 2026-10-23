from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import re
import json

from expenses.models import Expense, Category
from userincome.models import UserIncome


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def process_voice_input(request):
    """
    Process voice input transcription and parse expense details
    
    Expected POST data:
    {
        "transcript": "500 coffee",
        "type": "expense" or "income"  # optional, default: expense
    }
    
    Returns parsed data:
    {
        "success": true,
        "amount": 500,
        "description": "coffee",
        "category": "Food & Dining",
        "date": "2026-05-14",
        "confidence": 0.95
    }
    """
    try:
        data = json.loads(request.body)
        transcript = data.get('transcript', '').strip()
        input_type = data.get('type', 'expense').lower()
        
        if not transcript:
            return JsonResponse({
                'success': False,
                'error': 'No transcript provided'
            }, status=400)
        
        # Parse the voice input
        parsed = parse_voice_transcript(transcript, input_type)
        
        return JsonResponse({
            'success': True,
            'data': parsed
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def parse_voice_transcript(transcript, input_type='expense'):
    """
    Parse voice transcript to extract expense/income details
    
    Supports patterns:
    - "500 coffee" → amount: 500, description: coffee
    - "1500 grocery food" → amount: 1500, description: grocery, category: Food
    - "100" → amount: 100
    - "coffee" → description: coffee
    - "500 coffee today" → amount: 500, description: coffee, date: today
    - "500 coffee yesterday" → amount: 500, description: coffee, date: yesterday
    """
    
    result = {
        'amount': None,
        'description': '',
        'category': None,
        'date': datetime.now().date().isoformat(),
        'type': input_type,
        'confidence': 0.8
    }
    
    # Normalize transcript
    text = transcript.lower().strip()
    
    # Extract date references
    date_match = extract_date_reference(text)
    if date_match['date']:
        result['date'] = date_match['date']
        text = date_match['remaining_text']
    
    # Extract amount (numbers with currency symbols or just numbers)
    amount_match = re.search(r'(\d+(?:\.\d{2})?)\s*(pkr|rupees?|rs|usd|\$)?', text)
    if amount_match:
        result['amount'] = float(amount_match.group(1))
        # Remove amount from text
        text = text[:amount_match.start()] + text[amount_match.end():]
        text = text.strip()
    
    # Remaining text is description
    if text:
        result['description'] = text.title()
    
    # Try to predict category from description if not provided
    if result['description'] and not result['category']:
        result['category'] = predict_category_from_text(result['description'])
    
    # Adjust confidence based on how much data we extracted
    if result['amount'] and result['description']:
        result['confidence'] = 0.95
    elif result['amount'] or result['description']:
        result['confidence'] = 0.75
    else:
        result['confidence'] = 0.5
    
    return result


def extract_date_reference(text):
    """
    Extract date references from text
    Returns: {'date': '2026-05-14', 'remaining_text': 'text without date'}
    """
    today = datetime.now().date()
    result = {'date': None, 'remaining_text': text}
    
    # Check for date references
    if 'today' in text:
        result['date'] = today.isoformat()
        result['remaining_text'] = text.replace('today', '').strip()
    elif 'yesterday' in text:
        yesterday = today - timedelta(days=1)
        result['date'] = yesterday.isoformat()
        result['remaining_text'] = text.replace('yesterday', '').strip()
    elif 'tomorrow' in text:
        tomorrow = today + timedelta(days=1)
        result['date'] = tomorrow.isoformat()
        result['remaining_text'] = text.replace('tomorrow', '').strip()
    elif 'day before' in text or 'two days ago' in text:
        two_days_ago = today - timedelta(days=2)
        result['date'] = two_days_ago.isoformat()
        result['remaining_text'] = text.replace('day before', '').replace('two days ago', '').strip()
    elif 'this week' in text or 'last week' in text:
        # Keep current date for "this week" entries
        result['remaining_text'] = text.replace('this week', '').replace('last week', '').strip()
    
    return result


def predict_category_from_text(text):
    """
    Simple category prediction from keywords
    Returns matching category or None
    """
    
    # Keyword mappings to categories
    category_keywords = {
        'food': ['food', 'coffee', 'lunch', 'dinner', 'breakfast', 'restaurant', 'cafe', 'pizza', 'burger', 'snack'],
        'transport': ['taxi', 'uber', 'bus', 'fuel', 'petrol', 'parking', 'gas', 'train', 'metro', 'car'],
        'entertainment': ['movie', 'cinema', 'game', 'gaming', 'show', 'concert', 'netflix', 'spotify'],
        'shopping': ['shopping', 'buy', 'clothes', 'shoes', 'dress', 'shirt', 'pants', 'mall', 'store'],
        'health': ['doctor', 'medicine', 'pharmacy', 'hospital', 'health', 'medical', 'gym', 'fitness'],
        'utilities': ['electricity', 'water', 'bill', 'internet', 'phone', 'gas', 'utility'],
        'income': ['salary', 'freelance', 'bonus', 'investment', 'income', 'earn', 'payment', 'revenue'],
    }
    
    text_lower = text.lower()
    
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category.title()
    
    return None


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def save_voice_expense(request):
    """
    Save expense from voice input
    
    Expected POST data:
    {
        "amount": 500,
        "description": "Coffee",
        "category": "Food & Dining",
        "date": "2026-05-14"
    }
    """
    try:
        data = json.loads(request.body)
        
        amount = data.get('amount')
        description = data.get('description')
        category_name = data.get('category')
        date_str = data.get('date')
        
        if not amount or not description:
            return JsonResponse({
                'success': False,
                'error': 'Amount and description are required'
            }, status=400)
        
        # Parse date
        try:
            expense_date = datetime.fromisoformat(date_str).date() if date_str else datetime.now().date()
        except:
            expense_date = datetime.now().date()
        
        # Get or create category
        category = None
        if category_name:
            try:
                category = Category.objects.get(name__iexact=category_name)
            except Category.DoesNotExist:
                category = Category.objects.create(name=category_name, description=f'Created from voice input: {description}')
        
        # Create expense
        expense = Expense.objects.create(
            owner=request.user,
            amount=float(amount),
            description=description,
            category=category_name or 'Other',
            date=expense_date,
            created_from='voice_input'
        )
        
        return JsonResponse({
            'success': True,
            'expense_id': expense.id,
            'message': f'Expense saved: {amount} PKR for {description}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def save_voice_income(request):
    """
    Save income from voice input
    
    Expected POST data:
    {
        "amount": 5000,
        "source": "Freelance",
        "date": "2026-05-14"
    }
    """
    try:
        data = json.loads(request.body)
        
        amount = data.get('amount')
        source = data.get('source') or data.get('description')
        date_str = data.get('date')
        
        if not amount or not source:
            return JsonResponse({
                'success': False,
                'error': 'Amount and source are required'
            }, status=400)
        
        # Parse date
        try:
            income_date = datetime.fromisoformat(date_str).date() if date_str else datetime.now().date()
        except:
            income_date = datetime.now().date()
        
        # Create income
        income = UserIncome.objects.create(
            owner=request.user,
            amount=float(amount),
            source=source,
            date=income_date,
            description=f'Created from voice input'
        )
        
        return JsonResponse({
            'success': True,
            'income_id': income.id,
            'message': f'Income saved: {amount} PKR from {source}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["GET"])
@login_required
@require_http_methods(["GET"])
def voice_stats(request):
    """
    Get voice input statistics
    """
    try:
        total_voice_expenses = Expense.objects.filter(
            owner=request.user,
            created_from='voice_input'
        ).count()
        
        total_voice_income = UserIncome.objects.filter(
            owner=request.user,
            description__contains='voice input'
        ).count()
        
        return JsonResponse({
            'success': True,
            'total_voice_expenses': total_voice_expenses,
            'total_voice_income': total_voice_income,
            'total_entries': total_voice_expenses + total_voice_income
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
