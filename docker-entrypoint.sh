#!/bin/bash
# dirvex Docker Entrypoint
# Handles first-run setup and credential onboarding
# Auto-generates defaults when running non-interactively (no TTY)

set -e

# If .env doesn't exist, run setup wizard
if [ ! -f /app/.env ]; then
    echo "============================================"
    echo "  dirvex — First Run Setup"
    echo "============================================"
    echo ""
    
    # Generate random secret
    SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Check if running interactively
    if [ -t 0 ]; then
        # Interactive mode
        read -p "Use mock mode (no live AD required)? [Y/n]: " MOCK
        MOCK=${MOCK:-Y}
        
        if [[ "$MOCK" =~ ^[Yy] ]]; then
            MOCK_MODE=true
            echo "✅ Mock mode enabled — no AD credentials needed."
        else
            MOCK_MODE=false
            read -p "AD Domain (e.g., corp.local): " AD_DOMAIN
            read -p "AD Server hostname: " AD_SERVER
            read -p "AD Username: " AD_USERNAME
            read -s -p "AD Password: " AD_PASSWORD
            echo ""
        fi
        
        read -p "Port [5000]: " PORT
        PORT=${PORT:-5000}
    else
        # Non-interactive mode — use defaults
        echo "Non-interactive mode — using auto-generated defaults"
        MOCK_MODE=true
        PORT=5000
    fi
    
    # Write .env
    cat > /app/.env <<EOF
SECRET_KEY=${SECRET}
MOCK_MODE=${MOCK_MODE:-true}
PORT=${PORT:-5000}
AD_DOMAIN=${AD_DOMAIN:-}
AD_SERVER=${AD_SERVER:-}
AD_USERNAME=${AD_USERNAME:-}
AD_PASSWORD=${AD_PASSWORD:-}
LOG_LEVEL=INFO
EOF
    
    echo ""
    echo "✅ Configuration saved to /app/.env"
    echo "============================================"
fi

# Source .env
export $(grep -v '^#' /app/.env | xargs)

echo "Starting dirvex..."
exec "$@"
