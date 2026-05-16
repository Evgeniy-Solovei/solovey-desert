#!/bin/sh
set -eu

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
ENV_FILE="${ENV_FILE:-.env}"

read_env_value() {
    key="$1"

    if [ ! -f "${ENV_FILE}" ]; then
        printf ''
        return
    fi

    value="$(grep -E "^${key}=" "${ENV_FILE}" | tail -n 1 | cut -d= -f2- || true)"
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"
    printf '%s' "${value}"
}

DOMAIN="${DOMAIN_NAME:-$(read_env_value DOMAIN_NAME)}"
WWW_DOMAIN="${DOMAIN_WWW:-$(read_env_value DOMAIN_WWW)}"
EMAIL="${LETSENCRYPT_EMAIL:-$(read_env_value LETSENCRYPT_EMAIL)}"

DOMAIN="${DOMAIN:-solovey-desert.by}"
WWW_DOMAIN="${WWW_DOMAIN:-www.solovey-desert.by}"

if [ -z "${EMAIL}" ] || [ "${EMAIL}" = "admin@solovey-desert.by" ]; then
    echo "Set a real LETSENCRYPT_EMAIL in ${ENV_FILE} before issuing the certificate."
    exit 1
fi

docker compose -f "${COMPOSE_FILE}" up -d nginx

docker compose -f "${COMPOSE_FILE}" run --rm --entrypoint sh certbot -c \
    "rm -rf /etc/letsencrypt/live/${DOMAIN} /etc/letsencrypt/archive/${DOMAIN} /etc/letsencrypt/renewal/${DOMAIN}.conf"

if [ -n "${WWW_DOMAIN}" ]; then
    docker compose -f "${COMPOSE_FILE}" run --rm --entrypoint certbot certbot certonly \
        --webroot \
        -w /var/www/certbot \
        --email "${EMAIL}" \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d "${DOMAIN}" \
        -d "${WWW_DOMAIN}"
else
    docker compose -f "${COMPOSE_FILE}" run --rm --entrypoint certbot certbot certonly \
        --webroot \
        -w /var/www/certbot \
        --email "${EMAIL}" \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d "${DOMAIN}"
fi

docker compose -f "${COMPOSE_FILE}" exec nginx nginx -s reload
