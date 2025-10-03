FROM python:3.10-slim

ENV DOCKER=true \
    GIT_PYTHON_REFRESH=quiet \
    PIP_NO_CACHE_DIR=1

RUN apt update && \
    apt install -y --no-install-recommends \
        curl \
        libcairo2 \
        git \
        ffmpeg \
        libavcodec-dev \
        libavutil-dev \
        libavformat-dev \
        libswscale-dev \
        libavdevice-dev \
        gcc \
        python3-dev \
        gnupg2 \
        ca-certificates \
        wget \
        tini

RUN wget https://github.com/fastfetch-cli/fastfetch/releases/latest/download/fastfetch-linux-aarch64.deb -O /tmp/fastfetch.deb && \
    dpkg -i /tmp/fastfetch.deb && \
    apt-get install -f -y && \
    rm /tmp/fastfetch.deb

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives /tmp/*

RUN git clone https://github.com/sz3333/LidFax-userbot /hikka

WORKDIR /hikka

RUN pip install --no-warn-script-location --no-cache-dir -r requirements.txt

EXPOSE 8080

RUN mkdir /data

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python3", "-m", "hikka"]