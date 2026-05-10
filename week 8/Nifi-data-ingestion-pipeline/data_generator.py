import json
import time
import random
import uuid
import os
from datetime import datetime

output_dir = r"./data/input"
os.makedirs(output_dir, exist_ok=True)

def generate_messy_data():
    records = []
    for _ in range(random.randint(2, 5)):
        record = {
            "id": str(uuid.uuid4()) if random.random() > 0.1 else None, 
            "user_id": random.randint(1000, 5000),
            "amount": round(random.uniform(50.0, 1500.0), 2) if random.random() > 0.15 else "INVALID_AMOUNT",
            "status": random.choice(["Active", "Pending", "Failed", "???"]), 
            "timestamp": datetime.now().isoformat(),
            "category": random.choice(["Tech", "Food", "Fashion", "Books"])
        }
        records.append(record)
        
        if random.random() > 0.9:
            records.append(record)
            
    return records

print(f"Starting real-time data generation in: {output_dir}")
print("Press Ctrl+C to stop.")

try:
    while True:
        data = generate_messy_data()
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Transaction_{current_time}.json"
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Generated: {filename} containing {len(data)} records.")
        time.sleep(4) 
except KeyboardInterrupt:
    print("\nData generation stopped by user.")