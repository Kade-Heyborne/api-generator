"""
API Generator SDK - Main Generator Interface
===========================================

Main API generation interface providing a clean, object-oriented API
for generating FastAPI and Django REST framework projects.
"""

import logging
from typing import Optional, Dict, Any, Callable, Type
from pathlib import Path

from .nlp_core import (
    NLPCore, 
    NLPPatternRegistry, 
    ProjectRequirements, 
    FrameworkType, 
    DatabaseType, 
    AuthType
)
from .fastapi_gen import FastAPIGenerator
from .django_gen import DjangoGenerator
from .exceptions import (
    GenerationError,
    InvalidDescriptionError,
    FrameworkNotSupportedError,
    DatabaseNotSupportedError,
    AuthMethodNotSupportedError,
    ConfigurationError,
    ExtensionError
)

logger = logging.getLogger(__name__)

class BaseGenerator:
    """Base class for framework generators"""
    
    def __init__(self, requirements: ProjectRequirements):
        self.requirements = requirements
    
    def generate_project(self, output_dir: str) -> str:
        """Generate project - to be implemented by subclasses"""
        raise NotImplementedError
    
    def register_template_override(self, template_key: str, new_template_content: str):
        """Register template override - to be implemented by subclasses"""
        raise NotImplementedError

class ApiGenerator:
    """
    Main API Generator class providing the primary interface for the SDK
    
    This class orchestrates the NLP parsing, project analysis, and code generation
    steps to create complete API projects from natural language descriptions.
    """
    
    def __init__(self):
        """Initialize the API Generator"""
        
        # Core components
        self.pattern_registry = NLPPatternRegistry()
        self.nlp_core = NLPCore(self.pattern_registry)
        
        # Configuration
        self.config = {
            'default_framework': FrameworkType.AUTO,
            'default_database': DatabaseType.AUTO,
            'default_auth_method': AuthType.AUTO,
            'default_output_dir': './generated_projects',
            'enable_validation': True,
            'enable_interactive_refinement': False,
        }
        
        # Extension registries
        self.framework_generators: Dict[FrameworkType, Type[BaseGenerator]] = {
            FrameworkType.FASTAPI: FastAPIGenerator,
            FrameworkType.DJANGO: DjangoGenerator,
        }
        
        self.template_overrides: Dict[str, str] = {}
        
        logger.info("API Generator initialized")
    
    def configure(self, **kwargs):
        """
        Configure the API Generator
        
        Args:
            default_framework: Default framework to use (fastapi, django, auto)
            default_database: Default database to use (postgresql, mysql, sqlite, mongodb, auto)
            default_auth_method: Default auth method (jwt, session, api_key, oauth2, none, auto)
            default_output_dir: Default output directory
            enable_validation: Enable input validation
            enable_interactive_refinement: Enable interactive refinement
        """
        
        for key, value in kwargs.items():
            if key in self.config:
                # Validate enum values
                if key == 'default_framework' and isinstance(value, str):
                    try:
                        value = FrameworkType(value.lower())
                    except ValueError:
                        raise ConfigurationError(f"Invalid framework: {value}")
                
                elif key == 'default_database' and isinstance(value, str):
                    try:
                        value = DatabaseType(value.lower())
                    except ValueError:
                        raise ConfigurationError(f"Invalid database: {value}")
                
                elif key == 'default_auth_method' and isinstance(value, str):
                    try:
                        value = AuthType(value.lower())
                    except ValueError:
                        raise ConfigurationError(f"Invalid auth method: {value}")
                
                self.config[key] = value
                logger.info(f"Configuration updated: {key} = {value}")
            else:
                logger.warning(f"Unknown configuration key: {key}")
    
    def generate_api(
        self,
        description: str,
        framework: Optional[str] = None,
        database: Optional[str] = None,
        auth_method: Optional[str] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate API project from natural language description
        
        Args:
            description: Natural language description of the API project
            framework: Framework to use (fastapi, django, auto)
            database: Database to use (postgresql, mysql, sqlite, mongodb, auto)
            auth_method: Authentication method (jwt, session, api_key, oauth2, none, auto)
            output_dir: Output directory for the generated project
            **kwargs: Additional configuration options
            
        Returns:
            Path to the generated project directory
            
        Raises:
            InvalidDescriptionError: If description is invalid
            FrameworkNotSupportedError: If framework is not supported
            DatabaseNotSupportedError: If database is not supported
            AuthMethodNotSupportedError: If auth method is not supported
            GenerationError: If generation fails
        """
        
        try:
            logger.info("Starting API generation process")
            
            # Validate inputs
            if self.config['enable_validation']:
                self._validate_inputs(description, framework, database, auth_method)
            
            # Extract requirements from description
            requirements = self.nlp_core.extract_requirements(description)
            
            # Override with explicit parameters
            if framework:
                try:
                    requirements.framework = FrameworkType(framework.lower())
                except ValueError:
                    raise FrameworkNotSupportedError(f"Unsupported framework: {framework}")
            
            if database:
                try:
                    requirements.database_type = DatabaseType(database.lower())
                except ValueError:
                    raise DatabaseNotSupportedError(f"Unsupported database: {database}")
            
            if auth_method:
                try:
                    requirements.auth_type = AuthType(auth_method.lower())
                except ValueError:
                    raise AuthMethodNotSupportedError(f"Unsupported auth method: {auth_method}")
            
            # Apply defaults for AUTO values
            requirements = self._apply_defaults(requirements)
            
            # Interactive refinement if enabled
            if self.config['enable_interactive_refinement']:
                requirements = self._interactive_refinement(requirements)
            
            # Validate final requirements
            if self.config['enable_validation']:
                self.nlp_core.validate_requirements(requirements)
            
            # Determine output directory
            if not output_dir:
                output_dir = self.config['default_output_dir']
            
            # Generate project
            project_path = self._generate_project(requirements, output_dir)
            
            logger.info(f"API generation completed successfully: {project_path}")
            return project_path
            
        except Exception as e:
            logger.error(f"API generation failed: {e}")
            if isinstance(e, (InvalidDescriptionError, FrameworkNotSupportedError, 
                            DatabaseNotSupportedError, AuthMethodNotSupportedError)):
                raise
            else:
                raise GenerationError(f"Generation failed: {e}")
    
    def register_nlp_pattern(self, pattern_name: str, regex: str, mapping_function: Callable):
        """
        Register a custom NLP pattern
        
        Args:
            pattern_name: Unique name for the pattern
            regex: Regular expression pattern
            mapping_function: Function to process matches
            
        Raises:
            ExtensionError: If pattern registration fails
        """
        
        try:
            self.pattern_registry.register_pattern(pattern_name, regex, mapping_function)
            logger.info(f"Registered NLP pattern: {pattern_name}")
        except Exception as e:
            raise ExtensionError(f"Failed to register NLP pattern '{pattern_name}': {e}")
    
    def register_framework_generator(self, framework_name: str, generator_class: Type[BaseGenerator]):
        """
        Register a custom framework generator
        
        Args:
            framework_name: Name of the framework
            generator_class: Generator class implementing BaseGenerator
            
        Raises:
            ExtensionError: If generator registration fails
        """
        
        try:
            # Validate generator class
            if not issubclass(generator_class, BaseGenerator):
                raise ExtensionError(f"Generator class must inherit from BaseGenerator")
            
            framework_type = FrameworkType(framework_name.lower())
            self.framework_generators[framework_type] = generator_class
            logger.info(f"Registered framework generator: {framework_name}")
            
        except ValueError:
            raise ExtensionError(f"Invalid framework name: {framework_name}")
        except Exception as e:
            raise ExtensionError(f"Failed to register framework generator '{framework_name}': {e}")
    
    def register_template_override(self, template_key: str, new_template_content: str):
        """
        Register a template override
        
        Args:
            template_key: Key identifying the template to override
            new_template_content: New template content
        """
        
        self.template_overrides[template_key] = new_template_content
        logger.info(f"Registered template override: {template_key}")
    
    def get_supported_frameworks(self) -> list:
        """Get list of supported frameworks"""
        return [framework.value for framework in self.framework_generators.keys()]
    
    def get_supported_databases(self) -> list:
        """Get list of supported databases"""
        return [db.value for db in DatabaseType if db != DatabaseType.AUTO]
    
    def get_supported_auth_methods(self) -> list:
        """Get list of supported authentication methods"""
        return [auth.value for auth in AuthType if auth != AuthType.AUTO]
    
    def _validate_inputs(self, description: str, framework: Optional[str], 
                        database: Optional[str], auth_method: Optional[str]):
        """Validate input parameters"""
        
        if not description or not description.strip():
            raise InvalidDescriptionError("Description cannot be empty")
        
        if len(description.strip()) < 10:
            raise InvalidDescriptionError("Description is too short (minimum 10 characters)")
        
        if framework and framework.lower() not in [f.value for f in FrameworkType]:
            raise FrameworkNotSupportedError(f"Unsupported framework: {framework}")
        
        if database and database.lower() not in [d.value for d in DatabaseType]:
            raise DatabaseNotSupportedError(f"Unsupported database: {database}")
        
        if auth_method and auth_method.lower() not in [a.value for a in AuthType]:
            raise AuthMethodNotSupportedError(f"Unsupported auth method: {auth_method}")
    
    def _apply_defaults(self, requirements: ProjectRequirements) -> ProjectRequirements:
        """Apply default values for AUTO settings"""
        
        # Framework selection logic
        if requirements.framework == FrameworkType.AUTO:
            if self.config['default_framework'] != FrameworkType.AUTO:
                requirements.framework = self.config['default_framework']
            else:
                # Smart framework selection based on requirements
                if (requirements.api_type == APIType.GRAPHQL or 
                    len(requirements.models) > 5 or
                    any(len(model.fields) > 10 for model in requirements.models)):
                    requirements.framework = FrameworkType.DJANGO
                else:
                    requirements.framework = FrameworkType.FASTAPI
        
        # Database selection logic
        if requirements.database_type == DatabaseType.AUTO:
            if self.config['default_database'] != DatabaseType.AUTO:
                requirements.database_type = self.config['default_database']
            else:
                # Smart database selection
                if len(requirements.models) > 3:
                    requirements.database_type = DatabaseType.POSTGRESQL
                else:
                    requirements.database_type = DatabaseType.SQLITE
        
        # Auth method selection logic
        if requirements.auth_type == AuthType.AUTO:
            if self.config['default_auth_method'] != AuthType.AUTO:
                requirements.auth_type = self.config['default_auth_method']
            else:
                # Smart auth selection
                has_user_model = any(model.name.lower() in ['user', 'account', 'customer'] 
                                   for model in requirements.models)
                if has_user_model:
                    requirements.auth_type = AuthType.JWT
                else:
                    requirements.auth_type = AuthType.NONE
        
        return requirements
    
    def _interactive_refinement(self, requirements: ProjectRequirements) -> ProjectRequirements:
        """Interactive refinement of requirements (placeholder for future implementation)"""
        
        # This would implement interactive prompts to refine requirements
        # For now, just return the requirements as-is
        logger.info("Interactive refinement is not yet implemented")
        return requirements
    
    def _generate_project(self, requirements: ProjectRequirements, output_dir: str) -> str:
        """Generate the actual project using the appropriate generator"""
        
        # Get the appropriate generator
        if requirements.framework not in self.framework_generators:
            raise FrameworkNotSupportedError(f"No generator available for framework: {requirements.framework}")
        
        generator_class = self.framework_generators[requirements.framework]
        generator = generator_class(requirements)
        
        # Apply template overrides
        for template_key, template_content in self.template_overrides.items():
            if hasattr(generator, 'register_template_override'):
                generator.register_template_override(template_key, template_content)
        
        # Generate the project
        project_path = generator.generate_project(output_dir)
        
        return project_path

# Convenience functions for direct usage
def generate_fastapi_project(description: str, output_dir: str = "./generated_projects") -> str:
    """
    Convenience function to generate a FastAPI project
    
    Args:
        description: Natural language description
        output_dir: Output directory
        
    Returns:
        Path to generated project
    """
    
    generator = ApiGenerator()
    return generator.generate_api(description, framework="fastapi", output_dir=output_dir)

def generate_django_project(description: str, output_dir: str = "./generated_projects") -> str:
    """
    Convenience function to generate a Django project
    
    Args:
        description: Natural language description
        output_dir: Output directory
        
    Returns:
        Path to generated project
    """
    
    generator = ApiGenerator()
    return generator.generate_api(description, framework="django", output_dir=output_dir)

