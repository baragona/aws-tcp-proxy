FROM alpine:3.8

RUN apk update && apk add socat

RUN apk -v --update add \
        python \
        py-pip \
        groff \
        less \
        mailcap \
        wget \
        curl \
        bash \
            && \
        pip install --upgrade awscli==1.14.5 s3cmd==2.0.1 python-magic boto3 requests && \
        apk -v --purge del py-pip

RUN wget http://s3.amazonaws.com/ec2metadata/ec2-metadata && chmod u+x ec2-metadata && mv ec2-metadata /bin/

COPY code /code

WORKDIR /code
RUN mkdir pidfiles listeners

CMD python keep_alive.py python refresh_looper.py