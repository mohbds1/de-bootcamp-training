from typing import Dict, List
import numpy as np

def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    if not isinstance(vectors, np.ndarray):
        raise ValueError("vectors must be a numpy ndarray")
    if vectors.ndim != 2:
        raise ValueError("vectors must be a 2-D array")

    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    eps = np.finfo(norms.dtype).eps * 10
    normalized_vectors = np.zeros_like(vectors, dtype=np.float32)
    valid_rows_mask = (norms > eps).flatten()
    normalized_vectors[valid_rows_mask] = vectors[valid_rows_mask] / norms[valid_rows_mask]

    sim = normalized_vectors @ normalized_vectors.T
    # تأكد أن قطر المصفوفة يساوي 1 دائمًا (حتى للمتجهات الصفرية)
    np.fill_diagonal(sim, 1.0)
    return sim

def top_k_similar_titles(
    article_id: str,
    articles: List[Dict[str, str]],
    sim_matrix: np.ndarray,
    k: int = 3
) -> List[str]:
    id_to_index = {a["id"]: i for i, a in enumerate(articles)}
    if article_id not in id_to_index:
        raise ValueError(f"article_id '{article_id}' not found.")
    n = len(articles)
    if sim_matrix.shape != (n, n):
        raise ValueError("sim_matrix must be square with size matching number of articles")
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer")

    idx = id_to_index[article_id]
    sims = sim_matrix[idx]
    k = min(k, n - 1)
    if k <= 0:
        return []

    partition_size = min(k + 1, n)
    kth = min(partition_size - 1, len(sims) - 1)
    top_indices_partition = np.argpartition(-sims, kth=kth)[:partition_size]
    sorted_top_indices = sorted(top_indices_partition, key=lambda i: -sims[i])
    final_indices = [i for i in sorted_top_indices if i != idx][:k]
    return [articles[i]["title"] for i in final_indices]

def search_by_text(
    query: str,
    inverted_index: Dict[str, List[int]],
    articles: List[Dict[str, str]],
    k: int = 3,
) -> List[str]:
    from preprocessing import clean_and_tokenize
    from collections import Counter

    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer")
    query_tokens = clean_and_tokenize(query)
    if not query_tokens:
        return []

    doc_scores: Counter = Counter()
    for token in query_tokens:
        if token in inverted_index:
            doc_scores.update(inverted_index[token])

    if not doc_scores:
        return []
    top_doc_indices = [doc_id for doc_id, _ in doc_scores.most_common(k)]
    return [articles[i]["title"] for i in top_doc_indices]