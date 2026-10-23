# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
from .serializers import YourDataSerializer  
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)  

# Import from expenses module to avoid duplication
from expenses.views import preprocess_text

# Custom throttle classes
class PredictThrottle(UserRateThrottle):
    scope = 'predict'
    THROTTLE_RATES = {
        'predict': '100/hour'
    }

class UpdateThrottle(UserRateThrottle):
    scope = 'update'
    THROTTLE_RATES = {
        'update': '50/hour'
    }

def load_dataset():
    """Load and cache the dataset for predictions"""
    try:
        dataset_path = os.path.join(settings.BASE_DIR, 'dataset.csv')
        if os.path.exists(dataset_path):
            return pd.read_csv(dataset_path)
        else:
            logger.warning("Dataset not found. Using empty dataset.")
            return pd.DataFrame(columns=['description', 'category', 'clean_description'])
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return pd.DataFrame(columns=['description', 'category', 'clean_description'])


class PredictCategory(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [PredictThrottle]

    def post(self, request):
        try:
            user_input = request.data.get('description', '').strip()
            
            # Input validation
            if not user_input:
                return Response({'error': 'Description cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
            if len(user_input) < 3:
                return Response({'error': 'Description must be at least 3 characters'}, status=status.HTTP_400_BAD_REQUEST)
            if len(user_input) > 500:
                return Response({'error': 'Description cannot exceed 500 characters'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = load_dataset()
            if len(data) == 0:
                logger.warning("No training data available for prediction")
                return Response({'error': 'No training data available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            tfidf_vectorizer = TfidfVectorizer()
            X = tfidf_vectorizer.fit_transform(data['clean_description'])
            model = RandomForestClassifier()
            model.fit(X, data['category'])
            user_input_processed = preprocess_text(user_input)
            user_input_vector = tfidf_vectorizer.transform([user_input_processed])
            similarities = cosine_similarity(user_input_vector, X)
            closest_match_index = similarities.argmax()
            predicted_category = model.predict(X[closest_match_index])
            
            logger.info(f"Category predicted for user {request.user.username}: {predicted_category[0]}")
            return Response({'predicted_category': predicted_category[0]}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Prediction error for user {request.user.username}: {e}")
            return Response({'error': 'Prediction failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UpdateDataset(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UpdateThrottle]

    def post(self, request):
        # Only superusers/staff can update the dataset
        if not request.user.is_staff:
            return Response({'error': 'Only staff members can update the dataset'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            new_data = request.data.get('new_data')
            
            if not new_data or 'description' not in new_data or 'category' not in new_data:
                return Response({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Load existing dataset
            data = load_dataset()
            new_category = new_data['category']
            new_description = new_data['description']

            # Append new data
            new_row = {'description': new_description, 'category': new_category, 'clean_description': preprocess_text(new_description)}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save updated dataset
            dataset_path = os.path.join(settings.BASE_DIR, 'dataset.csv')
            data.to_csv(dataset_path, index=False)
            logger.info(f"Dataset updated by {request.user.username}")
            
            return Response({'message': 'Dataset updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Dataset update error: {e}")
            return Response({'error': 'Failed to update dataset'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


