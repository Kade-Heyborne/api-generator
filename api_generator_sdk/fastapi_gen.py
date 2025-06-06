"""
API Generator SDK - FastAPI Generator Module
===========================================

Refactored FastAPI code generation capabilities for the SDK.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .nlp_core import ProjectRequirements, FrameworkType, DatabaseType, AuthType, APIType
from .exceptions import CodeGenerationError, TemplateError

logger = logging.getLogger(__name__)

class FastAPIGenerator:
    """
    FastAPI code generator for the SDK
    """
    
    def __init__(self, requirements: ProjectRequirements):
        """Initialize FastAPI generator"""
        self.requirements = requirements
        self.template_overrides: Dict[str, str] = {}
        
        logger.info("FastAPI Generator initialized")
    
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
        Generate FastAPI project
        
        Args:
            output_dir: Output directory for the project
            
        Returns:
            Path to the generated project
            
        Raises:
            CodeGenerationError: If generation fails
        """
        
        try:
            logger.info(f"Generating FastAPI project in {output_dir}")
            
            # Create project directory
            project_path = Path(output_dir) / self.requirements.project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Generate project structure
            self._create_directory_structure(project_path)
            
            # Generate core files
            self._generate_main_app(project_path)
            self._generate_config(project_path)
            self._generate_database(project_path)
            
            # Generate models and schemas
            self._generate_models(project_path)
            self._generate_schemas(project_path)
            
            # Generate API routes
            self._generate_routes(project_path)
            
            # Generate authentication if needed
            if self.requirements.auth_type != AuthType.NONE:
                self._generate_auth(project_path)
            
            # Generate additional features
            self._generate_additional_features(project_path)
            
            # Generate project files
            self._generate_project_files(project_path)
            
            logger.info(f"FastAPI project generated successfully at {project_path}")
            return str(project_path)
            
        except Exception as e:
            logger.error(f"Failed to generate FastAPI project: {e}")
            raise CodeGenerationError(f"FastAPI generation failed: {e}")
    
    def _create_directory_structure(self, project_path: Path):
        """Create project directory structure"""
        
        directories = [
            "app",
            "app/api",
            "app/api/v1",
            "app/core",
            "app/db",
            "app/models",
            "app/schemas",
            "app/crud",
            "tests",
            "docs",
        ]
        
        for directory in directories:
            (project_path / directory).mkdir(parents=True, exist_ok=True)
            # Create __init__.py files
            if directory.startswith("app"):
                (project_path / directory / "__init__.py").touch()
    
    def _generate_main_app(self, project_path: Path):
        """Generate main FastAPI application"""
        
        template_key = "main_app"
        if template_key in self.template_overrides:
            content = self.template_overrides[template_key]
        else:
            content = self._get_main_app_template()
        
        self._write_file(project_path / "main.py", content)
        self._write_file(project_path / "app" / "main.py", self._get_app_factory_template())
    
    def _get_main_app_template(self) -> str:
        """Get main application template"""
        
        return f'''"""
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
    
    def _get_app_factory_template(self) -> str:
        """Get app factory template"""
        
        cors_import = "from fastapi.middleware.cors import CORSMiddleware" if self.requirements.cors_enabled else ""
        
        return f'''"""
FastAPI Application Factory
"""

from fastapi import FastAPI
{cors_import}

from app.core.config import get_settings
from app.api.v1.router import api_router
from app.db.database import engine, Base

settings = get_settings()

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="{self.requirements.project_name.replace('_', ' ').title()} API",
        description="{self.requirements.description}",
        version="1.0.0",
    )
    
    # Setup middleware
    {"setup_middleware(app)" if self.requirements.cors_enabled else ""}
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    return app

{"def setup_middleware(app: FastAPI):" if self.requirements.cors_enabled else ""}
{'''    """Setup application middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )''' if self.requirements.cors_enabled else ""}
'''
    
    def _generate_config(self, project_path: Path):
        """Generate configuration files"""
        
        config_content = f'''"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    app_name: str = "{self.requirements.project_name.replace('_', ' ').title()} API"
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"
    
    # Database
    database_url: str = "{self._get_database_url()}"
    
    {"# JWT settings" if self.requirements.auth_type == AuthType.JWT else ""}
    {"access_token_expire_minutes: int = 30" if self.requirements.auth_type == AuthType.JWT else ""}
    {"algorithm: str = 'HS256'" if self.requirements.auth_type == AuthType.JWT else ""}
    
    class Config:
        env_file = ".env"

_settings = None

def get_settings() -> Settings:
    """Get application settings"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
'''
        
        self._write_file(project_path / "app" / "core" / "config.py", config_content)
    
    def _generate_database(self, project_path: Path):
        """Generate database configuration"""
        
        if self.requirements.database_type == DatabaseType.MONGODB:
            db_content = '''"""
MongoDB Database Configuration
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    return db.client

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.database_url)

async def close_mongo_connection():
    db.client.close()
'''
        else:
            db_content = f'''"""
SQLAlchemy Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        
        self._write_file(project_path / "app" / "db" / "database.py", db_content)
    
    def _generate_models(self, project_path: Path):
        """Generate SQLAlchemy models"""
        
        # Generate __init__.py
        model_imports = []
        for model in self.requirements.models:
            model_imports.append(f"from .{model.name.lower()} import {model.name}")
        
        init_content = f'''"""
Database Models
"""

{chr(10).join(model_imports)}
'''
        
        self._write_file(project_path / "app" / "models" / "__init__.py", init_content)
        
        # Generate individual model files
        for model in self.requirements.models:
            self._generate_model_file(project_path, model)
    
    def _generate_model_file(self, project_path: Path, model):
        """Generate individual model file"""
        
        model_name = model.name
        model_name_lower = model_name.lower()
        
        # Generate field definitions
        field_definitions = []
        for field in model.fields:
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            
            field_def = self._generate_field_definition(field)
            if field_def:
                field_definitions.append(field_def)
        
        content = f'''"""
{model_name} Model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Decimal, func
from app.db.database import Base

class {model_name}(Base):
    """
    {model_name} model
    """
    
    __tablename__ = "{model_name_lower}s"
    
    id = Column(Integer, primary_key=True, index=True)
{chr(10).join(field_definitions)}
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<{model_name}(id={{self.id}})>"
'''
        
        self._write_file(project_path / "app" / "models" / f"{model_name_lower}.py", content)
    
    def _generate_field_definition(self, field) -> str:
        """Generate SQLAlchemy field definition"""
        
        type_mapping = {
            'string': 'String(255)',
            'text': 'Text',
            'integer': 'Integer',
            'decimal': 'Decimal(10, 2)',
            'boolean': 'Boolean',
            'datetime': 'DateTime',
            'email': 'String(255)',
            'url': 'String(500)'
        }
        
        sql_type = type_mapping.get(field.type, 'String(255)')
        nullable = "nullable=False" if field.required else "nullable=True"
        unique = ", unique=True" if field.unique else ""
        index = ", index=True" if field.indexed else ""
        
        return f"    {field.name} = Column({sql_type}, {nullable}{unique}{index})"
    
    def _generate_schemas(self, project_path: Path):
        """Generate Pydantic schemas"""
        
        # Generate __init__.py
        schema_imports = []
        for model in self.requirements.models:
            model_name = model.name
            schema_imports.append(f"from .{model_name.lower()} import {model_name}Base, {model_name}Create, {model_name}Update, {model_name}Response")
        
        init_content = f'''"""
Pydantic Schemas
"""

{chr(10).join(schema_imports)}
'''
        
        self._write_file(project_path / "app" / "schemas" / "__init__.py", init_content)
        
        # Generate individual schema files
        for model in self.requirements.models:
            self._generate_schema_file(project_path, model)
    
    def _generate_schema_file(self, project_path: Path, model):
        """Generate individual schema file"""
        
        model_name = model.name
        
        # Generate field definitions for schemas
        base_fields = []
        for field in model.fields:
            if field.name in ['id', 'created_at', 'updated_at']:
                continue
            
            python_type = self._map_field_type_to_python(field.type)
            if field.required:
                base_fields.append(f"    {field.name}: {python_type}")
            else:
                base_fields.append(f"    {field.name}: Optional[{python_type}] = None")
        
        content = f'''"""
{model_name} Schemas
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class {model_name}Base(BaseModel):
    """Base {model_name} schema"""
{chr(10).join(base_fields) if base_fields else "    pass"}

class {model_name}Create({model_name}Base):
    """Schema for creating {model_name}"""
    pass

class {model_name}Update(BaseModel):
    """Schema for updating {model_name}"""
{chr(10).join([f"    {field.name}: Optional[{self._map_field_type_to_python(field.type)}] = None" for field in model.fields if field.name not in ['id', 'created_at', 'updated_at']]) if model.fields else "    pass"}

class {model_name}Response({model_name}Base):
    """Schema for {model_name} response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
'''
        
        self._write_file(project_path / "app" / "schemas" / f"{model_name.lower()}.py", content)
    
    def _generate_routes(self, project_path: Path):
        """Generate API routes"""
        
        # Generate main router
        router_imports = []
        router_includes = []
        
        for model in self.requirements.models:
            model_name_lower = model.name.lower()
            router_imports.append(f"from .{model_name_lower} import router as {model_name_lower}_router")
            router_includes.append(f'api_router.include_router({model_name_lower}_router, prefix="/{model_name_lower}s", tags=["{model.name}s"])')
        
        main_router_content = f'''"""
API Router
"""

from fastapi import APIRouter

{chr(10).join(router_imports)}

api_router = APIRouter()

{chr(10).join(router_includes)}
'''
        
        self._write_file(project_path / "app" / "api" / "v1" / "router.py", main_router_content)
        
        # Generate individual route files
        for model in self.requirements.models:
            self._generate_route_file(project_path, model)
    
    def _generate_route_file(self, project_path: Path, model):
        """Generate individual route file"""
        
        model_name = model.name
        model_name_lower = model_name.lower()
        
        content = f'''"""
{model_name} Routes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.{model_name_lower} import {model_name}
from app.schemas.{model_name_lower} import {model_name}Create, {model_name}Update, {model_name}Response

router = APIRouter()

@router.get("/", response_model=List[{model_name}Response])
def get_{model_name_lower}s(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all {model_name_lower}s"""
    {model_name_lower}s = db.query({model_name}).offset(skip).limit(limit).all()
    return {model_name_lower}s

@router.post("/", response_model={model_name}Response, status_code=status.HTTP_201_CREATED)
def create_{model_name_lower}({model_name_lower}_data: {model_name}Create, db: Session = Depends(get_db)):
    """Create a new {model_name_lower}"""
    {model_name_lower} = {model_name}(**{model_name_lower}_data.dict())
    db.add({model_name_lower})
    db.commit()
    db.refresh({model_name_lower})
    return {model_name_lower}

@router.get("/{{id}}", response_model={model_name}Response)
def get_{model_name_lower}(id: int, db: Session = Depends(get_db)):
    """Get a specific {model_name_lower}"""
    {model_name_lower} = db.query({model_name}).filter({model_name}.id == id).first()
    if not {model_name_lower}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return {model_name_lower}

@router.put("/{{id}}", response_model={model_name}Response)
def update_{model_name_lower}(id: int, {model_name_lower}_data: {model_name}Update, db: Session = Depends(get_db)):
    """Update a {model_name_lower}"""
    {model_name_lower} = db.query({model_name}).filter({model_name}.id == id).first()
    if not {model_name_lower}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    for field, value in {model_name_lower}_data.dict(exclude_unset=True).items():
        setattr({model_name_lower}, field, value)
    
    db.commit()
    db.refresh({model_name_lower})
    return {model_name_lower}

@router.delete("/{{id}}", status_code=status.HTTP_204_NO_CONTENT)
def delete_{model_name_lower}(id: int, db: Session = Depends(get_db)):
    """Delete a {model_name_lower}"""
    {model_name_lower} = db.query({model_name}).filter({model_name}.id == id).first()
    if not {model_name_lower}:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    db.delete({model_name_lower})
    db.commit()
'''
        
        self._write_file(project_path / "app" / "api" / "v1" / f"{model_name_lower}.py", content)
    
    def _generate_auth(self, project_path: Path):
        """Generate authentication system"""
        
        if self.requirements.auth_type == AuthType.JWT:
            auth_content = '''"""
JWT Authentication
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
'''
            
            self._write_file(project_path / "app" / "core" / "auth.py", auth_content)
    
    def _generate_additional_features(self, project_path: Path):
        """Generate additional features based on requirements"""
        
        # Generate health check endpoint
        health_content = '''"""
Health Check Endpoint
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}
'''
        
        self._write_file(project_path / "app" / "api" / "v1" / "health.py", health_content)
    
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
2. Start the server: `python main.py`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Models

{chr(10).join([f"- {model.name}: {model.description}" for model in self.requirements.models])}
'''
        
        self._write_file(project_path / "README.md", readme_content)
        
        # .env.example
        env_content = f'''# FastAPI Settings
DEBUG=true
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL={self._get_database_url()}

# JWT (if using JWT auth)
{"ACCESS_TOKEN_EXPIRE_MINUTES=30" if self.requirements.auth_type == AuthType.JWT else ""}
{"ALGORITHM=HS256" if self.requirements.auth_type == AuthType.JWT else ""}
'''
        
        self._write_file(project_path / ".env.example", env_content)
    
    def _get_requirements(self) -> List[str]:
        """Get Python requirements"""
        
        requirements = [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.5.0",
            "pydantic-settings>=2.1.0",
        ]
        
        # Database requirements
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            requirements.extend(["sqlalchemy>=2.0.23", "psycopg2-binary>=2.9.9"])
        elif self.requirements.database_type == DatabaseType.MYSQL:
            requirements.extend(["sqlalchemy>=2.0.23", "pymysql>=1.1.0"])
        elif self.requirements.database_type == DatabaseType.SQLITE:
            requirements.append("sqlalchemy>=2.0.23")
        elif self.requirements.database_type == DatabaseType.MONGODB:
            requirements.extend(["motor>=3.3.2", "beanie>=1.23.6"])
        else:
            requirements.append("sqlalchemy>=2.0.23")
        
        # Authentication requirements
        if self.requirements.auth_type == AuthType.JWT:
            requirements.extend(["python-jose[cryptography]>=3.3.0", "passlib[bcrypt]>=1.7.4"])
        
        # Additional features
        if self.requirements.cors_enabled:
            requirements.append("python-multipart>=0.0.6")
        
        return requirements
    
    def _get_database_url(self) -> str:
        """Get database URL"""
        
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
    
    def _map_field_type_to_python(self, field_type: str) -> str:
        """Map field type to Python type"""
        
        type_mapping = {
            'string': 'str',
            'text': 'str',
            'integer': 'int',
            'decimal': 'float',
            'boolean': 'bool',
            'datetime': 'datetime',
            'email': 'str',
            'url': 'str'
        }
        
        return type_mapping.get(field_type, 'str')
    
    def _write_file(self, file_path: Path, content: str):
        """Write content to file"""
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Generated file: {file_path}")

