FROM python:2.7

WORKDIR /code
ADD http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz ./geodb.mmdb.gz
ADD requirements_prod.txt /code/requirements_prod.txt
RUN pip install -r requirements_prod.txt
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code
CMD ["python", "server.py"]
