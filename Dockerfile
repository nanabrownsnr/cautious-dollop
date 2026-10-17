FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY --chown=appuser pyproject.toml ./
COPY --chown=appuser README.md ./
COPY --chown=appuser src/ ./src/

RUN pip install --no-cache-dir .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "cautious_dollop"]
