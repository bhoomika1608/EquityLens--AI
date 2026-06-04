# syntax=docker/dockerfile:1

# ─────────────────────────────────────────────────────
# EquityLens AI — Dockerfile
# Multi-stage build for minimal production image
# ─────────────────────────────────────────────────────

FROM python:3.12-slim AS base

# Security: don't run as root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Install system dependencies for unstructured
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ── Dependencies stage ──
FROM base AS deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App stage ──
FROM deps AS app

COPY . .

# Create data directories
RUN mkdir -p data/vector_store data/history && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
