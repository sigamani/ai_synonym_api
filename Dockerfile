# Use the official Python image with the specified version
FROM python:3.11.11
LABEL authors="michaelsigamani"

# Set the working directory
WORKDIR /app

# Copy the application files to the working directory
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV PORT=8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port=${PORT:-8000}"]