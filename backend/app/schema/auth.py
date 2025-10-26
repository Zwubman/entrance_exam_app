from pydantic import BaseModel

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str