# =============================================================================
# dirvex — Production Dockerfile
# python:3.11-slim base
# Tag: ghcr.io/onebyjorah/dirvex:latest
# =============================================================================

FROM python:3.14-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:14.2.0-1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.14-slim

# Create non-root user
RUN groupadd -r -g 10001 dirvex \
    && useradd -r -u 10001 -g dirvex -d /app -s /sbin/nologin dirvex

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates=20250419 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /usr/local

# Create application directory
RUN mkdir -p /app

# Copy application code
COPY . /app
WORKDIR /app

# Set ownership
RUN chown -R dirvex:dirvex /app

# Switch to non-root user
USER 10001

# Expose application port
EXPOSE 5000

# Healthcheck — verify the app responds
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"]

# Run with gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
