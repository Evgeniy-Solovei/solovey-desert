#!/bin/sh
set -eu

mkdir -p /app/solovey_desert/staticfiles /app/solovey_desert/media
chown -R appuser:appuser /app/solovey_desert/staticfiles /app/solovey_desert/media

exec gosu appuser "$@"
