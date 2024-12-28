# Use the official Python image with the specified version
FROM python:3.11.11-slim
LABEL authors="michaelsigamani"

ENTRYPOINT ["top", "-b"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Set the working directory
WORKDIR /app

# Copy the application files to the working directory
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE ${PORT}

# Define the command to run the application
CMD ["sh", "-c", "uvicorn app.main:app --host=0.0.0.0 --port=${PORT}"]