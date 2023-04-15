# Base image
FROM openjdk:8-jdk-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y wget ssh rsync && \
    rm -rf /var/lib/apt/lists/*

# Download and install Hadoop
ENV HADOOP_VERSION=3.2.1
RUN wget -qO- https://www.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar zx -C /opt/ && \
    ln -s /opt/hadoop-$HADOOP_VERSION /opt/hadoop && \
    mkdir /opt/hadoop/logs

# Download and install Spark
ENV SPARK_VERSION=3.2.0
RUN wget -qO- https://www.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.2.tgz | tar zx -C /opt/ && \
    ln -s /opt/spark-$SPARK_VERSION-bin-hadoop3.2 /opt/spark && \
    mkdir /opt/spark/logs

# Configure environment variables
ENV JAVA_HOME=/usr/local/openjdk-8 \
    HADOOP_HOME=/opt/hadoop \
    HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
    SPARK_HOME=/opt/spark \
    PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Copy configuration files
COPY config/* $HADOOP_HOME/etc/hadoop/
COPY spark-defaults.conf $SPARK_HOME/conf/

# Format HDFS
RUN hdfs namenode -format

# Expose ports
EXPOSE 50070 8080 8081 7077 4040

# Start SSH daemon
CMD service ssh start && tail -f /dev/null