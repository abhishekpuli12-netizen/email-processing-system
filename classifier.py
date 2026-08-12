import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

class MessageClassifier:
    def __init__(self):
        # Rule-based patterns for initial classification
        self.patterns = {
            'action_required': [
                r'\b(please|kindly|request|ask|need|must|should|required)\b',
                r'\b(submit|send|complete|finish|provide|update|review|approve)\b',
                r'\b(deadline|due date|by\s+\w+\s+\d+)\b'
            ],
            'meeting_or_event': [
                r'\b(meeting|event|schedule|calendar|appointment|call|zoom|teams|webinar)\b',
                r'\b(at\s+\d{1,2}:\d{2}\s*(am|pm)?)\b',
                r'\b(on\s+\w+\s+\d{1,2},?\s+\d{4}?)\b'
            ],
            'personal_information': [
                r'\b(address|phone|email|contact|birthday|age|medical|health)\b',
                r'\b(id|identification|ssn|social\s+security)\b'
            ],
            'promotional': [
                r'\b(sale|discount|offer|promotion|subscribe|unsubscribe|newsletter)\b',
                r'\b(50%|free|buy|purchase|shop|deal)\b'
            ],
            'sensitive': [
                r'\b(password|passcode|pin|otp|verification)\b',
                r'\b(credit\s+card|bank|account|payment)\b'
            ]
        }
        
        self.category_mapping = {
            'action_required': 'Action Required',
            'meeting_or_event': 'Meeting or Event',
            'personal_information': 'Personal Information',
            'promotional': 'Promotional',
            'sensitive': 'Sensitive Information',
            'general': 'General Information'
        }
        
        # Initialize TF-IDF vectorizer (for ML approach)
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = LogisticRegression()
        self.is_trained = False
        
        # Load pre-trained model if available
        try:
            with open('models/classifier.pkl', 'rb') as f:
                self.classifier = pickle.load(f)
            with open('models/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.is_trained = True
        except:
            print("No pre-trained model found. Using rule-based classification only.")
    
    def classify(self, message, sender, message_id=None):
        """Classify a single message"""
        message_lower = message.lower()
        
        # Rule-based scoring
        scores = {category: 0 for category in self.patterns.keys()}
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower))
                scores[category] += matches
        
        # Determine primary category
        max_score = max(scores.values())
        
        # Check for sensitive first (highest priority)
        if scores.get('sensitive', 0) > 0:
            category = 'sensitive'
        elif max_score == 0:
            category = 'general'
        else:
            category = max(scores, key=scores.get)
        
        # If we have ML model trained, use it for confidence
        if self.is_trained:
            # Use ML for confidence scoring
            features = self.vectorizer.transform([message])
            probabilities = self.classifier.predict_proba(features)[0]
            confidence = max(probabilities)
        else:
            # Calculate confidence based on rule matches
            total_matches = sum(scores.values())
            if total_matches > 0:
                confidence = min(scores.get(category, 0) / total_matches, 0.95)
                # Boost confidence if multiple patterns match
                if scores.get(category, 0) > 1:
                    confidence = min(confidence + 0.1, 0.95)
            else:
                confidence = 0.5  # Default for general messages
        
        # Generate reason
        reason = self.generate_reason(category, message, sender, scores)
        
        return {
            'message_id': message_id,
            'category': self.category_mapping[category],
            'confidence': round(confidence, 2),
            'reason': reason,
            'raw_category': category
        }
    
    def generate_reason(self, category, message, sender, scores):
        """Generate explanation for classification"""
        reasons = {
            'action_required': 'The message contains action words like "please", "submit", or "complete"',
            'meeting_or_event': 'The message includes date/time references and meeting-related keywords',
            'personal_information': 'The message contains personal identifiers or contact information',
            'promotional': 'The message has marketing language, offers, or promotional content',
            'sensitive': 'The message contains sensitive information like passwords or financial details',
            'general': 'The message does not fit specific categories - general informational content'
        }
        
        base_reason = reasons.get(category, 'General communication')
        
        # Add confidence details
        if category != 'general':
            matching_patterns = sum(scores.values())
            base_reason += f" (found {matching_patterns} matching patterns)"
        
        return base_reason
    
    def train_model(self, labeled_data_file):
        """Train ML model with labeled data (optional improvement)"""
        df = pd.read_csv(labeled_data_file)
        X = df['message'].values
        y = df['category'].values
        
        X_vectorized = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_vectorized, y)
        self.is_trained = True
        
        # Save model
        import pickle
        with open('models/classifier.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)
        with open('models/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)