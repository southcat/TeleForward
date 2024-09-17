from pydantic import BaseModel


class CodeRequest(BaseModel):
    phone_number: str
    code: str
    phone_code_hash: str
    pass_word: str