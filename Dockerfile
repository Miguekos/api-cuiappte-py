FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requeriment.txt

EXPOSE 9879

CMD [ "python" , "main.py" ]