FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Create a non-root user (Hugging Face strongly recommends this)
RUN useradd -m -u 1000 user \
    && chown -R user:user /app

# Switch to the non-root user
USER user

# Copy dependency files first to leverage Docker layer caching
COPY --chown=user:user pyproject.toml uv.lock ./

# Install dependencies into a virtual environment (.venv)
RUN uv sync --frozen --no-dev

# Copy the rest of the application code
COPY --chown=user:user . .

# Hugging Face Spaces defaults to exposing port 7860
EXPOSE 7860

# Run the FastAPI application using uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
