"""
API Generator SDK - NLP Core Module
===================================

Refactored NLP processing capabilities for the SDK, providing clean
interfaces for requirement extraction and pattern matching.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .exceptions import NLPParsingError, ValidationError, ExtensionError

logger = logging.getLogger(__name__)

class FrameworkType(Enum):
    """Supported framework types"""
    FASTAPI = "fastapi"
    DJANGO = "django"
    AUTO = "auto"

class DatabaseType(Enum):
    """Supported database types"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    AUTO = "auto"

class AuthType(Enum):
    """Supported authentication types"""
    JWT = "jwt"
    SESSION = "session"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    NONE = "none"
    AUTO = "auto"

class APIType(Enum):
    """Supported API types"""
    REST = "rest"
    GRAPHQL = "graphql"
    HYBRID = "hybrid"
    AUTO = "auto"

@dataclass
class ModelField:
    """Represents a model field"""
    name: str
    type: str
    required: bool = True
    unique: bool = False
    indexed: bool = False
    default: Any = None
    description: str = ""

@dataclass
class ModelDefinition:
    """Represents a data model"""
    name: str
    fields: List[ModelField]
    description: str = ""
    table_name: Optional[str] = None

@dataclass
class Relationship:
    """Represents a model relationship"""
    from_model: str
    to_model: str
    relationship_type: str  # one_to_one, one_to_many, many_to_many
    field_name: Optional[str] = None

@dataclass
class EndpointDefinition:
    """Represents an API endpoint"""
    path: str
    method: str
    description: str
    model: Optional[str] = None
    auth_required: bool = True
    parameters: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ProjectRequirements:
    """Complete project requirements extracted from description"""
    
    # Basic project info
    project_name: str
    description: str
    
    # Framework and technology choices
    framework: FrameworkType = FrameworkType.AUTO
    database_type: DatabaseType = DatabaseType.AUTO
    auth_type: AuthType = AuthType.AUTO
    api_type: APIType = APIType.REST
    
    # Data models and relationships
    models: List[ModelDefinition] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    endpoints: List[EndpointDefinition] = field(default_factory=list)
    
    # Feature flags
    cors_enabled: bool = True
    rate_limiting: bool = False
    caching: bool = False
    use_redis: bool = False
    use_celery: bool = False
    file_uploads: bool = False
    real_time: bool = False
    background_tasks: bool = False
    
    # Quality and deployment
    include_tests: bool = True
    include_docs: bool = True
    docker_support: bool = True
    logging_level: str = "INFO"
    
    # Advanced features
    custom_business_logic: List[str] = field(default_factory=list)
    third_party_integrations: List[str] = field(default_factory=list)

class NLPPatternRegistry:
    """Registry for custom NLP patterns"""
    
    def __init__(self):
        self._patterns: Dict[str, Tuple[str, Callable]] = {}
        self._field_type_patterns: Dict[str, str] = {}
        self._framework_patterns: Dict[str, FrameworkType] = {}
        self._auth_patterns: Dict[str, AuthType] = {}
        self._database_patterns: Dict[str, DatabaseType] = {}
    
    def register_pattern(self, pattern_name: str, regex: str, mapping_function: Callable):
        """Register a custom NLP pattern"""
        try:
            # Validate regex
            re.compile(regex)
            self._patterns[pattern_name] = (regex, mapping_function)
            logger.info(f"Registered NLP pattern: {pattern_name}")
        except re.error as e:
            raise ExtensionError(f"Invalid regex pattern '{regex}': {e}")
    
    def register_field_type_pattern(self, pattern: str, field_type: str):
        """Register a field type detection pattern"""
        self._field_type_patterns[pattern] = field_type
    
    def register_framework_pattern(self, pattern: str, framework: FrameworkType):
        """Register a framework detection pattern"""
        self._framework_patterns[pattern] = framework
    
    def register_auth_pattern(self, pattern: str, auth_type: AuthType):
        """Register an authentication detection pattern"""
        self._auth_patterns[pattern] = auth_type
    
    def register_database_pattern(self, pattern: str, database_type: DatabaseType):
        """Register a database detection pattern"""
        self._database_patterns[pattern] = database_type
    
    def get_patterns(self) -> Dict[str, Tuple[str, Callable]]:
        """Get all registered patterns"""
        return self._patterns.copy()
    
    def get_field_type_patterns(self) -> Dict[str, str]:
        """Get field type patterns"""
        return self._field_type_patterns.copy()
    
    def get_framework_patterns(self) -> Dict[str, FrameworkType]:
        """Get framework patterns"""
        return self._framework_patterns.copy()
    
    def get_auth_patterns(self) -> Dict[str, AuthType]:
        """Get auth patterns"""
        return self._auth_patterns.copy()
    
    def get_database_patterns(self) -> Dict[str, DatabaseType]:
        """Get database patterns"""
        return self._database_patterns.copy()

class NLPCore:
    """
    Core NLP processing engine for extracting requirements from descriptions
    """
    
    def __init__(self, pattern_registry: Optional[NLPPatternRegistry] = None):
        """Initialize NLP core with optional custom patterns"""
        self.pattern_registry = pattern_registry or NLPPatternRegistry()
        self._setup_default_patterns()
        
        logger.info("NLP Core initialized")
    
    def _setup_default_patterns(self):
        """Setup default NLP patterns"""
        
        # Framework detection patterns
        framework_patterns = {
            r'\b(fastapi|fast\s*api)\b': FrameworkType.FASTAPI,
            r'\b(django|django\s*rest)\b': FrameworkType.DJANGO,
            r'\b(api|rest|restful)\b': FrameworkType.AUTO,
        }
        
        for pattern, framework in framework_patterns.items():
            self.pattern_registry.register_framework_pattern(pattern, framework)
        
        # Database detection patterns
        database_patterns = {
            r'\b(postgresql|postgres|pg)\b': DatabaseType.POSTGRESQL,
            r'\b(mysql|mariadb)\b': DatabaseType.MYSQL,
            r'\b(sqlite|sqlite3)\b': DatabaseType.SQLITE,
            r'\b(mongodb|mongo|nosql)\b': DatabaseType.MONGODB,
        }
        
        for pattern, database in database_patterns.items():
            self.pattern_registry.register_database_pattern(pattern, database)
        
        # Authentication detection patterns
        auth_patterns = {
            r'\b(jwt|json\s*web\s*token)\b': AuthType.JWT,
            r'\b(session|cookie)\b': AuthType.SESSION,
            r'\b(api\s*key|token)\b': AuthType.API_KEY,
            r'\b(oauth|oauth2|social\s*login)\b': AuthType.OAUTH2,
            r'\b(no\s*auth|public)\b': AuthType.NONE,
        }
        
        for pattern, auth in auth_patterns.items():
            self.pattern_registry.register_auth_pattern(pattern, auth)
        
        # Field type detection patterns
        field_type_patterns = {
            r'\b(email|mail)\b': 'email',
            r'\b(url|link|website)\b': 'url',
            r'\b(phone|telephone)\b': 'string',
            r'\b(password|pass)\b': 'string',
            r'\b(description|content|text|body)\b': 'text',
            r'\b(price|cost|amount|salary)\b': 'decimal',
            r'\b(count|quantity|number|age)\b': 'integer',
            r'\b(active|enabled|published|verified)\b': 'boolean',
            r'\b(date|created|updated|born)\b': 'datetime',
            r'\b(name|title|label)\b': 'string',
        }
        
        for pattern, field_type in field_type_patterns.items():
            self.pattern_registry.register_field_type_pattern(pattern, field_type)
    
    def extract_requirements(self, description: str) -> ProjectRequirements:
        """
        Extract project requirements from natural language description
        
        Args:
            description: Natural language project description
            
        Returns:
            ProjectRequirements object
            
        Raises:
            NLPParsingError: If parsing fails
            ValidationError: If description is invalid
        """
        
        if not description or not description.strip():
            raise ValidationError("Description cannot be empty")
        
        try:
            logger.info("Extracting requirements from description")
            
            # Clean and normalize description
            normalized_desc = self._normalize_description(description)
            
            # Extract basic project info
            project_name = self._extract_project_name(normalized_desc)
            
            # Detect framework, database, and auth preferences
            framework = self._detect_framework(normalized_desc)
            database_type = self._detect_database(normalized_desc)
            auth_type = self._detect_auth_type(normalized_desc)
            api_type = self._detect_api_type(normalized_desc)
            
            # Extract models and relationships
            models = self._extract_models(normalized_desc)
            relationships = self._extract_relationships(normalized_desc, models)
            
            # Extract endpoints
            endpoints = self._extract_endpoints(normalized_desc, models)
            
            # Detect features
            features = self._detect_features(normalized_desc)
            
            # Create requirements object
            requirements = ProjectRequirements(
                project_name=project_name,
                description=description,
                framework=framework,
                database_type=database_type,
                auth_type=auth_type,
                api_type=api_type,
                models=models,
                relationships=relationships,
                endpoints=endpoints,
                **features
            )
            
            logger.info(f"Successfully extracted requirements for project: {project_name}")
            return requirements
            
        except Exception as e:
            logger.error(f"Failed to extract requirements: {e}")
            raise NLPParsingError(f"Failed to parse description: {e}")
    
    def _normalize_description(self, description: str) -> str:
        """Normalize description for processing"""
        # Convert to lowercase and clean whitespace
        normalized = re.sub(r'\s+', ' ', description.lower().strip())
        return normalized
    
    def _extract_project_name(self, description: str) -> str:
        """Extract project name from description"""
        
        # Look for explicit project name patterns
        name_patterns = [
            r'(?:create|build|develop|make)\s+(?:a|an)?\s*([a-zA-Z][a-zA-Z0-9\s]{2,30}?)(?:\s+(?:api|system|platform|app|application|service))',
            r'(?:project|app|application|system)\s+(?:called|named)\s+([a-zA-Z][a-zA-Z0-9\s]{2,30})',
            r'^([a-zA-Z][a-zA-Z0-9\s]{2,30}?)(?:\s+(?:api|system|platform|app|application))',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean and format name
                name = re.sub(r'\s+', '_', name.lower())
                name = re.sub(r'[^a-z0-9_]', '', name)
                if name and len(name) >= 3:
                    return name
        
        # Fallback: extract key nouns
        nouns = re.findall(r'\b([a-zA-Z]{3,15})\b', description)
        if nouns:
            return f"{nouns[0].lower()}_api"
        
        return "generated_api"
    
    def _detect_framework(self, description: str) -> FrameworkType:
        """Detect preferred framework from description"""
        
        framework_patterns = self.pattern_registry.get_framework_patterns()
        
        for pattern, framework in framework_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                logger.debug(f"Detected framework: {framework}")
                return framework
        
        return FrameworkType.AUTO
    
    def _detect_database(self, description: str) -> DatabaseType:
        """Detect preferred database from description"""
        
        database_patterns = self.pattern_registry.get_database_patterns()
        
        for pattern, database in database_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                logger.debug(f"Detected database: {database}")
                return database
        
        return DatabaseType.AUTO
    
    def _detect_auth_type(self, description: str) -> AuthType:
        """Detect authentication type from description"""
        
        auth_patterns = self.pattern_registry.get_auth_patterns()
        
        for pattern, auth in auth_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                logger.debug(f"Detected auth type: {auth}")
                return auth
        
        # Default to JWT if authentication is mentioned
        if re.search(r'\b(auth|login|user|account)\b', description, re.IGNORECASE):
            return AuthType.AUTO
        
        return AuthType.AUTO
    
    def _detect_api_type(self, description: str) -> APIType:
        """Detect API type from description"""
        
        if re.search(r'\b(graphql|graph\s*ql)\b', description, re.IGNORECASE):
            return APIType.GRAPHQL
        elif re.search(r'\b(rest|restful)\b', description, re.IGNORECASE):
            return APIType.REST
        elif re.search(r'\b(hybrid|both|rest.*graphql|graphql.*rest)\b', description, re.IGNORECASE):
            return APIType.HYBRID
        
        return APIType.REST
    
    def _extract_models(self, description: str) -> List[ModelDefinition]:
        """Extract data models from description"""
        
        models = []
        
        # Entity extraction patterns
        entity_patterns = [
            r'\b(user|customer|client|account|person|member)s?\b',
            r'\b(product|item|good|merchandise)s?\b',
            r'\b(order|purchase|transaction|sale)s?\b',
            r'\b(post|article|blog|content|entry)s?\b',
            r'\b(comment|review|feedback|rating)s?\b',
            r'\b(category|tag|label|group)s?\b',
            r'\b(project|task|todo|assignment)s?\b',
            r'\b(team|organization|company|group)s?\b',
            r'\b(message|notification|alert)s?\b',
            r'\b(file|document|attachment|upload)s?\b',
        ]
        
        found_entities = set()
        
        for pattern in entity_patterns:
            matches = re.finditer(pattern, description, re.IGNORECASE)
            for match in matches:
                entity = match.group(1).lower()
                if entity not in found_entities:
                    found_entities.add(entity)
                    
                    # Generate fields for this entity
                    fields = self._generate_model_fields(entity, description)
                    
                    model = ModelDefinition(
                        name=entity.capitalize(),
                        fields=fields,
                        description=f"{entity.capitalize()} entity"
                    )
                    
                    models.append(model)
        
        # Ensure we have at least one model
        if not models:
            models.append(ModelDefinition(
                name="Item",
                fields=[
                    ModelField("name", "string", required=True),
                    ModelField("description", "text", required=False),
                ],
                description="Generic item entity"
            ))
        
        return models
    
    def _generate_model_fields(self, entity: str, description: str) -> List[ModelField]:
        """Generate fields for a model based on entity type and description"""
        
        fields = []
        field_type_patterns = self.pattern_registry.get_field_type_patterns()
        
        # Common fields for all entities
        common_fields = [
            ModelField("name", "string", required=True),
        ]
        
        # Entity-specific fields
        entity_fields = {
            'user': [
                ModelField("email", "email", required=True, unique=True),
                ModelField("password", "string", required=True),
                ModelField("first_name", "string", required=False),
                ModelField("last_name", "string", required=False),
                ModelField("is_active", "boolean", default=True),
            ],
            'product': [
                ModelField("description", "text", required=False),
                ModelField("price", "decimal", required=True),
                ModelField("quantity", "integer", default=0),
                ModelField("is_available", "boolean", default=True),
            ],
            'order': [
                ModelField("total_amount", "decimal", required=True),
                ModelField("status", "string", default="pending"),
                ModelField("order_date", "datetime", default="now"),
            ],
            'post': [
                ModelField("title", "string", required=True),
                ModelField("content", "text", required=True),
                ModelField("published", "boolean", default=False),
                ModelField("publish_date", "datetime", required=False),
            ],
            'comment': [
                ModelField("content", "text", required=True),
                ModelField("rating", "integer", required=False),
            ],
        }
        
        # Add common fields
        fields.extend(common_fields)
        
        # Add entity-specific fields
        if entity in entity_fields:
            fields.extend(entity_fields[entity])
        
        # Extract additional fields from description
        additional_fields = self._extract_additional_fields(entity, description, field_type_patterns)
        fields.extend(additional_fields)
        
        return fields
    
    def _extract_additional_fields(self, entity: str, description: str, field_type_patterns: Dict[str, str]) -> List[ModelField]:
        """Extract additional fields mentioned in description"""
        
        fields = []
        
        # Look for field mentions in context of the entity
        entity_context_pattern = rf'\b{entity}s?\b[^.]*?(?:with|has|have|including|contains?)\s+([^.]*)'
        
        matches = re.finditer(entity_context_pattern, description, re.IGNORECASE)
        for match in matches:
            context = match.group(1)
            
            # Extract potential field names
            field_candidates = re.findall(r'\b([a-zA-Z]{3,20})\b', context)
            
            for candidate in field_candidates:
                candidate_lower = candidate.lower()
                
                # Skip common words
                if candidate_lower in ['and', 'or', 'the', 'with', 'for', 'can', 'will', 'should']:
                    continue
                
                # Determine field type
                field_type = 'string'  # default
                for pattern, ftype in field_type_patterns.items():
                    if re.search(pattern, candidate_lower):
                        field_type = ftype
                        break
                
                # Check if field already exists
                existing_names = [f.name for f in fields]
                if candidate_lower not in existing_names:
                    fields.append(ModelField(
                        name=candidate_lower,
                        type=field_type,
                        required=False,
                        description=f"Additional {candidate_lower} field"
                    ))
        
        return fields
    
    def _extract_relationships(self, description: str, models: List[ModelDefinition]) -> List[Relationship]:
        """Extract relationships between models"""
        
        relationships = []
        
        if len(models) < 2:
            return relationships
        
        model_names = [model.name.lower() for model in models]
        
        # Common relationship patterns
        relationship_patterns = [
            (r'\b(\w+)s?\s+(?:belong\s+to|owned\s+by|created\s+by)\s+(\w+)s?\b', 'many_to_one'),
            (r'\b(\w+)s?\s+(?:has\s+many|contains?)\s+(\w+)s?\b', 'one_to_many'),
            (r'\b(\w+)s?\s+(?:has\s+one|contains?\s+one)\s+(\w+)s?\b', 'one_to_one'),
            (r'\b(\w+)s?\s+(?:and|with)\s+(\w+)s?\s+(?:are\s+)?(?:related|connected|linked)\b', 'many_to_many'),
        ]
        
        for pattern, rel_type in relationship_patterns:
            matches = re.finditer(pattern, description, re.IGNORECASE)
            for match in matches:
                from_model = match.group(1).lower()
                to_model = match.group(2).lower()
                
                # Check if both models exist
                if from_model in model_names and to_model in model_names:
                    relationships.append(Relationship(
                        from_model=from_model.capitalize(),
                        to_model=to_model.capitalize(),
                        relationship_type=rel_type
                    ))
        
        return relationships
    
    def _extract_endpoints(self, description: str, models: List[ModelDefinition]) -> List[EndpointDefinition]:
        """Extract API endpoints from description"""
        
        endpoints = []
        
        # Generate standard CRUD endpoints for each model
        for model in models:
            model_name_lower = model.name.lower()
            model_name_plural = f"{model_name_lower}s"
            
            # Standard CRUD endpoints
            crud_endpoints = [
                EndpointDefinition(
                    path=f"/{model_name_plural}",
                    method="GET",
                    description=f"List all {model_name_plural}",
                    model=model.name
                ),
                EndpointDefinition(
                    path=f"/{model_name_plural}",
                    method="POST",
                    description=f"Create a new {model_name_lower}",
                    model=model.name
                ),
                EndpointDefinition(
                    path=f"/{model_name_plural}/{{id}}",
                    method="GET",
                    description=f"Get a specific {model_name_lower}",
                    model=model.name
                ),
                EndpointDefinition(
                    path=f"/{model_name_plural}/{{id}}",
                    method="PUT",
                    description=f"Update a {model_name_lower}",
                    model=model.name
                ),
                EndpointDefinition(
                    path=f"/{model_name_plural}/{{id}}",
                    method="DELETE",
                    description=f"Delete a {model_name_lower}",
                    model=model.name
                ),
            ]
            
            endpoints.extend(crud_endpoints)
        
        # Extract custom endpoints from description
        custom_endpoints = self._extract_custom_endpoints(description)
        endpoints.extend(custom_endpoints)
        
        return endpoints
    
    def _extract_custom_endpoints(self, description: str) -> List[EndpointDefinition]:
        """Extract custom endpoints mentioned in description"""
        
        endpoints = []
        
        # Look for action patterns
        action_patterns = [
            r'\b(search|find|filter)\s+([a-zA-Z]+)s?\b',
            r'\b(login|authenticate|signin)\b',
            r'\b(logout|signout)\b',
            r'\b(register|signup|create\s+account)\b',
            r'\b(upload|download)\s+([a-zA-Z]+)s?\b',
            r'\b(export|import)\s+([a-zA-Z]+)s?\b',
        ]
        
        for pattern in action_patterns:
            matches = re.finditer(pattern, description, re.IGNORECASE)
            for match in matches:
                action = match.group(1).lower()
                target = match.group(2).lower() if len(match.groups()) > 1 else None
                
                if action in ['search', 'find', 'filter'] and target:
                    endpoints.append(EndpointDefinition(
                        path=f"/{target}s/search",
                        method="GET",
                        description=f"Search {target}s",
                        model=target.capitalize() if target else None
                    ))
                elif action in ['login', 'authenticate', 'signin']:
                    endpoints.append(EndpointDefinition(
                        path="/auth/login",
                        method="POST",
                        description="User login",
                        auth_required=False
                    ))
                elif action in ['logout', 'signout']:
                    endpoints.append(EndpointDefinition(
                        path="/auth/logout",
                        method="POST",
                        description="User logout"
                    ))
                elif action in ['register', 'signup']:
                    endpoints.append(EndpointDefinition(
                        path="/auth/register",
                        method="POST",
                        description="User registration",
                        auth_required=False
                    ))
        
        return endpoints
    
    def _detect_features(self, description: str) -> Dict[str, Any]:
        """Detect additional features from description"""
        
        features = {
            'cors_enabled': True,  # Default to enabled
            'rate_limiting': False,
            'caching': False,
            'use_redis': False,
            'use_celery': False,
            'file_uploads': False,
            'real_time': False,
            'background_tasks': False,
            'include_tests': True,
            'include_docs': True,
            'docker_support': True,
            'logging_level': 'INFO',
            'custom_business_logic': [],
            'third_party_integrations': [],
        }
        
        # Feature detection patterns
        feature_patterns = {
            'rate_limiting': r'\b(rate\s*limit|throttl|quota)\b',
            'caching': r'\b(cach|redis|memcach)\b',
            'use_redis': r'\b(redis|cache)\b',
            'use_celery': r'\b(celery|background\s*task|async\s*task|queue)\b',
            'file_uploads': r'\b(upload|file|image|document|attachment)\b',
            'real_time': r'\b(real\s*time|websocket|live|instant)\b',
            'background_tasks': r'\b(background|async|queue|task)\b',
        }
        
        for feature, pattern in feature_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                features[feature] = True
        
        # Extract integrations
        integration_patterns = [
            r'\b(stripe|payment)\b',
            r'\b(email|sendgrid|mailgun)\b',
            r'\b(aws|amazon|s3)\b',
            r'\b(google|firebase)\b',
            r'\b(facebook|social)\b',
        ]
        
        for pattern in integration_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            features['third_party_integrations'].extend(matches)
        
        return features
    
    def validate_requirements(self, requirements: ProjectRequirements) -> bool:
        """
        Validate extracted requirements
        
        Args:
            requirements: ProjectRequirements to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If requirements are invalid
        """
        
        if not requirements.project_name:
            raise ValidationError("Project name is required")
        
        if not requirements.description:
            raise ValidationError("Project description is required")
        
        if not requirements.models:
            raise ValidationError("At least one model is required")
        
        # Validate model names are unique
        model_names = [model.name for model in requirements.models]
        if len(model_names) != len(set(model_names)):
            raise ValidationError("Model names must be unique")
        
        # Validate field names within models
        for model in requirements.models:
            field_names = [field.name for field in model.fields]
            if len(field_names) != len(set(field_names)):
                raise ValidationError(f"Field names in model '{model.name}' must be unique")
        
        logger.info("Requirements validation passed")
        return True

