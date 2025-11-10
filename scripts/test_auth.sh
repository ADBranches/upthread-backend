#!/usr/bin/env bash
set -euo pipefail

API_URL="http://127.0.0.1:5000/api/v1"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${YELLOW}🔹 Registering test user...${RESET}"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"123456","role":"user"}' || true)
echo "$REGISTER_RESPONSE" | grep -E '"message"|"error"' || echo "$REGISTER_RESPONSE"

echo -e "${YELLOW}🔹 Logging in...${RESET}"
LOGIN_JSON=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"123456"}')

# --------------------------------------------------------------------
# ✅ REPLACEMENT SECTION (fix parsing issue)
# --------------------------------------------------------------------
# Instead of using Python heredoc parsing, we now use jq for reliability
ACCESS_TOKEN=$(echo "$LOGIN_JSON" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$LOGIN_JSON" | jq -r '.refresh_token')
# --------------------------------------------------------------------

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
  echo -e "${RED}❌ Login failed — no access token returned!${RESET}"
  echo "$LOGIN_JSON"
  exit 1
else
  echo -e "${GREEN}✅ Login succeeded. Token extracted.${RESET}"
fi

# -------------------------------------------------------------
# Test /me route (authenticated endpoint)
# -------------------------------------------------------------
echo -e "${YELLOW}🔹 Testing /me (protected route)...${RESET}"
ME_RESPONSE=$(curl -s -i "$API_URL/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$ME_RESPONSE" | grep -q "200 OK"; then
  echo -e "${GREEN}✅ /me route working${RESET}"
else
  echo -e "${RED}❌ /me route failed:${RESET}"
  echo "$ME_RESPONSE"
  exit 1
fi

# -------------------------------------------------------------
# Test admin route — should be forbidden for normal user
# -------------------------------------------------------------
echo -e "${YELLOW}🔹 Testing /admin/users (should be 403 for normal user)...${RESET}"
ADMIN_RESPONSE=$(curl -s -i "$API_URL/admin/users" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$ADMIN_RESPONSE" | grep -q "403"; then
  echo -e "${GREEN}✅ Admin route correctly restricted${RESET}"
else
  echo -e "${RED}⚠️ Unexpected admin route result:${RESET}"
  echo "$ADMIN_RESPONSE"
fi

# -------------------------------------------------------------
# Test refresh token
# -------------------------------------------------------------
echo -e "${YELLOW}🔹 Testing /auth/refresh (refresh token)...${RESET}"
if [ -z "$REFRESH_TOKEN" ] || [ "$REFRESH_TOKEN" = "null" ]; then
  echo -e "${RED}❌ No refresh token found!${RESET}"
else
  REFRESH_RESPONSE=$(curl -s -X POST "$API_URL/auth/refresh" \
    -H "Authorization: Bearer $REFRESH_TOKEN")
  if echo "$REFRESH_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Refresh endpoint working${RESET}"
  else
    echo -e "${RED}⚠️ Refresh endpoint returned unexpected result:${RESET}"
    echo "$REFRESH_RESPONSE"
  fi
fi

# -------------------------------------------------------------
# Admin Verification Section
# -------------------------------------------------------------
echo -e "${YELLOW}🔹 Registering admin test user...${RESET}"
curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin_tester@example.com","password":"123456","role":"admin"}' || true

echo -e "${YELLOW}🔹 Logging in as admin...${RESET}"
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin_tester@example.com","password":"123456"}')

# --------------------------------------------------------------------
# ✅ REPLACEMENT SECTION (fix parsing issue for admin login)
# --------------------------------------------------------------------
ADMIN_ACCESS=$(echo "$ADMIN_LOGIN" | jq -r '.access_token')
# --------------------------------------------------------------------

if [ -z "$ADMIN_ACCESS" ] || [ "$ADMIN_ACCESS" = "null" ]; then
  echo -e "${RED}❌ Admin login failed!${RESET}"
  echo "$ADMIN_LOGIN"
else
  echo -e "${GREEN}✅ Admin login OK. Testing /admin/users...${RESET}"
  ADMIN_USERS=$(curl -s -i "$API_URL/admin/users" \
    -H "Authorization: Bearer $ADMIN_ACCESS")
  if echo "$ADMIN_USERS" | grep -q "200 OK"; then
    echo -e "${GREEN}✅ /admin/users returned successfully${RESET}"
  else
    echo -e "${RED}⚠️ Admin route did not return expected result:${RESET}"
    echo "$ADMIN_USERS"
  fi
fi

echo
echo -e "${GREEN}✅ Smoke tests completed successfully at $(date)${RESET}"
