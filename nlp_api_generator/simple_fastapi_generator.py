"""
Simplified FastAPI Generator for Demo
Generates a working FastAPI project with core functionality
"""

import os
from typing import Dict, List, Any
from pathlib import Path
from nlp_extractor import ProjectRequirements, FrameworkType, AuthType, DatabaseType

class SimpleFastAPIGenerator:
    """Simplified FastAPI generator that creates working projects"""
    
    def __init__(self, requirements: ProjectRequirements):
        self.requirements = requirements
    
    def generate_complete_project(self, output_dir: str = ".") -> str:
        """Generate a complete FastAPI project"""
        
        # Create project directory
        project_path = Path(output_dir) / self.requirements.project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Generate all files
        self._generate_main_app(project_path)
        self._generate_models(project_path)
        self._generate_schemas(project_path)
        self._generate_routes(project_path)
        self._generate_database(project_path)
        self._generate_requirements(project_path)
        self._generate_readme(project_path)
        
        return str(project_path)
    
    def _generate_main_app(self, project_path: Path):
        """Generate main FastAPI application"""
        
        content = f'''"""
{self.requirements.project_name.replace('_', ' ').title()} API
{self.requirements.description}
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="{self.requirements.project_name.replace('_', ' ').title()} API",
    description="{self.requirements.description}",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {{
        "message": "Welcome to {self.requirements.project_name.replace('_', ' ').title()} API",
        "version": "1.0.0",
        "docs": "/docs"
    }}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
        
        self._write_file(project_path, "main.py", content)
    
    def _generate_models(self, project_path: Path):
        """Generate SQLAlchemy models"""
        
        content = '''"""
Database models
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

'''
        
        # Generate models
        for model in self.requirements.models:
            model_name = model['name']
            content += f'''
class {model_name}(Base):
    """
    {model_name} model
    """
    __tablename__ = "{model_name.lower()}s"
    
    id = Column(Integer, primary_key=True, index=True)
'''
            
            # Add fields
            for field in model['fields']:
                field_name = field['name']
                field_type = field['type']
                
                if field_name in ['id']:
                    continue
                
                if field_type == 'string':
                    content += f'    {field_name} = Column(String(255))\n'
                elif field_type == 'text':
                    content += f'    {field_name} = Column(Text)\n'
                elif field_type == 'integer':
                    content += f'    {field_name} = Column(Integer)\n'
                elif field_type == 'boolean':
                    content += f'    {field_name} = Column(Boolean, default=False)\n'
                elif field_type == 'datetime':
                    content += f'    {field_name} = Column(DateTime, default=datetime.utcnow)\n'
                elif field_type == 'email':
                    content += f'    {field_name} = Column(String(255))\n'
                else:
                    content += f'    {field_name} = Column(String(255))\n'
            
            content += f'''
    def __repr__(self):
        return f"<{model_name}(id={{self.id}})>"
'''
        
        self._write_file(project_path, "app/models.py", content)
    
    def _generate_schemas(self, project_path: Path):
        """Generate Pydantic schemas"""
        
        content = '''"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

'''
        
        # Generate schemas for each model
        for model in self.requirements.models:
            model_name = model['name']
            
            # Base schema
            content += f'''
class {model_name}Base(BaseModel):
    """Base {model_name} schema"""
'''
            
            # Add fields
            for field in model['fields']:
                field_name = field['name']
                field_type = field['type']
                
                if field_name in ['id', 'created_at', 'updated_at']:
                    continue
                
                if field_type == 'string':
                    content += f'    {field_name}: Optional[str] = None\n'
                elif field_type == 'text':
                    content += f'    {field_name}: Optional[str] = None\n'
                elif field_type == 'integer':
                    content += f'    {field_name}: Optional[int] = None\n'
                elif field_type == 'boolean':
                    content += f'    {field_name}: Optional[bool] = False\n'
                elif field_type == 'email':
                    content += f'    {field_name}: Optional[str] = None\n'
                else:
                    content += f'    {field_name}: Optional[str] = None\n'
            
            # Create and Update schemas
            content += f'''

class {model_name}Create({model_name}Base):
    """Schema for creating {model_name}"""
    pass

class {model_name}Update({model_name}Base):
    """Schema for updating {model_name}"""
    pass

class {model_name}Response({model_name}Base):
    """Schema for {model_name} response"""
    id: int
    
    class Config:
        from_attributes = True
'''
        
        self._write_file(project_path, "app/schemas.py", content)
    
    def _generate_routes(self, project_path: Path):
        """Generate API routes"""
        
        content = '''"""
API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import *
from app.schemas import *

router = APIRouter()

'''
        
        # Generate routes for each model
        for model in self.requirements.models:
            model_name = model['name']
            model_name_lower = model_name.lower()
            model_name_plural = f"{model_name_lower}s"
            
            content += f'''
# {model_name} routes
@router.get("/{model_name_plural}/", response_model=List[{model_name}Response])
async def list_{model_name_plural}(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all {model_name_plural}"""
    {model_name_plural} = db.query({model_name}).offset(skip).limit(limit).all()
    return {model_name_plural}

@router.post("/{model_name_plural}/", response_model={model_name}Response, status_code=status.HTTP_201_CREATED)
async def create_{model_name_lower}({model_name_lower}: {model_name}Create, db: Session = Depends(get_db)):
    """Create a new {model_name_lower}"""
    db_{model_name_lower} = {model_name}(**{model_name_lower}.dict())
    db.add(db_{model_name_lower})
    db.commit()
    db.refresh(db_{model_name_lower})
    return db_{model_name_lower}

@router.get("/{model_name_plural}/{{item_id}}", response_model={model_name}Response)
async def get_{model_name_lower}(item_id: int, db: Session = Depends(get_db)):
    """Get a specific {model_name_lower}"""
    {model_name_lower} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if {model_name_lower} is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return {model_name_lower}

@router.put("/{model_name_plural}/{{item_id}}", response_model={model_name}Response)
async def update_{model_name_lower}(item_id: int, {model_name_lower}: {model_name}Update, db: Session = Depends(get_db)):
    """Update a {model_name_lower}"""
    db_{model_name_lower} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if db_{model_name_lower} is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    for key, value in {model_name_lower}.dict(exclude_unset=True).items():
        setattr(db_{model_name_lower}, key, value)
    
    db.commit()
    db.refresh(db_{model_name_lower})
    return db_{model_name_lower}

@router.delete("/{model_name_plural}/{{item_id}}")
async def delete_{model_name_lower}(item_id: int, db: Session = Depends(get_db)):
    """Delete a {model_name_lower}"""
    {model_name_lower} = db.query({model_name}).filter({model_name}.id == item_id).first()
    if {model_name_lower} is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    
    db.delete({model_name_lower})
    db.commit()
    return {{"message": "{model_name} deleted successfully"}}
'''
        
        self._write_file(project_path, "app/routes.py", content)
    
    def _generate_database(self, project_path: Path):
        """Generate database configuration"""
        
        if self.requirements.database_type == DatabaseType.SQLITE:
            database_url = f"sqlite:///./{self.requirements.database_name}.db"
        elif self.requirements.database_type == DatabaseType.POSTGRESQL:
            database_url = f"postgresql://user:password@localhost/{self.requirements.database_name}"
        else:
            database_url = f"sqlite:///./{self.requirements.database_name}.db"
        
        content = f'''"""
Database configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Database URL
DATABASE_URL = "{database_url}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
        
        self._write_file(project_path, "app/database.py", content)
        
        # Create __init__.py
        self._write_file(project_path, "app/__init__.py", "")
    
    def _generate_requirements(self, project_path: Path):
        """Generate requirements.txt"""
        
        requirements = [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "sqlalchemy>=2.0.23",
            "pydantic>=2.5.0",
        ]
        
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            requirements.append("psycopg2-binary>=2.9.9")
        elif self.requirements.database_type == DatabaseType.MYSQL:
            requirements.append("pymysql>=1.1.0")
        
        if self.requirements.auth_type == AuthType.JWT:
            requirements.append("python-jose[cryptography]>=3.3.0")
            requirements.append("passlib[bcrypt]>=1.7.4")
        
        content = "\\n".join(requirements)
        self._write_file(project_path, "requirements.txt", content)
    
    def _generate_readme(self, project_path: Path):
        """Generate README.md"""
        
        content = f'''# {self.requirements.project_name.replace('_', ' ').title()}

{self.requirements.description}

## Features

- **Framework**: FastAPI
- **Database**: {self.requirements.database_type.value.title()}
- **Authentication**: {self.requirements.auth_type.value.replace('_', ' ').title()}

## Models

'''
        
        for model in self.requirements.models:
            content += f"- **{model['name']}**: {len(model['fields'])} fields\\n"
        
        content += f'''
## API Endpoints

### Resources
'''
        
        for model in self.requirements.models:
            model_name_plural = f"{model['name'].lower()}s"
            content += f'''
#### {model['name']}
- `GET /api/v1/{model_name_plural}/` - List {model_name_plural}
- `POST /api/v1/{model_name_plural}/` - Create {model['name'].lower()}
- `GET /api/v1/{model_name_plural}/{{id}}` - Get {model['name'].lower()}
- `PUT /api/v1/{model_name_plural}/{{id}}` - Update {model['name'].lower()}
- `DELETE /api/v1/{model_name_plural}/{{id}}` - Delete {model['name'].lower()}
'''
        
        content += f'''
## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

3. Open your browser:
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Usage

The API provides full CRUD operations for all models. Use the interactive documentation at `/docs` to explore and test the endpoints.

## Configuration

- Database URL can be configured in `app/database.py`
- Add environment variables for production settings
- Customize authentication in the routes as needed

## Development

This project was generated using the NLP-Powered API Generator. Customize the generated code to fit your specific requirements.
'''
        
        self._write_file(project_path, "README.md", content)
    
    def _write_file(self, project_path: Path, file_path: str, content: str):
        """Write content to file"""
        full_path = project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)

