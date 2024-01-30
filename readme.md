# Fastapi + Postgresql

This is a basic template that contains the necessary configuration to start a project with Fastapi and postgresql.

We use Pipenv as the package manager and alembic to handle the migrations of the database.

You can use any other virutal environment manager or package manager, but you need to make sure to install the dependencies and run the migrations. Using pipenv allows you to leverage the Pipfile script we've created

## Installation

1. Clone the repository

```bash
git clone https://github.com/olaracode/fastapi-postgresql.git

# Change to the project directory
cd fastapi-postgresql
```

2. Install the dependencies
   > It is recommended to use a virtual environment, in this case we are using Pipenv

```sh
# Start a new virtual environment
pipenv shell

# Install the dependencies
pipenv install
```

3. Copy the .env.example file to .env and configure the environment variables

```sh
cp .env.example .env
```

4. Run the migrations. We are using alembic to handle the migrations of the database so you need to run the following command to create the tables in the database

```sh
# ------ First -------- Create the migrations
alembic revision --autogenerate
# OR IF USING PIPENV
pipenv run migrate # This leverages the Pipfile to run the alembic command

# ------ Then -------- Run the migrations
alembic upgrade head
# OR IF USING PIPENV
pipenv run upgrade # This leverages the Pipfile to run the alembic command
```

5. Run the project. The project is configured to the default port(8000)

```sh
uvicorn app.main:app --reload
# OR IF USING PIPENV
pipenv run start
```

## Considerations

1. All the models most be defined inside the `src.models` module so the migrations can be created and run correctly. if you opt to use a different module, you need to update the `alembic/env.py` file to include the models

```py
from src.models import *
# Add your models below
from src.your.module import YourModel
```

2. You MUST use the `.env` file to include your postgresql connection string. This is used inside the `src.database.py` file to connect to the database and inside the `alembic/env.py` file. This allows for a single source of truth for the database connection string. The other option is to hardcode the connection string in the `src.database.py` and `alembic/env.py` files

The `alembic.ini` file is configured to use the `%(DB_URL)s` variable to connect to the database. You need to replace this with your connection string. As well as remove the usage from the `alembic/env.py` file

```ini
# alembic.ini

# Replace this
sqlalchemy.url = %(DB_URL)s

# With this
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

```py
# alembic/env.py

section = config.config_ini_section # Remove this line

config.set_section_option(section, "DB_URL", os.environ.get("POSTGRES_URL")) # Remove this line
```
