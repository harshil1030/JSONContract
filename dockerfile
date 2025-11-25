# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run Flask using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
