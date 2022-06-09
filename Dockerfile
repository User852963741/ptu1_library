# syntax=docker/dockerfile:1
FROM python:3.10.5-slim-buster
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./library .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "-b", "0.0.0.0:8000", "library.wsgi"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
