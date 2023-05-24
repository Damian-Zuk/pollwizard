from pydantic import BaseModel


class OptionCreate(BaseModel):
    value: str
