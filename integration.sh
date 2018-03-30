#! /usr/bin/env bash

docker-compose -f docker-compose.test.yml up -d
sleep 160
docker build -t endpoint_test .
docker run -e "token=$TOKEN" -p 3002:3002 --net="host" -d --rm --name tested endpoint_test

python query_endpoint_test.py
if [ $? -eq 1 ]
then
  echo 'test failed' >&2
  docker-compose -f docker-compose.test.yml down
  docker stop tested
  exit 1
else
  echo 'test was successful'
  docker-compose -f docker-compose.test.yml down
  docker stop tested
  exit 0
fi
