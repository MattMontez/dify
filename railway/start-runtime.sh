#!/usr/bin/env bash
set -euo pipefail

export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
export FLASK_APP="${FLASK_APP:-app.py}"
export DIFY_BIND_ADDRESS="${DIFY_BIND_ADDRESS:-0.0.0.0}"
export DIFY_PORT="${PORT:-${DIFY_PORT:-5001}}"
export SERVER_WORKER_AMOUNT="${SERVER_WORKER_AMOUNT:-1}"
export SERVER_WORKER_CLASS="${SERVER_WORKER_CLASS:-gevent}"
export SERVER_WORKER_CONNECTIONS="${SERVER_WORKER_CONNECTIONS:-10}"
export GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-360}"
export CELERY_WORKER_AMOUNT="${CELERY_WORKER_AMOUNT:-1}"
export CELERY_WORKER_CLASS="${CELERY_WORKER_CLASS:-gevent}"
export CELERY_PREFETCH_MULTIPLIER="${CELERY_PREFETCH_MULTIPLIER:-1}"
export MAX_TASKS_PER_CHILD="${MAX_TASKS_PER_CHILD:-50}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export MIGRATION_ENABLED="${MIGRATION_ENABLED:-true}"

if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Running Dify database migrations"
  flask upgrade-db
fi

echo "Starting Redis, Dify API, and Dify worker"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/dify.conf
