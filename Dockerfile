FROM tensorflow/tensorflow:latest-py3
# LABEL image for a very simple flask application
COPY ./requirements.txt /docker-flask/requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS /key.json
WORKDIR /docker-flask
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["python","main.py"]

