# Use the official MongoDB image as a base
FROM mongo:latest

# Copy your initialization scripts
COPY ./mongo-init.js /docker-entrypoint-initdb.d/

# Give execution permissions to the scripts
RUN chmod +x /docker-entrypoint-initdb.d/*

# The CMD instruction will use the MongoDB image's default CMD
