from pydantic import BaseModel, constr, conlist, validator


class PollCreate(BaseModel):
    title: constr(max_length=200)
    options: conlist(str, min_items=2, max_items=16)

    @validator('options', each_item=True)
    def validate_option_length(cls, value):
        if len(value) < 1 or len(value) > 200:
            raise ValueError("Each option must have a length between 1 and 200 characters.")
        return value
