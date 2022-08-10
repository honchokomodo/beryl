#!/usr/bin/env bash

# Bot Token
if [[ -v TOKEN ]]; then
    echo "Beryl_Keys=${TOKEN}" >> /Beryl/Bot/.env
else
    echo "Missing bot token! TOKEN environment variable is not set."
    exit 1;
fi

# Hypixel API Keys
if [[ -v HYPIXEL_API_KEY ]]; then
    echo "Hypixel_API_Key=${HYPIXEL_API_KEY}" >> /Beryl/Bot/.env
else
    echo "Missing Hypixel API key! HYPIXEL_API_KEY environment variable is not set."
fi 

if [[ -v POSTGRES_PASSWORD ]]; then
    echo "Postgres_Password=${POSTGRES_PASSWORD}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_Password env var! Postgres_Password environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_IP ]]; then
    echo "Postgres_IP=${POSTGRES_IP}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_IP env var! POSTGRES_IP environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_USER ]]; then
    echo "Postgres_User=${POSTGRES_USER}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_User env var! POSTGRES_USER environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_DISQUEST_DATABASE ]]; then
    echo "Postgres_Database=${POSTGRES_DISQUEST_DATABASE}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_Disquest_Database env var! POSTGRES_DISQUEST_DATABASE environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_EVENTS_DATABASE ]]; then
    echo "Postgres_Events_Database=${POSTGRES_EVENTS_DATABASE}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_Events_Database env var! POSTGRES_EVENTS_DATABASE environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PORT ]]; then
    echo "Postgres_Port=${POSTGRES_PORT}" >> /Beryl/Bot/.env
else
    echo "Missing Postgres_Port env var ! POSTGRES_PORT environment variable is not set."
    exit 1;
fi

exec python3 /Beryl/Bot/beryl.py