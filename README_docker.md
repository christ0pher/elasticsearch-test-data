# README: es_test_data.py as Docker container

With Docker, run the Elasticsearch test script in a Docker container.

## Requirements

* Docker version 17.x and higher
* Internet access to build the docker image
* Elasticsearch node or cluster with *disabled* X-Pack security

## Usage

### Build instructions (Docker)

* clone the repository
* open a terminal/console and change into the directory
* start the docker build process with the command:

```bash
$ docker build -t datadrivers/es_test_data:v0.1 .
```

### Run instructions (Docker)

* after the build, start the docker container with Docker ENV parameters:

```bash
$ docker run -it -e "ES_URL=http://localhost:9200" -e "ES_COUNT=1000" -e "ES_BATCH_SIZE=100" datadrivers/es_test_data:v0.1
```

## Environment variables

| ENV variable | Description | Value |
| ------------ | ----------- | ----- |
| `ES_URL` | Url to the target Elasticsearch host with port & protocol | `http://localhost:9200` |
| `ES_COUNT` | Define the number of documents, which will be generate & upload for testing | `1000000` |
| `ES_BATCH_SIZE` | Define the upload batch-size for the testing | `1000` |

## Supported Elasticsearch versions

* 5.0.1 - 6.1.1

## Authors information

* Company [Datadrivers GmbH](http://www.datadrivers.de) (Germany - Hamburg)
