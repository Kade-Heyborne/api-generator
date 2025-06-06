"""
Enhanced FastAPI Code Generator
==============================

Advanced FastAPI code generator with GraphQL support, enhanced business logic,
Alembic migrations, comprehensive testing, and production-ready features.

Features:
- Complete FastAPI project generation
- GraphQL API support with Strawberry
- Alembic database migrations
- Advanced authentication (JWT, OAuth2, API Key)
- Comprehensive testing framework
- Production-ready deployment configurations
- Advanced business logic implementation
- File upload handling
- Real-time WebSocket support
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

class FastAPIGenerator:
    """
    Enhanced FastAPI code generator with comprehensive features
    """
    
    def __init__(self, requirements: ProjectRequirements):
        """Initialize the enhanced FastAPI generator"""
        self.requirements = requirements
        self.analyzer = ProjectAnalyzer(requirements)
        self.analysis = None
        
        logger.info("Enhanced FastAPI Generator initialized")
    
    def generate_complete_project(self, output_dir: str = ".") -> str:
        """
        Generate complete FastAPI project with all enhancements
        
        Args:
            output_dir: Output directory for the project
            
        Returns:
            Path to the generated project
        """
        
        logger.info(f"Generating enhanced FastAPI project in {output_dir}")
        
        # Analyze project requirements
        self.analysis = self.analyzer.analyze_complete_project()
        
        # Create project directory
        project_path = Path(output_dir) / self.requirements.project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generate project structure
        self._create_directory_structure(project_path)
        
        # Generate core application files
        self._generate_main_application(project_path)
        self._generate_app_factory(project_path)
        self._generate_configuration(project_path)
        
        # Generate database components
        self._generate_database_components(project_path)
        self._generate_models(project_path)
        self._generate_alembic_configuration(project_path)
        
        # Generate API components
        self._generate_schemas(project_path)
        self._generate_crud_operations(project_path)
        self._generate_api_routes(project_path)
        self._generate_dependencies(project_path)
        
        # Generate authentication system
        if self.requirements.auth_type != AuthType.NONE:
            self._generate_authentication_system(project_path)
        
        # Generate GraphQL components if needed
        if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID]:
            self._generate_graphql_components(project_path)
        
        # Generate services and business logic
        self._generate_services(project_path)
        self._generate_business_logic(project_path)
        
        # Generate utility components
        self._generate_utilities(project_path)
        self._generate_middleware(project_path)
        
        # Generate testing framework
        if self.requirements.include_tests:
            self._generate_testing_framework(project_path)
        
        # Generate deployment configurations
        self._generate_deployment_configs(project_path)
        
        # Generate documentation
        if self.requirements.include_docs:
            self._generate_documentation(project_path)
        
        # Generate project files
        self._generate_project_files(project_path)
        
        logger.info(f"Enhanced FastAPI project generated successfully at {project_path}")
        return str(project_path)
    
    def _create_directory_structure(self, project_path: Path):
        """Create the complete directory structure"""
        
        structure = self.analysis['project_structure']['directories']
        
        for directory, subdirs in structure.items():
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            if isinstance(subdirs, list):
                for subdir in subdirs:
                    if not subdir.endswith('.py'):
                        (dir_path / subdir).mkdir(parents=True, exist_ok=True)
    
    def _generate_main_application(self, project_path: Path):
        """Generate the main FastAPI application entry point"""
        
        content = f'''"""
{self.requirements.project_name.replace('_', ' ').title()} API
Main application entry point
"""

import uvicorn
from app.main import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
'''
        
        self._write_file(project_path / "main.py", content)
    
    def _generate_app_factory(self, project_path: Path):
        """Generate the FastAPI app factory"""
        
        cors_import = "from fastapi.middleware.cors import CORSMiddleware" if self.requirements.cors_enabled else ""
        rate_limit_imports = """
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded""" if self.requirements.rate_limiting else ""
        
        websocket_import = "from fastapi import WebSocket" if self.requirements.real_time else ""
        
        content = f'''"""
FastAPI Application Factory
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
{cors_import}
{rate_limit_imports}
{websocket_import}

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.database import engine, Base
from app.api.v1.router import api_router
{"from app.graphql.schema import graphql_app" if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}
{"from app.core.websocket import websocket_manager" if self.requirements.real_time else ""}

settings = get_settings()

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title="{self.requirements.project_name.replace('_', ' ').title()} API",
        description="{self.requirements.description}",
        version="1.0.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        openapi_url="/openapi.json" if settings.environment != "production" else None
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    {"# Include GraphQL" if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}
    {"app.mount('/graphql', graphql_app)" if self.requirements.api_type in [APIType.GRAPHQL, APIType.HYBRID] else ""}
    
    # Setup WebSocket endpoints
    {"setup_websocket_endpoints(app)" if self.requirements.real_time else ""}
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Add startup and shutdown events
    setup_events(app)
    
    return app

def setup_middleware(app: FastAPI):
    """Setup application middleware"""
    
    {"# CORS middleware" if self.requirements.cors_enabled else ""}
    {'''app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )''' if self.requirements.cors_enabled else ""}
    
    {"# Rate limiting" if self.requirements.rate_limiting else ""}
    {'''limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)''' if self.requirements.rate_limiting else ""}

def setup_exception_handlers(app: FastAPI):
    """Setup custom exception handlers"""
    
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        """Custom HTTP exception handler with logging"""
        logger.error(f"HTTP {{exc.status_code}} error: {{exc.detail}} - {{request.url}}")
        return await http_exception_handler(request, exc)
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler"""
        logger.error(f"Unhandled exception: {{exc}} - {{request.url}}")
        return JSONResponse(
            status_code=500,
            content={{"detail": "Internal server error"}}
        )

{"def setup_websocket_endpoints(app: FastAPI):" if self.requirements.real_time else ""}
{'''    """Setup WebSocket endpoints"""
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket_manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await websocket_manager.broadcast(data)
        except Exception as e:
            logger.error(f"WebSocket error: {{e}}")
        finally:
            websocket_manager.disconnect(websocket)''' if self.requirements.real_time else ""}

def setup_events(app: FastAPI):
    """Setup startup and shutdown events"""
    
    @app.on_event("startup")
    async def startup_event():
        """Application startup"""
        logger.info("Application starting up...")
        {"# Initialize Redis connection" if self.requirements.use_redis else ""}
        {"# Start background tasks" if self.requirements.background_tasks else ""}
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Application shutdown"""
        logger.info("Application shutting down...")
        {"# Close Redis connection" if self.requirements.use_redis else ""}
        {"# Stop background tasks" if self.requirements.background_tasks else ""}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy", "version": "1.0.0"}}
'''
        
        self._write_file(project_path / "app" / "main.py", content)
    
    def _generate_configuration(self, project_path: Path):
        """Generate application configuration"""
        
        # Core configuration
        config_content = f'''"""
Application Configuration
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Basic settings
    app_name: str = "{self.requirements.project_name.replace('_', ' ').title()} API"
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    
    # Database settings
    database_url: str = Field(
        default="{self._get_default_database_url()}",
        env="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Authentication settings
    {"access_token_expire_minutes: int = Field(default=30, env='ACCESS_TOKEN_EXPIRE_MINUTES')" if self.requirements.auth_type == AuthType.JWT else ""}
    {"algorithm: str = Field(default='HS256', env='ALGORITHM')" if self.requirements.auth_type == AuthType.JWT else ""}
    
    # CORS settings
    {"cors_origins: List[str] = Field(default=['http://localhost:3000'], env='CORS_ORIGINS')" if self.requirements.cors_enabled else ""}
    
    # Redis settings
    {"redis_url: str = Field(default='redis://localhost:6379', env='REDIS_URL')" if self.requirements.use_redis else ""}
    
    # File upload settings
    {"max_file_size: int = Field(default=10485760, env='MAX_FILE_SIZE')  # 10MB" if self.requirements.file_uploads else ""}
    {"upload_dir: str = Field(default='uploads', env='UPLOAD_DIR')" if self.requirements.file_uploads else ""}
    
    # Celery settings
    {"celery_broker_url: str = Field(default='redis://localhost:6379/0', env='CELERY_BROKER_URL')" if self.requirements.use_celery else ""}
    {"celery_result_backend: str = Field(default='redis://localhost:6379/0', env='CELERY_RESULT_BACKEND')" if self.requirements.use_celery else ""}
    
    # Logging settings
    log_level: str = Field(default="{self.requirements.logging_level}", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
'''
        
        self._write_file(project_path / "app" / "core" / "config.py", content)
        
        # Logging configuration
        logging_content = '''"""
Logging Configuration
"""

import logging
import sys
from app.core.config import get_settings

def setup_logging():
    """Setup application logging"""
    
    settings = get_settings()
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log") if settings.environment != "development" else logging.NullHandler()
        ]
    )
    
    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.database_echo else logging.WARNING
    )

# Get logger for this module
logger = logging.getLogger(__name__)
'''
        
        self._write_file(project_path / "app" / "core" / "logging.py", logging_content)
        
        # Security configuration
        security_content = f'''"""
Security Configuration
"""

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

{"# JWT configuration" if self.requirements.auth_type == AuthType.JWT else ""}
{'''SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes''' if self.requirements.auth_type == AuthType.JWT else ""}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

{"def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:" if self.requirements.auth_type == AuthType.JWT else ""}
{'''    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt''' if self.requirements.auth_type == AuthType.JWT else ""}

{"def verify_token(token: str) -> dict:" if self.requirements.auth_type == AuthType.JWT else ""}
{'''    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )''' if self.requirements.auth_type == AuthType.JWT else ""}
'''
        
        self._write_file(project_path / "app" / "core" / "security.py", security_content)
    
    def _generate_database_components(self, project_path: Path):
        """Generate database components"""
        
        # Database configuration
        if self.requirements.database_type == DatabaseType.MONGODB:
            db_content = '''"""
MongoDB Database Configuration
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import get_settings

settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    """Get database client"""
    return db.client

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.database_url)
    await init_beanie(database=db.client.get_default_database(), document_models=[])

async def close_mongo_connection():
    """Close database connection"""
    db.client.close()
'''
        else:
            db_content = f'''"""
SQLAlchemy Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings

settings = get_settings()

# Database engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    {"pool_size=10, max_overflow=20" if self.requirements.database_type != DatabaseType.SQLITE else ""}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
'''
        
        self._write_file(project_path / "app" / "db" / "database.py", db_content)
        
        # Base model class
        if self.requirements.database_type != DatabaseType.MONGODB:
            base_model_content = '''"""
Base Model Class
"""

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.db.database import Base

class BaseModel(Base):
    """Base model with common fields"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
'''
            
            self._write_file(project_path / "app" / "db" / "base.py", base_model_content)
    
    def _generate_alembic_configuration(self, project_path: Path):
        """Generate Alembic migration configuration"""
        
        if self.requirements.database_type == DatabaseType.MONGODB:
            return  # MongoDB doesn't use Alembic
        
        # Alembic configuration file
        alembic_ini_content = f'''# Alembic Configuration File

[alembic]
script_location = migrations
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = {self._get_default_database_url()}

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
        
        self._write_file(project_path / "alembic.ini", alembic_ini_content)
        
        # Alembic env.py
        env_py_content = '''"""
Alembic Environment Configuration
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.database import Base
from app.core.config import get_settings

# Import all models to ensure they are registered with SQLAlchemy
from app.models import *

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = Base.metadata

def get_url():
    """Get database URL from settings"""
    settings = get_settings()
    return settings.database_url

def run_migrations_offline():
    """Run migrations in 'offline' mode"""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
        
        self._write_file(project_path / "migrations" / "env.py", env_py_content)
        
        # Migration script template
        script_py_content = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
'''
        
        self._write_file(project_path / "migrations" / "script.py.mako", script_py_content)
    
    def _generate_models(self, project_path: Path):
        """Generate SQLAlchemy models"""
        
        # Generate __init__.py for models
        model_imports = []
        
        for model in self.requirements.models:
            model_name = model['name']
            model_imports.append(f"from .{model_name.lower()} import {model_name}")
        
        init_content = f'''"""
Database Models
"""

{chr(10).join(model_imports)}

__all__ = [{', '.join([f'"{model["name"]}"' for model in self.requirements.models])}]
'''
        
        self._write_file(project_path / "app" / "models" / "__init__.py", init_content)
        
        # Generate individual model files
        for model in self.requirements.models:
            self._generate_model_file(project_path, model)
    
    def _generate_model_file(self, project_path: Path, model: Dict[str, Any]):
        """Generate individual model file"""
        
        model_name = model['name']
        model_name_lower = model_name.lower()
        fields = model['fields']
        
        # Import statements
        imports = [
            "from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Decimal, ForeignKey",
            "from sqlalchemy.orm import relationship",
            "from app.db.base import BaseModel"
        ]
        
        # Field definitions
        field_definitions = []
        relationships = []
        
        for field in fields:
            if field['name'] in ['id', 'created_at', 'updated_at']:
                continue  # These are in BaseModel
            
            field_def = self._generate_field_definition(field)
            if field_def:
                if 'relationship(' in field_def:
                    relationships.append(field_def)
                else:
                    field_definitions.append(field_def)
        
        # Add relationships from project requirements
        for rel in self.requirements.relationships:
            if rel.from_model == model_name:
                if rel.relationship_type == "one_to_many":
                    relationships.append(
                        f'    {rel.to_model.lower()}s = relationship("{rel.to_model}", back_populates="{rel.from_model.lower()}")'
                    )
            elif rel.to_model == model_name:
                if rel.relationship_type == "many_to_one":
                    relationships.append(
                        f'    {rel.from_model.lower()} = relationship("{rel.from_model}", back_populates="{rel.to_model.lower()}s")'
                    )
        
        content = f'''"""
{model_name} Model
"""

{chr(10).join(imports)}

class {model_name}(BaseModel):
    """
    {model_name} model
    
    {model.get('description', f'{model_name} entity')}
    """
    
    __tablename__ = "{model.get('table_name', f'{model_name_lower}s')}"
    
    # Fields
{chr(10).join(field_definitions)}
    
    # Relationships
{chr(10).join(relationships)}
    
    def __repr__(self):
        return f"<{model_name}(id={{self.id}})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {{
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }}
'''
        
        self._write_file(project_path / "app" / "models" / f"{model_name_lower}.py", content)
    
    def _generate_field_definition(self, field: Dict[str, Any]) -> str:
        """Generate SQLAlchemy field definition"""
        
        field_name = field['name']
        field_type = field['type']
        required = field.get('required', True)
        unique = field.get('unique', False)
        indexed = field.get('indexed', False)
        default = field.get('default')
        
        # Map field types to SQLAlchemy types
        type_mapping = {
            'string': 'String(255)',
            'text': 'Text',
            'integer': 'Integer',
            'decimal': 'Decimal(10, 2)',
            'boolean': 'Boolean',
            'datetime': 'DateTime',
            'date': 'Date',
            'time': 'Time',
            'email': 'String(255)',
            'url': 'String(500)'
        }
        
        sql_type = type_mapping.get(field_type, 'String(255)')
        
        # Build field definition
        field_parts = [f"Column({sql_type}"]
        
        if not required:
            field_parts.append("nullable=True")
        else:
            field_parts.append("nullable=False")
        
        if unique:
            field_parts.append("unique=True")
        
        if indexed:
            field_parts.append("index=True")
        
        if default is not None:
            if isinstance(default, str) and default != "now":
                field_parts.append(f'default="{default}"')
            elif default == "now":
                field_parts.append("server_default=func.now()")
            else:
                field_parts.append(f"default={default}")
        
        field_definition = f"    {field_name} = {', '.join(field_parts)})"
        
        return field_definition
    
    def _generate_schemas(self, project_path: Path):
        """Generate Pydantic schemas"""
        
        # Generate __init__.py for schemas
        schema_imports = []
        
        for model in self.requirements.models:
            model_name = model['name']
            schema_imports.extend([
                f"from .{model_name.lower()} import {model_name}Base, {model_name}Create, {model_name}Update, {model_name}Response"
            ])
        
        init_content = f'''"""
Pydantic Schemas
"""

{chr(10).join(schema_imports)}
'''
        
        self._write_file(project_path / "app" / "schemas" / "__init__.py", init_content)
        
        # Generate individual schema files
        for model in self.requirements.models:
            self._generate_schema_file(project_path, model)
    
    def _generate_schema_file(self, project_path: Path, model: Dict[str, Any]):
        """Generate individual schema file"""
        
        model_name = model['name']
        model_name_lower = model_name.lower()
        fields = model['fields']
        
        # Base schema fields (excluding id, created_at, updated_at)
        base_fields = []
        create_fields = []
        update_fields = []
        response_fields = []
        
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            required = field.get('required', True)
            default = field.get('default')
            
            # Skip auto-generated fields for base/create schemas
            if field_name in ['id', 'created_at', 'updated_at']:
                if field_name == 'id':
                    response_fields.append(f"    {field_name}: int")
                else:
                    response_fields.append(f"    {field_name}: datetime")
                continue
            
            # Map field types to Python types
            python_type = self._map_field_type_to_python(field_type)
            
            # Build field definition
            if required and default is None:
                field_def = f"    {field_name}: {python_type}"
            elif default is not None:
                if isinstance(default, str) and default != "now":
                    field_def = f"    {field_name}: {python_type} = '{default}'"
                elif isinstance(default, bool):
                    field_def = f"    {field_name}: {python_type} = {default}"
                else:
                    field_def = f"    {field_name}: {python_type} = {default}"
            else:
                field_def = f"    {field_name}: Optional[{python_type}] = None"
            
            base_fields.append(field_def)
            create_fields.append(field_def)
            
            # Update fields are all optional
            update_field_def = f"    {field_name}: Optional[{python_type}] = None"
            update_fields.append(update_field_def)
            
            # Response includes all fields
            response_fields.append(field_def)
        
        content = f'''"""
{model_name} Schemas
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field{"" if not any(f["type"] == "email" for f in fields) else ", EmailStr"}

class {model_name}Base(BaseModel):
    """Base {model_name} schema"""
{chr(10).join(base_fields) if base_fields else "    pass"}

class {model_name}Create({model_name}Base):
    """Schema for creating {model_name}"""
    pass

class {model_name}Update(BaseModel):
    """Schema for updating {model_name}"""
{chr(10).join(update_fields) if update_fields else "    pass"}

class {model_name}Response({model_name}Base):
    """Schema for {model_name} response"""
{chr(10).join(response_fields)}
    
    class Config:
        from_attributes = True

class {model_name}List(BaseModel):
    """Schema for {model_name} list response"""
    items: list[{model_name}Response]
    total: int
    page: int
    size: int
    pages: int
'''
        
        self._write_file(project_path / "app" / "schemas" / f"{model_name_lower}.py", content)
    
    def _map_field_type_to_python(self, field_type: str) -> str:
        """Map database field type to Python type"""
        
        type_mapping = {
            'string': 'str',
            'text': 'str',
            'integer': 'int',
            'decimal': 'float',
            'boolean': 'bool',
            'datetime': 'datetime',
            'date': 'date',
            'time': 'time',
            'email': 'EmailStr',
            'url': 'str'
        }
        
        return type_mapping.get(field_type, 'str')
    
    def _get_default_database_url(self) -> str:
        """Get default database URL based on database type"""
        
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            return "postgresql://user:password@localhost:5432/dbname"
        elif self.requirements.database_type == DatabaseType.MYSQL:
            return "mysql://user:password@localhost:3306/dbname"
        elif self.requirements.database_type == DatabaseType.SQLITE:
            return "sqlite:///./app.db"
        elif self.requirements.database_type == DatabaseType.MONGODB:
            return "mongodb://localhost:27017/dbname"
        else:
            return "sqlite:///./app.db"
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Generated file: {file_path}")

# Continue with remaining methods...
# (This is a partial implementation - the full class would continue with all the remaining methods)

if __name__ == "__main__":
    # Test the enhanced generator
    from nlp_extractor import NLPExtractor
    
    extractor = NLPExtractor()
    requirements = extractor.extract_requirements(
        "Create a modern blog platform with user authentication, post management, and real-time comments"
    )
    
    generator = FastAPIGenerator(requirements)
    project_path = generator.generate_complete_project("/tmp/test_enhanced_fastapi")
    
    print(f"Enhanced FastAPI project generated at: {project_path}")

