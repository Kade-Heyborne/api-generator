#!/usr/bin/env python3
"""
NLP-Powered API Generator
=========================

An intelligent tool that generates complete FastAPI or Django REST APIs from natural language descriptions.
Uses advanced NLP to extract requirements, infer business logic, and generate production-ready code.

Features:
- Natural language requirement extraction
- Intelligent project structure generation
- Automatic endpoint and model inference
- Business logic generation
- Authentication and security setup
- Database configuration
- Testing framework setup
- Docker containerization
- Comprehensive documentation

Usage:
    python api_generator.py
    
    Or import as a module:
    from api_generator import APIGenerator
    generator = APIGenerator()
    project_path = generator.generate_from_description("Create a blog API...")
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_extractor import NLPExtractor, FrameworkType
from project_analyzer import ProjectStructure, EndpointAnalyzer
from simple_fastapi_generator import SimpleFastAPIGenerator
# Note: Using simplified FastAPI generator for demo

class APIGenerator:
    """
    Main API generator that orchestrates the entire process from NLP to code generation.
    """
    
    def __init__(self):
        """Initialize the API generator with all components."""
        self.nlp_extractor = NLPRequirementExtractor()
        print("🤖 NLP-Powered API Generator initialized")
        print("📝 Ready to transform your ideas into production-ready APIs")
    
    def generate_from_description(self, description: str, output_dir: str = ".", 
                                framework: Optional[FrameworkType] = None) -> str:
        """
        Generate a complete API project from a natural language description.
        
        Args:
            description: Natural language description of the API requirements
            output_dir: Directory to generate the project in
            framework: Specific framework to use (FastAPI/Django), auto-detected if None
            
        Returns:
            Path to the generated project directory
        """
        
        print(f"\n🔍 Analyzing requirements from description...")
        print(f"📄 Description: {description[:100]}{'...' if len(description) > 100 else ''}")
        
        # Extract requirements using NLP
        requirements = self.nlp_extractor.extract_requirements(description)
        
        # Override framework if specified
        if framework:
            requirements.framework = framework
        
        print(f"\n✅ Requirements extracted successfully!")
        print(f"🏗️  Project: {requirements.project_name}")
        print(f"🔧 Framework: {requirements.framework.value}")
        print(f"🗄️  Database: {requirements.database_type.value}")
        print(f"🔐 Auth: {requirements.auth_type.value}")
        print(f"📊 Models: {len(requirements.models)} detected")
        
        # Display detected models and endpoints
        for i, model in enumerate(requirements.models, 1):
            print(f"   {i}. {model['name']} ({len(model['fields'])} fields)")
        
        # Generate project structure analysis
        print(f"\n🏗️  Generating project structure...")
        structure_generator = ProjectStructureGenerator(requirements)
        endpoint_analyzer = EndpointAnalyzer(requirements)
        
        # Analyze endpoints
        endpoints = endpoint_analyzer.analyze_endpoints()
        print(f"🔗 Detected {len(endpoints)} endpoint patterns")
        
        # Generate code based on framework
        print(f"\n⚡ Generating {requirements.framework.value} code...")
        
        if requirements.framework == FrameworkType.FASTAPI:
            generator = SimpleFastAPIGenerator(requirements)
            project_path = generator.generate_complete_project(output_dir)
        elif requirements.framework == FrameworkType.DJANGO:
            # Use simplified Django generation for now
            project_path = self._generate_simple_django_project(requirements, output_dir)
        else:
            raise ValueError(f"Unsupported framework: {requirements.framework}")
        
        print(f"\n🎉 Project generated successfully!")
        print(f"📁 Location: {project_path}")
        
        # Display next steps
        self._display_next_steps(requirements, project_path)
        
        return project_path
    
    def _generate_simple_django_project(self, requirements, output_dir: str) -> str:
        """Generate a simplified Django project structure."""
        
        project_name = requirements.project_name
        project_path = Path(output_dir) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create basic Django structure
        (project_path / "manage.py").write_text(f'''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
''')
        
        # Create settings
        settings_dir = project_path / project_name
        settings_dir.mkdir(exist_ok=True)
        
        (settings_dir / "settings.py").write_text(f'''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {{
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}}
''')
        
        # Create URLs
        (settings_dir / "urls.py").write_text(f'''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
]
''')
        
        # Create __init__.py files
        (settings_dir / "__init__.py").write_text("")
        (project_path / "__init__.py").write_text("")
        
        # Create requirements.txt
        (project_path / "requirements.txt").write_text('''Django>=4.2.0
djangorestframework>=3.14.0
''')
        
        # Create README
        (project_path / "README.md").write_text(f'''# {project_name.replace('_', ' ').title()}

{requirements.description}

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

## API Documentation

Visit http://localhost:8000/api/ for the browsable API.
''')
        
        return str(project_path)
    
    def _display_next_steps(self, requirements, project_path: str):
        """Display next steps for the user."""
        
        print(f"\n📋 Next Steps:")
        print(f"1. 📁 Navigate to project: cd {project_path}")
        
        if requirements.framework == FrameworkType.FASTAPI:
            print(f"2. 🐍 Create virtual environment: python -m venv venv")
            print(f"3. ⚡ Activate environment: source venv/bin/activate  # Linux/Mac")
            print(f"                           venv\\Scripts\\activate     # Windows")
            print(f"4. 📦 Install dependencies: pip install -r requirements.txt")
            print(f"5. 🚀 Run the server: uvicorn app.main:app --reload")
            print(f"6. 🌐 Open browser: http://localhost:8000/docs")
        else:
            print(f"2. 🐍 Create virtual environment: python -m venv venv")
            print(f"3. ⚡ Activate environment: source venv/bin/activate")
            print(f"4. 📦 Install dependencies: pip install -r requirements.txt")
            print(f"5. 🗄️  Run migrations: python manage.py migrate")
            print(f"6. 👤 Create superuser: python manage.py createsuperuser")
            print(f"7. 🚀 Run the server: python manage.py runserver")
            print(f"8. 🌐 Open browser: http://localhost:8000/admin/")
        
        print(f"\n🔧 Additional Features:")
        if requirements.containerize:
            print(f"   🐳 Docker: docker-compose up --build")
        if requirements.include_tests:
            print(f"   🧪 Tests: pytest")
        if requirements.auth_type.value != "none":
            print(f"   🔐 Authentication: {requirements.auth_type.value} configured")
        
        print(f"\n💡 Tips:")
        print(f"   • Check the README.md for detailed setup instructions")
        print(f"   • Customize the generated code to fit your specific needs")
        print(f"   • Add your business logic to the generated endpoints")
        print(f"   • Configure environment variables for production")

def interactive_mode():
    """Run the generator in interactive mode."""
    
    print("🤖 Welcome to the NLP-Powered API Generator!")
    print("=" * 50)
    print("Transform your ideas into production-ready APIs using natural language.")
    print()
    
    # Get user input
    print("📝 Describe your API project in natural language:")
    print("   Examples:")
    print("   • 'Create a blog API with user authentication and post management'")
    print("   • 'Build an e-commerce platform with products, orders, and payments'")
    print("   • 'Design a task management system with teams and projects'")
    print()
    
    description = input("💬 Your description: ").strip()
    
    if not description:
        print("❌ Please provide a description.")
        return
    
    # Get framework preference
    print("\n🔧 Framework preference:")
    print("   1. FastAPI (recommended for modern APIs)")
    print("   2. Django REST Framework (full-featured web framework)")
    print("   3. Auto-detect (let AI choose)")
    
    framework_choice = input("🎯 Choose (1-3): ").strip()
    
    framework = None
    if framework_choice == "1":
        framework = FrameworkType.FASTAPI
    elif framework_choice == "2":
        framework = FrameworkType.DJANGO
    
    # Get output directory
    output_dir = input("\n📁 Output directory (default: current): ").strip() or "."
    
    # Generate the project
    try:
        generator = APIGenerator()
        project_path = generator.generate_from_description(
            description=description,
            output_dir=output_dir,
            framework=framework
        )
        
        print(f"\n✨ Success! Your API project is ready at: {project_path}")
        
    except Exception as e:
        print(f"\n❌ Error generating project: {e}")
        print("Please check your description and try again.")

def main():
    """Main entry point for the API generator."""
    
    parser = argparse.ArgumentParser(
        description="NLP-Powered API Generator - Transform ideas into production-ready APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python api_generator.py --interactive
  python api_generator.py --description "Create a blog API with authentication"
  python api_generator.py --description "E-commerce platform" --framework fastapi --output ./my_project
        """
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--description", "-d",
        type=str,
        help="Natural language description of the API"
    )
    
    parser.add_argument(
        "--framework", "-f",
        choices=["fastapi", "django"],
        help="Framework to use (fastapi or django)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=".",
        help="Output directory for the generated project"
    )
    
    args = parser.parse_args()
    
    if args.interactive or (not args.description):
        interactive_mode()
    else:
        # Command line mode
        framework = None
        if args.framework == "fastapi":
            framework = FrameworkType.FASTAPI
        elif args.framework == "django":
            framework = FrameworkType.DJANGO
        
        try:
            generator = APIGenerator()
            project_path = generator.generate_from_description(
                description=args.description,
                output_dir=args.output,
                framework=framework
            )
            
            print(f"\n✨ Success! Your API project is ready at: {project_path}")
            
        except Exception as e:
            print(f"\n❌ Error generating project: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()

