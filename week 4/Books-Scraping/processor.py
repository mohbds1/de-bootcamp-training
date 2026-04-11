import pandas as pd

def process_data(raw_books):
    """Cleans raw data and prepares it for organization."""
    df = pd.DataFrame(raw_books)

    # first saving the raw data
    df.to_csv("./data/raw/raw_books.csv", index=True)

    # cleaning data
    # Use regex=False to prevent FutureWarnings
    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace('£', '', regex=False)
        df['price'] = df['price'].astype(str).str.replace('Â', '', regex=False)

    if 'star_rating' in df.columns:
        df['star_rating'] = df['star_rating'].map({
            'One' : 1,
            'Two' : 2,
            'Three': 3,
            'Four': 4,
            'Five':5,
        })

    # changing type
    if 'price' in df.columns:
        df['price'] = df['price'].astype(float)
    if 'star_rating' in df.columns:
        df['star_rating'] = df['star_rating'].astype('Int64')

    df.dropna(inplace=True)
    # df.drop_duplicates(inplace=True) doesn't work well with dicts/lists if they exist, but here it's strings/numbers
    if not df.empty:
        df.drop_duplicates(subset=['title'], inplace=True)

    return df
