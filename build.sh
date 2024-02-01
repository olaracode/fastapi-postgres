
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

alembic revision --autogenerate
alembic upgrade head
