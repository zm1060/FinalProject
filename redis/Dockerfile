FROM redis:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the default Redis port
EXPOSE 6379

# Start Redis server
CMD ["redis-server"]
