FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garante que o SQLite tenha permissões corretas
RUN chmod 666 /app/meu_banco.db || true

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

# Garante que as permissões do diretório da aplicação estejam corretas
RUN chown -R nobody:nogroup /app

# Muda para um usuário não-root por segurança
USER nobody

CMD ["python", "run.py"]