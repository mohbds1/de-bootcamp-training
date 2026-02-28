# Article Similarity Calculator

A fast and efficient Python-based tool for calculating text similarity between articles and providing an interactive search interface.

## 🚀 Features

- **Text Preprocessing**: Cleans and tokenizes article text by converting to lowercase, removing digits, and eliminating punctuation.
- **Binary Vectorization**: Builds a vocabulary and generates binary bag-of-words vectors for articles.
- **Fast Cosine Similarity**: Computes an optimized article-to-article similarity correlation matrix using NumPy and saves it for real-time querying.
- **Top-K Similar Articles**: Recommends the most similar articles related to a specific target article using nearest neighbors.
- **Interactive Search**: Allows users to dynamically query the internal article database and instantly retrieve the best matches via an inverted index.

## 📁 Project Structure

- `main.py`: The main entry point to execute the data processing pipeline and launch the interactive text search interface.
- `preprocessing.py`: Contains text cleaning and tokenization logic.
- `vectorization.py`: Responsible for building the vocabulary, text-to-binary vectorization, and inverted index creation.
- `similarity.py`: Core logic for mathematical cosine similarity computation, top-k similar articles finding, and search matching functionality.
- `utils.py`: Helper functions for reading CSV data files and saving/loading Python serialized Pickle objects.
- `articles.csv`: The required input dataset consisting of `row_id`, `id`, `title`, and `content`.
- `similarities.pkl`: The generated output file successfully storing the dense computed similarity matrix.

## 🛠 Prerequisites

Ensure you have Python 3.7+ installed. The project relies on **NumPy** for fast numerical matrix operations:

```bash
pip install numpy
```

## ⚙️ Usage

1. **Prepare Data**: Ensure your articles are placed in `articles.csv` within the project root directory. The CSV file must contain `id`, `title`, and `content` columns.
2. **Run Execution**: Simply run the `main.py` entry script.

```bash
python main.py
```

### What happens when you run `main.py`?
1. **Pipeline Execution**: The system reads the `articles.csv`, cleans the text, tokenizes it, builds a dictionary, vectorizes documents, and computes the similarity matrix which gets saved in `similarities.pkl`.
2. **Demonstration**: The system will automatically compute and display the top 3 similar articles corresponding to the first article in the dataset.
3. **Interactive Search Loop**: An interactive prompt opens up. You can type keywords or sentences to search through the indexed database. Type an empty string (press Enter) to exit the loop.

## 🧠 How It Works under the hood

1. **Data Ingestion**: Texts are extracted from `content` and `title` variables.
2. **Text Normalization**: Special characters are substituted with spaces, letters are lowercased, and digits are omitted.
3. **Term-Document Matrix Creation**: A binary Bag of Words matrix represents the presence/absence of distinct words across total tokens. 
4. **Vector Mathematics**: Cosine Similitude is quickly computed for row vectors utilizing normalized dot matrix product operations over vector shapes and broadcasting logic logic ensuring no division-by-zero scenarios.
5. **Inverted Indexing**: Implements a highly scalable document retrieval strategy based on `(token) -> [doc_id]` mappings to drastically improve lookup time.
