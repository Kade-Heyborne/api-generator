"""
API Generator SDK - Django Generator Module
==========================================

Refactored Django REST framework code generation capabilities for the SDK.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .nlp_core import ProjectRequirements, FrameworkType, DatabaseType, AuthType, APIType
from .exceptions import CodeGenerationError, TemplateError

logger = logging.getLogger(__name__)

class DjangoGenerator:
    """
    Django REST framework code generator for the SDK
    """
    
    def __init__(self, requirements: ProjectRequirements):
        """Initialize Django generator"""
        self.requirements = requirements
        self.template_overrides: Dict[str, str] = {}
        
        logger.info("Django Generator initialized")
    
    def register_template_override(self, template_key: str, new_template_content: str):
        """
        Register a template override
        
        Args:
            template_key: Key identifying the template to override
            new_template_content: New template content
        """
        self.template_overrides[template_key] = new_template_content
        logger.info(f"Registered template override for: {template_key}")
    
    def generate_project(self, output_dir: str) -> str:
        """
        Generate Django REST framework project
        
        Args:
            output_dir: Output directory for the project
            
        Returns:
            Path to the generated project
            
        Raises:
            CodeGenerationError: If generation fails
        """
        
        try:
            logger.info(f"Generating Django project in {output_dir}")
            
            # Create project directory
            project_path = Path(output_dir) / self.requirements.project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Generate project structure
            self._create_directory_structure(project_path)
            
            # Generate Django project files
            self._generate_django_project(project_path)
            self._generate_settings(project_path)
            self._generate_urls(project_path)
            
            # Generate apps for each model
            self._generate_apps(project_path)
            
            # Generate authentication if needed
            if self.requirements.auth_type != AuthType.NONE:
                self._generate_auth(project_path)
            
            # Generate additional features
            self._generate_additional_features(project_path)
            
            # Generate project files
            self._generate_project_files(project_path)
            
            logger.info(f"Django project generated successfully at {project_path}")
            return str(project_path)
            
        except Exception as e:
            logger.error(f"Failed to generate Django project: {e}")
            raise CodeGenerationError(f"Django generation failed: {e}")
    
    def _create_directory_structure(self, project_path: Path):
        """Create Django project directory structure"""
        
        project_name = self.requirements.project_name
        
        directories = [
            project_name,
            f"{project_name}/settings",
            "apps",
            "apps/api",
            "apps/core",
            "static",
            "media",
            "templates",
            "tests",
            "docs",
        ]
        
        # Add app directories for each model
        for model in self.requirements.models:
            app_name = f"{model.name.lower()}s"
            directories.extend([
                f"apps/{app_name}",
                f"apps/{app_name}/migrations",
            ])
        
        for directory in directories:
            (project_path / directory).mkdir(parents=True, exist_ok=True)
            # Create __init__.py files for Python packages
            if directory.startswith("apps") or directory == project_name:
                (project_path / directory / "__init__.py").touch()
    
    def _generate_django_project(self, project_path: Path):
        """Generate main Django project files"""
        
        project_name = self.requirements.project_name
        
        # manage.py
        manage_content = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if __name__ == '__main__':
    """Run administrative tasks."""
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
'''
        
        self._write_file(project_path / "manage.py", manage_content)
        
        # Make manage.py executable
        os.chmod(project_path / "manage.py", 0o755)
        
        # wsgi.py
        wsgi_content = f'''"""
WSGI config for {project_name} project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
'''
        
        self._write_file(project_path / project_name / "wsgi.py", wsgi_content)
        
        # asgi.py
        asgi_content = f'''"""
ASGI config for {project_name} project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_asgi_application()
'''
        
        self._write_file(project_path / project_name / "asgi.py", asgi_content)
    
    def _generate_settings(self, project_path: Path):
        """Generate Django settings"""
        
        project_name = self.requirements.project_name
        
        # Base settings
        base_settings = f'''"""
Django Base Settings
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    {'rest_framework_simplejwt,' if self.requirements.auth_type == AuthType.JWT else ''}
]

LOCAL_APPS = [
    'apps.api',
    'apps.core',
{chr(10).join([f"    'apps.{model.name.lower()}s'," for model in self.requirements.models])}
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name}.wsgi.application'

# Database
DATABASES = {{
    'default': {{
        'ENGINE': '{self._get_django_database_engine()}',
        'NAME': os.getenv('DB_NAME', '{project_name}'),
        'USER': os.getenv('DB_USER', 'user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '{self._get_default_db_port()}'),
    }}
}}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': [
        {'rest_framework_simplejwt.authentication.JWTAuthentication,' if self.requirements.auth_type == AuthType.JWT else ''}
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}}

# CORS
{"CORS_ALLOWED_ORIGINS = ['http://localhost:3000']" if self.requirements.cors_enabled else ""}
{"CORS_ALLOW_ALL_ORIGINS = DEBUG" if self.requirements.cors_enabled else ""}

# JWT Settings
{f'''SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}}''' if self.requirements.auth_type == AuthType.JWT else ""}
'''
        
        self._write_file(project_path / project_name / "settings" / "base.py", base_settings)
        
        # Development settings
        dev_settings = f'''"""
Development Settings
"""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Development database
DATABASES['default']['NAME'] = '{project_name}_dev'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
'''
        
        self._write_file(project_path / project_name / "settings" / "development.py", dev_settings)
        
        # Production settings
        prod_settings = f'''"""
Production Settings
"""

from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
'''
        
        self._write_file(project_path / project_name / "settings" / "production.py", prod_settings)
        
        # Settings __init__.py
        settings_init = '''"""
Settings Package
"""

import os

environment = os.getenv('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *
'''
        
        self._write_file(project_path / project_name / "settings" / "__init__.py", settings_init)
    
    def _generate_urls(self, project_path: Path):
        """Generate URL configuration"""
        
        project_name = self.requirements.project_name
        
        # Main URLs
        main_urls = f'''"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    path('', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
        
        self._write_file(project_path / project_name / "urls.py", main_urls)
    
    def _generate_apps(self, project_path: Path):
        """Generate Django apps"""
        
        # Generate API app
        self._generate_api_app(project_path)
        
        # Generate core app
        self._generate_core_app(project_path)
        
        # Generate model-specific apps
        for model in self.requirements.models:
            self._generate_model_app(project_path, model)
    
    def _generate_api_app(self, project_path: Path):
        """Generate main API app"""
        
        # API URLs
        api_urls = f'''"""
API URL Configuration
"""

from django.urls import path, include

urlpatterns = [
{chr(10).join([f"    path('{model.name.lower()}s/', include('apps.{model.name.lower()}s.urls'))," for model in self.requirements.models])}
]
'''
        
        self._write_file(project_path / "apps" / "api" / "urls.py", api_urls)
        
        # API apps.py
        api_apps = '''"""
API App Configuration
"""

from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'
'''
        
        self._write_file(project_path / "apps" / "api" / "apps.py", api_apps)
    
    def _generate_core_app(self, project_path: Path):
        """Generate core app"""
        
        # Core views
        core_views = '''"""
Core Views
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'healthy', 'version': '1.0.0'})
'''
        
        self._write_file(project_path / "apps" / "core" / "views.py", core_views)
        
        # Core URLs
        core_urls = '''"""
Core URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
]
'''
        
        self._write_file(project_path / "apps" / "core" / "urls.py", core_urls)
        
        # Core apps.py
        core_apps = '''"""
Core App Configuration
"""

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
'''
        
        self._write_file(project_path / "apps" / "core" / "apps.py", core_apps)
    
    def _generate_model_app(self, project_path: Path, model):
        """Generate app for a specific model"""
        
        model_name = model.name
        app_name = f"{model_name.lower()}s"
        
        # Models
        model_content = self._generate_django_model(model)
        self._write_file(project_path / "apps" / app_name / "models.py", model_content)
        
        # Serializers
        serializer_content = self._generate_django_serializer(model)
        self._write_file(project_path / "apps" / app_name / "serializers.py", serializer_content)
        
        # Views
        views_content = self._generate_django_views(model)
        self._write_file(project_path / "apps" / app_name / "views.py", views_content)
        
        # URLs
        urls_content = self._generate_django_urls_for_model(model)
        self._write_file(project_path / "apps" / app_name / "urls.py", urls_content)
        
        # Admin
        admin_content = self._generate_django_admin(model)
        self._write_file(project_path / "apps" / app_name / "admin.py", admin_content)
        
        # Apps configuration
        apps_content = self._generate_django_apps_config(model)
        self._write_file(project_path / "apps" / app_name / "apps.py", apps_content)
        
        # Migrations __init__.py
        self._write_file(project_path / "apps" / app_name / "migrations" / "__init__.py", "")
    
    def _generate_django_model(self, model) -> str:
        """Generate Django model"""
        
        model_name = model.name
        
        # Generate field definitions
        field_definitions = []
        for field in model.fields:
            if field.name == 'id':
                continue  # Django auto-generates id
            
            field_def = self._generate_django_field_definition(field)
            if field_def:
                field_definitions.append(field_def)
        
        content = f'''"""
{model_name} Model
"""

from django.db import models

class {model_name}(models.Model):
    """
    {model_name} model
    """
    
{chr(10).join(field_definitions)}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '{model_name}'
        verbose_name_plural = '{model_name}s'
    
    def __str__(self):
        return f"{model_name} {{self.id}}"
'''
        
        return content
    
    def _generate_django_field_definition(self, field) -> str:
        """Generate Django model field definition"""
        
        type_mapping = {
            'string': 'CharField(max_length=255',
            'text': 'TextField(',
            'integer': 'IntegerField(',
            'decimal': 'DecimalField(max_digits=10, decimal_places=2',
            'boolean': 'BooleanField(',
            'datetime': 'DateTimeField(',
            'email': 'EmailField(',
            'url': 'URLField('
        }
        
        django_type = type_mapping.get(field.type, 'CharField(max_length=255')
        
        field_parts = [django_type]
        
        if not field.required:
            field_parts.append("null=True, blank=True")
        
        if field.unique:
            field_parts.append("unique=True")
        
        if field.default is not None and field.default != "now":
            if isinstance(field.default, str):
                field_parts.append(f'default="{field.default}"')
            else:
                field_parts.append(f"default={field.default}")
        
        return f"    {field.name} = models.{', '.join(field_parts)})"
    
    def _generate_django_serializer(self, model) -> str:
        """Generate Django REST framework serializer"""
        
        model_name = model.name
        
        content = f'''"""
{model_name} Serializers
"""

from rest_framework import serializers
from .models import {model_name}

class {model_name}Serializer(serializers.ModelSerializer):
    """
    {model_name} serializer
    """
    
    class Meta:
        model = {model_name}
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class {model_name}CreateSerializer(serializers.ModelSerializer):
    """
    {model_name} creation serializer
    """
    
    class Meta:
        model = {model_name}
        exclude = ('id', 'created_at', 'updated_at')

class {model_name}UpdateSerializer(serializers.ModelSerializer):
    """
    {model_name} update serializer
    """
    
    class Meta:
        model = {model_name}
        exclude = ('id', 'created_at', 'updated_at')
'''
        
        return content
    
    def _generate_django_views(self, model) -> str:
        """Generate Django REST framework views"""
        
        model_name = model.name
        
        content = f'''"""
{model_name} Views
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import {model_name}
from .serializers import {model_name}Serializer, {model_name}CreateSerializer, {model_name}UpdateSerializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    """
    {model_name} ViewSet
    """
    
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
    {"permission_classes = [IsAuthenticated]" if self.requirements.auth_type != AuthType.NONE else ""}
    
    def get_serializer_class(self):
        if self.action == 'create':
            return {model_name}CreateSerializer
        elif self.action in ['update', 'partial_update']:
            return {model_name}UpdateSerializer
        return {model_name}Serializer
'''
        
        return content
    
    def _generate_django_urls_for_model(self, model) -> str:
        """Generate Django URLs for model"""
        
        model_name = model.name
        
        content = f'''"""
{model_name} URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.{model_name}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
'''
        
        return content
    
    def _generate_django_admin(self, model) -> str:
        """Generate Django admin configuration"""
        
        model_name = model.name
        
        content = f'''"""
{model_name} Admin Configuration
"""

from django.contrib import admin
from .models import {model_name}

@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    """
    {model_name} admin configuration
    """
    
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
'''
        
        return content
    
    def _generate_django_apps_config(self, model) -> str:
        """Generate Django apps configuration"""
        
        model_name = model.name
        app_name = f"{model_name.lower()}s"
        
        content = f'''"""
{model_name} App Configuration
"""

from django.apps import AppConfig

class {model_name}sConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{model_name}s'
'''
        
        return content
    
    def _generate_auth(self, project_path: Path):
        """Generate authentication system"""
        
        if self.requirements.auth_type == AuthType.JWT:
            # Create auth app
            auth_views = '''"""
JWT Authentication Views
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login with JWT"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if username and email and password:
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    return Response(
        {'error': 'Missing required fields'},
        status=status.HTTP_400_BAD_REQUEST
    )
'''
            
            self._write_file(project_path / "apps" / "auth" / "views.py", auth_views)
    
    def _generate_additional_features(self, project_path: Path):
        """Generate additional features"""
        pass  # Placeholder for additional features
    
    def _generate_project_files(self, project_path: Path):
        """Generate project files"""
        
        # Requirements.txt
        requirements = self._get_requirements()
        self._write_file(project_path / "requirements.txt", '\n'.join(requirements))
        
        # README.md
        readme_content = f'''# {self.requirements.project_name.replace('_', ' ').title()}

{self.requirements.description}

## Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start server: `python manage.py runserver`

## API Documentation

Visit `http://localhost:8000/admin/` for Django admin interface.

## Models

{chr(10).join([f"- {model.name}: {model.description}" for model in self.requirements.models])}
'''
        
        self._write_file(project_path / "README.md", readme_content)
        
        # .env.example
        env_content = f'''# Django Settings
DJANGO_ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME={self.requirements.project_name}
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT={self._get_default_db_port()}
'''
        
        self._write_file(project_path / ".env.example", env_content)
    
    def _get_requirements(self) -> List[str]:
        """Get Django requirements"""
        
        requirements = [
            "Django>=4.2.7",
            "djangorestframework>=3.14.0",
            "django-cors-headers>=4.3.1",
        ]
        
        # Database requirements
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            requirements.append("psycopg2-binary>=2.9.9")
        elif self.requirements.database_type == DatabaseType.MYSQL:
            requirements.append("mysqlclient>=2.2.0")
        
        # Authentication requirements
        if self.requirements.auth_type == AuthType.JWT:
            requirements.append("djangorestframework-simplejwt>=5.3.0")
        
        return requirements
    
    def _get_django_database_engine(self) -> str:
        """Get Django database engine"""
        
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            return "django.db.backends.postgresql"
        elif self.requirements.database_type == DatabaseType.MYSQL:
            return "django.db.backends.mysql"
        elif self.requirements.database_type == DatabaseType.SQLITE:
            return "django.db.backends.sqlite3"
        else:
            return "django.db.backends.sqlite3"
    
    def _get_default_db_port(self) -> str:
        """Get default database port"""
        
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            return "5432"
        elif self.requirements.database_type == DatabaseType.MYSQL:
            return "3306"
        else:
            return ""
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Generated file: {file_path}")

