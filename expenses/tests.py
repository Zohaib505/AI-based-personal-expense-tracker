import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ChatbotWidgetTests(TestCase):
    def test_widget_is_present_on_login_page(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'id="ai-chatbot-wrapper"')
        self.assertContains(response, 'AI Expense Assistant')

    @patch('expenses.views.ollama.chat')
    def test_chatbot_receives_previous_turns_from_session(self, mock_chat):
        mock_chat.return_value = {'message': {'content': 'I remember the earlier question.'}}
        history = [
            {'role': 'user', 'message': 'I spent 20 on lunch.'},
            {'role': 'assistant', 'message': 'I recorded that expense.'},
        ]

        response = self.client.post(
            reverse('chatbot_api'),
            data=json.dumps({'message': 'What did I spend on lunch?', 'history': history}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        sent_messages = mock_chat.call_args.kwargs['messages']
        self.assertEqual(sent_messages[1:3], [
            {'role': 'user', 'content': 'I spent 20 on lunch.'},
            {'role': 'assistant', 'content': 'I recorded that expense.'},
        ])

    def test_widget_is_present_on_expenses_dashboard(self):
        user = User.objects.create_user(username='chatbot-test-user', password='test-password')
        self.client.force_login(user)

        response = self.client.get(reverse('expenses'))

        self.assertContains(response, 'id="ai-chatbot-wrapper"')
        self.assertContains(response, 'AI Expense Assistant')
