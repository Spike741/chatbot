# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt if you have one, or create it below
# If you don't have a requirements.txt, create one with the necessary packages:
# streamlit
# groq

# Create requirements.txt
RUN echo "streamlit\ngroq\n" > requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container
COPY stream.py .

# Expose the Streamlit default port
EXPOSE 8501

# Set environment variable for Streamlit to allow access from outside the container
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to run the Streamlit app
CMD ["streamlit", "run", "stream.py"]
