# Standard Libraries
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel


class MyUserModel(BaseModel):
    password: str
    is_active: Optional[bool]
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_team: Optional[bool]
    is_staff: Optional[bool]
    has_perm: Optional[bool]
