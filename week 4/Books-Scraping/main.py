import os


os.makedirs("./data/processed", exist_ok=True)
os.makedirs("./data/processed/1_star", exist_ok=True)
os.makedirs("./data/processed/2_star", exist_ok=True)
os.makedirs("./data/processed/3_star", exist_ok=True)
os.makedirs("./data/processed/4_star", exist_ok=True)
os.makedirs("./data/processed/5_star", exist_ok=True)

os.makedirs("./data/raw", exist_ok=True)

os.makedirs("./images", exist_ok=True)
os.makedirs("./images/1_star", exist_ok=True)
os.makedirs("./images/2_star", exist_ok=True)
os.makedirs("./images/3_star", exist_ok=True)
os.makedirs("./images/4_star", exist_ok=True)
os.makedirs("./images/5_star", exist_ok=True)

from scraper import scrape_books
from processor import process_data
from organizer import organize_data

print("\n[1/3] 🌐 Scraping books data and downloading images...")
raw_books = scrape_books(max_pages=6)
print(f"      ✓ Successfully scraped {len(raw_books)} books.")

print("\n[2/3] 🧹 Cleaning and processing raw data...")
df = process_data(raw_books)
print(f"      ✓ Processed and deduplicated {len(df)} records.")

print("\n[3/3] 📁 Organizing images and datasets by star rating...")
organize_data(df)
print("      ✓ Files organized successfully.")

print("\n✨ Pipeline Complete! Your datasets and images are ready in the './data' and './images' folders.\n")
