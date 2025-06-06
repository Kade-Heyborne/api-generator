# NLP-Powered API Generator

🤖 **Transform your ideas into production-ready APIs using natural language**

An intelligent tool that automatically generates complete FastAPI or Django REST APIs from natural language descriptions. Uses advanced NLP to extract requirements, infer business logic, and generate production-ready code with authentication, database configuration, testing, and documentation.

## 🌟 Features

### 🧠 Intelligent NLP Processing
- **Natural Language Understanding**: Parses complex descriptions to extract project requirements
- **Smart Entity Recognition**: Automatically detects models, fields, relationships, and business logic
- **Framework Detection**: Intelligently chooses between FastAPI and Django based on requirements
- **Business Logic Inference**: Generates appropriate CRUD operations and endpoint patterns

### 🏗️ Comprehensive Code Generation
- **Complete Project Structure**: Generates organized, production-ready project layouts
- **Database Integration**: Supports PostgreSQL, MySQL, and SQLite with proper ORM setup
- **Authentication Systems**: JWT, API Key, Session, and OAuth2 authentication options
- **API Documentation**: Automatic OpenAPI/Swagger documentation generation
- **Testing Framework**: Complete test suites with fixtures and examples
- **Docker Support**: Containerization with Docker and docker-compose configurations

### 🔧 Advanced Features
- **CORS Configuration**: Cross-origin resource sharing setup
- **Rate Limiting**: API throttling and rate limiting
- **File Uploads**: File handling and storage configuration
- **Caching**: Redis caching integration
- **Background Tasks**: Celery task queue setup
- **Logging**: Comprehensive logging configuration
- **Environment Management**: Development, staging, and production configurations

## 🚀 Quick Start

### Installation

1. **Clone or download the NLP API Generator**:
```bash
# All files are in the nlp_api_generator directory
cd nlp_api_generator
```

2. **No additional installation required** - uses Python standard library and built-in NLP capabilities

### Basic Usage

#### Interactive Mode (Recommended)
```bash
python api_generator.py --interactive
```

#### Command Line Mode
```bash
# Generate a FastAPI project
python api_generator.py --description "Create a blog API with user authentication and post management" --framework fastapi

# Generate a Django project
python api_generator.py --description "Build an e-commerce platform with products and orders" --framework django --output ./my_project
```

## 📝 Usage Examples

### Example 1: Blog API
```bash
python api_generator.py --description "Create a modern blog platform with user registration, authentication, post creation, comments, and categories. Use JWT authentication and PostgreSQL database." --framework fastapi
```

**Generated Features**:
- User model with authentication
- Post model with CRUD operations
- Comment system with relationships
- Category management
- JWT authentication setup
- PostgreSQL configuration
- Complete API documentation

### Example 2: E-commerce Platform
```bash
python api_generator.py --description "Build an e-commerce platform with products, categories, shopping cart, orders, and payment processing. Include admin interface and comprehensive testing." --framework django
```

**Generated Features**:
- Product catalog with categories
- Shopping cart functionality
- Order management system
- User authentication
- Admin interface
- Payment processing structure
- Comprehensive test suite

### Example 3: Task Management System
```bash
python api_generator.py --description "Design a task management API with teams, projects, tasks, and user collaboration. Include real-time notifications and file attachments." --framework fastapi
```

**Generated Features**:
- Team and project management
- Task assignment and tracking
- User collaboration features
- File upload capabilities
- Real-time notification structure
- Role-based permissions

## 🏗️ Architecture

### Core Components

1. **NLP Requirement Extractor** (`nlp_extractor.py`)
   - Parses natural language descriptions
   - Extracts project requirements and specifications
   - Identifies models, fields, and relationships
   - Determines authentication and database needs

2. **Project Structure Generator** (`project_analyzer.py`)
   - Creates intelligent project organization
   - Generates endpoint patterns
   - Analyzes business logic requirements
   - Plans database relationships

3. **Framework Generators**
   - **FastAPI Generator** (`simple_fastapi_generator.py`): Modern async API generation
   - **Django Generator** (`api_generator.py`): Full-featured web framework generation

4. **Main API Generator** (`api_generator.py`)
   - Orchestrates the entire generation process
   - Provides command-line and interactive interfaces
   - Manages output and user feedback

### Generated Project Structure

#### FastAPI Projects
```
project_name/
├── app/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── routes.py          # API endpoints
│   └── database.py        # Database configuration
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

#### Django Projects
```
project_name/
├── manage.py
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── [model_apps]/
├── requirements.txt
└── README.md
```

## 🔧 Configuration Options

### Supported Frameworks
- **FastAPI**: Modern, fast, async API framework
- **Django REST Framework**: Full-featured web framework with REST capabilities

### Database Support
- **PostgreSQL**: Production-ready relational database
- **MySQL**: Popular relational database
- **SQLite**: Lightweight database for development

### Authentication Methods
- **JWT**: JSON Web Tokens for stateless authentication
- **API Key**: Simple API key-based authentication
- **Session**: Traditional session-based authentication
- **OAuth2**: OAuth2 flow support
- **None**: No authentication required

### Additional Features
- **CORS**: Cross-origin resource sharing
- **Rate Limiting**: API throttling
- **File Uploads**: File handling capabilities
- **Caching**: Redis caching integration
- **Background Tasks**: Celery task queues
- **Testing**: Comprehensive test suites
- **Docker**: Containerization support

## 🎯 Advanced Usage

### Custom Requirements
The NLP engine can understand complex requirements including:

- **Business Logic**: "Calculate shipping costs based on weight and distance"
- **Relationships**: "Users can have multiple projects, projects contain tasks"
- **Permissions**: "Only project owners can delete projects"
- **Validation**: "Email addresses must be unique and valid"
- **Workflows**: "Orders go through pending, processing, shipped, delivered states"

### Environment-Specific Generation
```bash
# Development environment
python api_generator.py --description "..." --framework fastapi --env development

# Production environment with security features
python api_generator.py --description "..." --framework django --env production
```

### Integration with Existing Projects
The generator can create modular components that integrate with existing codebases:

```bash
# Generate only models and schemas
python api_generator.py --description "..." --components models,schemas

# Generate API endpoints for existing models
python api_generator.py --description "..." --components routes,tests
```

## 🧪 Testing Generated Projects

### FastAPI Projects
```bash
cd generated_project
pip install -r requirements.txt
python main.py
# Visit http://localhost:8000/docs for API documentation
```

### Django Projects
```bash
cd generated_project
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/admin/ for admin interface
```

## 🔍 How It Works

### 1. Natural Language Processing
The system uses advanced pattern matching and entity recognition to:
- Extract project names and descriptions
- Identify data models and their fields
- Detect relationships between entities
- Understand business requirements
- Infer authentication and security needs

### 2. Intelligent Code Generation
Based on the extracted requirements:
- Generates appropriate project structure
- Creates database models with proper relationships
- Builds API endpoints with CRUD operations
- Sets up authentication and security
- Configures testing frameworks
- Generates comprehensive documentation

### 3. Framework-Specific Optimization
- **FastAPI**: Async/await patterns, Pydantic schemas, automatic documentation
- **Django**: Model-View-Template patterns, admin interface, ORM optimization

## 🛠️ Customization

### Extending the NLP Engine
Add custom patterns in `nlp_extractor.py`:
```python
def extract_custom_requirements(self, description: str):
    # Add custom business logic extraction
    pass
```

### Custom Code Templates
Modify generators to use custom templates:
```python
def generate_custom_component(self, requirements):
    # Add custom code generation logic
    pass
```

### Framework Extensions
Add support for new frameworks by creating new generator classes:
```python
class CustomFrameworkGenerator:
    def generate_complete_project(self, requirements):
        # Implement custom framework generation
        pass
```

## 📚 Examples and Demos

### Generated Project Examples

1. **Task Management API** (`/tmp/test_project/create_a_modern/`)
   - FastAPI with JWT authentication
   - PostgreSQL database
   - User management system
   - Complete CRUD operations

2. **E-commerce Platform** (`/tmp/test_django/build_an/`)
   - Django REST framework
   - SQLite database
   - Product and order management
   - Session authentication

### Live Demos
Run the interactive mode to see the generator in action:
```bash
python api_generator.py --interactive
```

## 🚀 Production Deployment

### Generated projects include:
- **Environment configuration** for development, staging, and production
- **Docker support** with Dockerfile and docker-compose.yml
- **Security best practices** with proper authentication and validation
- **Database migrations** and schema management
- **Monitoring and logging** configuration
- **API documentation** with OpenAPI/Swagger

### Deployment Steps:
1. **Configure environment variables** for production
2. **Set up database** (PostgreSQL/MySQL for production)
3. **Configure reverse proxy** (Nginx/Apache)
4. **Set up SSL certificates** for HTTPS
5. **Deploy using Docker** or traditional hosting
6. **Monitor and maintain** using generated logging

## 🤝 Contributing

The NLP-Powered API Generator is designed to be extensible:

### Adding New Frameworks
1. Create a new generator class
2. Implement the required methods
3. Add framework detection logic
4. Update the main generator

### Improving NLP Capabilities
1. Enhance pattern recognition in `nlp_extractor.py`
2. Add new entity types and relationships
3. Improve business logic inference
4. Add domain-specific vocabularies

### Extending Code Generation
1. Add new code templates
2. Implement additional features
3. Improve code quality and structure
4. Add new testing patterns

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For questions, issues, or feature requests:
1. Check the generated README.md files for project-specific help
2. Review the code comments for implementation details
3. Examine the example projects for usage patterns
4. Modify the generators for custom requirements

---

**🎉 Start building amazing APIs with natural language today!**

```bash
python api_generator.py --interactive
```

