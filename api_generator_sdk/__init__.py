"""
API Generator SDK
================

A Python SDK for generating FastAPI and Django REST framework projects
from natural language descriptions using NLP-powered analysis.

This package provides a clean, object-oriented interface for:
- Extracting project requirements from natural language
- Generating complete, production-ready API projects
- Supporting multiple frameworks (FastAPI, Django)
- Extensible architecture for custom patterns and generators

Example usage:

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

For more examples and documentation, see the README.md file.
"""

__version__ = "1.0.0"
__author__ = "API Generator SDK Team"
__email__ = "contact@apigenerator.dev"

# Main exports
from .generator import ApiGenerator, generate_fastapi_project, generate_django_project
from .nlp_core import (
    NLPCore,
    NLPPatternRegistry,
    ProjectRequirements,
    FrameworkType,
    DatabaseType,
    AuthType,
    APIType,
    ModelDefinition,
    ModelField,
    Relationship,
    EndpointDefinition
)
from .exceptions import (
    APIGeneratorError,
    GenerationError,
    InvalidDescriptionError,
    FrameworkNotSupportedError,
    DatabaseNotSupportedError,
    AuthMethodNotSupportedError,
    ConfigurationError,
    NLPParsingError,
    ProjectStructureError,
    CodeGenerationError,
    ValidationError,
    TemplateError,
    ExtensionError
)

# Convenience imports for common use cases
from .fastapi_gen import FastAPIGenerator
from .django_gen import DjangoGenerator

__all__ = [
    # Main interface
    'ApiGenerator',
    'generate_fastapi_project',
    'generate_django_project',
    
    # Core components
    'NLPCore',
    'NLPPatternRegistry',
    'FastAPIGenerator',
    'DjangoGenerator',
    
    # Data structures
    'ProjectRequirements',
    'ModelDefinition',
    'ModelField',
    'Relationship',
    'EndpointDefinition',
    
    # Enums
    'FrameworkType',
    'DatabaseType',
    'AuthType',
    'APIType',
    
    # Exceptions
    'APIGeneratorError',
    'GenerationError',
    'InvalidDescriptionError',
    'FrameworkNotSupportedError',
    'DatabaseNotSupportedError',
    'AuthMethodNotSupportedError',
    'ConfigurationError',
    'NLPParsingError',
    'ProjectStructureError',
    'CodeGenerationError',
    'ValidationError',
    'TemplateError',
    'ExtensionError',
]

# Package metadata
__package_info__ = {
    'name': 'api-generator-sdk',
    'version': __version__,
    'description': 'NLP-powered API generator for FastAPI and Django REST framework',
    'author': __author__,
    'author_email': __email__,
    'url': 'https://github.com/api-generator/api-generator-sdk',
    'license': 'MIT',
    'keywords': ['api', 'generator', 'fastapi', 'django', 'nlp', 'code-generation'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
}

