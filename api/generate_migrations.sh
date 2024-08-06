
env_file=".env"
export $(grep -v '^#' $env_file | xargs)
poetry run alembic revision --autogenerate -m "$1"