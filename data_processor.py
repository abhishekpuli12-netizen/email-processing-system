import pandas as pd
import json
from datetime import datetime
from classifier import MessageClassifier
from task_extractor import TaskExtractor
from sensitive_detector import SensitiveDetector

class DataProcessor:
    def __init__(self):
        self.classifier = MessageClassifier()
        self.task_extractor = TaskExtractor()
        self.sensitive_detector = SensitiveDetector()
        
    def process_messages(self, csv_file_path=r"C:\Users\USER\Downloads\L1_Candidate_Dataset\messages.csv"):
        """Process all messages from CSV file"""
        df = pd.read_csv(csv_file_path)
        
        results = {
            'classifications': [],
            'tasks': [],
            'events': [],
            'sensitive': [],
            'statistics': {
                'total': len(df),
                'categories': {},
                'sensitive_count': 0,
                'tasks_count': 0,
                'events_count': 0
            }
        }
        
        for index, row in df.iterrows():
            message_id = row['message_id']
            sender = row['sender']
            message = row['message']
            timestamp = row['timestamp']
            
            # Part 1: Classify message
            classification = self.classifier.classify(message, sender, message_id)
            results['classifications'].append(classification)
            
            # Update category statistics
            category = classification['category']
            results['statistics']['categories'][category] = \
                results['statistics']['categories'].get(category, 0) + 1
            
            # Part 2: Extract tasks/events (from ALL messages)
            extracted = self.task_extractor.extract(message, message_id)
            if extracted:
                if extracted['type'] == 'task':
                    results['tasks'].append(extracted)
                    results['statistics']['tasks_count'] += 1
                else:
                    results['events'].append(extracted)
                    results['statistics']['events_count'] += 1
            
            # Part 3: Detect sensitive information
            sensitive = self.sensitive_detector.detect(message, message_id)
            if sensitive:
                results['sensitive'].append(sensitive)
                results['statistics']['sensitive_count'] += 1
        
        # Save outputs
        self.save_results(results)
        return results
    
    def save_results(self, results):
        """Save all results to JSON files"""
        with open('output/classifications.json', 'w') as f:
            json.dump(results['classifications'], f, indent=2)
        
        with open('output/tasks.json', 'w') as f:
            json.dump({
                'tasks': results['tasks'],
                'events': results['events']
            }, f, indent=2)
        
        with open('output/sensitive.json', 'w') as f:
            json.dump(results['sensitive'], f, indent=2)
        
        with open('output/statistics.json', 'w') as f:
            json.dump(results['statistics'], f, indent=2)