#!/bin/bash

# LegalEdge AI - Docker Stop Script

echo "🛑 Stopping LegalEdge AI Docker containers..."

docker-compose down

echo "✅ All containers stopped"
echo ""
echo "💡 To remove all data (including database):"
echo "   docker-compose down -v"
echo ""

