from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional
from datetime import UTC, datetime, timezone


class UserRole(str, Enum):
    """User role enumeration as specified in API Contracts Plan."""
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(
        default_factory=uuid4,
        frozen=True,
        description="Unique identifier for the user.",
        examples=[str(uuid4())],
        json_schema_extra={"readOnly": True}
    )
    email: EmailStr = Field(
        max_length=255,
        description="User's email address.",
        examples=["john.doe@example.com"],
        json_schema_extra={"format": "email"}
    )
    password_hash: str = Field(
        min_length=1,  # Add this
        max_length=255,
        description="Hashed password for the user.",
        exclude=True,
        json_schema_extra={"writeOnly": True}
    )
    first_name: Optional[str] = Field(
        default=None,
        max_length=100,
        # Remove pattern from here, use validator instead
        title="First Name",
        description="User's first name, alphabetic characters and spaces only.",
        examples=["John"]
    )
    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
        # Remove pattern from here, use validator instead
        title="Last Name",
        description="User's last name, alphabetic characters and spaces only.",
        examples=["Doe"]
    )

    role: UserRole = Field(
        default=UserRole.USER,
        description="User's role in the system.",
        examples=["USER"]
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active.",
        json_schema_extra={"readOnly": False}
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        frozen=True,
        description="Timestamp when the user was created.",
        json_schema_extra={"readOnly": True}
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was last updated.",
        json_schema_extra={"readOnly": True}
    )
    last_login_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the user's last login.",
        json_schema_extra={"readOnly": True}
    )

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and v != "":
            import re
            if not re.match(r"^[a-zA-Z\s]*$", v):
                raise ValueError('Name must contain only alphabetic characters and spaces')
        return v