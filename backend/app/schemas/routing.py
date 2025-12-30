"""
app.schema.routing
"""
from pydantic import BaseModel, Field
from app.state import Route


class RouteDecision(BaseModel):
    route: Route = Field(description="Which specialist handles user request")
    confidence: float = Field(ge=0.0, le=1.0, description="Router confidence")
    reason: str = Field(description="Short reason for observability")
    needs_human_review: bool = Field(
        default=False,
        description="Sensitive requests or risky actions",
    )
