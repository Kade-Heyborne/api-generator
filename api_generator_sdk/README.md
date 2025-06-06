# API Generator SDK

A powerful Python SDK for generating FastAPI and Django REST framework projects from natural language descriptions using advanced NLP processing.

## 🚀 Features

- **Natural Language Processing**: Extract project requirements from plain English descriptions
- **Multi-Framework Support**: Generate FastAPI and Django REST framework projects
- **Intelligent Analysis**: Automatically detect models, relationships, and API endpoints
- **Production Ready**: Generate complete projects with authentication, testing, and deployment configs
- **Extensible Architecture**: Add custom NLP patterns and framework generators
- **Clean API**: Simple, object-oriented interface for programmatic usage

## 📦 Installation

```bash
# Basic installation
pip install api-generator-sdk

# With FastAPI support
pip install api-generator-sdk[fastapi]

# With Django support
pip install api-generator-sdk[django]

# With database drivers
pip install api-generator-sdk[postgresql,mysql]

# Full installation with all features
pip install api-generator-sdk[all]
```

## 🎯 Quick Start

### Basic Usage

```python
from api_generator_sdk import ApiGenerator

# Initialize the generator
generator = ApiGenerator()

# Generate a FastAPI project
project_path = generator.generate_api(
    description="Create a blog API with user authentication and post management",
    framework="fastapi",
    database="postgresql",
    auth_method="jwt",
    output_dir="./my_blog_api"
)

print(f"Project generated at: {project_path}")
```

### Configuration

```python
from api_generator_sdk import ApiGenerator

# Initialize with configuration
generator = ApiGenerator()

# Configure defaults
generator.configure(
    default_framework="django",
    default_database="postgresql",
    default_auth_method="jwt",
    default_output_dir="./generated_projects"
)

# Generate with defaults
project_path = generator.generate_api(
    description="Build a task management system with teams and projects"
)
```

### Convenience Functions

```python
from api_generator_sdk import generate_fastapi_project, generate_django_project

# Quick FastAPI generation
fastapi_path = generate_fastapi_project(
    "Create a user management API with CRUD operations",
    output_dir="./fastapi_project"
)

# Quick Django generation
django_path = generate_django_project(
    "Build an e-commerce platform with products and orders",
    output_dir="./django_project"
)
```

## 🧠 NLP Capabilities

The SDK can understand complex project descriptions and automatically extract:

- **Project Structure**: Names, descriptions, and organization
- **Data Models**: Entities, fields, types, and constraints
- **Relationships**: One-to-one, one-to-many, many-to-many relationships
- **API Endpoints**: CRUD operations and custom endpoints
- **Authentication**: JWT, session, API key, OAuth2 requirements
- **Features**: File uploads, real-time, caching, background tasks

### Example Descriptions

```python
# Simple blog platform
generator.generate_api(
    "Create a blog platform where users can write posts and leave comments"
)

# E-commerce system
generator.generate_api(
    "Build an e-commerce API with products, categories, shopping cart, and order management"
)

# Task management
generator.generate_api(
    "Design a project management system with teams, projects, tasks, and user collaboration"
)

# Social media platform
generator.generate_api(
    "Create a social media API with user profiles, posts, likes, comments, and friend connections"
)
```

## 🔧 Advanced Usage

### Custom NLP Patterns

```python
from api_generator_sdk import ApiGenerator

generator = ApiGenerator()

# Register custom field type pattern
def extract_custom_field(match):
    return {"type": "custom", "validation": "special"}

generator.register_nlp_pattern(
    "custom_field",
    r"\\b(special|custom)\\s+(field|attribute)\\b",
    extract_custom_field
)
```

### Template Overrides

```python
# Override default templates
generator.register_template_override(
    "main_app",
    """
# Custom main application template
from fastapi import FastAPI

app = FastAPI(title="Custom API")

@app.get("/")
def custom_root():
    return {"message": "Custom API"}
"""
)
```

### Custom Framework Generators

```python
from api_generator_sdk import ApiGenerator, BaseGenerator

class CustomFrameworkGenerator(BaseGenerator):
    def generate_project(self, output_dir: str) -> str:
        # Custom generation logic
        pass
    
    def register_template_override(self, template_key: str, content: str):
        # Custom template handling
        pass

# Register custom generator
generator = ApiGenerator()
generator.register_framework_generator("custom", CustomFrameworkGenerator)
```

## 📊 Supported Technologies

### Frameworks
- **FastAPI**: Modern, fast web framework for building APIs
- **Django REST Framework**: Powerful and flexible toolkit for building Web APIs

### Databases
- **PostgreSQL**: Advanced open source relational database
- **MySQL**: Popular open source relational database
- **SQLite**: Lightweight file-based database
- **MongoDB**: Document-oriented NoSQL database

### Authentication
- **JWT**: JSON Web Tokens for stateless authentication
- **Session**: Traditional session-based authentication
- **API Key**: Simple API key authentication
- **OAuth2**: Industry-standard authorization framework

### Features
- **CORS**: Cross-Origin Resource Sharing support
- **Rate Limiting**: Request throttling and quota management
- **Caching**: Redis-based caching integration
- **File Uploads**: File handling and storage
- **Real-time**: WebSocket support for live updates
- **Background Tasks**: Celery integration for async processing
- **Testing**: Comprehensive test suite generation
- **Documentation**: Auto-generated API documentation
- **Docker**: Containerization support

## 🏗️ Generated Project Structure

### FastAPI Project
```
my_api_project/
├── main.py                 # Application entry point
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app factory
│   ├── core/
│   │   ├── config.py      # Configuration
│   │   ├── auth.py        # Authentication
│   │   └── security.py    # Security utilities
│   ├── db/
│   │   └── database.py    # Database configuration
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── api/
│   │   └── v1/           # API routes
│   └── crud/             # Database operations
├── tests/                # Test suite
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── Dockerfile           # Docker configuration
└── README.md           # Documentation
```

### Django Project
```
my_django_project/
├── manage.py              # Django management
├── my_project/
│   ├── __init__.py
│   ├── settings/         # Settings package
│   ├── urls.py          # URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── apps/
│   ├── api/             # API configuration
│   ├── core/            # Core utilities
│   └── [model_apps]/    # Model-specific apps
├── static/              # Static files
├── media/               # Media files
├── templates/           # Templates
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
├── docker-compose.yml  # Docker Compose
└── README.md          # Documentation
```

## 🧪 Testing

```python
# The SDK generates comprehensive test suites
import pytest
from api_generator_sdk import ApiGenerator

def test_api_generation():
    generator = ApiGenerator()
    
    project_path = generator.generate_api(
        description="Simple user management API",
        framework="fastapi",
        output_dir="/tmp/test_project"
    )
    
    assert project_path.exists()
    assert (project_path / "main.py").exists()
    assert (project_path / "requirements.txt").exists()
```

## 🚀 Deployment

Generated projects include deployment configurations:

### Docker
```bash
# Build and run with Docker
cd generated_project
docker build -t my-api .
docker run -p 8000:8000 my-api
```

### Docker Compose
```bash
# Full stack with database
docker-compose up -d
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

# Django
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/api-generator/api-generator-sdk.git
cd api-generator-sdk

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run linting
black .
isort .
flake8
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [https://api-generator-sdk.readthedocs.io/](https://api-generator-sdk.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/api-generator/api-generator-sdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/api-generator/api-generator-sdk/discussions)
- **Email**: contact@apigenerator.dev

## 🗺️ Roadmap

- [ ] **Enhanced NLP**: Support for more complex descriptions and domain-specific terminology
- [ ] **Additional Frameworks**: Flask, Starlette, Tornado support
- [ ] **GraphQL**: Native GraphQL API generation
- [ ] **Microservices**: Multi-service project generation
- [ ] **Cloud Integration**: AWS, GCP, Azure deployment templates
- [ ] **API Versioning**: Automatic API versioning strategies
- [ ] **Performance Optimization**: Advanced caching and optimization patterns
- [ ] **Security Enhancements**: Advanced security patterns and compliance
- [ ] **Visual Interface**: Web-based project generator
- [ ] **IDE Integration**: VS Code and PyCharm plugins

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- Django team for the robust web framework
- Pydantic team for data validation
- SQLAlchemy team for the ORM
- All contributors and users of this project

---

**Made with ❤️ by the API Generator SDK Team**

