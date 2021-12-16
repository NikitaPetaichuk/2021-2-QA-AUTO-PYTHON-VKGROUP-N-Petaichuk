FROM python:3.8

ADD requirements.txt /requirements.txt
RUN pip3 install --upgrade pip -r /requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 9090

CMD ["python3", "vk_api_service.py"]

