FROM python:3.9-slim-buster
WORKDIR /app

# Install ntpdate for time synchronization
RUN apt-get update && apt-get install -y ntpdate && apt-get clean

# Synchronize time
RUN ntpdate pool.ntp.org || true

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
