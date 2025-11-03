# Use a lightweight Python image
FROM python:3.13.9-alpine3.22

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    curl \
    git

# Copy the application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit default port
EXPOSE 8501

# Add a healthcheck for the Streamlit app
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "mgfhub.py", "--server.port=8501", "--server.address=0.0.0.0"]
