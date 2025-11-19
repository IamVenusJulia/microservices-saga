FROM python:3.10-slim
WORKDIR /app

COPY girl-service/requirements.txt .
COPY girl-service/app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]