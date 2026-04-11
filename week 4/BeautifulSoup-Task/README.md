# 📚 Web Scraping with BeautifulSoup

A web scraping task that extracts book data from [Books to Scrape](https://books.toscrape.com/) using Python and BeautifulSoup.

---

## 📌 Task Description

Scrape book information (title, price, rating, and cover image) from multiple pages of an online book catalogue, download the cover images locally, and export the collected data to a CSV file.

---

## 🛠️ Tools & Libraries

- **requests** — HTTP requests
- **BeautifulSoup4** — HTML parsing
- **pandas** — Data handling & CSV export
- **os** — File system operations

---

## 📂 Files

| File | Description |
|------|-------------|
| `main.ipynb` | Jupyter Notebook containing the scraping code |
| `scraped_books.csv` | Output dataset (80 books) |
| `images/` | Downloaded book cover images |

---

## ▶️ How to Run

1. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```
2. Open and run `main.ipynb` in Jupyter Notebook.

---

## 📊 Output

The scraper collects **80 books** across 4 pages with the following fields:

| Field | Example |
|-------|---------|
| `title` | Sapiens: A Brief History of Humankind |
| `price` | 54.23 |
| `rating` | Five |
| `file_path` | images/Sapiens A Brief History of Humankind.jpg |
