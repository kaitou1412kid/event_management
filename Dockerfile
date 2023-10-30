FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY event /app/
COPY .env /app/
EXPOSE 8000

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A event beat --loglevel=info & celery -A event.celery worker --pool=solo -l info"]