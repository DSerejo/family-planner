env_vars=$(grep -v '^#' .env.staging | grep -v '^[[:space:]]*$' | sed 's/^/-e /' | tr '\n' ' ')
cmd="docker run --rm -it $env_vars gcr.io/serene-smoke-429712-n5/family-planner-api alembic upgrade head"
echo $cmd
eval $cmd
