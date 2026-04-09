#!/bin/bash

# ==========================================
# Xentic Comply API - cURL Examples
# ==========================================

# Replace with your actual RapidAPI Key
export RAPIDAPI_KEY="YOUR_RAPIDAPI_KEY_HERE"
export RAPIDAPI_HOST="xentic-comply-api.p.rapidapi.com"

echo "1. Checking API Health..."
curl --request GET \
	--url https://$RAPIDAPI_HOST/v1/health \
	--header "x-rapidapi-host: $RAPIDAPI_HOST" \
	--header "x-rapidapi-key: $RAPIDAPI_KEY"

echo -e "\n\n2. Running a Basic Compliance Scan (EU / GDPR)..."
curl --request POST \
	--url https://$RAPIDAPI_HOST/v1/scan \
	--header 'Content-Type: application/json' \
	--header "x-rapidapi-host: $RAPIDAPI_HOST" \
	--header "x-rapidapi-key: $RAPIDAPI_KEY" \
	--data '{
    "domain": "example.com",
    "country_code": "EU",
    "include_pdf": false
}'

echo -e "\n\n3. Running a Scan for Panama (Ley 81)..."
curl --request POST \
	--url https://$RAPIDAPI_HOST/v1/scan \
	--header 'Content-Type: application/json' \
	--header "x-rapidapi-host: $RAPIDAPI_HOST" \
	--header "x-rapidapi-key: $RAPIDAPI_KEY" \
	--data '{
    "domain": "telemetro.com",
    "country_code": "PA"
}'
