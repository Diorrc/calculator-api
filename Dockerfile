# Use official Python runtime - debian-based for better compatibility
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Poetry
ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies only (no dev dependencies)
RUN poetry install --no-root --only main

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run injects PORT env variable (default 8080)
ENV PORT=8080

# Expose port (documentation only)
EXPOSE 8080

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
