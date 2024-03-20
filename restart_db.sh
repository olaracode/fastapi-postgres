psql -d postgres -c "DROP DATABASE $1;"
psql -d postgres -c "CREATE DATABASE $1;"
rm -rf alembic/versions/*
pipenv run migrate
pipenv run upgrade
