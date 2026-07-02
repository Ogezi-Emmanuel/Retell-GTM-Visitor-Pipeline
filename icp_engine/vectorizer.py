# vectorizer.py
import math
import re
from collections import Counter
from typing import List, Dict

class VectorEngine:
    def __init__(self):
        self.vocab = set()
        self.idf = {}
        
    def _tokenize(self, text: str) -> List[str]:
        """Pure alphanumeric extraction, dropping short words to reduce noise."""
        return re.findall(r'\b[a-z]{4,}\b', str(text).lower())

    def train(self, base_documents: List[str]):
        """Builds the TF-IDF matrix weights based on your blueprint and noise corpus."""
        total_docs = len(base_documents)
        doc_freqs = Counter()
        
        for doc in base_documents:
            tokens = set(self._tokenize(doc))
            self.vocab.update(tokens)
            for token in tokens:
                doc_freqs[token] += 1
                
        # Calculate IDF: log(N / df)
        for token, count in doc_freqs.items():
            self.idf[token] = math.log(total_docs / (1 + count))

    def vectorize(self, text: str) -> Dict[str, float]:
        """Projects raw text into the trained vector space."""
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        total_terms = len(tokens) if tokens else 1
        
        vector = {}
        for token in self.vocab:
            # TF-IDF calculation
            term_freq = tf[token] / total_terms
            vector[token] = term_freq * self.idf.get(token, 0)
        return vector

    @staticmethod
    def calculate_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
        """Calculates the Cosine Similarity angle between two vectors."""
        dot_product = sum(v1[k] * v2.get(k, 0) for k in v1)
        mag1 = math.sqrt(sum(val**2 for val in v1.values()))
        mag2 = math.sqrt(sum(val**2 for val in v2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)