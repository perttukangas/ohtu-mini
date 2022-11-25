FROM python:3.10.8-slim-bullseye

# Konffaa Poetry
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Asenna Poetry virtuaaliympäristössä
RUN python3 -m venv $POETRY_VENV \
  && $POETRY_VENV/bin/pip install -U pip setuptools \
  && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Lisää `poetry` PATH:iin
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Tee sovellukselle uusi kansio ja mene sinne
WORKDIR /app

# Asenna Poetry riippuvuudet
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Aja softa
COPY . /app
CMD [ "poetry", "run", "invoke", "start" ]