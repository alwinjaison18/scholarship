#!/bin/bash

# Quick diagnostic script for 404 auth error

echo "🔍 Diagnosing 404 Auth Error..."
echo "================================"

# Check if Next.js dev server is running
echo "1. Checking if development server is running..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Server is running on port 3000"
else
    echo "❌ Server is NOT running on port 3000"
    echo "💡 Run: npm run dev"
fi

# Check if auth API is accessible
echo ""
echo "2. Checking NextAuth API endpoint..."
if curl -s http://localhost:3000/api/auth/session > /dev/null; then
    echo "✅ NextAuth API is accessible"
else
    echo "❌ NextAuth API is NOT accessible"
fi

# Check if signin page files exist
echo ""
echo "3. Checking signin page files..."
if [ -f "src/app/auth/signin/page.tsx" ]; then
    echo "✅ signin/page.tsx exists"
else
    echo "❌ signin/page.tsx is missing"
fi

if [ -f "src/app/api/auth/[...nextauth]/route.ts" ]; then
    echo "✅ NextAuth route exists"
else
    echo "❌ NextAuth route is missing"
fi

# Check package.json for dependencies
echo ""
echo "4. Checking dependencies..."
if grep -q "next-auth" package.json; then
    echo "✅ next-auth is installed"
else
    echo "❌ next-auth is missing"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Run 'npm run dev' to start the development server"
echo "2. Visit http://localhost:3000 to check homepage"
echo "3. Try http://localhost:3000/test-auth as alternative"
echo "4. Check browser console for error messages"
