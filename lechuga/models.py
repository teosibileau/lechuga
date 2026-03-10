from pydantic import BaseModel


class Rate(BaseModel):
    date: str
    usd: float
    euro: float
