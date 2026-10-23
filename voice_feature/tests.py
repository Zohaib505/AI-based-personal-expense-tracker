"""
Voice Feature Tests
Tests for voice input functionality including parsing, ML integration, and database operations
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from expenses.models import Expense, Category
from userincome.models import UserIncome
from voice_feature.models import VoiceInputLog, VoiceCommand
from voice_feature.views import parse_voice_transcript
import json
from datetime import datetime, timedelta


class VoiceTranscriptParsingTest(TestCase):
    """Test voice transcript parsing and extraction"""
    
    def test_parse_amount_and_description(self):
        """Test parsing '500 coffee' → amount:500, description:coffee"""
        result = parse_voice_transcript("500 coffee", "expense")
        self.assertEqual(result['amount'], 500.0)
        self.assertIn('coffee', result['description'].lower())
    
    def test_parse_amount_only(self):
        """Test parsing numeric-only input"""
        result = parse_voice_transcript("1500", "expense")
        self.assertEqual(result['amount'], 1500.0)
    
    def test_parse_description_only(self):
        """Test parsing description-only input"""
        result = parse_voice_transcript("grocery", "expense")
        self.assertIsNone(result['amount'])
        self.assertIn('grocery', result['description'].lower())
    
    def test_parse_with_date_today(self):
        """Test parsing 'amount description today' pattern"""
        result = parse_voice_transcript("500 coffee today", "expense")
        self.assertEqual(result['amount'], 500.0)
        self.assertEqual(result['date'], datetime.now().date().isoformat())
    
    def test_parse_with_date_yesterday(self):
        """Test parsing 'amount description yesterday' pattern"""
        result = parse_voice_transcript("500 coffee yesterday", "expense")
        self.assertEqual(result['amount'], 500.0)
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        self.assertEqual(result['date'], yesterday)
    
    def test_parse_with_date_tomorrow(self):
        """Test parsing 'amount description tomorrow' pattern"""
        result = parse_voice_transcript("500 coffee tomorrow", "expense")
        tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
        self.assertEqual(result['date'], tomorrow)
    
    def test_parse_complex_description(self):
        """Test parsing complex descriptions"""
        result = parse_voice_transcript("1500 grocery shopping food", "expense")
        self.assertEqual(result['amount'], 1500.0)
        self.assertGreaterEqual(len(result['description']), 3)
    
    def test_parse_decimal_amount(self):
        """Test parsing decimal amounts"""
        result = parse_voice_transcript("99.50 coffee", "expense")
        self.assertEqual(result['amount'], 99.50)
    
    def test_parse_amount_with_thousands_separator(self):
        """Test parsing amounts with commas"""
        result = parse_voice_transcript("5,000 salary", "expense")
        self.assertEqual(result['amount'], 5000.0)
    
    def test_currency_symbol_handling(self):
        """Test ignoring currency symbols"""
        result = parse_voice_transcript("$500 coffee", "expense")
        self.assertEqual(result['amount'], 500.0)
    
    def test_income_type_parsing(self):
        """Test parsing income type"""
        result = parse_voice_transcript("5000 freelance", "income")
        self.assertEqual(result['amount'], 5000.0)
        self.assertEqual(result['type'], 'income')


class VoiceExpenseApiTest(TestCase):
    """Test voice expense API endpoints"""
    
    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_process_voice_input_endpoint(self):
        """Test /voice/process/ endpoint"""
        response = self.client.post(
            '/voice/process/',
            data=json.dumps({'transcript': '500 coffee'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['amount'], 500.0)
    
    def test_save_voice_expense_endpoint(self):
        """Test /voice/save-expense/ endpoint"""
        response = self.client.post(
            '/voice/save-expense/',
            data=json.dumps({
                'amount': 500,
                'description': 'Coffee',
                'category': 'Food & Dining',
                'date': datetime.now().date().isoformat()
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('expense_id', data)
        
        # Verify expense was created
        expense = Expense.objects.get(id=data['expense_id'])
        self.assertEqual(expense.amount, 500)
        self.assertEqual(expense.owner, self.user)
        self.assertEqual(expense.created_from, 'voice_input')
    
    def test_voice_stats_endpoint(self):
        """Test /voice/stats/ endpoint"""
        # Create a voice expense first
        Expense.objects.create(
            owner=self.user,
            amount=100,
            description='Test',
            category='Other',
            created_from='voice_input'
        )
        
        response = self.client.get('/voice/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['total_voice_expenses'], 1)


class VoiceIncomeApiTest(TestCase):
    """Test voice income API endpoints"""
    
    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_save_voice_income_endpoint(self):
        """Test /voice/save-income/ endpoint"""
        response = self.client.post(
            '/voice/save-income/',
            data=json.dumps({
                'amount': 5000,
                'source': 'Freelance',
                'date': datetime.now().date().isoformat()
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('income_id', data)
        
        # Verify income was created
        income = UserIncome.objects.get(id=data['income_id'])
        self.assertEqual(income.amount, 5000)
        self.assertEqual(income.owner, self.user)


class VoiceInputLogTest(TestCase):
    """Test voice input logging and analytics"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_voice_input_log_creation(self):
        """Test creating voice input logs"""
        log = VoiceInputLog.objects.create(
            user=self.user,
            transcript='500 coffee',
            parsed_data={'amount': 500, 'description': 'coffee'},
            confidence=0.95,
            was_saved=True
        )
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.transcript, '500 coffee')
        self.assertTrue(log.was_saved)
    
    def test_voice_command_creation(self):
        """Test creating custom voice commands"""
        command = VoiceCommand.objects.create(
            user=self.user,
            command_name='quick_coffee',
            command_pattern='coffee',
            category='Food & Dining',
            examples='500 coffee, coffee, get me coffee'
        )
        self.assertEqual(command.user, self.user)
        self.assertEqual(command.category, 'Food & Dining')


class VoiceFeatureIntegrationTest(TestCase):
    """Integration tests for full voice feature workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_end_to_end_voice_expense_workflow(self):
        """Test complete workflow: parse → save → verify"""
        # Step 1: Parse voice input
        parse_response = self.client.post(
            '/voice/process/',
            data=json.dumps({'transcript': '500 coffee today'}),
            content_type='application/json'
        )
        self.assertTrue(parse_response.json()['success'])
        parsed_data = parse_response.json()['data']
        
        # Step 2: Save parsed data as expense
        save_response = self.client.post(
            '/voice/save-expense/',
            data=json.dumps({
                'amount': parsed_data['amount'],
                'description': parsed_data['description'],
                'category': parsed_data['category'] or 'Other',
                'date': parsed_data['date']
            }),
            content_type='application/json'
        )
        self.assertTrue(save_response.json()['success'])
        
        # Step 3: Verify expense appears in database
        expense = Expense.objects.filter(
            owner=self.user,
            created_from='voice_input'
        ).first()
        self.assertIsNotNone(expense)
        self.assertEqual(expense.amount, 500)
    
    def test_voice_feature_without_authentication(self):
        """Test that unauthenticated requests are rejected"""
        self.client.logout()
        
        response = self.client.post(
            '/voice/process/',
            data=json.dumps({'transcript': '500 coffee'}),
            content_type='application/json'
        )
        # Should redirect to login or return 401/403
        self.assertNotEqual(response.status_code, 200)


class VoiceBrowserCompatibilityTest(TestCase):
    """Test JavaScript functionality (conceptual)"""
    
    def test_voice_input_manager_exists(self):
        """Verify voice-input.js exists and contains VoiceInputManager"""
        import os
        js_file = 'static/js/voice-input.js'
        self.assertTrue(os.path.exists(js_file))
        
        with open(js_file, 'r') as f:
            content = f.read()
            self.assertIn('VoiceInputManager', content)
            self.assertIn('startListening', content)
            self.assertIn('processVoiceInput', content)


# Test command: python manage.py test voice_feature
