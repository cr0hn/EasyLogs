FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests redis-server curl && \
    addgroup --gid 1001 --system easylogs && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group easylogs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt .
COPY requirements-deployment.txt .

RUN pip install --disable-pip-version-check --no-cache-dir -r /requirements.txt -r /requirements-deployment.txt

# Install MongoDB for standalone mode
RUN curl https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian11-6.0.2.tgz -o mongo.tgz && \
    tar -xzf mongo.tgz && \
    mkdir -p /data/db/mongo && \
    mv mongodb-linux-x86_64-debian11-6.0.2 /usr/local/mongodb && \
    rm mongo.tgz

COPY ./entrypoint.sh ./usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint

COPY ./easy_logs ./easy_logs
RUN chown -R easylogs:easylogs /easy_logs

EXPOSE 8080

#USER easylogs
WORKDIR /
CMD ["entrypoint"]
