"""
API Generator SDK - Custom Exceptions
====================================

Custom exception classes for the API Generator SDK providing meaningful
error messages for programmatic users.
"""

class APIGeneratorError(Exception):
    """Base exception for API Generator SDK"""
    pass

class GenerationError(APIGeneratorError):
    """Raised when API generation fails"""
    pass

class InvalidDescriptionError(APIGeneratorError):
    """Raised when the provided description is invalid or cannot be parsed"""
    pass

class FrameworkNotSupportedError(APIGeneratorError):
    """Raised when an unsupported framework is specified"""
    pass

class DatabaseNotSupportedError(APIGeneratorError):
    """Raised when an unsupported database is specified"""
    pass

class AuthMethodNotSupportedError(APIGeneratorError):
    """Raised when an unsupported authentication method is specified"""
    pass

class ConfigurationError(APIGeneratorError):
    """Raised when SDK configuration is invalid"""
    pass

class NLPParsingError(APIGeneratorError):
    """Raised when NLP parsing fails"""
    pass

class ProjectStructureError(APIGeneratorError):
    """Raised when project structure analysis fails"""
    pass

class CodeGenerationError(APIGeneratorError):
    """Raised when code generation fails"""
    pass

class ValidationError(APIGeneratorError):
    """Raised when input validation fails"""
    pass

class TemplateError(APIGeneratorError):
    """Raised when template processing fails"""
    pass

class ExtensionError(APIGeneratorError):
    """Raised when extension registration or execution fails"""
    pass

