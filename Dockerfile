FROM ubuntu:bionic

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
                    python-pip python-setuptools python-wheel \
                    locales tzdata \
                    ca-certificates \
                    strace gdb lsof locate net-tools htop iputils-ping dnsutils \
                    python2.7-dbg python2.7 libpython2.7 python-dbg libpython-dbg \
                    curl nano vim tree less telnet patch \
                    graphviz sqlite3 \
                    dumb-init \
 && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

COPY /code /planet/code
COPY /config /planet/config
COPY /static /planet/static

#RUN mkdir /srv/planetpython.org/
VOLUME /srv/planetpython.org/
WORKDIR /planet

ENTRYPOINT ["dumb-init"]

RUN echo "#!/bin/bash -eux \n\
python2.7 code/planet.py config/config.ini \n\
cd /srv/planetpython.org/ \n\
python2.7 -mSimpleHTTPServer 8080 \n\
"> /start.sh
RUN chmod +x /start.sh
EXPOSE 8080

