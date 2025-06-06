"""
Enhanced Project Structure Analyzer
===================================

Advanced project analysis with visual representation, improved relationship mapping,
and intelligent architecture decisions.

Features:
- Visual project structure representation
- Advanced relationship mapping
- Intelligent endpoint pattern recognition
- Business logic workflow analysis
- Architecture optimization recommendations
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import networkx as nx
from nlp_extractor import ProjectRequirements, ModelRelationship, BusinessRule

logger = logging.getLogger(__name__)

@dataclass
class EndpointAnalyzer:
    """Represents an API endpoint pattern"""
    path: str
    method: str
    operation: str
    model: str
    description: str
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    business_logic: List[str] = field(default_factory=list)
    security: List[str] = field(default_factory=list)

@dataclass
class ProjectStructure:
    """Represents the complete project structure"""
    directories: Dict[str, List[str]]
    files: Dict[str, str]
    dependencies: List[str]
    configuration: Dict[str, Any]
    deployment: Dict[str, Any]

@dataclass
class VisualRepresentation:
    """Visual representation of the project structure"""
    model_diagram: Dict[str, Any]
    endpoint_map: Dict[str, Any]
    relationship_graph: Dict[str, Any]
    architecture_diagram: Dict[str, Any]

class ProjectAnalyzer:
    """
    Enhanced project structure analyzer with visual representation and advanced analysis
    """
    
    def __init__(self, requirements: ProjectRequirements):
        """Initialize the enhanced project analyzer"""
        self.requirements = requirements
        self.graph = nx.DiGraph()
        self.endpoints = []
        self.structure = None
        self.visual_representation = None
        
        logger.info("Enhanced Project Analyzer initialized")
    
    def analyze_complete_project(self) -> Dict[str, Any]:
        """
        Perform complete project analysis including structure, endpoints, and visualization
        
        Returns:
            Complete analysis results
        """
        
        logger.info("Starting complete project analysis")
        
        # Step 1: Analyze project structure
        self.structure = self._analyze_project_structure()
        
        # Step 2: Analyze endpoints and patterns
        self.endpoints = self._analyze_endpoint_patterns()
        
        # Step 3: Build relationship graph
        self._build_relationship_graph()
        
        # Step 4: Generate visual representation
        self.visual_representation = self._generate_visual_representation()
        
        # Step 5: Analyze business logic workflows
        workflows = self._analyze_business_workflows()
        
        # Step 6: Generate architecture recommendations
        recommendations = self._generate_architecture_recommendations()
        
        analysis_result = {
            'project_structure': self.structure.__dict__,
            'endpoints': [ep.__dict__ for ep in self.endpoints],
            'visual_representation': self.visual_representation.__dict__,
            'business_workflows': workflows,
            'architecture_recommendations': recommendations,
            'complexity_metrics': self._calculate_complexity_metrics(),
            'security_analysis': self._analyze_security_requirements(),
            'performance_considerations': self._analyze_performance_requirements()
        }
        
        logger.info("Complete project analysis finished")
        return analysis_result
    
    def _analyze_project_structure(self) -> ProjectStructure:
        """Analyze and generate optimal project structure"""
        
        framework = self.requirements.framework
        api_type = self.requirements.api_type
        
        if framework.value.startswith('fastapi'):
            return self._generate_fastapi_structure()
        elif framework.value.startswith('django'):
            return self._generate_django_structure()
        elif framework.value.startswith('graphql'):
            return self._generate_graphql_structure()
        else:
            return self._generate_generic_structure()
    
    def _generate_fastapi_structure(self) -> ProjectStructure:
        """Generate FastAPI project structure"""
        
        directories = {
            'app': [
                'api', 'core', 'models', 'schemas', 'crud', 'db', 
                'utils', 'auth', 'services', 'tests'
            ],
            'app/api': ['v1', 'deps.py'],
            'app/api/v1': ['endpoints'],
            'app/core': ['config.py', 'security.py', 'logging.py'],
            'app/models': [],
            'app/schemas': [],
            'app/crud': [],
            'app/services': [],
            'app/tests': ['unit', 'integration', 'e2e'],
            'migrations': ['versions'],
            'scripts': [],
            'docs': [],
            'docker': []
        }
        
        # Add model-specific directories
        for model in self.requirements.models:
            model_name = model['name'].lower()
            directories['app/api/v1/endpoints'].append(f'{model_name}.py')
            directories['app/models'].append(f'{model_name}.py')
            directories['app/schemas'].append(f'{model_name}.py')
            directories['app/crud'].append(f'{model_name}.py')
            directories['app/services'].append(f'{model_name}.py')
        
        files = {
            'main.py': 'FastAPI application entry point',
            'requirements.txt': 'Python dependencies',
            'requirements-dev.txt': 'Development dependencies',
            'pyproject.toml': 'Project configuration',
            '.env.example': 'Environment variables template',
            '.gitignore': 'Git ignore rules',
            'README.md': 'Project documentation',
            'Dockerfile': 'Docker container configuration',
            'docker-compose.yml': 'Docker compose configuration',
            'alembic.ini': 'Database migration configuration',
            'pytest.ini': 'Test configuration',
            '.pre-commit-config.yaml': 'Pre-commit hooks',
            'app/__init__.py': 'App package initialization',
            'app/main.py': 'FastAPI app factory',
        }
        
        dependencies = self._get_fastapi_dependencies()
        configuration = self._get_fastapi_configuration()
        deployment = self._get_deployment_configuration()
        
        return ProjectStructure(
            directories=directories,
            files=files,
            dependencies=dependencies,
            configuration=configuration,
            deployment=deployment
        )
    
    def _generate_django_structure(self) -> ProjectStructure:
        """Generate Django project structure"""
        
        project_name = self.requirements.project_name
        
        directories = {
            project_name: ['settings', 'urls.py', 'wsgi.py', 'asgi.py'],
            'apps': [],
            'config': ['settings'],
            'static': ['css', 'js', 'images'],
            'media': ['uploads'],
            'templates': ['base'],
            'tests': ['unit', 'integration'],
            'docs': [],
            'scripts': [],
            'requirements': []
        }
        
        # Add app directories for each model
        for model in self.requirements.models:
            app_name = f"{model['name'].lower()}s"
            directories['apps'].append(app_name)
            directories[f'apps/{app_name}'] = [
                'models.py', 'views.py', 'serializers.py', 'urls.py',
                'admin.py', 'apps.py', 'tests.py', 'migrations'
            ]
        
        files = {
            'manage.py': 'Django management script',
            'requirements.txt': 'Python dependencies',
            'requirements-dev.txt': 'Development dependencies',
            '.env.example': 'Environment variables template',
            '.gitignore': 'Git ignore rules',
            'README.md': 'Project documentation',
            'Dockerfile': 'Docker container configuration',
            'docker-compose.yml': 'Docker compose configuration',
            'pytest.ini': 'Test configuration',
            'setup.cfg': 'Project setup configuration',
        }
        
        dependencies = self._get_django_dependencies()
        configuration = self._get_django_configuration()
        deployment = self._get_deployment_configuration()
        
        return ProjectStructure(
            directories=directories,
            files=files,
            dependencies=dependencies,
            configuration=configuration,
            deployment=deployment
        )
    
    def _generate_graphql_structure(self) -> ProjectStructure:
        """Generate GraphQL project structure"""
        
        base_structure = self._generate_fastapi_structure() if 'fastapi' in self.requirements.framework.value else self._generate_django_structure()
        
        # Add GraphQL-specific directories and files
        base_structure.directories['app'].extend(['graphql', 'resolvers', 'types'])
        base_structure.directories['app/graphql'] = ['schema.py', 'queries.py', 'mutations.py', 'subscriptions.py']
        base_structure.directories['app/resolvers'] = []
        base_structure.directories['app/types'] = []
        
        # Add model-specific GraphQL files
        for model in self.requirements.models:
            model_name = model['name'].lower()
            base_structure.directories['app/resolvers'].append(f'{model_name}.py')
            base_structure.directories['app/types'].append(f'{model_name}.py')
        
        base_structure.files['app/graphql/schema.py'] = 'GraphQL schema definition'
        
        # Add GraphQL dependencies
        if 'fastapi' in self.requirements.framework.value:
            base_structure.dependencies.extend(['strawberry-graphql', 'strawberry-graphql[fastapi]'])
        else:
            base_structure.dependencies.extend(['graphene-django', 'django-graphql-jwt'])
        
        return base_structure
    
    def _generate_generic_structure(self) -> ProjectStructure:
        """Generate generic project structure"""
        return self._generate_fastapi_structure()  # Default to FastAPI
    
    def _analyze_endpoint_patterns(self) -> List[EndpointAnalyzer]:
        """Analyze and generate endpoint patterns"""
        
        endpoints = []
        
        # Generate CRUD endpoints for each model
        for model in self.requirements.models:
            model_name = model['name']
            model_name_lower = model_name.lower()
            model_name_plural = f"{model_name_lower}s"
            
            # List endpoint
            endpoints.append(EndpointAnalyzer(
                path=f"/{model_name_plural}/",
                method="GET",
                operation="list",
                model=model_name,
                description=f"List all {model_name_plural}",
                parameters=[
                    {"name": "skip", "type": "integer", "default": 0, "description": "Number of items to skip"},
                    {"name": "limit", "type": "integer", "default": 100, "description": "Maximum number of items to return"},
                    {"name": "search", "type": "string", "required": False, "description": "Search query"},
                    {"name": "sort", "type": "string", "required": False, "description": "Sort field"},
                    {"name": "order", "type": "string", "required": False, "description": "Sort order (asc/desc)"}
                ],
                responses=[
                    {"status": 200, "description": f"List of {model_name_plural}", "schema": f"List[{model_name}Response]"},
                    {"status": 400, "description": "Invalid parameters"},
                    {"status": 500, "description": "Internal server error"}
                ],
                business_logic=["pagination", "filtering", "sorting", "search"],
                security=["optional_auth"] if self.requirements.auth_type.value != "none" else []
            ))
            
            # Create endpoint
            endpoints.append(EndpointAnalyzer(
                path=f"/{model_name_plural}/",
                method="POST",
                operation="create",
                model=model_name,
                description=f"Create a new {model_name_lower}",
                parameters=[
                    {"name": "body", "type": f"{model_name}Create", "required": True, "description": f"{model_name} data"}
                ],
                responses=[
                    {"status": 201, "description": f"{model_name} created successfully", "schema": f"{model_name}Response"},
                    {"status": 400, "description": "Invalid input data"},
                    {"status": 409, "description": "Conflict (duplicate data)"},
                    {"status": 422, "description": "Validation error"}
                ],
                business_logic=["validation", "duplicate_check", "business_rules"],
                security=["auth_required"] if self.requirements.auth_type.value != "none" else []
            ))
            
            # Get by ID endpoint
            endpoints.append(EndpointAnalyzer(
                path=f"/{model_name_plural}/{{id}}",
                method="GET",
                operation="get",
                model=model_name,
                description=f"Get a specific {model_name_lower}",
                parameters=[
                    {"name": "id", "type": "integer", "required": True, "description": f"{model_name} ID"}
                ],
                responses=[
                    {"status": 200, "description": f"{model_name} details", "schema": f"{model_name}Response"},
                    {"status": 404, "description": f"{model_name} not found"},
                    {"status": 403, "description": "Access denied"}
                ],
                business_logic=["existence_check", "permission_check"],
                security=["optional_auth"] if self.requirements.auth_type.value != "none" else []
            ))
            
            # Update endpoint
            endpoints.append(EndpointAnalyzer(
                path=f"/{model_name_plural}/{{id}}",
                method="PUT",
                operation="update",
                model=model_name,
                description=f"Update a {model_name_lower}",
                parameters=[
                    {"name": "id", "type": "integer", "required": True, "description": f"{model_name} ID"},
                    {"name": "body", "type": f"{model_name}Update", "required": True, "description": "Updated data"}
                ],
                responses=[
                    {"status": 200, "description": f"{model_name} updated successfully", "schema": f"{model_name}Response"},
                    {"status": 404, "description": f"{model_name} not found"},
                    {"status": 400, "description": "Invalid input data"},
                    {"status": 403, "description": "Access denied"}
                ],
                business_logic=["existence_check", "permission_check", "validation", "business_rules"],
                security=["auth_required"] if self.requirements.auth_type.value != "none" else []
            ))
            
            # Delete endpoint
            endpoints.append(EndpointAnalyzer(
                path=f"/{model_name_plural}/{{id}}",
                method="DELETE",
                operation="delete",
                model=model_name,
                description=f"Delete a {model_name_lower}",
                parameters=[
                    {"name": "id", "type": "integer", "required": True, "description": f"{model_name} ID"}
                ],
                responses=[
                    {"status": 204, "description": f"{model_name} deleted successfully"},
                    {"status": 404, "description": f"{model_name} not found"},
                    {"status": 403, "description": "Access denied"},
                    {"status": 409, "description": "Cannot delete (has dependencies)"}
                ],
                business_logic=["existence_check", "permission_check", "dependency_check"],
                security=["auth_required"] if self.requirements.auth_type.value != "none" else []
            ))
        
        # Add relationship endpoints
        endpoints.extend(self._generate_relationship_endpoints())
        
        # Add business logic endpoints
        endpoints.extend(self._generate_business_logic_endpoints())
        
        # Add authentication endpoints
        if self.requirements.auth_type.value != "none":
            endpoints.extend(self._generate_auth_endpoints())
        
        # Add utility endpoints
        endpoints.extend(self._generate_utility_endpoints())
        
        return endpoints
    
    def _generate_relationship_endpoints(self) -> List[EndpointAnalyzer]:
        """Generate endpoints for model relationships"""
        
        endpoints = []
        
        for relationship in self.requirements.relationships:
            from_model = relationship.from_model
            to_model = relationship.to_model
            
            if relationship.relationship_type == "one_to_many":
                # Get related items endpoint
                endpoints.append(EndpointAnalyzer(
                    path=f"/{from_model.lower()}s/{{id}}/{to_model.lower()}s/",
                    method="GET",
                    operation="get_related",
                    model=f"{from_model}-{to_model}",
                    description=f"Get {to_model.lower()}s for a specific {from_model.lower()}",
                    parameters=[
                        {"name": "id", "type": "integer", "required": True, "description": f"{from_model} ID"},
                        {"name": "skip", "type": "integer", "default": 0},
                        {"name": "limit", "type": "integer", "default": 100}
                    ],
                    responses=[
                        {"status": 200, "description": f"List of related {to_model.lower()}s"},
                        {"status": 404, "description": f"{from_model} not found"}
                    ],
                    business_logic=["relationship_validation", "pagination"],
                    security=["optional_auth"] if self.requirements.auth_type.value != "none" else []
                ))
        
        return endpoints
    
    def _generate_business_logic_endpoints(self) -> List[EndpointAnalyzer]:
        """Generate endpoints based on business rules"""
        
        endpoints = []
        
        for rule in self.requirements.business_rules:
            if rule.context == "workflow":
                # Generate workflow endpoints
                if "order" in rule.condition.lower():
                    endpoints.append(EndpointAnalyzer(
                        path="/orders/{id}/status",
                        method="PATCH",
                        operation="update_status",
                        model="Order",
                        description="Update order status",
                        parameters=[
                            {"name": "id", "type": "integer", "required": True},
                            {"name": "status", "type": "string", "required": True}
                        ],
                        responses=[
                            {"status": 200, "description": "Status updated"},
                            {"status": 400, "description": "Invalid status transition"}
                        ],
                        business_logic=["status_validation", "workflow_rules"],
                        security=["auth_required"]
                    ))
        
        return endpoints
    
    def _generate_auth_endpoints(self) -> List[EndpointAnalyzer]:
        """Generate authentication endpoints"""
        
        endpoints = []
        
        if self.requirements.auth_type == AuthType.JWT:
            endpoints.extend([
                EndpointAnalyzer(
                    path="/auth/login",
                    method="POST",
                    operation="login",
                    model="Auth",
                    description="User login",
                    parameters=[
                        {"name": "credentials", "type": "LoginRequest", "required": True}
                    ],
                    responses=[
                        {"status": 200, "description": "Login successful", "schema": "TokenResponse"},
                        {"status": 401, "description": "Invalid credentials"}
                    ],
                    business_logic=["credential_validation", "token_generation"],
                    security=[]
                ),
                EndpointAnalyzer(
                    path="/auth/register",
                    method="POST",
                    operation="register",
                    model="Auth",
                    description="User registration",
                    parameters=[
                        {"name": "user_data", "type": "RegisterRequest", "required": True}
                    ],
                    responses=[
                        {"status": 201, "description": "User registered", "schema": "UserResponse"},
                        {"status": 400, "description": "Invalid data"},
                        {"status": 409, "description": "User already exists"}
                    ],
                    business_logic=["validation", "duplicate_check", "password_hashing"],
                    security=[]
                ),
                EndpointAnalyzer(
                    path="/auth/refresh",
                    method="POST",
                    operation="refresh_token",
                    model="Auth",
                    description="Refresh access token",
                    parameters=[
                        {"name": "refresh_token", "type": "RefreshRequest", "required": True}
                    ],
                    responses=[
                        {"status": 200, "description": "Token refreshed", "schema": "TokenResponse"},
                        {"status": 401, "description": "Invalid refresh token"}
                    ],
                    business_logic=["token_validation", "token_generation"],
                    security=[]
                )
            ])
        
        return endpoints
    
    def _generate_utility_endpoints(self) -> List[EndpointAnalyzer]:
        """Generate utility endpoints"""
        
        endpoints = [
            EndpointAnalyzer(
                path="/health",
                method="GET",
                operation="health_check",
                model="System",
                description="Health check endpoint",
                parameters=[],
                responses=[
                    {"status": 200, "description": "System healthy", "schema": "HealthResponse"}
                ],
                business_logic=["system_check"],
                security=[]
            ),
            EndpointAnalyzer(
                path="/version",
                method="GET",
                operation="version_info",
                model="System",
                description="API version information",
                parameters=[],
                responses=[
                    {"status": 200, "description": "Version info", "schema": "VersionResponse"}
                ],
                business_logic=[],
                security=[]
            )
        ]
        
        # Add file upload endpoint if needed
        if self.requirements.file_uploads:
            endpoints.append(EndpointAnalyzer(
                path="/upload",
                method="POST",
                operation="upload_file",
                model="File",
                description="Upload file",
                parameters=[
                    {"name": "file", "type": "UploadFile", "required": True},
                    {"name": "category", "type": "string", "required": False}
                ],
                responses=[
                    {"status": 200, "description": "File uploaded", "schema": "FileResponse"},
                    {"status": 400, "description": "Invalid file"},
                    {"status": 413, "description": "File too large"}
                ],
                business_logic=["file_validation", "virus_scan", "storage"],
                security=["auth_required"] if self.requirements.auth_type.value != "none" else []
            ))
        
        return endpoints
    
    def _build_relationship_graph(self):
        """Build a graph representation of model relationships"""
        
        # Add nodes for each model
        for model in self.requirements.models:
            self.graph.add_node(model['name'], type='model', **model)
        
        # Add edges for relationships
        for relationship in self.requirements.relationships:
            self.graph.add_edge(
                relationship.from_model,
                relationship.to_model,
                relationship_type=relationship.relationship_type,
                foreign_key=relationship.foreign_key,
                related_name=relationship.related_name
            )
    
    def _generate_visual_representation(self) -> VisualRepresentation:
        """Generate visual representation of the project structure"""
        
        # Model diagram
        model_diagram = {
            'nodes': [],
            'edges': [],
            'layout': 'hierarchical'
        }
        
        for model in self.requirements.models:
            model_diagram['nodes'].append({
                'id': model['name'],
                'label': model['name'],
                'type': 'model',
                'fields': model['fields'],
                'position': {'x': 0, 'y': 0}  # Will be calculated by frontend
            })
        
        for relationship in self.requirements.relationships:
            model_diagram['edges'].append({
                'from': relationship.from_model,
                'to': relationship.to_model,
                'type': relationship.relationship_type,
                'label': relationship.relationship_type.replace('_', ' ').title()
            })
        
        # Endpoint map
        endpoint_map = {
            'groups': {},
            'endpoints': []
        }
        
        for endpoint in self.endpoints:
            group = endpoint.model
            if group not in endpoint_map['groups']:
                endpoint_map['groups'][group] = []
            
            endpoint_map['groups'][group].append({
                'path': endpoint.path,
                'method': endpoint.method,
                'operation': endpoint.operation,
                'description': endpoint.description
            })
            
            endpoint_map['endpoints'].append({
                'path': endpoint.path,
                'method': endpoint.method,
                'group': group,
                'security': endpoint.security,
                'business_logic': endpoint.business_logic
            })
        
        # Relationship graph
        relationship_graph = {
            'nodes': [{'id': node, 'label': node} for node in self.graph.nodes()],
            'edges': [
                {
                    'from': edge[0],
                    'to': edge[1],
                    'type': self.graph.edges[edge].get('relationship_type', 'related')
                }
                for edge in self.graph.edges()
            ]
        }
        
        # Architecture diagram
        architecture_diagram = {
            'layers': [
                {
                    'name': 'Presentation Layer',
                    'components': ['API Endpoints', 'Authentication', 'Validation']
                },
                {
                    'name': 'Business Logic Layer',
                    'components': ['Services', 'Business Rules', 'Workflows']
                },
                {
                    'name': 'Data Access Layer',
                    'components': ['Models', 'Repositories', 'Database']
                },
                {
                    'name': 'Infrastructure Layer',
                    'components': ['Caching', 'Logging', 'Monitoring']
                }
            ],
            'connections': [
                {'from': 'API Endpoints', 'to': 'Services'},
                {'from': 'Services', 'to': 'Models'},
                {'from': 'Models', 'to': 'Database'}
            ]
        }
        
        return VisualRepresentation(
            model_diagram=model_diagram,
            endpoint_map=endpoint_map,
            relationship_graph=relationship_graph,
            architecture_diagram=architecture_diagram
        )
    
    def _analyze_business_workflows(self) -> List[Dict[str, Any]]:
        """Analyze business workflows from requirements"""
        
        workflows = []
        
        for rule in self.requirements.business_rules:
            if rule.context == "workflow":
                workflow = {
                    'name': f"Workflow: {rule.condition}",
                    'steps': [
                        {'step': 1, 'action': rule.condition, 'type': 'condition'},
                        {'step': 2, 'action': rule.action, 'type': 'action'}
                    ],
                    'triggers': [rule.condition],
                    'outcomes': [rule.action],
                    'priority': rule.priority
                }
                workflows.append(workflow)
        
        # Add common workflows based on models
        if any(model['name'].lower() == 'order' for model in self.requirements.models):
            workflows.append({
                'name': 'Order Processing Workflow',
                'steps': [
                    {'step': 1, 'action': 'Create order', 'type': 'action'},
                    {'step': 2, 'action': 'Validate order', 'type': 'validation'},
                    {'step': 3, 'action': 'Process payment', 'type': 'action'},
                    {'step': 4, 'action': 'Update inventory', 'type': 'action'},
                    {'step': 5, 'action': 'Send confirmation', 'type': 'notification'}
                ],
                'triggers': ['order_created'],
                'outcomes': ['order_confirmed', 'order_failed'],
                'priority': 1
            })
        
        return workflows
    
    def _generate_architecture_recommendations(self) -> List[Dict[str, Any]]:
        """Generate architecture recommendations based on requirements"""
        
        recommendations = []
        
        # Database recommendations
        if len(self.requirements.models) > 10:
            recommendations.append({
                'category': 'Database',
                'recommendation': 'Consider database sharding or read replicas',
                'reason': 'Large number of models detected',
                'priority': 'medium',
                'implementation': 'Set up read replicas for query optimization'
            })
        
        # Caching recommendations
        if self.requirements.caching or len(self.endpoints) > 20:
            recommendations.append({
                'category': 'Performance',
                'recommendation': 'Implement Redis caching',
                'reason': 'High number of endpoints or caching enabled',
                'priority': 'high',
                'implementation': 'Add Redis for session storage and query caching'
            })
        
        # Security recommendations
        if self.requirements.auth_type.value != "none":
            recommendations.append({
                'category': 'Security',
                'recommendation': 'Implement rate limiting',
                'reason': 'Authentication enabled',
                'priority': 'high',
                'implementation': 'Add rate limiting middleware to prevent abuse'
            })
        
        # Monitoring recommendations
        recommendations.append({
            'category': 'Monitoring',
            'recommendation': 'Add application monitoring',
            'reason': 'Production readiness',
            'priority': 'medium',
            'implementation': 'Integrate with monitoring tools like Prometheus or DataDog'
        })
        
        # Scalability recommendations
        if self.requirements.real_time or self.requirements.background_tasks:
            recommendations.append({
                'category': 'Scalability',
                'recommendation': 'Implement message queue',
                'reason': 'Real-time features or background tasks detected',
                'priority': 'high',
                'implementation': 'Add Redis or RabbitMQ for task queuing'
            })
        
        return recommendations
    
    def _calculate_complexity_metrics(self) -> Dict[str, Any]:
        """Calculate project complexity metrics"""
        
        return {
            'model_count': len(self.requirements.models),
            'endpoint_count': len(self.endpoints),
            'relationship_count': len(self.requirements.relationships),
            'business_rule_count': len(self.requirements.business_rules),
            'complexity_score': self._calculate_complexity_score(),
            'estimated_development_time': self._estimate_development_time(),
            'recommended_team_size': self._recommend_team_size()
        }
    
    def _calculate_complexity_score(self) -> float:
        """Calculate overall complexity score (0-10)"""
        
        score = 0.0
        
        # Model complexity
        score += min(len(self.requirements.models) * 0.5, 3.0)
        
        # Relationship complexity
        score += min(len(self.requirements.relationships) * 0.3, 2.0)
        
        # Endpoint complexity
        score += min(len(self.endpoints) * 0.1, 2.0)
        
        # Feature complexity
        feature_count = sum([
            self.requirements.cors_enabled,
            self.requirements.rate_limiting,
            self.requirements.caching,
            self.requirements.file_uploads,
            self.requirements.real_time,
            self.requirements.background_tasks
        ])
        score += min(feature_count * 0.3, 2.0)
        
        # Authentication complexity
        auth_complexity = {
            'none': 0, 'api_key': 0.2, 'session': 0.4, 'jwt': 0.6, 'oauth2': 1.0
        }
        score += auth_complexity.get(self.requirements.auth_type.value, 0)
        
        return min(score, 10.0)
    
    def _estimate_development_time(self) -> str:
        """Estimate development time based on complexity"""
        
        complexity = self._calculate_complexity_score()
        
        if complexity <= 3:
            return "1-2 weeks"
        elif complexity <= 5:
            return "2-4 weeks"
        elif complexity <= 7:
            return "1-2 months"
        else:
            return "2-4 months"
    
    def _recommend_team_size(self) -> str:
        """Recommend team size based on complexity"""
        
        complexity = self._calculate_complexity_score()
        
        if complexity <= 3:
            return "1-2 developers"
        elif complexity <= 5:
            return "2-3 developers"
        elif complexity <= 7:
            return "3-4 developers"
        else:
            return "4-6 developers"
    
    def _analyze_security_requirements(self) -> Dict[str, Any]:
        """Analyze security requirements and recommendations"""
        
        security_analysis = {
            'authentication_type': self.requirements.auth_type.value,
            'security_features': [],
            'vulnerabilities': [],
            'recommendations': []
        }
        
        # Identify security features
        if self.requirements.auth_type.value != "none":
            security_analysis['security_features'].append('Authentication')
        
        if self.requirements.rate_limiting:
            security_analysis['security_features'].append('Rate Limiting')
        
        if self.requirements.cors_enabled:
            security_analysis['security_features'].append('CORS Configuration')
        
        # Identify potential vulnerabilities
        if self.requirements.auth_type.value == "none" and any(
            'user' in model['name'].lower() for model in self.requirements.models
        ):
            security_analysis['vulnerabilities'].append({
                'type': 'No Authentication',
                'severity': 'high',
                'description': 'User management without authentication'
            })
        
        if self.requirements.file_uploads and not self.requirements.rate_limiting:
            security_analysis['vulnerabilities'].append({
                'type': 'Unprotected File Upload',
                'severity': 'medium',
                'description': 'File uploads without rate limiting'
            })
        
        # Security recommendations
        security_analysis['recommendations'] = [
            'Implement input validation for all endpoints',
            'Use HTTPS in production',
            'Implement proper error handling to avoid information leakage',
            'Add request logging for security monitoring',
            'Implement API versioning for security updates'
        ]
        
        return security_analysis
    
    def _analyze_performance_requirements(self) -> Dict[str, Any]:
        """Analyze performance requirements and recommendations"""
        
        performance_analysis = {
            'caching_strategy': 'none',
            'database_optimization': [],
            'scaling_considerations': [],
            'performance_recommendations': []
        }
        
        # Caching strategy
        if self.requirements.caching:
            performance_analysis['caching_strategy'] = 'redis'
        elif len(self.endpoints) > 10:
            performance_analysis['caching_strategy'] = 'recommended'
        
        # Database optimization
        if self.requirements.database_type in [DatabaseType.POSTGRESQL, DatabaseType.MYSQL]:
            performance_analysis['database_optimization'] = [
                'Index frequently queried fields',
                'Use connection pooling',
                'Implement query optimization'
            ]
        
        # Scaling considerations
        if self.requirements.real_time:
            performance_analysis['scaling_considerations'].append('WebSocket scaling')
        
        if self.requirements.background_tasks:
            performance_analysis['scaling_considerations'].append('Task queue scaling')
        
        if len(self.requirements.models) > 5:
            performance_analysis['scaling_considerations'].append('Database scaling')
        
        # Performance recommendations
        performance_analysis['performance_recommendations'] = [
            'Implement pagination for list endpoints',
            'Use async/await patterns where possible',
            'Add response compression',
            'Implement database query optimization',
            'Add performance monitoring'
        ]
        
        return performance_analysis
    
    def _get_fastapi_dependencies(self) -> List[str]:
        """Get FastAPI dependencies based on requirements"""
        
        dependencies = [
            'fastapi>=0.104.1',
            'uvicorn[standard]>=0.24.0',
            'pydantic>=2.5.0',
            'pydantic-settings>=2.1.0'
        ]
        
        # Database dependencies
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            dependencies.extend(['sqlalchemy>=2.0.23', 'psycopg2-binary>=2.9.9', 'alembic>=1.13.0'])
        elif self.requirements.database_type == DatabaseType.MYSQL:
            dependencies.extend(['sqlalchemy>=2.0.23', 'pymysql>=1.1.0', 'alembic>=1.13.0'])
        elif self.requirements.database_type == DatabaseType.SQLITE:
            dependencies.extend(['sqlalchemy>=2.0.23', 'alembic>=1.13.0'])
        elif self.requirements.database_type == DatabaseType.MONGODB:
            dependencies.extend(['motor>=3.3.2', 'beanie>=1.23.6'])
        
        # Authentication dependencies
        if self.requirements.auth_type == AuthType.JWT:
            dependencies.extend(['python-jose[cryptography]>=3.3.0', 'passlib[bcrypt]>=1.7.4'])
        elif self.requirements.auth_type == AuthType.OAUTH2:
            dependencies.extend(['authlib>=1.2.1', 'httpx>=0.25.2'])
        
        # Additional feature dependencies
        if self.requirements.caching or self.requirements.use_redis:
            dependencies.append('redis>=5.0.1')
        
        if self.requirements.use_celery or self.requirements.background_tasks:
            dependencies.extend(['celery>=5.3.4', 'redis>=5.0.1'])
        
        if self.requirements.file_uploads:
            dependencies.append('python-multipart>=0.0.6')
        
        if self.requirements.rate_limiting:
            dependencies.append('slowapi>=0.1.9')
        
        if self.requirements.real_time:
            dependencies.append('websockets>=12.0')
        
        # GraphQL dependencies
        if self.requirements.api_type == APIType.GRAPHQL:
            dependencies.extend(['strawberry-graphql>=0.215.1', 'strawberry-graphql[fastapi]'])
        
        # Development dependencies
        dev_dependencies = [
            'pytest>=7.4.3',
            'pytest-asyncio>=0.21.1',
            'httpx>=0.25.2',
            'black>=23.11.0',
            'isort>=5.12.0',
            'flake8>=6.1.0',
            'mypy>=1.7.1',
            'pre-commit>=3.6.0'
        ]
        
        return dependencies + dev_dependencies
    
    def _get_django_dependencies(self) -> List[str]:
        """Get Django dependencies based on requirements"""
        
        dependencies = [
            'Django>=4.2.7',
            'djangorestframework>=3.14.0',
            'django-cors-headers>=4.3.1'
        ]
        
        # Database dependencies
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            dependencies.append('psycopg2-binary>=2.9.9')
        elif self.requirements.database_type == DatabaseType.MYSQL:
            dependencies.append('mysqlclient>=2.2.0')
        
        # Authentication dependencies
        if self.requirements.auth_type == AuthType.JWT:
            dependencies.append('djangorestframework-simplejwt>=5.3.0')
        elif self.requirements.auth_type == AuthType.OAUTH2:
            dependencies.append('django-oauth-toolkit>=1.7.1')
        
        # Additional features
        if self.requirements.caching or self.requirements.use_redis:
            dependencies.extend(['redis>=5.0.1', 'django-redis>=5.4.0'])
        
        if self.requirements.use_celery or self.requirements.background_tasks:
            dependencies.extend(['celery>=5.3.4', 'django-celery-beat>=2.5.0'])
        
        if self.requirements.rate_limiting:
            dependencies.append('django-ratelimit>=4.1.0')
        
        # GraphQL dependencies
        if self.requirements.api_type == APIType.GRAPHQL:
            dependencies.extend(['graphene-django>=3.1.5', 'django-graphql-jwt>=0.3.4'])
        
        return dependencies
    
    def _get_fastapi_configuration(self) -> Dict[str, Any]:
        """Get FastAPI configuration"""
        
        return {
            'app_settings': {
                'title': f"{self.requirements.project_name.replace('_', ' ').title()} API",
                'description': self.requirements.description,
                'version': '1.0.0',
                'docs_url': '/docs',
                'redoc_url': '/redoc'
            },
            'cors_settings': {
                'allow_origins': ['*'] if self.requirements.cors_enabled else [],
                'allow_credentials': True,
                'allow_methods': ['*'],
                'allow_headers': ['*']
            },
            'database_settings': {
                'url': self._get_database_url(),
                'echo': False,
                'pool_size': 10,
                'max_overflow': 20
            }
        }
    
    def _get_django_configuration(self) -> Dict[str, Any]:
        """Get Django configuration"""
        
        return {
            'installed_apps': [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'rest_framework',
                'corsheaders'
            ],
            'middleware': [
                'corsheaders.middleware.CorsMiddleware',
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware'
            ],
            'database_settings': {
                'default': {
                    'ENGINE': self._get_django_database_engine(),
                    'NAME': self.requirements.project_name,
                    'USER': 'user',
                    'PASSWORD': 'password',
                    'HOST': 'localhost',
                    'PORT': '5432'
                }
            }
        }
    
    def _get_deployment_configuration(self) -> Dict[str, Any]:
        """Get deployment configuration"""
        
        return {
            'docker': {
                'base_image': 'python:3.11-slim',
                'port': 8000,
                'environment_variables': [
                    'DATABASE_URL',
                    'SECRET_KEY',
                    'DEBUG',
                    'ALLOWED_HOSTS'
                ]
            },
            'docker_compose': {
                'services': ['api', 'database'],
                'volumes': ['postgres_data'] if self.requirements.database_type == DatabaseType.POSTGRESQL else [],
                'networks': ['api_network']
            },
            'kubernetes': {
                'deployments': ['api-deployment', 'database-deployment'],
                'services': ['api-service', 'database-service'],
                'configmaps': ['api-config'],
                'secrets': ['api-secrets']
            }
        }
    
    def _get_database_url(self) -> str:
        """Get database URL based on database type"""
        
        if self.requirements.database_type == DatabaseType.POSTGRESQL:
            return "postgresql://user:password@localhost:5432/dbname"
        elif self.requirements.database_type == DatabaseType.MYSQL:
            return "mysql://user:password@localhost:3306/dbname"
        elif self.requirements.database_type == DatabaseType.SQLITE:
            return "sqlite:///./app.db"
        else:
            return "sqlite:///./app.db"
    
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

# Main execution for testing
if __name__ == "__main__":
    from nlp_extractor import NLPExtractor
    
    # Test with a complex description
    extractor = NLPExtractor()
    requirements = extractor.extract_requirements(
        "Create a modern e-commerce platform with user authentication, product management, and order processing"
    )
    
    analyzer = ProjectAnalyzer(requirements)
    analysis = analyzer.analyze_complete_project()
    
    print(f"Project Structure: {len(analysis['project_structure']['directories'])} directories")
    print(f"Endpoints: {len(analysis['endpoints'])} endpoints")
    print(f"Complexity Score: {analysis['complexity_metrics']['complexity_score']:.1f}/10")
    print(f"Estimated Time: {analysis['complexity_metrics']['estimated_development_time']}")
    print(f"Recommendations: {len(analysis['architecture_recommendations'])} recommendations")

