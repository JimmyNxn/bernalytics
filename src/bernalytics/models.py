"""
Pydantic model for LinkedIn job search term counts.
"""

from pydantic import BaseModel, ConfigDict, Field


class JobCounts(BaseModel):
    """Model representing counts for three search terms."""

    data_engineer: int = Field(default=0, ge=0, description='Count for "Data Engineer"')
    junior_data_engineer: int = Field(default=0, ge=0, description='Count for "Junior Data Engineer"')
    senior_data_engineer: int = Field(default=0, ge=0, description='Count for "Senior Data Engineer"')

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data_engineer": 237,
                "junior_data_engineer": 10,
                "senior_data_engineer": 191,
            }
        }
    )
