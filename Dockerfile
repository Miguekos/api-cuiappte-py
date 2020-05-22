FROM python:3.6

WORKDIR /app

COPY . /app

RUN pip install -r requeriment.txt

EXPOSE 9876

CMD [ "python" , "main.py" ]