FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    pkgconf \
    python3-dev \
    libffi-dev \
    openssl-dev \
    netcat-openbsd

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/scripts/wait-for-db.sh /app/scripts/create_superuser.py
RUN chmod +x /app/scripts/wait-for-db.sh

EXPOSE 8000

CMD ["sh", "/app/scripts/wait-for-db.sh"]