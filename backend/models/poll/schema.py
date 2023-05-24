from pydantic import BaseModel


class PollCreate(BaseModel):
    title: str
