from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class Widget:
    id: int
    key: str
    name: str
    theme: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    allowed_domains: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True