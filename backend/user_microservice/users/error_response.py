from pydantic import BaseModel, Field

class ErrorResponseModel(BaseModel):
    detail: str = Field(..., description="Detailed error message")
    error_code: str = Field(..., description="Error code for the specific error")
    resolution: str = Field(None, description="Suggested resolution for the error")
