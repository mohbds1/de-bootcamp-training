import numpy as np
import os
from utils import read_articles_csv, save_pickle
from preprocessing import clean_and_tokenize_articles
from vectorization import build_vocabulary, vectorize_articles_binary, build_inverted_index
from similarity import cosine_similarity_matrix, top_k_similar_titles, search_by_text

def main():
    input_csv = "articles.csv"
    output_pkl = "similarities.pkl"

    if not os.path.exists(input_csv):
        print(f"Error: Could not find '{input_csv}' in the current directory.")
        return

    # --- Article-to-Article Similarity Pipeline ---
    print("Reading and processing articles for article-to-article similarity...")
    articles = list(read_articles_csv(input_csv))
    tokenized_articles = list(clean_and_tokenize_articles(articles))

    vocab = build_vocabulary(tokenized_articles)
    vectors = vectorize_articles_binary(tokenized_articles, vocab)
    sim_matrix = cosine_similarity_matrix(vectors)
    save_pickle(sim_matrix, output_pkl)
    print(f"Saved similarity matrix to {output_pkl} (Shape: {sim_matrix.shape})")

    if articles:
        demo_id = articles[0]["id"]
        top_titles = top_k_similar_titles(demo_id, articles, sim_matrix, k=3)
        print(f"\nTop 3 similar to article id={demo_id} ({articles[0]['title']}):")
        for t in top_titles:
            print(" -", t)

    # --- Interactive Search Pipeline (اختياري) ---
    print("\nBuilding inverted index for interactive search...")
    inverted_index = build_inverted_index(tokenized_articles)
    print("Index built.")

    while True:
        query = input("\nEnter search query (or blank to exit): ").strip()
        if not query:
            break
        results = search_by_text(query, inverted_index, articles, k=3)
        if results:
            print("Top matches:")
            for t in results:
                print(" -", t)
        else:
            print("No matches found.")

if __name__ == "__main__":
    main()