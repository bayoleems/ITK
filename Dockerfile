FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

RUN playwright install chromium && playwright install-deps

COPY . .

ENV PYTHONPATH=.

EXPOSE 8000

CMD ["python", "app/main.py"]