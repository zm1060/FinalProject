FROM rabbitmq:latest

# Set environment variables
ENV RABBITMQ_DEFAULT_USER=admin \
    RABBITMQ_DEFAULT_PASS=admin

# Enable the management plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Expose ports
EXPOSE 5672 15672

# Start RabbitMQ server
CMD ["rabbitmq-server"]
