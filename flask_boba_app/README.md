This is the flask app backend that includes files for the modeling and classes for any metadata associated with boba businesses

Utilizes `SQLAlchemy` for local databases to cache results that are stored in `boba_data.db` with `flask_migrate` which uses `Alembic` in the backend to handle database migrations

Includes a `.flaskenv` file for environment variable for flask.

To run migrations:

0. `flask db init` (Only run if versions got out of sync)

1. `flask db migrate`

2. `flask db upgrade`

To run the app: 

1. `flask run`