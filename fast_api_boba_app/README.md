To make new migrations:

0. To initialize alembic: `alembic init`

1. To create a new migration `alembic revision --autogenerate -m <your comment>`

2. To run migrations to become up to date `alembic upgrade head`

3. To run the initial data `python app/init_data.py`

To run app:

1. `uvicorn app.main:app --reload`
