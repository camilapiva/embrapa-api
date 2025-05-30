FROM python:3.13-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry

# Copia arquivos essenciais para instalar dependências
COPY pyproject.toml poetry.lock* /app/

# Instala dependências com poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copia o restante da aplicação
COPY ./app /app/app

EXPOSE 8011

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8011"]