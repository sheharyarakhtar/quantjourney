FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install pandas flask

# Copy application files
COPY download_data.py .
COPY serve_csv.py .

# Create output directory
RUN mkdir -p output

# Run the data download script and then start the server
CMD python download_data.py && python serve_csv.py 