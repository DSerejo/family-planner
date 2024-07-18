
env_file=".env"
export $(grep -v '^#' $env_file | xargs)
alembic revision --autogenerate -m "$1"