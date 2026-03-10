FROM python:3.12-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

USER appuser

CMD ["python", "run.py"]