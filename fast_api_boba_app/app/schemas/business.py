from typing import Optional
from pydantic import BaseModel

# Shared properties
class BusinessBase(BaseModel):
    business_id: str = None
    name: str = None
    address: str = None
    city: str = None
    state: str = None
    overall_star: float = None
    review_count: int = None
    