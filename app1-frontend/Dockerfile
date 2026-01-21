FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV API_URL=http://app2-api:5000

EXPOSE 8080

CMD ["python", "app.py"]
