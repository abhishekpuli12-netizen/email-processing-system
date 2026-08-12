import json

mandatory_ids = [
    'MSG_0002', 'MSG_0007', 'MSG_0001', 'MSG_0003', 'MSG_0009',
    'MSG_0016', 'MSG_0004', 'MSG_0006', 'MSG_0014', 'MSG_0015',
    'MSG_0005', 'MSG_0013', 'MSG_0012', 'MSG_0024', 'MSG_0037'
]

print("\n" + "="*70)
print("MANDATORY MESSAGE IDs - COMPREHENSIVE VERIFICATION")
print("="*70)

# Load all data
with open('output/classifications.json', 'r') as f:
    classifications = json.load(f)

with open('output/tasks.json', 'r') as f:
    data = json.load(f)
    tasks = data.get('tasks', [])

with open('output/sensitive.json', 'r') as f:
    sensitive = json.load(f)
    
with open('C:\\Users\\USER\\Downloads\\L1_Candidate_Dataset\\messages.csv', 'r', encoding='utf-8') as f:
    csv_lines = f.readlines()

# Create dictionaries
class_dict = {c['message_id']: c for c in classifications}
task_dict = {}
for task in tasks:
    source_id = task['source_message_id']
    if source_id not in task_dict:
        task_dict[source_id] = []
    task_dict[source_id].append(task)

sensitive_dict = {}
for sens in sensitive:
    msg_id = sens['message_id']
    if msg_id not in sensitive_dict:
        sensitive_dict[msg_id] = []
    sensitive_dict[msg_id].append(sens)

# Extract message content from CSV
msg_content = {}
for line in csv_lines[1:]:
    parts = line.strip().split(',', 3)
    if len(parts) >= 4:
        msg_id = parts[0]
        content = parts[3]
        msg_content[msg_id] = content

print("\nVERIFICATION RESULTS:")
print("="*70)

found_count = 0
for i, msg_id in enumerate(mandatory_ids, 1):
    if msg_id in class_dict:
        found_count += 1
        print(f"\n{i:2d}. {msg_id} ✅ FOUND")
        
        # Show classification
        c = class_dict[msg_id]
        print(f"    Category: {c['category']}")
        print(f"    Confidence: {c['confidence']}")
        
        # Show tasks/events
        if msg_id in task_dict:
            print(f"    Tasks/Events: {len(task_dict[msg_id])} extracted")
            for t in task_dict[msg_id]:
                print(f"      - [{t['type'].upper()}] {t['title']}")
        else:
            print(f"    Tasks/Events: None")
        
        # Show sensitive
        if msg_id in sensitive_dict:
            print(f"    Sensitive: {len(sensitive_dict[msg_id])} detected")
            for s in sensitive_dict[msg_id]:
                print(f"      - {s['sensitivity_type']} (Risk: {s['risk']})")
        else:
            print(f"    Sensitive: None")
    else:
        print(f"\n{i:2d}. {msg_id} ❌ MISSING")

print("\n" + "="*70)
print(f"SUMMARY: {found_count}/15 mandatory messages found")
if found_count == 15:
    print("✅ ALL MANDATORY MESSAGE IDs ARE PRESENT IN THE SYSTEM!")
else:
    print(f"⚠️  Missing {15-found_count} messages")
print("="*70 + "\n")
