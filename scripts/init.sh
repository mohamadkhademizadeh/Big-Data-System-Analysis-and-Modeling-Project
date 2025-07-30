#!/usr/bin/env bash
set -euo pipefail
docker compose up -d
echo "Waiting for MongoDB to become primary..."
sleep 8
docker compose logs --no-color mongo | tail -n 50
echo "Mongo running. Visit http://localhost:8081 for mongo-express."
