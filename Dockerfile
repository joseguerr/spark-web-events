FROM python:3.11-slim

EXPOSE 4040

RUN echo "Installing Packages" && \
    apt-get update && \
    apt-get install -y default-jre wget tar make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing Spark" && \
    cd /opt && \
    wget -q https://archive.apache.org/dist/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz && \
    tar -xf spark-3.5.2-bin-hadoop3.tgz && \
    rm -f spark-3.5.2-bin-hadoop3.tgz  && \
    pip install -e /opt/spark-3.5.2-bin-hadoop3/python

ENV HADOOP_CONF_DIR=/opt/spark-3.5.2-bin-hadoop3/conf

COPY . .

RUN make clean && \
    make setup && \
    make build

CMD ["/bin/bash"]
