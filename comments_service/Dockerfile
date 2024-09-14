FROM python:3.12

#RUN mkdir /comments_service

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#ENV PYTHONPATH=/comments_service

RUN alembic upgrade head

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8001"]