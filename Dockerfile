FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_ENV='production'
CMD ["flask", "--app", "api/", "run", "--host", "0.0.0.0"]