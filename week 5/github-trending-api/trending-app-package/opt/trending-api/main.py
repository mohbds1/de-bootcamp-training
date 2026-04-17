from fastapi import FastAPI
from scraper import fetch_trending_repos

# Define the FastAPI app with some info for the Swagger docs
app = FastAPI(
    title="GitHub Trending Scraper API",
    description="A network-based application that scrapes daily trending repositories from GitHub.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to GitHub Trending API!",
        "endpoints": "Visit /trending to get today's top repositories.",
        "documentation": "Visit /docs for Swagger UI."
    }

@app.get("/trending")
def get_trending():
    """
    Main endpoint to trigger the scraping script and return the data as JSON.
    """
    data = fetch_trending_repos()
    
    # Check if the scraper returned an error message
    if isinstance(data, dict) and "error" in data:
        return {"status": "failed", "error": data["error"]}
        
    return {
        "status": "success",
        "total_repos": len(data),
        "data": data
    }
