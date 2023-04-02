FROM python:3.11.1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn","comcigan_api.main:app", "--host", "0.0.0.0", "--port", "8000"]