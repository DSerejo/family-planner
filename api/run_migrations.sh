#if $1 is not provided, use staging
stage=$1
if [ -z "$stage" ]; then
    env_file=".env"
else
    env_file=".env.$stage"
fi
if [ "$stage" == "staging" ]; then  # Updated comparison operator
    env_vars=$(grep -v '^#' $env_file | grep -v '^[[:space:]]*$' | sed 's/^/-e /' | tr '\n' ' ')
    cmd="docker run --rm -it $env_vars gcr.io/serene-smoke-429712-n5/family-planner-api alembic upgrade head"
    echo $cmd
    eval $cmd
else
    export $(grep -v '^#' $env_file | xargs)
    alembic upgrade head
fi

