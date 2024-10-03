FROM python:3.10-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        postgresql-dev gcc musl-dev libpq-dev python3-dev

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]