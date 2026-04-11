# Books Scraper & Organizer

A complete Python pipeline that scrapes book information from [Books to Scrape](https://books.toscrape.com/), cleans the data, downloads the book cover images, and elegantly organizes them based on their star ratings.

## 🚀 Features

- **Web Scraping:** Sequentially extracts book titles, prices, star ratings, and image URLs directly from the website across multiple pages.
- **Data Processing & Cleaning:** Cleans the scraped price values (removing currency symbols) and standardizes the star ratings to integers. The data is deduplicated and safely stored in structured CSV files using `pandas`.
- **Image Downloading:** Downloads and saves all the associated cover images for the scraped books to the local filesystem.
- **Data Organization:** Intelligently sorts the scraped dataset and downloaded cover images into dedicated subdirectories (`1_star` to `5_star`) based on the book's rating, improving data accessibility and organization.

## 📂 Project Structure

```text
Books-Scraping/
│
├── data/
│   ├── raw/                 # Raw, uncleaned CSV data (raw_books.csv)
│   └── processed/           # Final CSV datasets separated into folders by star rating
│       ├── 1_star/
│       ├── 2_star/
│       ├── 3_star/
│       ├── 4_star/
│       └── 5_star/
│
├── images/                  # Downloaded book cover images
│   ├── ...                  # Temporary root storage before processing
│   ├── 1_star/              # Images correctly organized by star rating
│   ├── 2_star/
│   ├── 3_star/
│   ├── 4_star/
│   └── 5_star/
│
├── scraper.py               # Scrapes web data and downloads images (BeautifulSoup)
├── processor.py             # Cleans raw data and handles type conversion (Pandas)
├── organizer.py             # Automates distribution of datasets and image files
├── main.py                  # Main script that sequentially runs the whole pipeline
├── requirements.txt         # Required Python packages (requests, bs4, pandas)
└── .gitignore               # Ignores generated data, images, and cached files
```

## 🛠 Prerequisites

Ensure you have Python 3 installed. You can install all the required packages using the provided `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ How to Run

Simply execute the main script. It will sequentially run the scraper, processor, and organizer pipelines and log the output to the console.

```bash
python main.py
```

### Steps the Script Takes:
1. **Scraping** (`scraper.py`): Connects to the first 6 pages of the website, downloading images into the root `images/` directory and capturing book properties into a raw list.
2. **Processing** (`processor.py`): Uses Pandas to clean the raw data (removing formatting), safely structures it, drop duplicates, and stores the raw representation as a CSV.
3. **Organizing** (`organizer.py`): Segregates the cleaned DataFrame by star rating and relocates both the subset CSV files and downloaded image files into their respective `1_star` through `5_star` subdirectories.

## 📝 License

This project is licensed under the MIT License.
