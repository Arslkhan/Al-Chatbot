#!/bin/bash

# LegalEdge AI Deployment Script
echo "🚀 LegalEdge AI Deployment Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    echo "✅ Git repository initialized"
else
    echo "📦 Git repository already exists"
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "🔧 Installing Railway CLI..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed"
else
    echo "✅ Railway CLI already installed"
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "🔧 Installing Vercel CLI..."
    npm install -g vercel
    echo "✅ Vercel CLI installed"
else
    echo "✅ Vercel CLI already installed"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Push your code to GitHub:"
echo "   git remote add origin https://github.com/yourusername/legaledge-ai.git"
echo "   git push -u origin main"
echo ""
echo "2. Deploy Backend to Railway:"
echo "   - Go to https://railway.app"
echo "   - Create new project from GitHub repo"
echo "   - Set environment variables (DATABASE_URL, OPENAI_API_KEY)"
echo ""
echo "3. Deploy Frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Import your GitHub repo"
echo "   - Set root directory to 'frontend'"
echo "   - Set NEXT_PUBLIC_API_URL to your Railway backend URL"
echo ""
echo "📚 See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "🎉 Ready for deployment!"
