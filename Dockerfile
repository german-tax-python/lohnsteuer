FROM python:3.6

COPY . /app/lohnsteuer
WORKDIR app/lohnsteuer

RUN pip3 install -r requirements.txt && \
    python3 -m pytest test/test_steuer.py
