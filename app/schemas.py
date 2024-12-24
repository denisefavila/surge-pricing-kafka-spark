from typing import Dict, List, Optional

from pydantic import BaseModel


class PositionsCount(BaseModel):
    region: str
    count: int


class PositionsCountResponse(BaseModel):
    position_counts: Optional[List[PositionsCount]]
