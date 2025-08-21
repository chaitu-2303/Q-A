# Stage 1: Build the application
FROM python:3.9-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Stage 2: Create the final, production-ready image
FROM python:3.9-slim

WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code from the builder stage
COPY --from=builder /app .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
