#!/usr/bin/env bash
set -e
API="http://127.0.0.1:5000/api/v1/services"
echo "🔹 Listing services..."
curl -s "$API/"

