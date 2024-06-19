FROM python:3.11-bullseye
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000
RUN chmod +x run_server.sh
CMD ["/bin/sh", "./run_server.sh"]