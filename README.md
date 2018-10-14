[![Build Status](https://travis-ci.org/govready/experiment-microservices-grc.svg?branch=master)](https://travis-ci.org/govready/experiment-microservices-grc)

An experiment in a microservices approach to GRC software.

This repository leverages the sample code in "Microservices-docker-flask-react v2.3.2" from
[https://testdriven.io](https://testdriven.io).

# Launching

```
# Build Docker containers
docker-compose -f docker-compose-dev.yml build --no-cache

# Create databases
docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run users python manage.py seed-db
docker-compose -f docker-compose-dev.yml run roles python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run roles python manage.py seed-db
docker-compose -f docker-compose-dev.yml run components python manage.py recreate-db
docker-compose -f docker-compose-dev.yml run components python manage.py seed-db

# Launch docker containers
docker-compose -f docker-compose-dev.yml up
# Use `-d` to detach

```

# Stopping and removing containers
```
docker-compose -f docker-compose-dev.yaml stop
docker-compose -f docker-compose-dev.yaml down

# remove
docker rmi -f $(docker images -q)
```

# Connect to databases

```
# connect to user-db
docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres

# connect to roles-db
docker-compose -f docker-compose-dev.yaml exec roles-db psql -U postgres

# connect to components-db
docker-compose -f docker-compose-dev.yaml exec components-db psql -U postgres
```