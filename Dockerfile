FROM python:3.14

ENV TZ=Europe/Moscow

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python main.py"]