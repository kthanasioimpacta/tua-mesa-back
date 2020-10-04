FROM python:3.7

EXPOSE 5000

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
CMD ["flask","run", "--host=0.0.0.0",  "--port=5000"]