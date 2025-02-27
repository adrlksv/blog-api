FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip install poetry
RUN poetry install

EXPOSE 7000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7000"]
