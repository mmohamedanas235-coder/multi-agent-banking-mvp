from typing import List, Dict, Any
import re
import math
from app.data.knowledge_base import BANK_KNOWLEDGE_DOCS

class KnowledgeRetriever:
    """
    RAG engine utilizing hybrid lexical-keyword matching and BM25 term weighting
    against official NEXUS Banking Policy, Regulatory, and Product documentation.
    """
    def __init__(self, docs: List[Dict[str, str]] = None):
        self.docs = docs or BANK_KNOWLEDGE_DOCS

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text)]

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return self.docs[:top_k]

        scored_results = []
        for doc in self.docs:
            combined_text = f"{doc['title']} {doc['tags']} {doc['content']}".lower()
            doc_tokens = self._tokenize(combined_text)
            
            # Simple BM25-inspired scoring
            score = 0.0
            doc_len = len(doc_tokens)
            for token in query_tokens:
                freq = doc_tokens.count(token)
                if freq > 0:
                    tf = (freq * 2.2) / (freq + 1.2 * (0.25 + 0.75 * (doc_len / 120.0)))
                    # boost if matches tags or title
                    if token in doc['tags'].lower():
                        tf *= 2.0
                    if token in doc['title'].lower():
                        tf *= 2.5
                    score += tf

            if score > 0.1:
                scored_results.append({
                    "id": doc["id"],
                    "category": doc["category"],
                    "title": doc["title"],
                    "content": doc["content"],
                    "relevance_score": round(min(score / 5.0, 0.99), 3)
                })

        # Sort by relevance descending
        scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_results[:top_k]

rag_retriever = KnowledgeRetriever()
