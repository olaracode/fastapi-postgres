# Fastapi + Postgresql

This is a basic template that contains the necessary configuration to start a project with Fastapi and postgresql.

We use Pipenv as the package manager and alembic to handle the migrations of the database.

You can use any other virutal environment manager or package manager, but you need to make sure to install the dependencies and run the migrations. Using pipenv allows you to leverage the Pipfile script we've created

## Index

- [Installation](#installation)
- [Considerations](#considerations)
- [Workflow](#workflow)
- [Authentication](#authentication)
- [Deploy](#deploy)

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

1. All the models must be defined inside the `src.models` directory so the migrations can be created and run correctly. if you opt to use a different module/directory, you need to update the `alembic/env.py` file to include the models

   ```py
   # Add your models here
   from src.your.module import YourModel

   # Remove this ---------------
   directory_path = "src.models"
   absolute_path = os.path.abspath(directory_path.replace(".", "/"))
   for file_name in os.listdir(absolute_path):
       if file_name.endswith(".py") and file_name != "__init__.py":
           # Remove the file extension to get the module name
           module_name = file_name[:-3]

           # Import the module dynamically
           module = import_module(f"{directory_path}.{module_name}")
   # ----------------------------
   ```

2. You **MUST** use the `.env` file to include your postgresql connection string. This is used inside the `src.database.py` file to connect to the database and inside the `alembic/env.py` file. This allows for a single source of truth for the database connection string. The other option is to hardcode the connection string in the `src.database.py` and `alembic/env.py` files.

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

## Workflow

Following the FastAPI documentation, we have created a structure that allows you to create the models, routes, schemas, and db operations on a modular way

### Entry POINT

The **main.py** file is the entry point of the application. It contains the FastAPI app and the routes that will be used in the application

### Schemas

Inside the **schema** directory you can define the pydantic models that will be used to validate the request and response of the routes.

### Models

The **models** directory is used to define **ONLY** the database models

### Database

The **database.py** file is used to create the database connection and the session that will be used to interact with the database. It also contains the `get_db` function that is used to get the database session in the routes.

#### Database/Operations

The **operations** directory is used to define the operations that will be used to interact with the database. This is where you will define the functions that will be used to create, read, update, and delete the data from the database.

### Routes

The **routes** directory is used to define the routes that will be used in the application. You can define the routes in a modular way, for example, you can create a file for the users routes, another for the products routes, etc.

## Authentication

> [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

Following the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt) for the optimal way to handle the authentication, we installed `python-jose`(jwt) & `passlib`(hashing) and created the file `src/db/jwt.py` which contains the functions to create and verify the JWT token.

Following their documentation it is stated that `OAuth2PasswordBearer` should be used to handle the authentication. This is used in the `src/db/jwt.py` file to create the `oauth2_scheme` that will be used to protect the routes.

This `oauth2_scheme` is used with the `Depends` function inside the `get_current_user` function. This function can be used to authenticate the user and get the current user on any given **'protected | private'** route.

FastAPI Recommends this approach but it is worth noting that it's not the only approach for user authentication, other options could be used like `BasicAuth`, `Firebase Authentication`, `Supabase`, `Keycloak`, etc.

The approach you choose to take should be the one in which you are most comfortable with and that best fits your use case.

## Deploy

This template is optimized for a single click deploy on render using the blueprint. To learn more you can check out the `build.sh`for the commands used to deploy and `render.yaml`for the blueprint specifications

**WARNING** while deploying to render you need to update the fastapi Environment Variable for POSTGRES_URL. Since we are using psycopg2 you need to add "ql" to the start of the postgresql url

From:
`postgres://<postgres_user>:<password>@localhost:5432/<database_name>`

To:
`postgresql://<postgres_user>:<password>@localhost:5432/<database_name>`
