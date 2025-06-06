"""
Enhanced Django REST Framework Generator
=======================================

Advanced Django REST framework generator with GraphQL support, enhanced business logic,
comprehensive testing, and production-ready features.

Features:
- Complete Django REST framework project generation
- GraphQL API support with Graphene
- Advanced authentication (JWT, OAuth2, Session)
- Comprehensive testing framework
- Production-ready deployment configurations
- Advanced business logic implementation
- File upload handling
- Background task processing with Celery
- Redis caching integration
- Rate limiting and security features
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from nlp_extractor import ProjectRequirements, FrameworkType, DatabaseType, AuthType, APIType
from project_analyzer import ProjectAnalyzer, EndpointAnalyzer
logger = logging.getLogger(__name__)

class DjangoGenerator:
    """
    Enhanced Django REST framework generator with comprehensive features
    """
    
    def __init__(self, requirements: ProjectRequirements):
        """Initialize the enhanced Django generator"""
        self.requirements = requirements
        self.analyzer = ProjectAnalyzer(requirements)
        self.analysis = None
        
        logger.info("Enhanced Django Generator initialized")
    
    def generate_complete_project(self, output_dir: str = ".") -> str:
        """
        Generate complete Django REST framework project with all enhancements
        
        Args:
            output_dir: Output directory for the project
            
        Returns:
            Path to the generated project
        """
        
        logger.info(f"Generating enhanced Django project in {output_dir}")
        
        # Analyze project requirements
        self.analysis = self.analyzer.analyze_complete_project()
        
        # Create project directory
        project_path = Path(output_dir) / self.requirements.project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generate Django project structure
        self._create_django_project_structure(project_path)
        
        # Generate core Django files
        self._generate_django_settings(project_path)
        self._generate_django_urls(project_path)
        self._generate_django_wsgi_asgi(project_path)
        
        # Generate apps for each model
        self._generate_django_apps(project_path)
        
        # Generate authentication system
        if self.requirements.auth_type != AuthType.NONE:
            self._generate_django_authentication(project_path)
        
        # Generate GraphQL components if needed
        if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID]:
            self._generate_django_graphql(project_path)
        
        # Generate utility components
        self._generate_django_utilities(project_path)
        
        # Generate testing framework
        if self.requirements.include_tests:
            self._generate_django_testing(project_path)
        
        # Generate deployment configurations
        self._generate_django_deployment(project_path)
        
        # Generate documentation
        if self.requirements.include_docs:
            self._generate_django_documentation(project_path)
        
        # Generate project files
        self._generate_django_project_files(project_path)
        
        logger.info(f"Enhanced Django project generated successfully at {project_path}")
        return str(project_path)
    
    def _create_django_project_structure(self, project_path: Path):
        """Create Django project directory structure"""
        
        structure = self.analysis['project_structure']['directories']
        
        for directory, subdirs in structure.items():
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            if isinstance(subdirs, list):
                for subdir in subdirs:
                    if not subdir.endswith('.py'):
                        (dir_path / subdir).mkdir(parents=True, exist_ok=True)
    
    def _generate_django_settings(self, project_path: Path):
        """Generate Django settings files"""
        
        project_name = self.requirements.project_name
        
        # Base settings
        base_settings = f'''"""
Django Base Settings
"""

import os
from pathlib import Path
from typing import List

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security settings
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
    {'django_ratelimit,' if self.requirements.rate_limiting else ''}
    {'graphene_django,' if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ''}
]

LOCAL_APPS = [
{chr(10).join([f"    'apps.{model['name'].lower()}s'," for model in self.requirements.models])}
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
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

# Templates
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
ASGI_APPLICATION = '{project_name}.asgi.application'

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

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': [
        {'rest_framework_simplejwt.authentication.JWTAuthentication,' if self.requirements.auth_type == AuthType.JWT else ''}
        {'rest_framework.authentication.SessionAuthentication,' if self.requirements.auth_type == AuthType.SESSION else ''}
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}}

# CORS settings
{"CORS_ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')" if self.requirements.cors_enabled else ""}
{"CORS_ALLOW_ALL_ORIGINS = DEBUG" if self.requirements.cors_enabled else ""}

# JWT settings
{f'''SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}}''' if self.requirements.auth_type == AuthType.JWT else ""}

# Cache configuration
{"CACHES = {" if self.requirements.caching else ""}
{'''    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}''' if self.requirements.caching else ""}

# Celery configuration
{"CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')" if self.requirements.use_celery else ""}
{"CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')" if self.requirements.use_celery else ""}

# GraphQL configuration
{f'''GRAPHENE = {{
    'SCHEMA': 'apps.graphql.schema.schema'
}}''' if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}

# Logging configuration
LOGGING = {{
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {{
        'verbose': {{
            'format': '{{levelname}} {{asctime}} {{module}} {{process:d}} {{thread:d}} {{message}}',
            'style': '{{',
        }},
    }},
    'handlers': {{
        'file': {{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        }},
        'console': {{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }},
    }},
    'root': {{
        'handlers': ['console', 'file'],
        'level': 'INFO',
    }},
}}
'''
        
        self._write_file(project_path / project_name / "settings" / "base.py", base_settings)
        
        # Development settings
        dev_settings = f'''"""
Development Settings
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database for development
DATABASES['default']['NAME'] = '{project_name}_dev'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Additional development apps
INSTALLED_APPS += [
    'django_extensions',
]
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
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database for production
DATABASES['default']['NAME'] = os.getenv('DB_NAME', '{project_name}')

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
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
elif environment == 'staging':
    from .staging import *
else:
    from .development import *
'''
        
        self._write_file(project_path / project_name / "settings" / "__init__.py", settings_init)
    
    def _generate_django_urls(self, project_path: Path):
        """Generate Django URL configuration"""
        
        project_name = self.requirements.project_name
        
        main_urls = f'''"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
{"from graphene_django.views import GraphQLView" if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    {"path('graphql/', GraphQLView.as_view(graphiql=True))," if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}
    path('health/', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
        
        self._write_file(project_path / project_name / "urls.py", main_urls)
    
    def _generate_django_wsgi_asgi(self, project_path: Path):
        """Generate WSGI and ASGI configuration"""
        
        project_name = self.requirements.project_name
        
        # WSGI
        wsgi_content = f'''"""
WSGI config for {project_name} project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
'''
        
        self._write_file(project_path / project_name / "wsgi.py", wsgi_content)
        
        # ASGI
        asgi_content = f'''"""
ASGI config for {project_name} project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_asgi_application()
'''
        
        self._write_file(project_path / project_name / "asgi.py", asgi_content)
    
    def _generate_django_apps(self, project_path: Path):
        """Generate Django apps for each model"""
        
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
{chr(10).join([f"    path('{model['name'].lower()}s/', include('apps.{model['name'].lower()}s.urls'))," for model in self.requirements.models])}
]
'''
        
        self._write_file(project_path / "apps" / "api" / "urls.py", api_urls)
        
        # API __init__.py
        self._write_file(project_path / "apps" / "api" / "__init__.py", "")
    
    def _generate_core_app(self, project_path: Path):
        """Generate core utilities app"""
        
        # Core views
        core_views = '''"""
Core Views
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'version': '1.0.0'
    })

def version_info(request):
    """Version information"""
    return JsonResponse({
        'version': '1.0.0',
        'api_version': 'v1'
    })
'''
        
        self._write_file(project_path / "apps" / "core" / "views.py", core_views)
        
        # Core URLs
        core_urls = '''"""
Core URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('version/', views.version_info, name='version_info'),
]
'''
        
        self._write_file(project_path / "apps" / "core" / "urls.py", core_urls)
        
        # Core __init__.py
        self._write_file(project_path / "apps" / "core" / "__init__.py", "")
    
    def _generate_model_app(self, project_path: Path, model: Dict[str, Any]):
        """Generate Django app for a specific model"""
        
        model_name = model['name']
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
        
        # Tests
        if self.requirements.include_tests:
            tests_content = self._generate_django_tests(model)
            self._write_file(project_path / "apps" / app_name / "tests.py", tests_content)
        
        # __init__.py
        self._write_file(project_path / "apps" / app_name / "__init__.py", "")
    
    def _generate_django_model(self, model: Dict[str, Any]) -> str:
        """Generate Django model"""
        
        model_name = model['name']
        fields = model['fields']
        
        field_definitions = []
        
        for field in fields:
            if field['name'] in ['id']:
                continue  # Django auto-generates id
            
            field_def = self._generate_django_field_definition(field)
            if field_def:
                field_definitions.append(field_def)
        
        content = f'''"""
{model_name} Model
"""

from django.db import models
from django.contrib.auth.models import User

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
    
    def _generate_django_field_definition(self, field: Dict[str, Any]) -> str:
        """Generate Django model field definition"""
        
        field_name = field['name']
        field_type = field['type']
        required = field.get('required', True)
        unique = field.get('unique', False)
        default = field.get('default')
        
        # Map field types to Django field types
        type_mapping = {
            'string': 'CharField(max_length=255',
            'text': 'TextField(',
            'integer': 'IntegerField(',
            'decimal': 'DecimalField(max_digits=10, decimal_places=2',
            'boolean': 'BooleanField(',
            'datetime': 'DateTimeField(',
            'date': 'DateField(',
            'time': 'TimeField(',
            'email': 'EmailField(',
            'url': 'URLField('
        }
        
        django_type = type_mapping.get(field_type, 'CharField(max_length=255')
        
        # Build field definition
        field_parts = [django_type]
        
        if not required:
            field_parts.append("null=True, blank=True")
        
        if unique:
            field_parts.append("unique=True")
        
        if default is not None and default != "now":
            if isinstance(default, str):
                field_parts.append(f'default="{default}"')
            else:
                field_parts.append(f"default={default}")
        
        field_definition = f"    {field_name} = models.{', '.join(field_parts)})"
        
        return field_definition
    
    def _generate_django_serializer(self, model: Dict[str, Any]) -> str:
        """Generate Django REST framework serializer"""
        
        model_name = model['name']
        
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
        extra_kwargs = {{
            field.name: {{'required': False}} for field in {model_name}._meta.fields
            if field.name not in ('id', 'created_at', 'updated_at')
        }}
'''
        
        return content
    
    def _generate_django_views(self, model: Dict[str, Any]) -> str:
        """Generate Django REST framework views"""
        
        model_name = model['name']
        
        content = f'''"""
{model_name} Views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import {model_name}
from .serializers import {model_name}Serializer, {model_name}CreateSerializer, {model_name}UpdateSerializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    """
    {model_name} ViewSet
    
    Provides CRUD operations for {model_name}
    """
    
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
    {"permission_classes = [IsAuthenticated]" if self.requirements.auth_type != AuthType.NONE else ""}
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']  # Adjust based on model fields
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return {model_name}CreateSerializer
        elif self.action in ['update', 'partial_update']:
            return {model_name}UpdateSerializer
        return {model_name}Serializer
    
    @action(detail=True, methods=['post'])
    def custom_action(self, request, pk=None):
        """
        Custom action example
        """
        instance = self.get_object()
        # Add custom logic here
        return Response({{'message': 'Custom action performed'}})
'''
        
        return content
    
    def _generate_django_urls_for_model(self, model: Dict[str, Any]) -> str:
        """Generate Django URLs for model"""
        
        model_name = model['name']
        
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
    
    def _generate_django_admin(self, model: Dict[str, Any]) -> str:
        """Generate Django admin configuration"""
        
        model_name = model['name']
        
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
    
    def _generate_django_apps_config(self, model: Dict[str, Any]) -> str:
        """Generate Django apps configuration"""
        
        model_name = model['name']
        app_name = f"{model_name.lower()}s"
        
        content = f'''"""
{model_name} App Configuration
"""

from django.apps import AppConfig

class {model_name}sConfig(AppConfig):
    """
    {model_name}s app configuration
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{model_name}s'
'''
        
        return content
    
    def _generate_django_tests(self, model: Dict[str, Any]) -> str:
        """Generate Django tests"""
        
        model_name = model['name']
        
        content = f'''"""
{model_name} Tests
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from .models import {model_name}

class {model_name}ModelTest(TestCase):
    """
    {model_name} model tests
    """
    
    def setUp(self):
        """Set up test data"""
        self.{model_name.lower()} = {model_name}.objects.create(
            # Add required fields here
        )
    
    def test_model_creation(self):
        """Test {model_name} model creation"""
        self.assertTrue(isinstance(self.{model_name.lower()}, {model_name}))
        self.assertEqual(str(self.{model_name.lower()}), f"{model_name} {{self.{model_name.lower()}.id}}")

class {model_name}APITest(APITestCase):
    """
    {model_name} API tests
    """
    
    def setUp(self):
        """Set up test data"""
        {"self.user = User.objects.create_user(username='testuser', password='testpass')" if self.requirements.auth_type != AuthType.NONE else ""}
        self.{model_name.lower()} = {model_name}.objects.create(
            # Add required fields here
        )
    
    def test_get_{model_name.lower()}_list(self):
        """Test getting {model_name} list"""
        {"self.client.force_authenticate(user=self.user)" if self.requirements.auth_type != AuthType.NONE else ""}
        url = reverse('{model_name.lower()}-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_{model_name.lower()}(self):
        """Test creating {model_name}"""
        {"self.client.force_authenticate(user=self.user)" if self.requirements.auth_type != AuthType.NONE else ""}
        url = reverse('{model_name.lower()}-list')
        data = {{
            # Add required fields here
        }}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
'''
        
        return content
    
    def _generate_django_authentication(self, project_path: Path):
        """Generate Django authentication system"""
        
        if self.requirements.auth_type == AuthType.JWT:
            # JWT authentication views
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
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(
        {'error': 'Missing required fields'},
        status=status.HTTP_400_BAD_REQUEST
    )
'''
            
            self._write_file(project_path / "apps" / "auth" / "views.py", auth_views)
    
    def _generate_django_graphql(self, project_path: Path):
        """Generate Django GraphQL components"""
        
        if self.requirements.api_type not in [APIType.GRAPHQL, APIType.HYBRID]:
            return
        
        # GraphQL schema
        schema_content = f'''"""
GraphQL Schema
"""

import graphene
from graphene_django import DjangoObjectType
{chr(10).join([f"from apps.{model['name'].lower()}s.models import {model['name']}" for model in self.requirements.models])}

{chr(10).join([self._generate_graphql_type(model) for model in self.requirements.models])}

class Query(graphene.ObjectType):
    """GraphQL Query"""
    
{chr(10).join([f"    all_{model['name'].lower()}s = graphene.List({model['name']}Type)" for model in self.requirements.models])}
{chr(10).join([f"    {model['name'].lower()} = graphene.Field({model['name']}Type, id=graphene.Int())" for model in self.requirements.models])}
    
{chr(10).join([self._generate_graphql_resolver(model) for model in self.requirements.models])}

class Mutation(graphene.ObjectType):
    """GraphQL Mutation"""
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
'''
        
        self._write_file(project_path / "apps" / "graphql" / "schema.py", schema_content)
    
    def _generate_graphql_type(self, model: Dict[str, Any]) -> str:
        """Generate GraphQL type for model"""
        
        model_name = model['name']
        
        return f'''class {model_name}Type(DjangoObjectType):
    """GraphQL type for {model_name}"""
    
    class Meta:
        model = {model_name}
        fields = "__all__"'''
    
    def _generate_graphql_resolver(self, model: Dict[str, Any]) -> str:
        """Generate GraphQL resolver for model"""
        
        model_name = model['name']
        model_name_lower = model_name.lower()
        
        return f'''    def resolve_all_{model_name_lower}s(self, info):
        """Resolve all {model_name_lower}s"""
        return {model_name}.objects.all()
    
    def resolve_{model_name_lower}(self, info, id):
        """Resolve single {model_name_lower}"""
        try:
            return {model_name}.objects.get(pk=id)
        except {model_name}.DoesNotExist:
            return None'''
    
    def _generate_django_utilities(self, project_path: Path):
        """Generate Django utility components"""
        
        # Management commands
        if self.requirements.use_celery:
            celery_command = '''"""
Celery management command
"""

from django.core.management.base import BaseCommand
from celery import Celery

class Command(BaseCommand):
    """Start Celery worker"""
    
    help = 'Start Celery worker'
    
    def handle(self, *args, **options):
        app = Celery('django_app')
        app.config_from_object('django.conf:settings', namespace='CELERY')
        app.autodiscover_tasks()
        app.worker_main()
'''
            
            self._write_file(project_path / "apps" / "core" / "management" / "commands" / "celery_worker.py", celery_command)
    
    def _generate_django_testing(self, project_path: Path):
        """Generate Django testing framework"""
        
        # Test settings
        test_settings = '''"""
Test Settings
"""

from .base import *

# Use in-memory SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Test-specific settings
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
'''
        
        self._write_file(project_path / self.requirements.project_name / "settings" / "test.py", test_settings)
    
    def _generate_django_deployment(self, project_path: Path):
        """Generate Django deployment configurations"""
        
        # Docker configuration
        dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "{self.requirements.project_name}.wsgi:application"]
'''
        
        self._write_file(project_path / "Dockerfile", dockerfile_content)
        
        # Docker Compose
        docker_compose_content = f'''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/{self.requirements.project_name}
    depends_on:
      - db
      {"- redis" if self.requirements.use_redis else ""}
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB={self.requirements.project_name}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  {"redis:" if self.requirements.use_redis else ""}
  {"  image: redis:7-alpine" if self.requirements.use_redis else ""}
  {"  ports:" if self.requirements.use_redis else ""}
  {"    - '6379:6379'" if self.requirements.use_redis else ""}

volumes:
  postgres_data:
'''
        
        self._write_file(project_path / "docker-compose.yml", docker_compose_content)
    
    def _generate_django_documentation(self, project_path: Path):
        """Generate Django documentation"""
        
        readme_content = f'''# {self.requirements.project_name.replace('_', ' ').title()}

{self.requirements.description}

## Features

- Django REST Framework API
- {"JWT Authentication" if self.requirements.auth_type == AuthType.JWT else "Authentication"}
- {"GraphQL Support" if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else "REST API"}
- {"Redis Caching" if self.requirements.caching else "Database Integration"}
- {"Background Tasks with Celery" if self.requirements.use_celery else "Synchronous Processing"}
- Comprehensive Testing
- Docker Support

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## API Endpoints

{chr(10).join([f"- `/{model['name'].lower()}s/` - {model['name']} CRUD operations" for model in self.requirements.models])}

## Testing

Run tests with: `python manage.py test`

## Deployment

Use Docker: `docker-compose up -d`
'''
        
        self._write_file(project_path / "README.md", readme_content)
    
    def _generate_django_project_files(self, project_path: Path):
        """Generate Django project files"""
        
        # Requirements
        requirements = self._get_django_requirements()
        self._write_file(project_path / "requirements.txt", '\n'.join(requirements))
        
        # Manage.py
        manage_py = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.requirements.project_name}.settings')
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
        
        self._write_file(project_path / "manage.py", manage_py)
        
        # Make manage.py executable
        os.chmod(project_path / "manage.py", 0o755)
        
        # .env.example
        env_example = f'''# Django Settings
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

# CORS
{"CORS_ORIGINS=http://localhost:3000" if self.requirements.cors_enabled else ""}

# Redis
{"REDIS_URL=redis://localhost:6379" if self.requirements.use_redis else ""}

# Celery
{"CELERY_BROKER_URL=redis://localhost:6379/0" if self.requirements.use_celery else ""}
{"CELERY_RESULT_BACKEND=redis://localhost:6379/0" if self.requirements.use_celery else ""}
'''
        
        self._write_file(project_path / ".env.example", env_example)
        
        # .gitignore
        gitignore_content = '''# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
'''
        
        self._write_file(project_path / ".gitignore", gitignore_content)
    
    def _get_django_requirements(self) -> List[str]:
        """Get Django requirements"""
        
        requirements = [
            'Django>=4.2.7',
            'djangorestframework>=3.14.0',
            'django-cors-headers>=4.3.1',
            'django-filter>=23.5',
            'gunicorn>=21.2.0',
        ]
        
        # Database requirements
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            requirements.append('psycopg2-binary>=2.9.9')
        elif self.requirements.database_type == DatabaseType.MYSQL:
            requirements.append('mysqlclient>=2.2.0')
        
        # Authentication requirements
        if self.requirements.auth_type == AuthType.JWT:
            requirements.append('djangorestframework-simplejwt>=5.3.0')
        
        # Additional features
        if self.requirements.caching or self.requirements.use_redis:
            requirements.extend(['redis>=5.0.1', 'django-redis>=5.4.0'])
        
        if self.requirements.use_celery:
            requirements.extend(['celery>=5.3.4', 'django-celery-beat>=2.5.0'])
        
        if self.requirements.rate_limiting:
            requirements.append('django-ratelimit>=4.1.0')
        
        if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID]:
            requirements.extend(['graphene-django>=3.1.5', 'django-graphql-jwt>=0.3.4'])
        
        # Development requirements
        requirements.extend([
            'django-extensions>=3.2.3',
            'pytest-django>=4.7.0',
            'factory-boy>=3.3.0',
        ])
        
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

# Main execution for testing
if __name__ == "__main__":
    from nlp_extractor import NLPExtractor
    
    extractor = NLPExtractor()
    requirements = extractor.extract_requirements(
        "Create a comprehensive e-commerce platform with user management, product catalog, and order processing"
    )
    requirements.framework = FrameworkType.DJANGO
    
    generator = DjangoGenerator(requirements)
    project_path = generator.generate_complete_project("/tmp/test_enhanced_django")
    
    print(f"Enhanced Django project generated at: {project_path}")

