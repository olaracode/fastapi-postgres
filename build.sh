
#!/usr/bin/env bash
# exit on error
set -o errexit

python install -r requirements.txt

alembic revision --autogenerate
alembic upgrade head
