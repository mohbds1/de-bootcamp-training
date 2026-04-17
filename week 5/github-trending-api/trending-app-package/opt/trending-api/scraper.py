import requests
from bs4 import BeautifulSoup

def fetch_trending_repos():
    """
    Scrape the GitHub trending page to get the repository name, 
    programming language, and description.
    """
    url = "https://github.com/trending"
    
    # Adding a User-Agent so GitHub doesn't block our script thinking it's a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # Send a GET request with a 10-second timeout just in case the network is slow
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {"error": f"Failed to connect. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.text, 'html.parser')
        repos_data = []

        # Find all the 'article' tags that contain the trending repos
        articles = soup.find_all('article', class_='Box-row')

        for article in articles:
            # 1. Get the repo name and clean up the extra spaces and newlines
            h2_tag = article.find('h2', class_='h3')
            repo_name = h2_tag.text.strip().replace('\n', '').replace(' ', '') if h2_tag else "Unknown"

            # 2. Get the repo description
            p_tag = article.find('p', class_='col-9')
            description = p_tag.text.strip() if p_tag else "No description provided."

            # 3. Get the programming language used
            span_lang = article.find('span', itemprop='programmingLanguage')
            language = span_lang.text.strip() if span_lang else "Not specified"

            # Add the cleaned data to our list as a dictionary
            repos_data.append({
                "repository": repo_name,
                "language": language,
                "description": description
            })

        return repos_data

    except Exception as e:
        # Catch any errors (like no internet) so the program doesn't crash
        return {"error": str(e)}
