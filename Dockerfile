# FROM ubuntu:latest
# RUN apt-get update -y
# RUN apt-get install -y python2.7 python-pip
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# EXPOSE 5000
# CMD ["trend_hashtag.py python"]

FROM tensorflow/tensorflow:2.0.0-py3

# LABEL image for a very simple flask application
COPY ./requirements.txt /docker-flask/requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS /key.json
WORKDIR /docker-flask
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

# RUN ["pip3", "install", "pipenv"]

# RUN ["pipenv", "install"]
# RUN ["pipenv", "install", "twitter"]
# #RUN ["pipenv", "install", "pycopy-urllib.parse"]

# CMD pipenv run python app.py




# FROM ubuntu:16.04


# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

# # We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt

# WORKDIR /app

# RUN pip install -r requirements.txt

# COPY . /app

# ENTRYPOINT [ "python" ]

# CMD [ "app.py" ]