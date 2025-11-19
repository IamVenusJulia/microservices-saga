FROM python:3.10-slim
WORKDIR /app

COPY love-coordinator/requirements.txt .
COPY love-coordinator/app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]