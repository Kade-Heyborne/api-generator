#!/bin/bash

# NLP-Powered API Generator Demo Script
# Demonstrates the capabilities of the intelligent API generator

echo "🤖 NLP-Powered API Generator Demo"
echo "=================================="
echo ""

echo "This demo will show you how to generate complete APIs from natural language descriptions."
echo ""

# Demo 1: FastAPI Blog Platform
echo "📝 Demo 1: Generating a FastAPI Blog Platform"
echo "Description: 'Create a modern blog platform with user authentication, posts, comments, and categories'"
echo ""
read -p "Press Enter to generate the FastAPI blog project..."

python3 api_generator.py --description "Create a modern blog platform with user authentication, post creation, comments, and categories. Include JWT authentication, PostgreSQL database, and comprehensive testing." --framework fastapi --output ./demo_projects/blog_api

echo ""
echo "✅ FastAPI blog project generated in ./demo_projects/blog_api/"
echo ""

# Demo 2: Django E-commerce Platform
echo "🛒 Demo 2: Generating a Django E-commerce Platform"
echo "Description: 'Build an e-commerce platform with products, orders, and payment processing'"
echo ""
read -p "Press Enter to generate the Django e-commerce project..."

python3 api_generator.py --description "Build an e-commerce platform with products, categories, shopping cart, orders, and payment processing. Include admin interface and session authentication." --framework django --output ./demo_projects/ecommerce_api

echo ""
echo "✅ Django e-commerce project generated in ./demo_projects/ecommerce_api/"
echo ""

# Demo 3: Interactive Mode
echo "🎯 Demo 3: Interactive Mode"
echo "Now let's try the interactive mode where you can describe your own API:"
echo ""
read -p "Press Enter to start interactive mode..."

python3 api_generator.py --interactive

echo ""
echo "🎉 Demo completed!"
echo ""
echo "📁 Generated projects are available in:"
echo "   • ./demo_projects/blog_api/ (FastAPI)"
echo "   • ./demo_projects/ecommerce_api/ (Django)"
echo "   • Your custom project (if created in interactive mode)"
echo ""
echo "🚀 Next steps:"
echo "   1. Navigate to any generated project directory"
echo "   2. Follow the README.md instructions to set up and run"
echo "   3. Explore the generated code and customize as needed"
echo ""
echo "💡 Tips:"
echo "   • Check the API documentation at /docs (FastAPI) or /admin (Django)"
echo "   • Modify the generated code to add your specific business logic"
echo "   • Use the generated tests as a starting point for your test suite"
echo ""

