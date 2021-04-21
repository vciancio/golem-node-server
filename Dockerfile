ARG YA_CORE_VERSION=latest
FROM aabrioux/golem-node:${YA_CORE_VERSION}

ENV SETTINGS_NODE_NAME=golem_node
ENV SETTINGS_CORES=2
ENV SETTINGS_MEMORY=1.5Gib
ENV SETTINGS_DISK=10Gib
ENV SETTINGS_PRICE_FOR_START=0
ENV SETTINGS_PRICE_PER_HOUR=0.02
ENV SETTINGS_PRICE_PER_CPU_HOUR=0.1
ENV SETTINGS_SUBNET=public-beta

RUN apt-get update -q \
    && apt-get install -q -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt 
RUN rm /app/requirements.txt
COPY app /app 

CMD ["sh", "/app/run.sh"]