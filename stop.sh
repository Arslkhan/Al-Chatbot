#!/bin/bash

# LegalEdge AI - Stop Script
# Stops both backend and frontend services

echo "🛑 Stopping LegalEdge AI..."

# Read PIDs if they exist
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    kill $BACKEND_PID 2>/dev/null
    echo "  ✓ Backend stopped"
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    kill $FRONTEND_PID 2>/dev/null
    echo "  ✓ Frontend stopped"
    rm .frontend.pid
fi

# Clean up log files
rm -f backend.log frontend.log

# Also kill any uvicorn or next processes (backup)
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "next dev" 2>/dev/null

echo "✅ All services stopped"

