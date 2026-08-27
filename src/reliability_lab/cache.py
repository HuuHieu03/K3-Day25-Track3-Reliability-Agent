from __future__ import annotations

import hashlib
import logging
import math
import re
import time
from collections import Counter
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared utilities — use these in both ResponseCache and SharedRedisCache
# ---------------------------------------------------------------------------

PRIVACY_PATTERNS = re.compile(
    r"\b(balance|password|credit.card|ssn|social.security|user.\d+|account.\d+)\b",
    re.IGNORECASE,
)


def _is_uncacheable(query: str) -> bool:
    """Return True if query contains privacy-sensitive keywords."""
    return bool(PRIVACY_PATTERNS.search(query))


def _looks_like_false_hit(query: str, cached_key: str) -> bool:
    """Return True if query and cached key contain different 4-digit numbers (years, IDs)."""
    nums_q = set(re.findall(r"\b\d{4}\b", query))
    nums_c = set(re.findall(r"\b\d{4}\b", cached_key))
    return bool(nums_q and nums_c and nums_q != nums_c)


# ---------------------------------------------------------------------------
# In-memory cache (existing)
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class CacheEntry:
    key: str
    value: str
    created_at: float
    metadata: dict[str, str]


class ResponseCache:
    """In-memory semantic cache with n-gram cosine similarity and guardrails."""

    def __init__(self, ttl_seconds: int, similarity_threshold: float) -> None:
        self.ttl_seconds = ttl_seconds
        self.similarity_threshold = similarity_threshold
        self._entries: list[CacheEntry] = []
        self.false_hit_log: list[dict[str, object]] = []

    def get(self, query: str) -> tuple[str | None, float]:
        """Look up a cached response by semantic similarity."""
        if _is_uncacheable(query):
            return None, 0.0

        now = time.time()
        self._entries = [e for e in self._entries if (now - e.created_at) <= self.ttl_seconds]
        if not self._entries:
            return None, 0.0

        best_entry: CacheEntry | None = None
        best_score = 0.0
        for entry in self._entries:
            score = self.similarity(query, entry.key)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry is not None and best_score >= self.similarity_threshold:
            if _looks_like_false_hit(query, best_entry.key):
                self.false_hit_log.append(
                    {
                        "query": query,
                        "cached_key": best_entry.key,
                        "score": best_score,
                        "reason": "date_or_number_mismatch",
                    }
                )
                return None, best_score
            return best_entry.value, best_score

        return None, best_score

    def set(self, query: str, value: str, metadata: dict[str, str] | None = None) -> None:
        """Store a response in cache with privacy guardrail."""
        if _is_uncacheable(query):
            return
        meta = metadata if metadata is not None else {}
        self._entries.append(
            CacheEntry(key=query, value=value, created_at=time.time(), metadata=meta)
        )

    @staticmethod
    def similarity(a: str, b: str) -> float:
        """Compute semantic similarity between two strings using n-gram cosine similarity."""
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0

        words_a = a.lower().split()
        words_b = b.lower().split()

        ngrams_a = [w[i : i + 3] for w in words_a for i in range(len(w) - 2)]
        ngrams_b = [w[i : i + 3] for w in words_b for i in range(len(w) - 2)]

        tokens_a = words_a + ngrams_a
        tokens_b = words_b + ngrams_b

        vec_a = Counter(tokens_a)
        vec_b = Counter(tokens_b)

        dot_product = sum(vec_a[k] * vec_b[k] for k in vec_a if k in vec_b)
        norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
        norm_b = math.sqrt(sum(v * v for v in vec_b.values()))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))


# ---------------------------------------------------------------------------
# Redis shared cache (new)
# ---------------------------------------------------------------------------


class SharedRedisCache:
    """Redis-backed shared cache for multi-instance deployments."""

    def __init__(
        self,
        redis_url: str,
        ttl_seconds: int,
        similarity_threshold: float,
        prefix: str = "rl:cache:",
    ):
        import redis as redis_lib

        self.ttl_seconds = ttl_seconds
        self.similarity_threshold = similarity_threshold
        self.prefix = prefix
        self.false_hit_log: list[dict[str, object]] = []
        self._redis: Any = redis_lib.Redis.from_url(redis_url, decode_responses=True)

    def ping(self) -> bool:
        """Check Redis connectivity."""
        try:
            return bool(self._redis.ping())
        except Exception:  # noqa: BLE001
            return False

    def get(self, query: str) -> tuple[str | None, float]:
        """Look up a cached response from Redis."""
        if _is_uncacheable(query):
            return None, 0.0

        exact_key = f"{self.prefix}{self._query_hash(query)}"
        try:
            resp = self._redis.hget(exact_key, "response")
            if resp is not None:
                cached_query = self._redis.hget(exact_key, "query")
                if cached_query is not None and _looks_like_false_hit(query, str(cached_query)):
                    self.false_hit_log.append(
                        {
                            "query": query,
                            "cached_key": cached_query,
                            "score": 1.0,
                            "reason": "date_or_number_mismatch",
                        }
                    )
                    return None, 1.0
                return str(resp), 1.0
        except Exception as err:  # noqa: BLE001
            logger.debug("Redis exact lookup failed: %s", err)

        best_score = 0.0
        best_response: str | None = None
        best_query: str | None = None

        try:
            for key in self._redis.scan_iter(f"{self.prefix}*"):
                data = self._redis.hgetall(key)
                if not data:
                    continue
                cached_query = data.get("query")
                cached_response = data.get("response")
                if cached_query and cached_response:
                    score = ResponseCache.similarity(query, cached_query)
                    if score > best_score:
                        best_score = score
                        best_response = cached_response
                        best_query = cached_query
        except Exception as err:  # noqa: BLE001
            logger.debug("Redis scan lookup failed: %s", err)

        if best_response is not None and best_score >= self.similarity_threshold:
            if best_query is not None and _looks_like_false_hit(query, best_query):
                self.false_hit_log.append(
                    {
                        "query": query,
                        "cached_key": best_query,
                        "score": best_score,
                        "reason": "date_or_number_mismatch",
                    }
                )
                return None, best_score
            return best_response, best_score

        return None, best_score

    def set(self, query: str, value: str, metadata: dict[str, str] | None = None) -> None:
        """Store a response in Redis with TTL."""
        if _is_uncacheable(query):
            return
        key = f"{self.prefix}{self._query_hash(query)}"
        try:
            self._redis.hset(key, mapping={"query": query, "response": value})
            self._redis.expire(key, self.ttl_seconds)
        except Exception as err:  # noqa: BLE001
            logger.debug("Redis set failed: %s", err)

    def flush(self) -> None:
        """Remove all entries with this cache prefix (for testing)."""
        for key in self._redis.scan_iter(f"{self.prefix}*"):
            self._redis.delete(key)

    def close(self) -> None:
        """Close Redis connection."""
        if self._redis is not None:
            self._redis.close()

    @staticmethod
    def _query_hash(query: str) -> str:
        """Deterministic short hash for a query string."""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()[:12]
