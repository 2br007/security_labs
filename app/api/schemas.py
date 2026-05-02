from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    # This allows Pydantic to read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
