FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and assets
COPY . .

# Ensure unbuffered output for logs
ENV PYTHONUNBUFFERED=1

# Run Flask app
CMD ["python", "app.py"]