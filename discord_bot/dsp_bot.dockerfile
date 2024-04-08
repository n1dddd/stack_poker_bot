FROM python:3.9.18-slim

WORKDIR /discord_bot

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]