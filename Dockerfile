# 1. Base image
FROM python:3.12-slim

# 2. Set working directory inside the container
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update \
 && apt-get install -y curl \
 && rm -rf /var/lib/apt/lists/*

# 3. Copy dependency file first (better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the app code
COPY . .

# 6. Expose the app port
EXPOSE 5000

# 7. Command to run the app
CMD ["python", "main.py"]

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1