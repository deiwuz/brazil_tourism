# Use Python 3.14 as the base image
FROM python:3.14

# Install uv for fast dependency management
RUN pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies using uv
RUN uv pip install . --system

# Run standard ETL pipeline when the container launches
CMD ["python", "main.py"]