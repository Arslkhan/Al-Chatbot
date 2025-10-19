#!/bin/bash

# LegalEdge AI - Quick Start Script
# This script starts both backend and frontend in development mode

echo "🚀 Starting LegalEdge AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready &> /dev/null; then
    echo "⚠️  PostgreSQL is not running. Starting PostgreSQL..."
    brew services start postgresql@14
    sleep 2
fi

echo ""
echo "📦 Installing dependencies..."

# Backend dependencies
echo "  → Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "    Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Backend .env file not found!"
    echo "    Copying from env.example..."
    cp env.example .env
    echo "    ⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

# Initialize database
echo "  → Initializing database..."
python -c "from database import init_db; init_db()" 2>/dev/null

cd ..

# Frontend dependencies
echo "  → Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "    Installing npm packages (this may take a few minutes)..."
    npm install
else
    echo "    Dependencies already installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "    Creating .env.local..."
    cp env.local.example .env.local
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting services..."
echo ""

# Start backend in background
echo "  → Starting backend on http://localhost:8000"
cd backend
source venv/bin/activate
uvicorn main:app --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend in background
echo "  → Starting frontend on http://localhost:3000"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ LegalEdge AI is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop: Press Ctrl+C or run: ./stop.sh"
echo ""

# Save PIDs for stop script
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for Ctrl+C
trap 'echo ""; echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid backend.log frontend.log; echo "✅ Stopped"; exit 0' INT

# Keep script running
wait

