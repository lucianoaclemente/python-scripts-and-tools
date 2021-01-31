#!/bin/bash
app="lac.flask-scikitlearn"
docker build --network=host -t ${app} .
docker run -d -p 3000:80 \
  --name=${app} \
  -v $PWD:/app ${app}