from django.shortcuts import render
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from django.utils.timezone import now
from expenses.models import Expense
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

# Fetch the data from the Expense model and create the forecast
@login_required(login_url='/authentication/login')
def forecast(request):
    try:
        # Fetch the latest 30 expenses for the current user
        expenses = Expense.objects.filter(owner=request.user).order_by('-date')[:30]

        # Check if there are enough expenses for forecasting
        if len(expenses) < 10:
            messages.error(request, "Not enough expenses to make a forecast. Please add more expenses.")
            logger.warning(f"User {request.user} attempted forecast with insufficient data ({len(expenses)} expenses)")
            return render(request, 'expense_forecast/index.html')

        # Create a DataFrame from the expenses - only use Date and Expenses for ARIMA
        data = pd.DataFrame({
            'Date': [expense.date for expense in expenses], 
            'Expenses': [expense.amount for expense in expenses]
        })
        data.set_index('Date', inplace=True)
        data = data.sort_index()  # Sort by date ascending
        
        logger.info(f"Forecasting for user {request.user} with {len(data)} expenses")

        # Fit ARIMA model
        model = ARIMA(data['Expenses'], order=(5, 1, 0))
        model_fit = model.fit()

        # Forecast next 30 days of expenses starting from the next day
        forecast_steps = 30
        current_date = now().date()
        next_day = current_date + pd.Timedelta(days=1)
        forecast_index = pd.date_range(start=next_day, periods=forecast_steps, freq='D')

        # Predict the future expenses
        forecast_result = model_fit.forecast(steps=forecast_steps)

        # Create a DataFrame for the forecasted expenses
        forecast_data = pd.DataFrame({
            'Date': forecast_index, 
            'Forecasted_Expenses': forecast_result.values
        })
        
        # Round forecasted expenses to whole numbers
        forecast_data['Forecasted_Expenses'] = forecast_data['Forecasted_Expenses'].round(0).astype(int)
        
        # Convert the forecast data to a list of dictionaries
        forecast_data_list = forecast_data.to_dict(orient='records')

        # Create a plot but save it without displaying it
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Expenses'], label='Previous Expenses', marker='o')
        plt.plot(forecast_index, forecast_result, label='Forecasted Expenses', color='red', marker='s')
        plt.xlabel('Date')
        plt.ylabel('Expenses')
        plt.title('Expense Forecast for Next 30 Days')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Save the plot to a file without displaying it
        plot_file = 'static/img/forecast_plot.png'
        plt.savefig(plot_file, dpi=100, bbox_inches='tight')
        plt.close()
        
        # Get user's currency preference
        user_currency = UserPreference.objects.get(user=request.user).currency
        
        logger.info(f"Forecast generated successfully for user {request.user}")

        # Pass the data to the template
        context = {
            'forecast_data': forecast_data_list,
            'plot_file': plot_file,
            'total_forecasted_expenses': int(np.round(np.sum(forecast_result))),
            'currency': user_currency,
        }

        return render(request, 'expense_forecast/index.html', context)
    
    except Exception as e:
        logger.error(f"Error generating forecast for user {request.user}: {str(e)}", exc_info=True)
        messages.error(request, f"Error generating forecast: {str(e)}")
        return render(request, 'expense_forecast/index.html')
