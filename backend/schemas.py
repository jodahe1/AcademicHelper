from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    student_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    student_id: str

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    assignment_id: int
    message: str = "upload accepted"


class AnalysisResultResponse(BaseModel):
    id: int
    assignment_id: int
    suggested_sources: Optional[Any] = None
    plagiarism_score: Optional[float] = None
    flagged_sections: Optional[Any] = None
    research_suggestions: Optional[str] = None
    citation_recommendations: Optional[str] = None
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True


class SourcesQuery(BaseModel):
    q: str = Field(..., description="Search query for academic sources")
    limit: int = 5


class SourceItem(BaseModel):
    id: int
    title: str
    authors: str
    publication_year: Optional[int] = None
    source_type: Optional[str] = None
