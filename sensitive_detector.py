import re

class SensitiveDetector:
    def __init__(self):
        self.patterns = {
            'password': {
                'patterns': [
                    r'(?:password|passcode|pin)\s*(?:is|:|=)\s*([A-Za-z0-9@#$%^&+=]{4,20})',
                    r'(?:otp|one[- ]?time[- ]?password)\s*(?:is|:|=)\s*(\d{4,8})',
                    r'(?:verification|auth)\s*(?:code|token)\s*(?:is|:|=)\s*([A-Za-z0-9]{4,16})'
                ],
                'risk': 'high',
                'action': 'do_not_store'
            },
            'bank_details': {
                'patterns': [
                    r'(?:credit card|card number|payment)\s*(?:is|:|=)\s*(\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4})',
                    r'(?:bank|account)\s*(?:number|no)\s*(?:is|:|=)\s*(\d{8,12})',
                    r'(?:expiry|expiration)\s*(?:date)\s*(?:is|:|=)\s*(\d{2}/\d{2})'
                ],
                'risk': 'high',
                'action': 'do_not_send_external'
            },
            'personal_id': {
                'patterns': [
                    r'(?:ssn|social security)\s*(?:number|no)?\s*(?:is|:|=)\s*(\d{3}[- ]?\d{2}[- ]?\d{4})',
                    r'(?:phone|mobile|contact)\s*(?:number|no)?\s*(?:is|:|=)\s*(\+?\d{10,15})',
                    r'(?:email|mail|address)\s*(?:is|:|=)\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                ],
                'risk': 'medium',
                'action': 'ask_for_confirmation'
            },
            'token': {
                'patterns': [
                    r'(?:token|api[- ]?key|access[- ]?token)\s*(?:is|:|=)\s*([A-Za-z0-9_\-\.]{16,40})',
                    r'(?:auth|authentication)\s*(?:token|key)\s*(?:is|:|=)\s*([A-Za-z0-9_\-\.]{16,40})'
                ],
                'risk': 'high',
                'action': 'do_not_store'
            }
        }
    
    def detect(self, message, message_id):
        """Detect sensitive information in message"""
        detected_items = []
        
        for sensitivity_type, config in self.patterns.items():
            for pattern in config['patterns']:
                matches = re.finditer(pattern, message, re.IGNORECASE)
                
                for match in matches:
                    if match.groups():
                        sensitive_value = match.group(1)
                        
                        # Create masked version
                        masked_text = self.mask_sensitive(message, sensitive_value)
                        
                        detected_items.append({
                            'message_id': message_id,
                            'sensitivity_type': sensitivity_type,
                            'risk': config['risk'],
                            'masked_text': masked_text,
                            'recommended_action': config['action'],
                            'original_partial': sensitive_value[:2] + '***'  # For logging without exposing
                        })
        
        # Return the first detected sensitive item (or aggregate)
        if detected_items:
            return detected_items[0]  # For simplicity, return first detection
        
        return None
    
    def mask_sensitive(self, message, sensitive_value):
        """Mask sensitive value in message"""
        # Replace with asterisks
        masked_message = message.replace(sensitive_value, '*' * len(sensitive_value))
        
        # Also mask if it appears partially
        if len(sensitive_value) > 4:
            masked_message = re.sub(
                sensitive_value[:4] + r'\w+', 
                '*' * len(sensitive_value), 
                masked_message
            )
        
        return masked_message