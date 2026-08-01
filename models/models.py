from pydantic import BaseModel

class InputSchema(BaseModel):
    input: str

class OutputSchema(BaseModel):
    output: str