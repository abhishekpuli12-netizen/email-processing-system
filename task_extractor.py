import re
from datetime import datetime
import dateutil.parser as parser

class TaskExtractor:
    def __init__(self):
        # Patterns for extraction
        self.task_patterns = [
            r'(?i)(?:please|kindly|need to|must|should|required to)\s+(\w+\s+\w+\s+\w+)',
            r'(?i)(?:submit|send|complete|finish|provide|update|review|approve)\s+(\w+\s+\w+\s+\w+)'
        ]
        
        self.date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # 2026-08-15
            r'(\d{1,2}/\d{1,2}/\d{4})',  # 08/15/2026
            r'(\d{1,2}-\d{1,2}-\d{4})',  # 08-15-2026
            r'(by|on|before)\s+(\w+\s+\d{1,2},?\s+\d{4})',  # August 15, 2026
        ]
        
        self.time_patterns = [
            r'(\d{1,2}:\d{2}\s*(?:am|pm)?)',
            r'(at\s+\d{1,2}\s*(?:am|pm))'
        ]
        
        self.priority_keywords = {
            'high': ['urgent', 'important', 'asap', 'immediately', 'critical', 'high priority'],
            'medium': ['please', 'need', 'should', 'required'],
            'low': ['when possible', 'if you can', 'eventually', 'low priority']
        }
    
    def extract(self, message, message_id):
        """Extract tasks and events from message"""
        message_lower = message.lower()
        
        # Check if this is a task or event (use word boundaries for better matching)
        task_keywords = [r'\bsubmit\b', r'\bcomplete\b', r'\bfinish\b', r'\bprovide\b', 
                        r'\bupdate\b', r'\breview\b', r'\bapprove\b', r'\bsend\b',
                        r'\bplease\b', r'\bkindly\b', r'\bneed\b', r'\bmust\b', r'\bshould\b']
        
        event_keywords = [r'\bmeeting\b', r'\bevent\b', r'\bcall\b', r'\bzoom\b', 
                         r'\bteams\b', r'\bwebinar\b', r'\bappointment\b', r'\bschedule\b',
                         r'\bcalendar\b']
        
        is_task = any(re.search(pattern, message_lower) for pattern in task_keywords)
        is_event = any(re.search(pattern, message_lower) for pattern in event_keywords)
        
        if not is_task and not is_event:
            return None
        
        # Extract title
        title = self.extract_title(message, is_task, is_event)
        
        # Extract deadline/date
        deadline = self.extract_deadline(message)
        
        # Extract time
        time = self.extract_time(message)
        
        # Extract person involved
        person = self.extract_person(message)
        
        # Determine priority
        priority = self.determine_priority(message_lower)
        
        # Determine type (prioritize event if both found)
        item_type = 'event' if is_event else 'task'
        
        return {
            'item_id': f"{'TASK' if item_type == 'task' else 'EVENT'}_{message_id}",
            'type': item_type,
            'title': title,
            'description': message[:200] + '...' if len(message) > 200 else message,
            'deadline': deadline,
            'time': time,
            'person': person,
            'priority': priority,
            'source_message_id': message_id
        }
    
    def extract_title(self, message, is_task, is_event):
        """Extract title from message"""
        message_clean = message.replace('\n', ' ')
        
        if is_task:
            # Look for action verbs followed by text (case-insensitive)
            patterns = [
                r'(?i)(?:please|kindly|need to|must|should)\s+(.+?)(?:\s+by\s+|\s+before\s+|\.|\?|$)',
                r'(?i)(?:submit|send|complete|finish|provide|update|review|approve)\s+(.+?)(?:\s+by\s+|\s+before\s+|\.|\?|$)'
            ]
            for pattern in patterns:
                match = re.search(pattern, message_clean)
                if match:
                    title = match.group(1).strip()
                    # Limit to reasonable length
                    if len(title) > 100:
                        title = title[:100]
                    return title if title else 'Task'
        
        if is_event:
            # Look for event-related phrases (case-insensitive)
            patterns = [
                r'(?i)(?:meeting|event|call|webinar|calendar update)\s*(?::|about|for|on)?\s+(.+?)(?:\s+on\s+|\s+at\s+|,|\?|$)',
                r'(?i)(.+?)\s+(?:meeting|event|call|webinar)(?:\s+on\s+|\s+at\s+|,|\?|$)'
            ]
            for pattern in patterns:
                match = re.search(pattern, message_clean)
                if match:
                    title = match.group(1).strip()
                    # Limit to reasonable length
                    if len(title) > 100:
                        title = title[:100]
                    return title if title else 'Event'
        
        # Fallback: return first 50 characters
        return message_clean[:50].strip()
    
    def extract_deadline(self, message):
        """Extract deadline from message"""
        for pattern in self.date_patterns:
            match = re.search(pattern, message)
            if match:
                date_str = match.group(1) if len(match.groups()) == 1 else match.group(2)
                try:
                    parsed_date = parser.parse(date_str, fuzzy=True)
                    return parsed_date.strftime('%Y-%m-%d')
                except:
                    return date_str
        
        return None
    
    def extract_time(self, message):
        """Extract time from message"""
        for pattern in self.time_patterns:
            match = re.search(pattern, message)
            if match:
                time_str = match.group(1)
                # Standardize time format
                if 'am' in time_str or 'pm' in time_str:
                    return time_str
                else:
                    # Try to parse
                    try:
                        parsed_time = parser.parse(time_str)
                        return parsed_time.strftime('%H:%M')
                    except:
                        return time_str
        return None
    
    def extract_person(self, message):
        """Extract person involved"""
        # Look for names after "with", "from", "by"
        patterns = [
            r'with\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1).strip()
        
        return None
    
    def determine_priority(self, message):
        """Determine priority based on keywords"""
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return priority
        
        return 'medium'