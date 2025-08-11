#!/bin/bash
CIPHERTEXT="$1"

# Send to TCP oracle
response=$(nc crypto.traboda.net 62730 <<EOF
{"option": "check_padding", "ciphertext": "$CIPHERTEXT"}
EOF
)

# Parse JSON response
if echo "$response" | grep -q '"response":true'; then
    echo 1  # Valid padding
else
    echo 0  # Invalid padding
fi