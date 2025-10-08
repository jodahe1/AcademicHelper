# Academic Assignment Helper & Plagiarism Detector (RAG-Powered)

🧠 **A comprehensive backend + n8n automation system for academic assignment analysis with RAG-powered research suggestions and AI-driven plagiarism detection.**

## 🚀 Features

- **JWT-based Authentication** - Secure student registration and login
- **File Upload Processing** - Support for PDF, DOCX, and TXT files
- **RAG-Powered Research** - Vector similarity search against academic sources
- **AI Plagiarism Detection** - Advanced similarity analysis with flagged sections
- **Automated Workflow** - n8n orchestration for seamless processing
- **Vector Database** - PostgreSQL with pgvector for embeddings storage

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │───▶│     n8n     │───▶│ PostgreSQL  │
│  (Backend)  │    │ (Workflow)  │    │ + pgvector  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ JWT Auth    │    │ AI Analysis │    │ Vector DB   │
│ File Upload │    │ RAG Search  │    │ Embeddings  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🛠️ Setup Instructions

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key or Gemini API Key
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd AcademicHelper
```

### 2. Environment Configuration
```bash
cp env.example .env
# Edit .env with your API keys
```

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
# Database will auto-initialize with init.sql
# Access pgAdmin at http://localhost:8080
# Login: admin@academic.com / admin123
```

### 5. Import n8n Workflow
```bash
# Access n8n at http://localhost:5678
# Login: admin / admin123
# Import assignment_analysis_workflow.json
```

## 📡 API Endpoints

### Authentication
- `POST /auth/register` - Register new student
- `POST /auth/login` - Login and get JWT token

### Assignment Processing
- `POST /upload` - Upload assignment file (requires JWT)
- `GET /analysis/{id}` - Get analysis results (requires JWT)

### Research Sources
- `GET /sources` - Search academic sources via RAG
- `POST /sources/ingest` - Generate embeddings for sources

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_key_here
# OR
OPENAI_API_KEY=your_openai_key_here

# Database
DATABASE_URL=postgresql://student:secure_password@postgres:5432/academic_helper

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
```

## 🧪 Testing

### 1. Register a Student
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "password123",
    "full_name": "Test Student",
    "student_id": "STU001"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "password123"
  }'
```

### 3. Upload Assignment
```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@sample_assignment.pdf"
```

## 🗄️ Database Schema

### Tables
- **students** - User authentication and profiles
- **assignments** - Uploaded assignment metadata
- **analysis_results** - AI analysis results with plagiarism scores
- **academic_sources** - RAG knowledge base with vector embeddings

## 🔍 RAG Implementation

### Vector Search Pipeline
1. **Document Ingestion** - Academic papers → text chunks → embeddings
2. **Query Processing** - Assignment text → embedding → similarity search  
3. **Context Retrieval** - Top-k relevant sources for AI analysis

### Supported Models
- **Gemini** - `text-embedding-004` (preferred)
- **OpenAI** - `text-embedding-ada-002` (fallback)

## 🐳 Docker Services

- **backend** - FastAPI application (port 8000)
- **n8n** - Workflow automation (port 5678)
- **postgres** - Database with pgvector (port 5432)
- **pgadmin** - Database GUI (port 8080)

## 🔒 Security Features

- JWT-based authentication with role permissions
- Password hashing with bcrypt
- CORS protection for API endpoints
- File upload validation and size limits

## 📊 Monitoring

### Service Health
- Backend: `GET http://localhost:8000/health`
- n8n: `http://localhost:5678`
- pgAdmin: `http://localhost:8080`

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   docker-compose down
   docker-compose up -d postgres
   # Wait 30 seconds, then start other services
   ```

2. **n8n Workflow Not Triggering**
   - Check webhook URL in workflow settings
   - Verify n8n service is running
   - Check network connectivity between services

3. **Embedding Generation Fails**
   - Verify API keys in .env file
   - Check API rate limits
   - Ensure sufficient credits/quota

## 📁 Project Structure

```
AcademicHelper/
├── backend/                 # FastAPI application
│   ├── main.py             # API routes and endpoints
│   ├── auth.py             # JWT authentication
│   ├── models.py           # Database models
│   ├── rag_service.py      # Vector search and embeddings
│   ├── schemas.py          # Pydantic models
│   ├── utils.py            # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container config
├── workflows/              # n8n workflow exports
│   └── assignment_analysis_workflow.json
├── data/                   # Sample data for testing
│   └── sample_academic_sources.json
├── docker-compose.yml      # Service orchestration
├── init.sql               # Database initialization
├── .env.example           # Environment template
└── README.md              # This file
```

## 🎯 Key Features Demonstrated

- **RAG Pipeline** - Vector similarity search with academic sources
- **AI Integration** - OpenAI/Gemini for analysis and plagiarism detection
- **Workflow Automation** - Complex n8n processing pipeline
- **Security** - JWT authentication and authorization
- **Scalability** - Docker containerization and service orchestration

## 📝 License

This project is for educational and demonstration purposes.

---

**Built with ❤️ using FastAPI, n8n, PostgreSQL, and Docker**
