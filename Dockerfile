FROM python:3.6-alpine

COPY . /mosaic
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN cd /mosaic && pip install --upgrade setuptools && pip install -r requirements.txt

WORKDIR /mosaic

ENTRYPOINT ["python"]
CMD ["mosaic_app.py"]