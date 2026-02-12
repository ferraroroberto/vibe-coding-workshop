import csv
import os
import random
import datetime
import time

script_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(script_dir, "data")
LOGS_DIR = os.path.join(DATA_DIR, "server_logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

print(f"Generating data in {LOGS_DIR}...")
print("This might take a minute...")

# Settings
NUM_FILES = 5
ROWS_PER_FILE = 200_000 # Total 1 million rows

SERVER_NAMES = [f"srv-{i:03d}" for i in range(1, 20)]
ERROR_LEVELS = ["INFO", "INFO", "INFO", "WARN", "WARN", "ERROR"]
MESSAGES = [
    "Connection established",
    "Timeout waiting for response",
    "User authentication success",
    "Packet loss detected",
    "Database query limit exceeded",
    "Cache miss",
    "File not found",
    "Memory spike detected"
]

def generate_log_file(filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "server_id", "level", "message", "response_ms", "user_id"])
        
        start_time = datetime.datetime.now()
        
        rows = []
        for i in range(ROWS_PER_FILE):
            # Generate fake data
            ts = start_time - datetime.timedelta(seconds=random.randint(0, 86400))
            server = random.choice(SERVER_NAMES)
            level = random.choice(ERROR_LEVELS)
            msg = random.choice(MESSAGES)
            resp = random.randint(10, 5000) if level == "ERROR" else random.randint(5, 500)
            uid = random.randint(1000, 9999)
            
            rows.append([ts.isoformat(), server, level, msg, resp, uid])
            
            # Write in chunks to keep memory usage low during generation
            if len(rows) >= 10000:
                writer.writerows(rows)
                rows = []
        
        if rows:
            writer.writerows(rows)

for i in range(NUM_FILES):
    fpath = os.path.join(LOGS_DIR, f"log_chunk_{i+1}.csv")
    print(f"Creating {fpath}...")
    generate_log_file(fpath)

print("Setup complete! You have simulated big data.")
