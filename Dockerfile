FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["flask", "--app", "app/app", "run", "--host=0.0.0.0"]