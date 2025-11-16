#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
ENV_FILE="$SCRIPT_DIR/env.dev"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "env.dev not found at $ENV_FILE" >&2
  exit 1
fi

compose() {
  docker compose --env-file "$ENV_FILE" "$@"
}

usage() {
  echo "Usage: $0 {start|rebuild|clean}" >&2
}

case "${1:-}" in
  start)
    compose up -d
    ;;
  rebuild)
    compose build --no-cache
    compose up -d
    ;;
  clean)
    compose down -v
    docker system prune -a -f 
    ;;
  *)
    usage
    exit 1
    ;;
esac
