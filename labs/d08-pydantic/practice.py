from pydantic import BaseModel, field_validator
import json
# class C(BaseModel):
#     max_tokens:int = Field(default=512, ge=1, le=4096)

class Q(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def strip_and_check(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("prompt must not be empty or only spaces")
        return v

print(Q(prompt="  hello   "))

print(json.dumps(Q.model_json_schema(), indent=2))