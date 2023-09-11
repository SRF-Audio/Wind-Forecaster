#!/bin/bash

set -e

# Substitute env vars in the mongo-init.js file
sed -i 's/__MONGO_APP_USER__/'"$MONGO_APP_USER"'/' /docker-entrypoint-initdb.d/mongo-init.js
sed -i 's/__MONGO_APP_PASSWORD__/'"$MONGO_APP_PASSWORD"'/' /docker-entrypoint-initdb.d/mongo-init.js

# Run the original command provided by the MongoDB Docker image entrypoint
exec docker-entrypoint.sh mongod
