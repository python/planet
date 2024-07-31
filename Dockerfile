FROM ubuntu:noble

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
                    python3-pip python3-setuptools python3-wheel \
                    locales tzdata \
                    ca-certificates \
                    strace gdb lsof locate net-tools htop iputils-ping dnsutils \
                    python3-dbg libpython3-dbg \
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
python3.12 code/planet.py config/config.ini \n\
cd /srv/planetpython.org/ \n\
python3.12 -m http.server 8080 \n\
"> /start.sh
RUN chmod +x /start.sh
EXPOSE 8080

