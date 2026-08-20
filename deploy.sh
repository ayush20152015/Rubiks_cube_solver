#!/bin/bash
set -e

echo "🚀 Rubik's Cube Solver - Quick Deployment Setup"
echo "=============================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v git >/dev/null 2>&1 || { echo "❌ Git not found"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "❌ GitHub CLI not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm not found"; exit 1; }

echo "✅ All prerequisites found"
echo ""

# Check git status
echo "📍 Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Uncommitted changes detected"
    echo "Would you like to commit? (y/n)"
    read -r commit
    if [ "$commit" = "y" ]; then
        git add .
        git commit -m "chore: pre-deployment commit"
    fi
fi

echo ""
echo "📤 Pushing to GitHub..."
git push origin $(git rev-parse --abbrev-ref HEAD)
echo "✅ Pushed to GitHub"

echo ""
echo "🔗 Vercel Deployment Instructions:"
echo "=================================="
echo ""
echo "1. Visit: https://vercel.com/new"
echo "2. Click 'Import Git Repository'"
echo "3. Select your GitHub repo"
echo "4. Set Root Directory: frontend/"
echo "5. Framework: Vite"
echo "6. Add Environment Variable:"
echo "   VITE_API_URL=https://your-backend-url.com"
echo "7. Click Deploy"
echo ""

echo "🚂 Railway Backend Deployment Instructions:"
echo "==========================================="
echo ""
echo "1. Visit: https://railway.app"
echo "2. Click 'New Project' → 'Deploy from GitHub'"
echo "3. Select your GitHub repo"
echo "4. Set Root Directory: backend/"
echo "5. Add Environment Variables:"
echo "   PYTHONUNBUFFERED=1"
echo "   DEBUG=False"
echo "   CORS_ORIGINS=['https://your-vercel-url.vercel.app', 'http://localhost:5173']"
echo "6. Railway will auto-deploy"
echo ""

echo "💡 After Deployment:"
echo "===================="
echo ""
echo "1. Get your Vercel URL from: https://vercel.com/dashboard"
echo "2. Get your Railway URL from: https://railway.app/dashboard"
echo "3. Update Vercel env vars with Railway backend URL"
echo "4. Test at your Vercel URL"
echo ""

echo "✨ Done! Your deployment is ready."
echo ""
echo "📚 Full guide: see DEPLOYMENT.md"
