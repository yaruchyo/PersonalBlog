FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y curl

WORKDIR /PersonalBlog
# Copy the project files into the container
COPY . .

EXPOSE 8080
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]


