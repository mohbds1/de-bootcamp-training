# 🧠 Article Similarity Calculator

A high-performance Python-based system for computing article-to-article similarity using vector space modeling and efficient numerical computation.
The project also includes an interactive search engine powered by an inverted index for fast text retrieval.

---

## 🚀 Features

* **Advanced Text Preprocessing**

  * Lowercasing
  * Digit removal
  * Punctuation cleaning
  * Tokenization

* **Binary Bag-of-Words Representation**

  * Builds a global vocabulary from all articles
  * Converts each article into a binary vector (word presence/absence)

* **Efficient Cosine Similarity**

  * Fully implemented using NumPy
  * Vectorized operations for high performance
  * Handles zero vectors safely

* **Top-K Similar Articles**

  * Retrieves the most similar articles to a given article
  * Excludes the target article itself
  * Sorted by similarity score (descending)

* **Interactive Search Engine (Bonus)**

  * Uses an inverted index `(token → document_ids)`
  * Supports real-time query matching
  * Returns top relevant articles instantly

---

## 📁 Project Structure

```
.
├── main.py              # Entry point (pipeline + interactive search)
├── preprocessing.py     # Text cleaning and tokenization
├── vectorization.py     # Vocabulary building + vectorization + inverted index
├── similarity.py        # Cosine similarity + ranking + search logic
├── utils.py             # CSV reader + pickle save/load helpers
├── articles.csv         # Input dataset (id, title, content)
└── similarities.pkl     # Output similarity matrix
```

---

## 🛠 Requirements

* Python 3.7+
* NumPy

Install dependencies:

```bash
pip install numpy
```

---

## ⚙️ Usage

1. Place your dataset in the project root as `articles.csv`
   Required columns:

   ```
   id, title, content
   ```

2. Run the program:

```bash
python main.py
```

---

## 🔄 Execution Flow

When running `main.py`, the system performs:

1. **Data Loading**

   * Reads articles from CSV

2. **Text Processing**

   * Cleans and tokenizes `title + content`

3. **Vocabulary Construction**

   * Builds a global word dictionary

4. **Vectorization**

   * Converts each article into a binary vector

5. **Similarity Computation**

   * Computes cosine similarity matrix using NumPy

6. **Persistence**

   * Saves the similarity matrix to `similarities.pkl`

7. **Demo Output**

   * Displays top 3 similar articles for a sample input

8. **Interactive Search**

   * Accepts user queries
   * Returns best matching articles using inverted index

---

## 🧠 How It Works (Under the Hood)

### 1. Text Representation

Each article is represented as a combination of:

```
title + content
```

After preprocessing, it becomes a list of tokens.

---

### 2. Vector Space Model

* A global vocabulary is created from all tokens
* Each article is converted into a binary vector:

```
1 → word exists in article  
0 → word does not exist
```

---

### 3. Cosine Similarity

Similarity between articles is computed using:

```
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)
```

Implemented efficiently using NumPy matrix operations.

---

### 4. Inverted Index (Search Engine)

Maps:

```
word → [article_indices]
```

This allows fast lookup of relevant documents without scanning all articles.

---

## 🧪 Example Output

```
Top 3 similar to article id=1:
- AI in Healthcare
- Machine Learning Basics
- Deep Learning Advances
```

---

## ⚡ Performance Notes

* The similarity matrix is **precomputed once** and stored using `pickle`
* Enables **instant similarity queries** without recomputation
* Vectorized NumPy operations ensure scalability

---

## 📌 Notes

* No external NLP libraries are used (as required)
* Only standard Python + NumPy are used
* Designed to be modular, readable, and extendable

---

## 🏁 Conclusion

This project demonstrates:

* Text preprocessing fundamentals
* Vector space modeling
* Cosine similarity computation
* Efficient search using inverted indexing

It provides both:
✔ A complete similarity engine
✔ A lightweight search system

---

## 👨‍💻 Author

Developed as part of an academic assignment in text similarity and information retrieval.
