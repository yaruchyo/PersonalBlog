FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y curl && \
    apt-get install -y python3 && \
    apt-get install -y python3-venv && \
    apt-get install -y python3-pip && \
    git clone -b v1.0 https://github.com/yaruchyo/PersonalBlog.git

WORKDIR PersonalBlog

RUN python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate && export LC_ALL=en_US.utf-8 && export LANG=en_US.utf-8" && \
    pip3 install -r requirements.txt

CMD python3 run.py


