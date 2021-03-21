#!/bin/bash
python3 /app/app.py 2>&1 &
golemsp settings set --node-name $SETTINGS_NODE_NAME \
        --cores $SETTINGS_CORES \
        --memory $SETTINGS_MEMORY \
        --disk $SETTINGS_DISK \
        --account $YA_ACCOUNT \
        --payment-network $YA_PAYMENT_NETWORK \
        --starting-fee $SETTINGS_PRICE_FOR_START \
        --env-per-hour $SETTINGS_PRICE_PER_HOUR \
        --cpu-per-hour $SETTINGS_PRICE_PER_CPU_HOUR
golemsp run --payment-network $YA_PAYMENT_NETWORK --subnet $SETTINGS_SUBNET