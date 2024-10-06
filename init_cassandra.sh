#!/bin/bash
set -e

# Wait for Cassandra to be ready
until cqlsh -e "describe keyspaces" > /dev/null 2>&1; do
  echo "Cassandra is unavailable - sleeping"
  sleep 2
done

echo "Cassandra is up - executing command"

# Create superuser
cqlsh -u cassandra -p cassandra -e "CREATE USER IF NOT EXISTS $CASSANDRA_USERNAME WITH PASSWORD '$CASSANDRA_PASSWORD' SUPERUSER;"

echo "Superuser created successfully"