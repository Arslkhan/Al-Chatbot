#!/bin/bash

# LegalEdge AI - Docker Start Script
# Starts all services using Docker Compose

echo "🐳 Starting LegalEdge AI with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if .env.docker exists
if [ ! -f ".env.docker" ]; then
    echo "❌ .env.docker not found!"
    echo "   Creating from template..."
    cat > .env.docker << 'EOF'
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your-openai-api-key-here

# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=legaledge
EOF
    echo "   ⚠️  Please edit .env.docker and add your OpenAI API key"
    echo "   Then run this script again."
    exit 1
fi

# Load environment variables
export $(cat .env.docker | grep -v '^#' | xargs)

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old volumes (optional - uncomment to start fresh)
# echo "🗑️  Removing old volumes..."
# docker-compose down -v

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if PostgreSQL is ready
echo "🔍 Checking PostgreSQL..."
docker-compose exec -T postgres pg_isready -U postgres

# Initialize database
echo "📊 Initializing database..."
docker-compose exec -T backend python -c "from database import init_db; init_db()" 2>/dev/null || echo "   (Database already initialized)"

echo ""
echo "✅ LegalEdge AI is running!"
echo ""
echo "📍 Services:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   PostgreSQL: localhost:5432"
echo ""
echo "📝 View logs:"
echo "   All:       docker-compose logs -f"
echo "   Backend:   docker-compose logs -f backend"
echo "   Frontend:  docker-compose logs -f frontend"
echo "   Database:  docker-compose logs -f postgres"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
echo ""

