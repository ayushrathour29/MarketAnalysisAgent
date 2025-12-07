
FROM python:3.11-slim

# Set environment variable to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

EXPOSE 7860 


CMD ["python", "main.py"]