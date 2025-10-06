from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, get_db
from models import Student, Assignment, AnalysisResult, AcademicSource
from schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    StudentResponse,
    UploadResponse,
    AnalysisResultResponse,
    SourcesQuery,
    SourceItem,
)
from auth import hash_password, verify_password, create_access_token, get_current_student
from utils import save_upload_file
from rag_service import ingest_missing_embeddings, vector_search

app = FastAPI(title="Academic Helper API")

# CORS for local testing and n8n callbacks (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5678", "http://localhost:8080",
                   "http://localhost:3000", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    # Create tables on startup (idempotent)
    init_db()


# -------- Auth Routes --------
@app.post("/auth/register", response_model=StudentResponse)
def register_student(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")
    student = Student(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        student_id=payload.student_id,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == payload.email).first()
    if not student or not verify_password(payload.password, student.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=student.email)
    return TokenResponse(access_token=token)


# -------- Upload & Analysis --------
@app.post("/upload", response_model=UploadResponse)
def upload_assignment(
    file: UploadFile = File(...),
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    saved_path = save_upload_file(file)
    assignment = Assignment(
        student_id=current_student.id,
        filename=saved_path,
        original_text=None,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    # TODO: trigger n8n via webhook in Phase 4
    return UploadResponse(assignment_id=assignment.id)


@app.get("/analysis/{analysis_id}", response_model=AnalysisResultResponse)
def get_analysis(
    analysis_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    analysis = (
        db.query(AnalysisResult)
        .join(Assignment, AnalysisResult.assignment_id == Assignment.id)
        .filter(AnalysisResult.id == analysis_id, Assignment.student_id == current_student.id)
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


# -------- Sources (placeholder search) --------
@app.get("/sources", response_model=list[SourceItem])
def search_sources(q: str, limit: int = 5, db: Session = Depends(get_db)):
    # Use vector similarity if embeddings exist; fallback to ILIKE
    try:
        results = vector_search(db, q, limit=limit)
        if results:
            return [
                SourceItem(
                    id=r.id,
                    title=r.title,
                    authors=r.authors,
                    publication_year=r.publication_year,
                    source_type=r.source_type,
                )
                for r in results
            ]
    except Exception:
        # fall back to ILIKE when embedding model is unavailable or not configured
        pass

    results = (
        db.query(AcademicSource)
        .filter(
            (AcademicSource.title.ilike(f"%{q}%"))
            | (AcademicSource.authors.ilike(f"%{q}%"))
        )
        .limit(limit)
        .all()
    )
    return [
        SourceItem(
            id=r.id,
            title=r.title,
            authors=r.authors,
            publication_year=r.publication_year,
            source_type=r.source_type,
        )
        for r in results
    ]


@app.post("/sources/ingest")
def ingest_sources_embeddings(db: Session = Depends(get_db)):
    count = ingest_missing_embeddings(db)
    return {"embedded": count}
