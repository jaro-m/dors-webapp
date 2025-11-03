# Disease Outbreak Reporting System API

## About the project

This is an attempt to create an API service as a part of webapp.
The API has the following endpoints implemented:

- `POST    /api/reports`                  - Create new report
- `GET     /api/reports`                  - List reports (paginated)
- `GET     /api/reports/{id}`             - Get specific report
- `PUT     /api/reports/{id}`             - Update report (draft only)
- `DELETE  /api/reports/{id}`             - Delete report (draft only)
- `POST    /api/reports/{id}/reporter`    - Add/update reporter details
- `GET     /api/reports/{id}/reporter`    - Get reporter details
- `POST    /api/reports/{id}/patient`     - Add/update patient details
- `GET     /api/reports/{id}/patient`     - Get patient details
- `POST    /api/reports/{id}/disease`     - Add/update disease details
- `GET     /api/reports/{id}/disease`     - Get disease details
- `POST    /api/reports/{id}/submit`      - Submit report (change status)
- `GET     /api/reports/search`           - Search reports
- `GET     /api/statistics`               - Basic statistics

This was created and tested on Linux, but it should run on MacOS without any modifications to the steps described below.

## How to install it

After cloning the repo, create virtual environment (recommended), example:

```bash
python3 -venv ve
```

In the example above `venv` was used. It have to be installed on the system (usually it's `python3-venv` package on Linux).
The environment can be initialized, or used as in this way:

```bash
./ve/bin/python -m pip install --upgrade pip
```

That's to upugrade Python package installer.
Run this to install all needed modules:

```bash
./ve/bin/python -m pip install -r requirements.txt
```

After all the modules are installed, run this (otherwise alembic won't work as expocted, see: https://alembic.sqlalchemy.org/en/latest/front.html#installation)

```bash
./ve/bin/python -m pip install -e .
```

As alembic config files are already there, you can run this to create/update migration files:

```bash
./ve/bin/alembic revision --autogenerate -m "create_tables"
```

I should automatically generate the migration file based on the models defined in the project.
To actually make changes to the DB, run this:

```bash
./ve/bin/alembic upgrade head
```

(more on that here: https://alembic.sqlalchemy.org/en/latest/tutorial.html).
At this point it's probably ready to go.

## Run the server

To run the server you can use this tiny script provided to simplify things even further (it's a bash script):

```bash
./run_server.sh
```

It will also export ENV VARS from a `.env` file. If the script does nothing, you might need to make it executable first ():

```bash
chmod +x ./run_server
```

Once it's up and running you can check it typing this into the internet browser address line:

```text
https://localhost:8000/docs
```

As it uses self-signed certificates for development purposes, you might get notification/warning about it.
To be able to use the API, the connection (user) has to be authenticated. Please see section below to find out how to setup the user. `Authorize` the user (user's `username` and `password` can be found in the other section as well), and you can test all the endpoints.

## Database and setting up the user

run (for development purposes):

```bash
./ve/bin/python populate_db.py
```

to populate DB, then you'll be able to login as `johndoe` (username) and type in `secret` as password.

## Docker

docker compose can be run, but it needs the external network to be present, so first run this:

```bash
docker network create dors-net
```

then you can run docker compose.
