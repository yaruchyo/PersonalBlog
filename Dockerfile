FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y curl

WORKDIR /PersonalBlog
# Copy the project files into the container
COPY . .


RUN python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate" && \
    pip3 install -r requirements.txt

CMD gunicorn run:app --bind 0.0.0.0:8080


