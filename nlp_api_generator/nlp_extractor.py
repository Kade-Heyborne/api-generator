"""
Enhanced NLP Requirement Extractor
==================================

Advanced natural language processing engine with improved accuracy,
contextual understanding, feedback loops, and multi-language support.

Features:
- Enhanced business logic inference
- Interactive refinement system
- Validation and error reporting
- Learning from user feedback
- Support for complex conditional logic
- Multi-language pattern support
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# Enhanced logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrameworkType(Enum):
    FASTAPI = "fastapi"
    DJANGO = "django"
    GRAPHQL_FASTAPI = "graphql_fastapi"
    GRAPHQL_DJANGO = "graphql_django"

class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    DYNAMODB = "dynamodb"
    FIRESTORE = "firestore"

class AuthType(Enum):
    JWT = "jwt"
    SESSION = "session"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    NONE = "none"

class APIType(Enum):
    REST = "rest"
    GRAPHQL = "graphql"
    HYBRID = "hybrid"

@dataclass
class ValidationError:
    """Represents a validation error with context"""
    field: str
    message: str
    suggestion: Optional[str] = None
    severity: str = "error"  # error, warning, info

@dataclass
class BusinessRule:
    """Represents extracted business logic rules"""
    condition: str
    action: str
    priority: int = 1
    context: str = ""

@dataclass
class ModelField:
    """Enhanced model field representation"""
    name: str
    type: str
    required: bool = True
    unique: bool = False
    indexed: bool = False
    default: Optional[Any] = None
    validation_rules: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class ModelRelationship:
    """Represents relationships between models"""
    from_model: str
    to_model: str
    relationship_type: str  # one_to_one, one_to_many, many_to_many
    foreign_key: Optional[str] = None
    related_name: Optional[str] = None

@dataclass
class ProjectRequirements:
    """Enhanced project requirements with validation and feedback"""
    project_name: str
    description: str
    framework: FrameworkType
    api_type: APIType = APIType.REST
    database_type: DatabaseType = DatabaseType.SQLITE
    auth_type: AuthType = AuthType.NONE
    models: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[ModelRelationship] = field(default_factory=list)
    business_rules: List[BusinessRule] = field(default_factory=list)
    
    # Enhanced configuration options
    cors_enabled: bool = True
    rate_limiting: bool = False
    caching: bool = False
    file_uploads: bool = False
    real_time: bool = False
    background_tasks: bool = False
    
    # Advanced features
    use_celery: bool = False
    use_redis: bool = False
    use_elasticsearch: bool = False
    containerize: bool = True
    include_tests: bool = True
    include_docs: bool = True
    
    # Quality and deployment
    logging_level: str = "INFO"
    environment_configs: List[str] = field(default_factory=lambda: ["development", "staging", "production"])
    
    # Validation and feedback
    validation_errors: List[ValidationError] = field(default_factory=list)
    confidence_score: float = 0.0
    needs_clarification: List[str] = field(default_factory=list)

class NLPExtractor:
    """
    Enhanced NLP requirement extractor with improved accuracy and feedback capabilities
    """
    
    def __init__(self):
        """Initialize the enhanced NLP extractor"""
        self.patterns = self._load_patterns()
        self.business_logic_patterns = self._load_business_logic_patterns()
        self.validation_rules = self._load_validation_rules()
        self.feedback_data = self._load_feedback_data()
        
        logger.info("Enhanced NLP Extractor initialized with advanced patterns")
    
    def extract_requirements(self, description: str, language: str = "en") -> ProjectRequirements:
        """
        Extract requirements with enhanced accuracy and validation
        
        Args:
            description: Natural language description
            language: Language code (en, es, fr, de, etc.)
            
        Returns:
            Enhanced ProjectRequirements with validation and confidence scoring
        """
        
        logger.info(f"Extracting requirements from description (language: {language})")
        
        # Step 1: Validate input description
        validation_errors = self._validate_description(description)
        
        # Step 2: Preprocess text based on language
        processed_text = self._preprocess_text(description, language)
        
        # Step 3: Extract basic requirements
        requirements = self._extract_basic_requirements(processed_text)
        
        # Step 4: Enhanced entity extraction
        models, relationships = self._extract_enhanced_entities(processed_text)
        requirements.models = models
        requirements.relationships = relationships
        
        # Step 5: Extract business logic and rules
        requirements.business_rules = self._extract_business_logic(processed_text)
        
        # Step 6: Determine advanced features
        self._determine_advanced_features(requirements, processed_text)
        
        # Step 7: Calculate confidence score
        requirements.confidence_score = self._calculate_confidence_score(requirements, processed_text)
        
        # Step 8: Identify clarification needs
        requirements.needs_clarification = self._identify_clarification_needs(requirements, processed_text)
        
        # Step 9: Add validation errors
        requirements.validation_errors = validation_errors
        
        logger.info(f"Requirements extracted with confidence: {requirements.confidence_score:.2f}")
        
        return requirements
    
    def refine_requirements(self, requirements: ProjectRequirements, 
                          user_feedback: Dict[str, Any]) -> ProjectRequirements:
        """
        Refine requirements based on user feedback
        
        Args:
            requirements: Initial requirements
            user_feedback: User corrections and clarifications
            
        Returns:
            Refined requirements
        """
        
        logger.info("Refining requirements based on user feedback")
        
        # Apply user corrections
        if "models" in user_feedback:
            requirements.models = self._apply_model_corrections(
                requirements.models, user_feedback["models"]
            )
        
        if "framework" in user_feedback:
            requirements.framework = FrameworkType(user_feedback["framework"])
        
        if "database" in user_feedback:
            requirements.database_type = DatabaseType(user_feedback["database"])
        
        if "auth" in user_feedback:
            requirements.auth_type = AuthType(user_feedback["auth"])
        
        # Store feedback for learning
        self._store_feedback(requirements, user_feedback)
        
        # Recalculate confidence
        requirements.confidence_score = min(requirements.confidence_score + 0.2, 1.0)
        requirements.needs_clarification = []
        
        return requirements
    
    def _validate_description(self, description: str) -> List[ValidationError]:
        """Validate the input description for common issues"""
        
        errors = []
        
        if len(description.strip()) < 10:
            errors.append(ValidationError(
                field="description",
                message="Description is too short",
                suggestion="Please provide more details about your API requirements",
                severity="error"
            ))
        
        if len(description.strip()) > 5000:
            errors.append(ValidationError(
                field="description",
                message="Description is very long",
                suggestion="Consider breaking down into smaller, focused descriptions",
                severity="warning"
            ))
        
        # Check for contradictory requirements
        if "no authentication" in description.lower() and "user" in description.lower():
            errors.append(ValidationError(
                field="authentication",
                message="Contradictory authentication requirements detected",
                suggestion="Clarify whether user management requires authentication",
                severity="warning"
            ))
        
        # Check for ambiguous database requirements
        db_mentions = sum(1 for db in ["postgresql", "mysql", "sqlite", "mongodb"] 
                         if db in description.lower())
        if db_mentions > 1:
            errors.append(ValidationError(
                field="database",
                message="Multiple database types mentioned",
                suggestion="Please specify which database you prefer",
                severity="warning"
            ))
        
        return errors
    
    def _preprocess_text(self, text: str, language: str) -> str:
        """Enhanced text preprocessing with language support"""
        
        # Basic cleaning
        text = text.strip().lower()
        
        # Language-specific preprocessing
        if language == "es":  # Spanish
            text = self._preprocess_spanish(text)
        elif language == "fr":  # French
            text = self._preprocess_french(text)
        elif language == "de":  # German
            text = self._preprocess_german(text)
        
        # Normalize common variations
        text = re.sub(r'\b(api|rest api|restful api)\b', 'api', text)
        text = re.sub(r'\b(database|db|data store)\b', 'database', text)
        text = re.sub(r'\b(authentication|auth|login)\b', 'authentication', text)
        
        return text
    
    def _preprocess_spanish(self, text: str) -> str:
        """Spanish-specific preprocessing"""
        translations = {
            "crear": "create",
            "construir": "build",
            "diseñar": "design",
            "usuario": "user",
            "autenticación": "authentication",
            "base de datos": "database",
            "api": "api"
        }
        
        for spanish, english in translations.items():
            text = text.replace(spanish, english)
        
        return text
    
    def _preprocess_french(self, text: str) -> str:
        """French-specific preprocessing"""
        translations = {
            "créer": "create",
            "construire": "build",
            "concevoir": "design",
            "utilisateur": "user",
            "authentification": "authentication",
            "base de données": "database",
            "api": "api"
        }
        
        for french, english in translations.items():
            text = text.replace(french, english)
        
        return text
    
    def _preprocess_german(self, text: str) -> str:
        """German-specific preprocessing"""
        translations = {
            "erstellen": "create",
            "bauen": "build",
            "entwerfen": "design",
            "benutzer": "user",
            "authentifizierung": "authentication",
            "datenbank": "database",
            "api": "api"
        }
        
        for german, english in translations.items():
            text = text.replace(german, english)
        
        return text
    
    def _extract_basic_requirements(self, text: str) -> ProjectRequirements:
        """Extract basic project requirements"""
        
        # Extract project name
        project_name = self._extract_project_name(text)
        
        # Determine framework and API type
        framework, api_type = self._determine_framework_and_api_type(text)
        
        # Determine database type
        database_type = self._determine_database_type(text)
        
        # Determine authentication type
        auth_type = self._determine_auth_type(text)
        
        return ProjectRequirements(
            project_name=project_name,
            description=text,
            framework=framework,
            api_type=api_type,
            database_type=database_type,
            auth_type=auth_type
        )
    
    def _extract_enhanced_entities(self, text: str) -> Tuple[List[Dict[str, Any]], List[ModelRelationship]]:
        """Enhanced entity extraction with better relationship detection"""
        
        models = []
        relationships = []
        
        # Enhanced model detection patterns
        model_patterns = [
            r'\b(?:create|build|design|manage|track|store)\s+(?:a\s+)?(\w+)\s+(?:model|entity|table|collection)',
            r'\b(\w+)s?\s+(?:with|having|containing|include|consist\s+of)\s+',
            r'\b(?:each|every)\s+(\w+)\s+(?:has|contains|includes)',
            r'\b(\w+)\s+(?:management|system|module|service)',
            r'\b(?:list|show|display)\s+(?:all\s+)?(\w+)s?\b',
        ]
        
        detected_entities = set()
        
        for pattern in model_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entity = match.group(1).lower()
                if len(entity) > 2 and entity not in ['api', 'app', 'web', 'site']:
                    detected_entities.add(entity.capitalize())
        
        # Create enhanced models with fields
        for entity in detected_entities:
            model = self._create_enhanced_model(entity, text)
            models.append(model)
        
        # Extract relationships
        relationships = self._extract_relationships(list(detected_entities), text)
        
        return models, relationships
    
    def _create_enhanced_model(self, entity_name: str, text: str) -> Dict[str, Any]:
        """Create enhanced model with inferred fields and validation"""
        
        fields = [
            ModelField(name="id", type="integer", required=True, unique=True, indexed=True)
        ]
        
        # Common field patterns based on entity type
        entity_lower = entity_name.lower()
        
        if entity_lower in ['user', 'account', 'member']:
            fields.extend([
                ModelField(name="email", type="email", required=True, unique=True, indexed=True,
                          validation_rules=["email_format", "unique"]),
                ModelField(name="username", type="string", required=True, unique=True, indexed=True,
                          validation_rules=["min_length:3", "alphanumeric"]),
                ModelField(name="password_hash", type="string", required=True,
                          validation_rules=["min_length:8"]),
                ModelField(name="first_name", type="string", required=False),
                ModelField(name="last_name", type="string", required=False),
                ModelField(name="is_active", type="boolean", default=True),
                ModelField(name="created_at", type="datetime", default="now", indexed=True),
                ModelField(name="updated_at", type="datetime", default="now")
            ])
        
        elif entity_lower in ['post', 'article', 'blog']:
            fields.extend([
                ModelField(name="title", type="string", required=True, indexed=True,
                          validation_rules=["min_length:1", "max_length:255"]),
                ModelField(name="content", type="text", required=True),
                ModelField(name="excerpt", type="text", required=False),
                ModelField(name="published", type="boolean", default=False, indexed=True),
                ModelField(name="author_id", type="integer", required=True, indexed=True),
                ModelField(name="created_at", type="datetime", default="now", indexed=True),
                ModelField(name="updated_at", type="datetime", default="now")
            ])
        
        elif entity_lower in ['product', 'item']:
            fields.extend([
                ModelField(name="name", type="string", required=True, indexed=True,
                          validation_rules=["min_length:1", "max_length:255"]),
                ModelField(name="description", type="text", required=False),
                ModelField(name="price", type="decimal", required=True,
                          validation_rules=["min_value:0"]),
                ModelField(name="sku", type="string", required=False, unique=True, indexed=True),
                ModelField(name="stock_quantity", type="integer", default=0,
                          validation_rules=["min_value:0"]),
                ModelField(name="is_active", type="boolean", default=True, indexed=True),
                ModelField(name="created_at", type="datetime", default="now", indexed=True),
                ModelField(name="updated_at", type="datetime", default="now")
            ])
        
        elif entity_lower in ['order', 'purchase']:
            fields.extend([
                ModelField(name="order_number", type="string", required=True, unique=True, indexed=True),
                ModelField(name="customer_id", type="integer", required=True, indexed=True),
                ModelField(name="total_amount", type="decimal", required=True,
                          validation_rules=["min_value:0"]),
                ModelField(name="status", type="string", required=True, default="pending", indexed=True,
                          validation_rules=["choices:pending,processing,shipped,delivered,cancelled"]),
                ModelField(name="created_at", type="datetime", default="now", indexed=True),
                ModelField(name="updated_at", type="datetime", default="now")
            ])
        
        else:
            # Generic fields for unknown entities
            fields.extend([
                ModelField(name="name", type="string", required=True, indexed=True),
                ModelField(name="description", type="text", required=False),
                ModelField(name="created_at", type="datetime", default="now", indexed=True),
                ModelField(name="updated_at", type="datetime", default="now")
            ])
        
        # Extract additional fields from text context
        additional_fields = self._extract_contextual_fields(entity_name, text)
        fields.extend(additional_fields)
        
        return {
            "name": entity_name,
            "fields": [field.__dict__ for field in fields],
            "table_name": f"{entity_lower}s",
            "description": f"{entity_name} model with enhanced field detection"
        }
    
    def _extract_contextual_fields(self, entity_name: str, text: str) -> List[ModelField]:
        """Extract additional fields based on context in the description"""
        
        fields = []
        entity_lower = entity_name.lower()
        
        # Look for field mentions near the entity
        field_patterns = [
            rf'{entity_lower}\s+(?:with|having|includes?)\s+([^.]+)',
            rf'(?:each|every)\s+{entity_lower}\s+(?:has|contains)\s+([^.]+)',
        ]
        
        for pattern in field_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                field_text = match.group(1)
                extracted_fields = self._parse_field_text(field_text)
                fields.extend(extracted_fields)
        
        return fields
    
    def _parse_field_text(self, field_text: str) -> List[ModelField]:
        """Parse field descriptions from text"""
        
        fields = []
        
        # Common field indicators
        field_indicators = {
            'email': ModelField(name="email", type="email", validation_rules=["email_format"]),
            'phone': ModelField(name="phone", type="string", validation_rules=["phone_format"]),
            'address': ModelField(name="address", type="text"),
            'age': ModelField(name="age", type="integer", validation_rules=["min_value:0", "max_value:150"]),
            'date': ModelField(name="date", type="date"),
            'time': ModelField(name="time", type="time"),
            'url': ModelField(name="url", type="string", validation_rules=["url_format"]),
            'image': ModelField(name="image_url", type="string", validation_rules=["url_format"]),
            'file': ModelField(name="file_path", type="string"),
            'status': ModelField(name="status", type="string", indexed=True),
            'category': ModelField(name="category", type="string", indexed=True),
            'tag': ModelField(name="tags", type="string"),
            'rating': ModelField(name="rating", type="decimal", validation_rules=["min_value:0", "max_value:5"]),
            'count': ModelField(name="count", type="integer", validation_rules=["min_value:0"]),
            'amount': ModelField(name="amount", type="decimal", validation_rules=["min_value:0"]),
        }
        
        for indicator, field_template in field_indicators.items():
            if indicator in field_text.lower():
                fields.append(field_template)
        
        return fields
    
    def _extract_relationships(self, entities: List[str], text: str) -> List[ModelRelationship]:
        """Extract relationships between entities"""
        
        relationships = []
        
        # Enhanced relationship patterns
        relationship_patterns = [
            (r'(\w+)\s+(?:belongs?\s+to|is\s+owned\s+by)\s+(\w+)', 'many_to_one'),
            (r'(\w+)\s+(?:has\s+many|contains?\s+many)\s+(\w+)s?', 'one_to_many'),
            (r'(\w+)\s+(?:has\s+a|contains?\s+a)\s+(\w+)', 'one_to_one'),
            (r'(\w+)s?\s+(?:and|with)\s+(\w+)s?\s+(?:are\s+)?(?:related|connected|linked)', 'many_to_many'),
            (r'(?:each|every)\s+(\w+)\s+(?:can\s+have|has)\s+(?:multiple|many)\s+(\w+)s?', 'one_to_many'),
        ]
        
        for pattern, rel_type in relationship_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                from_entity = match.group(1).capitalize()
                to_entity = match.group(2).capitalize()
                
                if from_entity in entities and to_entity in entities:
                    relationships.append(ModelRelationship(
                        from_model=from_entity,
                        to_model=to_entity,
                        relationship_type=rel_type,
                        foreign_key=f"{to_entity.lower()}_id" if rel_type in ['many_to_one', 'one_to_one'] else None,
                        related_name=f"{from_entity.lower()}s" if rel_type == 'one_to_many' else None
                    ))
        
        return relationships
    
    def _extract_business_logic(self, text: str) -> List[BusinessRule]:
        """Extract business logic and conditional rules from text"""
        
        rules = []
        
        # Conditional logic patterns
        conditional_patterns = [
            r'if\s+([^,]+),?\s+then\s+([^.]+)',
            r'when\s+([^,]+),?\s+([^.]+)',
            r'unless\s+([^,]+),?\s+([^.]+)',
            r'only\s+([^,]+)\s+can\s+([^.]+)',
            r'([^,]+)\s+must\s+([^.]+)',
            r'([^,]+)\s+should\s+([^.]+)',
            r'([^,]+)\s+cannot\s+([^.]+)',
        ]
        
        for pattern in conditional_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                condition = match.group(1).strip()
                action = match.group(2).strip()
                
                rules.append(BusinessRule(
                    condition=condition,
                    action=action,
                    priority=1,
                    context="conditional_logic"
                ))
        
        # Validation rules
        validation_patterns = [
            r'([^,]+)\s+must\s+be\s+(?:unique|distinct)',
            r'([^,]+)\s+(?:is\s+)?required',
            r'([^,]+)\s+(?:is\s+)?optional',
            r'([^,]+)\s+must\s+be\s+(?:at\s+least|minimum)\s+(\d+)',
            r'([^,]+)\s+must\s+be\s+(?:at\s+most|maximum)\s+(\d+)',
        ]
        
        for pattern in validation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                field = match.group(1).strip()
                rule_type = "validation"
                
                if "unique" in match.group(0).lower():
                    action = f"ensure {field} is unique"
                elif "required" in match.group(0).lower():
                    action = f"ensure {field} is required"
                elif "optional" in match.group(0).lower():
                    action = f"make {field} optional"
                else:
                    action = match.group(0)
                
                rules.append(BusinessRule(
                    condition=f"validating {field}",
                    action=action,
                    priority=2,
                    context="validation"
                ))
        
        return rules
    
    def _determine_framework_and_api_type(self, text: str) -> Tuple[FrameworkType, APIType]:
        """Determine framework and API type with GraphQL support"""
        
        # GraphQL indicators
        graphql_indicators = [
            'graphql', 'graph ql', 'single endpoint', 'query language',
            'mutations', 'subscriptions', 'schema', 'resolver'
        ]
        
        # FastAPI indicators
        fastapi_indicators = [
            'modern', 'fast', 'async', 'microservice', 'api-first',
            'high-performance', 'real-time', 'websocket', 'fastapi'
        ]
        
        # Django indicators
        django_indicators = [
            'admin', 'cms', 'full-featured', 'web application',
            'traditional', 'monolithic', 'admin interface', 'django'
        ]
        
        # Check for GraphQL
        if any(indicator in text.lower() for indicator in graphql_indicators):
            # Determine framework for GraphQL
            if any(indicator in text.lower() for indicator in django_indicators):
                return FrameworkType.GRAPHQL_DJANGO, APIType.GRAPHQL
            else:
                return FrameworkType.GRAPHQL_FASTAPI, APIType.GRAPHQL
        
        # Check for hybrid (both REST and GraphQL)
        if 'hybrid' in text.lower() or ('rest' in text.lower() and 'graphql' in text.lower()):
            return FrameworkType.FASTAPI, APIType.HYBRID
        
        # Traditional framework selection
        if any(indicator in text.lower() for indicator in django_indicators):
            return FrameworkType.DJANGO, APIType.REST
        elif any(indicator in text.lower() for indicator in fastapi_indicators):
            return FrameworkType.FASTAPI, APIType.REST
        else:
            # Default based on complexity
            model_count = len(re.findall(r'\b\w+\s+(?:model|entity|table)', text, re.IGNORECASE))
            if model_count > 5 or 'admin' in text.lower():
                return FrameworkType.DJANGO, APIType.REST
            else:
                return FrameworkType.FASTAPI, APIType.REST
    
    def _determine_database_type(self, text: str) -> DatabaseType:
        """Determine database type with NoSQL support"""
        
        database_indicators = {
            DatabaseType.POSTGRESQL: ['postgresql', 'postgres', 'pg'],
            DatabaseType.MYSQL: ['mysql', 'mariadb'],
            DatabaseType.SQLITE: ['sqlite', 'sqlite3'],
            DatabaseType.MONGODB: ['mongodb', 'mongo', 'nosql', 'document'],
            DatabaseType.DYNAMODB: ['dynamodb', 'dynamo', 'aws'],
            DatabaseType.FIRESTORE: ['firestore', 'firebase', 'google cloud']
        }
        
        for db_type, indicators in database_indicators.items():
            if any(indicator in text.lower() for indicator in indicators):
                return db_type
        
        # Default selection based on other factors
        if 'nosql' in text.lower() or 'document' in text.lower():
            return DatabaseType.MONGODB
        elif 'cloud' in text.lower() or 'aws' in text.lower():
            return DatabaseType.DYNAMODB
        elif 'production' in text.lower() or 'scale' in text.lower():
            return DatabaseType.POSTGRESQL
        else:
            return DatabaseType.SQLITE
    
    def _determine_auth_type(self, text: str) -> AuthType:
        """Enhanced authentication type detection"""
        
        auth_indicators = {
            AuthType.JWT: ['jwt', 'token', 'stateless', 'bearer', 'json web token'],
            AuthType.SESSION: ['session', 'cookie', 'traditional', 'server-side'],
            AuthType.API_KEY: ['api key', 'key-based', 'simple auth', 'api token'],
            AuthType.OAUTH2: ['oauth', 'oauth2', 'google', 'facebook', 'social', 'third-party'],
            AuthType.NONE: ['no auth', 'public', 'open', 'anonymous']
        }
        
        for auth_type, indicators in auth_indicators.items():
            if any(indicator in text.lower() for indicator in indicators):
                return auth_type
        
        # Default logic
        if any(keyword in text.lower() for keyword in ['user', 'login', 'register', 'account']):
            return AuthType.JWT  # Modern default
        else:
            return AuthType.NONE
    
    def _determine_advanced_features(self, requirements: ProjectRequirements, text: str):
        """Determine advanced features from text"""
        
        feature_indicators = {
            'cors_enabled': ['cors', 'cross-origin', 'frontend', 'web app'],
            'rate_limiting': ['rate limit', 'throttle', 'limit requests', 'ddos'],
            'caching': ['cache', 'redis', 'memcached', 'performance'],
            'file_uploads': ['upload', 'file', 'image', 'document', 'attachment'],
            'real_time': ['real-time', 'websocket', 'live', 'push notification'],
            'background_tasks': ['background', 'async task', 'queue', 'job'],
            'use_celery': ['celery', 'task queue', 'background job'],
            'use_redis': ['redis', 'cache', 'session store'],
            'use_elasticsearch': ['search', 'elasticsearch', 'full-text'],
            'containerize': ['docker', 'container', 'kubernetes', 'deploy'],
        }
        
        for feature, indicators in feature_indicators.items():
            if any(indicator in text.lower() for indicator in indicators):
                setattr(requirements, feature, True)
    
    def _calculate_confidence_score(self, requirements: ProjectRequirements, text: str) -> float:
        """Calculate confidence score for the extraction"""
        
        score = 0.0
        
        # Base score for successful extraction
        if requirements.project_name:
            score += 0.2
        
        if requirements.models:
            score += 0.3
        
        if requirements.framework:
            score += 0.2
        
        # Bonus for clear indicators
        clear_indicators = [
            'create', 'build', 'design', 'api', 'database',
            'user', 'authentication', 'model', 'endpoint'
        ]
        
        indicator_count = sum(1 for indicator in clear_indicators if indicator in text.lower())
        score += min(indicator_count * 0.05, 0.3)
        
        # Penalty for validation errors
        error_penalty = len(requirements.validation_errors) * 0.1
        score = max(0.0, score - error_penalty)
        
        return min(score, 1.0)
    
    def _identify_clarification_needs(self, requirements: ProjectRequirements, text: str) -> List[str]:
        """Identify areas that need clarification"""
        
        clarifications = []
        
        if requirements.confidence_score < 0.5:
            clarifications.append("The description is ambiguous. Please provide more specific details.")
        
        if not requirements.models:
            clarifications.append("No clear data models detected. What entities should the API manage?")
        
        if len(requirements.models) == 1 and 'user' not in text.lower():
            clarifications.append("Only one model detected. Are there other entities or relationships?")
        
        if requirements.auth_type == AuthType.NONE and 'user' in text.lower():
            clarifications.append("User management detected but no authentication specified. What type of authentication do you need?")
        
        if 'payment' in text.lower() and requirements.database_type == DatabaseType.SQLITE:
            clarifications.append("Payment processing mentioned but SQLite selected. Consider a more robust database for production.")
        
        return clarifications
    
    def _extract_project_name(self, text: str) -> str:
        """Extract project name from description"""
        
        # Look for explicit project names
        name_patterns = [
            r'(?:project|app|application|system|platform|service)\s+(?:called|named)\s+(["\']?)(\w+)\1',
            r'(?:build|create|design)\s+(?:a|an)?\s*(["\']?)(\w+)\1\s+(?:api|app|system|platform)',
            r'^([A-Z]\w+(?:\s+[A-Z]\w+)*)\s+(?:api|system|platform|app)',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) > 1:
                    return match.group(2).lower().replace(' ', '_')
                else:
                    return match.group(1).lower().replace(' ', '_')
        
        # Fallback: extract from first few words
        words = text.split()[:3]
        meaningful_words = [word for word in words if word.lower() not in 
                          ['create', 'build', 'design', 'a', 'an', 'the', 'api', 'for']]
        
        if meaningful_words:
            return '_'.join(meaningful_words).lower()
        
        return "generated_api"
    
    def _apply_model_corrections(self, models: List[Dict[str, Any]], 
                                corrections: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply user corrections to models"""
        
        corrected_models = []
        
        for model in models:
            model_name = model['name']
            if model_name in corrections:
                correction = corrections[model_name]
                
                # Apply field corrections
                if 'fields' in correction:
                    model['fields'] = correction['fields']
                
                # Apply name correction
                if 'name' in correction:
                    model['name'] = correction['name']
                
                # Apply other corrections
                for key, value in correction.items():
                    if key not in ['fields', 'name']:
                        model[key] = value
            
            corrected_models.append(model)
        
        return corrected_models
    
    def _store_feedback(self, requirements: ProjectRequirements, feedback: Dict[str, Any]):
        """Store user feedback for learning (placeholder for ML integration)"""
        
        feedback_entry = {
            'original_description': requirements.description,
            'extracted_requirements': requirements.__dict__,
            'user_feedback': feedback,
            'timestamp': str(Path.cwd())  # Placeholder
        }
        
        # In a real implementation, this would store to a database or file
        logger.info(f"Feedback stored for learning: {len(feedback)} corrections")
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load NLP patterns (placeholder for external pattern files)"""
        return {
            'models': [],
            'relationships': [],
            'fields': []
        }
    
    def _load_business_logic_patterns(self) -> Dict[str, List[str]]:
        """Load business logic patterns"""
        return {
            'conditional': [],
            'validation': [],
            'workflow': []
        }
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules"""
        return {}
    
    def _load_feedback_data(self) -> Dict[str, Any]:
        """Load historical feedback data for learning"""
        return {}

# Convenience function for backward compatibility
def extract_requirements(description: str) -> ProjectRequirements:
    """Extract requirements using the enhanced NLP extractor"""
    extractor = NLPExtractor()
    return extractor.extract_requirements(description)

# Main execution for testing
if __name__ == "__main__":
    extractor = NLPExtractor()
    
    # Test with a complex description
    test_description = """
    Create a modern e-commerce platform with user authentication, product management, 
    shopping cart, and order processing. Users can browse products, add them to cart, 
    and place orders. Only authenticated users can make purchases. Each product has 
    a name, description, price, and stock quantity. Orders must track status from 
    pending to delivered. Include real-time notifications and file upload for product images.
    Use PostgreSQL database and JWT authentication.
    """
    
    requirements = extractor.extract_requirements(test_description)
    
    print(f"Project: {requirements.project_name}")
    print(f"Framework: {requirements.framework.value}")
    print(f"Database: {requirements.database_type.value}")
    print(f"Auth: {requirements.auth_type.value}")
    print(f"Models: {len(requirements.models)}")
    print(f"Business Rules: {len(requirements.business_rules)}")
    print(f"Confidence: {requirements.confidence_score:.2f}")
    print(f"Clarifications needed: {len(requirements.needs_clarification)}")

