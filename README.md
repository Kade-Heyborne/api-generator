# NLP-Powered API Generator

## Overview

The NLP-Powered API Generator is an advanced tool designed to create production-ready API projects from natural language descriptions. This innovative solution automates the process of API development using cutting-edge natural language processing (NLP) and intelligent code generation. It supports frameworks like FastAPI and Django, and provides native support for modern design and deployment practices.

## Features

- **Automatic API Creation**:
  - Parses plain language descriptions into structured requirements
  - Generates endpoints, models, authentication, and database configurations
  
- **Framework Support**:
  - FastAPI: Modern, async-first API framework
  - Django: Mature and feature-rich web framework with admin support
  
- **Database and Authentication**:
  - PostgreSQL, MySQL, SQLite, MongoDB support
  - Offers JWT, Session, and API Key authentication methods
  
- **Deployment Ready**:
  - Includes Docker configuration
  - Environment-specific settings for production readiness
  
- **Documentation and Testing**:
  - Generates Swagger/OpenAPI documentation
  - Provides comprehensive test suites

## Installation

### Prerequisites
- Python 3.8 or newer

### Option 1: Python SDK (Recommended)
```bash
cd api_generator_sdk
pip install -e .
pip install -e .[all]  # To install framework-specific dependencies
```

### Option 2: Enhanced CLI
```bash
cd enhanced_nlp_api_generator
pip install -r requirements.txt
```

### Option 3: Original CLI
```bash
cd nlp_api_generator
pip install -r requirements.txt
```

## Usage

### Method 1: Python SDK
Create a script, `generate_my_api.py`:
```python
from api_generator_sdk import ApiGenerator

generator = ApiGenerator()
project_path = generator.generate_api(
    description="Create a blog with user authentication, posts, and comments.",
    framework="fastapi",
    database="sqlite",
    auth_method="jwt",
    output_dir="./my_blog_api"
)
print(f"API project has been generated at: {project_path}")
```
Run it:
```bash
python generate_my_api.py
```

### Method 2: Enhanced CLI
```bash
python enhanced_api_generator.py --description "Create a task management app with teams and projects" --framework fastapi --database sqlite --output-dir ./my_task_app
```

### Method 3: Original CLI
```bash
python api_generator.py --description "Create a simple todo list API" --framework django --output-dir ./my_todo_api
```

## Generated Project Examples

### FastAPI Structure
```
my_blog_api/
├── app/
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── routes.py         # API endpoint definitions
│   └── database.py       # Database configuration
├── main.py               # FastAPI entry point
├── requirements.txt      # Python dependencies
└── README.md             # Project instructions
```

### Django Structure
```
my_django_app/
├── manage.py
├── my_django_app/
│   ├── settings.py       # Project settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI application
├── apps/
│   └── api/              # API configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Running Your API

### FastAPI
```bash
cd my_blog_api
pip install -r requirements.txt
python main.py
```
Access API at:
- `http://localhost:8000/docs` for Swagger UI
- `http://localhost:8000/redoc` for Redoc

### Django
```bash
cd my_django_app
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Access admin interface at `http://localhost:8000/admin`.

## Customization

### Frameworks:
- FastAPI or Django
- Choose based on project requirements and feature complexity

### Authentication:
- JWT: Token-based authentication for stateless APIs
- Session: Traditional session-based authentication
- API Key: Simple key-based access control

### Databases:
- SQLite: Lightweight and simple
- PostgreSQL/MySQL: Robust relational databases

## Extensibility

### Adding New Frameworks
- Extend generator classes in the `api_generator_sdk` module

### Enhancing NLP
- Improve entity recognition and requirement extraction
- Add domain-specific vocabularies

### Custom Code Templates
- Modify generators to include additional functionality

## Resources and Documentation

- Full project overview in `/docs/COMPLETE_PROJECT_CONTEXT.md`
- Architecture details in `/docs/ARCHITECTURE.md`
- Beginner's guide in `/docs/🚀 Complete Beginner's Guide to the NLP-Powered API Generator.md`

## Troubleshooting

### Common Issues
- **Module Not Found**: Ensure dependencies are correctly installed using `pip install -r requirements.txt`.
- **Port Conflicts**: Use a different port (e.g., `python main.py --port 8001`).
- **Database Errors**: Run migrations for Django projects (`python manage.py migrate`).

## Contribution Guidelines

- Fork the repository
- Develop features in a separate branch
- Submit pull requests following project standards