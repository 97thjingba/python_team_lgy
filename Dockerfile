FROM charact3/python-cassandra-driver:3.12.0

COPY src/ /opt/app
WORKDIR /opt/app

RUN curl -s http://ip-api.com | grep China > /dev/null && \
    pip install -r requirements.txt -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com || \
    pip install -r requirements.txt
