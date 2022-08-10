####################################################################################################
## Builder image
####################################################################################################
# Credits to Ellie (@TheSilkky) for the original system + Dockerfile
# Modifed for use with Poetry
FROM python:3.10.6-alpine3.16 AS builder

RUN apk add --no-cache \
    ca-certificates \
    build-base \
    curl \
    linux-headers

# Add Poetry locally
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Beryl

COPY /pyproject.toml /Beryl/
COPY /poetry.lock /Beryl/


# Create dependency wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip wheel --wheel-dir=/Beryl/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10.6-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Beryl

COPY /Bot/beryl.py /Beryl/Bot/
COPY /Bot/Cogs/ /Beryl/Bot/Cogs

# Copy dependency wheels from builder stage
COPY --from=builder /Beryl/wheels /Beryl/wheels
COPY --from=builder /Beryl/requirements.txt /Beryl/requirements.txt

COPY /Alpine-Docker/start.sh /Beryl/start.sh

RUN pip install --upgrade pip setuptools wheel

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" beryl \
    && chown -R beryl:beryl /Beryl \
    && chmod +x /Beryl/start.sh

USER beryl

# Install dependencies
RUN pip install --user --no-index --find-links=/Beryl/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Beryl/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Beryl"
LABEL org.opencontainers.image.description="A Discord Bot"
LABEL org.opencontainers.image.url=""
LABEL org.opencontainers.image.licenses=""
LABEL org.opencontainers.image.source="https://github.com/honchokomodo/beryl"