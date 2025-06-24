# Use an official Python base image
FROM python:3.12-slim

# 1. Set the working directory to /app
WORKDIR /app

# 1.1. Ensure Python will search /app for modules
ENV PYTHONPATH=/app

# 2. Copy and install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the code, including tests
COPY . .

# 4. Install test libraries
RUN pip install pytest httpx pytest-asyncio

# 5. Expose port and default command
EXPOSE 3011
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3011"]
