from enum import Enum

class SummarizeStyle(str, Enum):
    BULLET = "bullet"
    PARAGRAPH = "paragraph"
    EXECUTIVE = "executive"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IssueCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SECURITY = "security"
    ACCOUNT = "account"
    FEATURE_REQUEST = "feature_request"
    OTHER = "other"

class Audience(str,Enum):
    BEGINNER = "beginner"
    DEVELOPER = "developer"
    BACKEND_ENGINEER = "backend_engineer"
    EXECUTIVE = "executive"
    ML_ENGINEER = "ml_engineer"
    DATA_SCIENTIST = "data_scientist"
    AI_ENGINEER = "ai_engineer"
    PRODUCT_MANAGER = "product_manager"
    PROJECT_MANAGER = "project_manager"
    CEO = "ceo"
    CTO = "cto"
    FOUNDER = "founder"
    ENTREPRENEUR = "entrepreneur"
    C_SUITE = "c-suite"

class Tone(str,Enum):
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    CONCISE = "concise"

class Length(str,Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"  

class EmbeddingModels(str,Enum):
    LLAMA_NEMO_EMBED = "llama_nemo_embed"
    LIQUID_LM = "liquid_lm"