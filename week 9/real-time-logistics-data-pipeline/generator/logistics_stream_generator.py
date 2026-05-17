import csv
import os
import random
import time
import uuid
from datetime import datetime, timedelta, timezone

OUTPUT_DIR = "../data/input"
ROWS_PER_FILE = 1000     
SLEEP_BETWEEN_FILES = 5 

os.makedirs(OUTPUT_DIR, exist_ok=True)

CITIES = ["Sana'a", "Taiz", "Aden", "Ibb", "Hodeidah", "Mukalla"]
STATUSES = ["PICKED_UP", "IN_TRANSIT", "OUT_FOR_DELIVERY", "DELIVERED", "DELAYED"]

VEHICLES = [f"VEH-{str(i).zfill(3)}" for i in range(1, 51)]     
DRIVERS = [f"DRV-{str(i).zfill(4)}" for i in range(1000, 1050)]

last_valid_row = None

def get_current_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def generate_clean_row():
    return [
        str(uuid.uuid4()),                       # event_id
        f"SHP-{random.randint(100000, 999999)}", # shipment_id
        random.choice(VEHICLES),                 # vehicle_id (ثابت لكافكا)
        random.choice(DRIVERS),                  # driver_id
        random.choice(CITIES),                   # city
        round(random.uniform(12.0, 16.5), 6),    # latitude
        round(random.uniform(42.0, 54.0), 6),    # longitude
        round(random.uniform(0, 120), 2),        # speed_kmh
        round(random.uniform(0.5, 80), 2),       # package_weight_kg
        round(random.uniform(1, 900), 2),        # delivery_distance_km
        random.choice(STATUSES),                 # shipment_status
        get_current_timestamp()                  # event_timestamp
    ]

def inject_messy_data(row):
    global last_valid_row

    error_type = random.choices(
        ["clean", "missing_value", "duplicate", "invalid_type", "numeric_inconsistency"],
        weights=[90, 2, 2, 3, 3], 
        k=1
    )[0]

    if error_type == "clean":
        last_valid_row = row.copy()
        return row

    if error_type == "missing_value":
        messy_row = row.copy()
        missing_index = random.choice([4, 10])
        messy_row[missing_index] = ""
        return messy_row

    if error_type == "duplicate" and last_valid_row is not None:
        return last_valid_row.copy()

    if error_type == "invalid_type":
        messy_row = row.copy()
        messy_row[7] = "SPEED_SENSOR_ERROR" 
        return messy_row

    if error_type == "numeric_inconsistency":
        messy_row = row.copy()
        messy_row[8] = -50.5 
        return messy_row

    return row

def write_stream_file(file_index):
    filename = f"logistics_stream_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    headers = [
        "event_id", "shipment_id", "vehicle_id", "driver_id", "city",
        "latitude", "longitude", "speed_kmh", "package_weight_kg",
        "delivery_distance_km", "shipment_status", "event_timestamp"
    ]

    temp_filepath = filepath + ".tmp"

    with open(temp_filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for _ in range(ROWS_PER_FILE):
            clean_row = generate_clean_row()
            writer.writerow(inject_messy_data(clean_row))

    os.rename(temp_filepath, filepath)
    print(f"[{file_index}] Generated file: {filepath} (Size: ~{os.path.getsize(filepath)/1024:.1f} KB)")

def main():
    print("Starting Smart Logistics CSV Streaming Generator (INFINITE MODE)...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("Press Ctrl+C to stop the generator.")

    file_index = 1
    try:
        while True:
            write_stream_file(file_index)
            time.sleep(SLEEP_BETWEEN_FILES)
            file_index += 1
    except KeyboardInterrupt:
        print("\n[!] Generator stopped safely by user.")

if __name__ == "__main__":
    main()