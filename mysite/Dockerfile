FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev && \
    pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the entire project
COPY . /app/

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Expose port (different than compiler container)
EXPOSE 8001

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
