FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies and the package
RUN pip install --no-cache-dir -e .

# Expose port for FastAPI
EXPOSE 8000

# Command to run the FastAPI application
CMD ["python", "src/vizeval/main.py"]