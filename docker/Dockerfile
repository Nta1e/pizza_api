FROM python:3.7

WORKDIR /app

COPY ./scripts/start_server.sh /app
COPY ./scripts/wait_for_db.sh /app
COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x start_server.sh && \
    chmod +x wait_for_db.sh

ENTRYPOINT "./wait_for_db.sh"
