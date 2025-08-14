from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
import uuid
from settings import AppSettings

# In-memory vector store shared across service instances
_IN_MEMORY_POINTS: List[Dict[str, Any]] = []


def _cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors with safe handling."""
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))


class VectorDBService:
    def __init__(self):
        """Initialize sentence transformer model and in-memory store."""
        settings = AppSettings()
        self.embedding_model = SentenceTransformer(settings.sentence_transformer_model)
        self.collection_name = "conversation_embeddings"
        self.vector_size = self.embedding_model.get_sentence_embedding_dimension()

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for given text."""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []

    async def store_conversation_embedding(
        self,
        conversation_id: int,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store conversation embedding in the in-memory vector store."""
        try:
            text_to_embed = f"{title}: {content}"
            embedding = self.create_embedding(text_to_embed)
            if not embedding:
                return False

            point_metadata: Dict[str, Any] = {
                "conversation_id": conversation_id,
                "title": title,
                "content": content,
                "type": "conversation",
            }
            if metadata:
                point_metadata.update(metadata)

            _IN_MEMORY_POINTS.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": np.asarray(embedding, dtype=np.float32),
                    "payload": point_metadata,
                }
            )
            return True
        except Exception as e:
            print(f"Error storing conversation embedding: {e}")
            return False

    async def store_message_embedding(
        self,
        message_id: int,
        conversation_id: int,
        prompt_content: str,
        response_content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store message embedding in the in-memory vector store."""
        try:
            text_to_embed = f"Q: {prompt_content} A: {response_content}"
            embedding = self.create_embedding(text_to_embed)
            if not embedding:
                return False

            point_metadata: Dict[str, Any] = {
                "message_id": message_id,
                "conversation_id": conversation_id,
                "prompt_content": prompt_content,
                "response_content": response_content,
                "type": "message",
            }
            if metadata:
                point_metadata.update(metadata)

            _IN_MEMORY_POINTS.append(
                {
                    "id": str(uuid.uuid4()),
                    "vector": np.asarray(embedding, dtype=np.float32),
                    "payload": point_metadata,
                }
            )
            return True
        except Exception as e:
            print(f"Error storing message embedding: {e}")
            return False

    async def search_similar_conversations(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Search for similar conversations based on query."""
        try:
            query_embedding = self.create_embedding(query)
            if not query_embedding:
                return []
            qv = np.asarray(query_embedding, dtype=np.float32)

            scored: List[Dict[str, Any]] = []
            for point in _IN_MEMORY_POINTS:
                payload = point["payload"]
                if payload.get("type") != "conversation":
                    continue
                score = _cosine_similarity(qv, point["vector"])
                if score >= score_threshold:
                    scored.append(
                        {
                            "conversation_id": payload.get("conversation_id"),
                            "title": payload.get("title"),
                            "content": payload.get("content"),
                            "similarity_score": score,
                            "metadata": {
                                k: v
                                for k, v in payload.items()
                                if k not in ["conversation_id", "title", "content"]
                            },
                        }
                    )

            scored.sort(key=lambda x: x["similarity_score"], reverse=True)
            return scored[:limit]
        except Exception as e:
            print(f"Error searching similar conversations: {e}")
            return []

    async def search_similar_messages(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Search for similar messages based on query."""
        try:
            query_embedding = self.create_embedding(query)
            if not query_embedding:
                return []
            qv = np.asarray(query_embedding, dtype=np.float32)

            scored: List[Dict[str, Any]] = []
            for point in _IN_MEMORY_POINTS:
                payload = point["payload"]
                if payload.get("type") != "message":
                    continue
                score = _cosine_similarity(qv, point["vector"])
                if score >= score_threshold:
                    scored.append(
                        {
                            "message_id": payload.get("message_id"),
                            "conversation_id": payload.get("conversation_id"),
                            "prompt_content": payload.get("prompt_content"),
                            "response_content": payload.get("response_content"),
                            "similarity_score": score,
                            "metadata": {
                                k: v
                                for k, v in payload.items()
                                if k
                                not in [
                                    "message_id",
                                    "conversation_id",
                                    "prompt_content",
                                    "response_content",
                                ]
                            },
                        }
                    )

            scored.sort(key=lambda x: x["similarity_score"], reverse=True)
            return scored[:limit]
        except Exception as e:
            print(f"Error searching similar messages: {e}")
            return []

    async def delete_conversation_embeddings(self, conversation_id: int) -> bool:
        """Delete all embeddings for a specific conversation."""
        try:
            global _IN_MEMORY_POINTS
            _IN_MEMORY_POINTS = [
                p
                for p in _IN_MEMORY_POINTS
                if p.get("payload", {}).get("conversation_id") != conversation_id
            ]
            return True
        except Exception as e:
            print(f"Error deleting conversation embeddings: {e}")
            return False

    async def delete_message_embeddings(self, message_id: int) -> bool:
        """Delete embeddings for a specific message."""
        try:
            global _IN_MEMORY_POINTS
            _IN_MEMORY_POINTS = [
                p
                for p in _IN_MEMORY_POINTS
                if p.get("payload", {}).get("message_id") != message_id
            ]
            return True
        except Exception as e:
            print(f"Error deleting message embeddings: {e}")
            return False

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the in-memory vector collection."""
        try:
            return {
                "name": self.collection_name,
                "vector_size": self.vector_size,
                "distance": "cosine",
                "points_count": sum(1 for _ in _IN_MEMORY_POINTS),
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return {}