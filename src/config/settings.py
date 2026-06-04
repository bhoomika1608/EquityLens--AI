"""
settings.py — Centralized application configuration.
Loads all settings from environment variables with sensible defaults.

Supports:
  - xAI Grok (via OpenAI-compatible SDK)  ← default
  - OpenAI (set OPENAI_API_KEY instead)
  - Local HuggingFace embeddings (no embedding API key required)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


@dataclass
class LLMConfig:
    """LLM and embedding configuration.

    Priority: GROK_API_KEY → OPENAI_API_KEY
    The same openai-compatible SDK is used for both; only the base_url differs.
    """
    # Key resolution: prefer Grok, fall back to OpenAI
    grok_api_key: str = field(default_factory=lambda: os.getenv("GROK_API_KEY", ""))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    # Endpoint — xAI Grok uses https://api.x.ai/v1, OpenAI uses None (default)
    llm_base_url: str = field(
        default_factory=lambda: os.getenv("LLM_BASE_URL", "https://api.x.ai/v1")
    )

    model_name: str = field(
        default_factory=lambda: os.getenv("LLM_MODEL", "grok-3-fast-beta")
    )
    temperature: float = 0.7
    max_tokens: int = 800

    # Embedding provider: "local" (HuggingFace, free) or "openai"
    embedding_provider: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_PROVIDER", "local")
    )
    # Used only when embedding_provider="openai"
    embedding_model: str = "text-embedding-ada-002"
    # Used when embedding_provider="local"
    local_embedding_model: str = "all-MiniLM-L6-v2"

    @property
    def active_api_key(self) -> str:
        """Return whichever API key is configured."""
        return self.grok_api_key or self.openai_api_key

    @property
    def provider_name(self) -> str:
        """Human-readable provider label for the UI."""
        if self.grok_api_key:
            return "xAI Grok"
        if self.openai_api_key:
            return "OpenAI"
        return "Not configured"


@dataclass
class VectorStoreConfig:
    """FAISS vector store configuration."""
    store_dir: Path = field(default_factory=lambda: ROOT_DIR / "data" / "vector_store")
    store_filename: str = "faiss_index"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    k_retrieval: int = 4  # number of docs to retrieve


@dataclass
class AppConfig:
    """Streamlit application configuration."""
    title: str = "EquityLens AI"
    subtitle: str = "Institutional-Grade Equity Research Powered by AI"
    max_urls: int = 5
    history_file: Path = field(
        default_factory=lambda: ROOT_DIR / "data" / "history" / "research_history.json"
    )
    version: str = "2.1.0"


# Singleton instances used throughout the app
llm_config = LLMConfig()
vector_config = VectorStoreConfig()
app_config = AppConfig()


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate that required configuration values are present.

    Returns:
        (is_valid, list_of_error_messages)
    """
    errors: list[str] = []

    if not llm_config.active_api_key:
        errors.append(
            "No API key found. Set GROK_API_KEY (for xAI Grok) or "
            "OPENAI_API_KEY (for OpenAI) in your .env file."
        )

    return len(errors) == 0, errors
