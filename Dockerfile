FROM python:3.7-alpine

COPY . /mosaic
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN cd /mosaic &&  pip install -r requirements.txt

WORKDIR /mosaic

CMD ["python mosaic_app.py"]