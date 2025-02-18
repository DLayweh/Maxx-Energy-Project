# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
