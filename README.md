# FileHub

## Introduction

This is Dropbox like service where
users can upload, retrieve, and manage
their files

## Project Structure

The `filehub` directory holds the application logic

- `api/__init__.py` initializes the application, configures CORS, and includes a health check route.
- `api/db.py` manages database CRUD operations for file metadata using MongoDB.
- `api/files.py` implements a web API for file management, integrating with GCS and MongoDB.
- `api/gcs.py` interacts with GCS for file upload, download, SignedURL generation, and deletion.
- `api/logger.py` configures a basic logging system for the application.
- `configs/config.py` loads configuration settings based on the application environment (FLASK_ENV)
- `requirments.txt` Lists the dependencies required for running the project.
- `docker-compose.yml` contains configuration that defines two services, 'mongo' and 'app', to facilitate the deployment of the application.
- `Dockerfile` creates a lightweight image of application.
- `requirments.txt` Lists the dependencies required for running the project.

The `static` directory contains HTML, CSS and JS files responsible for the UI of the application.

## How to set up

You can setup and run this application using docker or python virtual environment.
1. [Steps to setup & run using Docker](#docker-setup)
2. [Steps to setup & run using venv](#venv-setup)


### Docker Setup

Clone the repository.
```
git clone git@github.com:RaviTejaKomma/filehub.git
```

Run Docker Compose
```
# navigate to the filehub directory
cd filehub

# run this command which starts the containers defined in the docker-compose.yml (i.e filehub flask app & mongo)
docker-compose up
```


### venv Setup

Start a python virtual env:
```
# navigate to the filehub directory
cd filehub

# create the virtual environment for filehub
python3 -m venv filehub-venv

# activate the virtual environment
source filehub-venv/bin/activate
```

Install dependencies
```
python3 -m pip install -r requirements.txt
```

Start the application
```
flask --app api/ run

# comment 'app' service in the docker-compose.yml file and run docker compose in another terminal to start only the mongo service

docker-compose up
```


## FileHub backend verification

The FileHub application is accessible at [localhost:5000](http://localhost:5000).
   
To verify its status, you can use the following `curl` command to hit the health check API:
```bash
curl -X GET 'localhost:5000'
```

A successful response indicates that the **filehub** flask application is up and running.

## FileHub UI
1. Navigate to the static directory: `cd static`
2. Open the `index.html` file in your preferred web browser. This will launch the FileHub UI