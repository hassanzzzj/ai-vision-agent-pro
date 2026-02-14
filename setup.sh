#!/bin/bash

# AI Vision Agent Pro - Setup Script
# Ye script complete project ko setup karta hai

set -e  # Exit on error

echo "======================================"
echo "🚀 AI Vision Agent Pro - Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose found${NC}"
echo ""

# Setup backend .env
echo -e "${YELLOW}📝 Setting up backend environment...${NC}"
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Created backend/.env${NC}"
    echo -e "${YELLOW}⚠️  Please edit backend/.env and add your API keys!${NC}"
else
    echo -e "${GREEN}✅ backend/.env already exists${NC}"
fi

# Setup frontend .env
echo ""
echo -e "${YELLOW}📝 Setting up frontend environment...${NC}"
if [ ! -f "frontend/.env" ]; then
    echo "VITE_API_URL=http://localhost:8000" > frontend/.env
    echo -e "${GREEN}✅ Created frontend/.env${NC}"
else
    echo -e "${GREEN}✅ frontend/.env already exists${NC}"
fi

# Ask user if they want to build and start
echo ""
read -p "Do you want to build and start the services now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}🔨 Building Docker images...${NC}"
    docker-compose build
    
    echo ""
    echo -e "${YELLOW}🚀 Starting services...${NC}"
    docker-compose up -d
    
    echo ""
    echo -e "${GREEN}======================================"
    echo "✅ Setup Complete!"
    echo "======================================${NC}"
    echo ""
    echo "📍 Access the application:"
    echo "   Frontend: http://localhost:5173"
    echo "   Backend:  http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose down"
    echo ""
else
    echo ""
    echo -e "${YELLOW}======================================"
    echo "⏸️  Setup prepared but not started"
    echo "======================================${NC}"
    echo ""
    echo "To start later, run:"
    echo "   docker-compose up -d"
    echo ""
fi
