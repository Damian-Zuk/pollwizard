from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints, field_validator


TitleStr = Annotated[str, StringConstraints(max_length=200)]
OptionStr = Annotated[str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True)]


class PollCreate(BaseModel):
    title: TitleStr
    options: Annotated[list[OptionStr], Field(min_length=2, max_length=16)]

    @field_validator("options")
    @classmethod
    def validate_options(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("Options must be unique.")
        return value
