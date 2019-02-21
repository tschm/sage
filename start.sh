#!/usr/bin/env bash
echo "http://localhost:9011"
docker-compose run -p "9011:8888" web sage-jupyter
