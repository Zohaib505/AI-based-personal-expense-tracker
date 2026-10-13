from django.urls import path
from . import views

app_name = 'voice_feature'

urlpatterns = [
    # Voice input processing endpoints
    path('process/', views.process_voice_input, name='process'),
    path('save-expense/', views.save_voice_expense, name='save_expense'),
    path('save-income/', views.save_voice_income, name='save_income'),
    path('stats/', views.voice_stats, name='stats'),
]
