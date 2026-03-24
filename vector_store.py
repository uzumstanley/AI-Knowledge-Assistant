from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleVectorStore:
    def __init__(self, docs):
        self.docs = docs
        self.texts = [d.get("page_content", "") for d in docs]
        self.metadata = [d.get("metadata", {}) for d in docs]
        self.vectorizer = TfidfVectorizer().fit(self.texts)
        self.vectors = self.vectorizer.transform(self.texts)

    def similarity_search(self, query, k=6):
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.vectors)[0]
        idx = scores.argsort()[::-1][:k]
        return [self.docs[i] for i in idx]


def create_vector_store(docs, persist_directory=None):
    return SimpleVectorStore(docs)
