ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-alpine

# ---POETRY SETUP---
ENV POETRY_VERSION=1.7.1
# Remove a interação do usuario
ENV POETRY_NO_INTERACTION=true
# Não cria ambientes virtuais na intalação das dependencias do projeto pelo poetry
ENV POETRY_VIRTUALENVS_CREATE=false
# Pasta de ambiente virtual não é setado no projeto
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

#Install  system dependency
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    py3-cryptography

#Worker directory
WORKDIR /app

#Copy dependency files
COPY pyproject.toml poetry.lock ./

#Install poetry
RUN pip install poetry==${POETRY_VERSION}

#Install project dependency
RUN poetry install --no-root

#Copy project
COPY . .

RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/manage.py

ENTRYPOINT [ "/bin/sh", "/app/entrypoint.sh" ]
