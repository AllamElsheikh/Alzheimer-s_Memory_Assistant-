# Faker Backend - Alzheimer's Memory Assistant API

Evidence-based FastAPI backend for Arabic-speaking Alzheimer's patients using Google Gemma 3n multimodal AI.

## Features

- **Multimodal AI Conversations**: Text, image, and audio processing with Gemma 3n
- **Cognitive Assessments**: Automated and interactive cognitive evaluations
- **Smart Reminders**: Medication, appointments, and activity reminders
- **Patient Management**: Comprehensive patient profiles and history
- **Arabic Language Support**: Culturally adapted responses in Egyptian Arabic
- **Caregiver Integration**: API endpoints for caregiver dashboard

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Google AI Studio API Key

### Installation

1. **Clone and navigate to backend**:
```bash
cd faker/backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Environment setup**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database setup**:
```bash
# Create PostgreSQL database
createdb faker_db

# Run migrations (auto-created on startup)
```

6. **Start the server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status

### Conversations
- `POST /api/v1/conversations/text` - Text conversation
- `POST /api/v1/conversations/multimodal` - Multimodal conversation
- `GET /api/v1/conversations/patient/{id}` - Patient conversations
- `GET /api/v1/conversations/session/{id}` - Session conversations

### Patients
- `POST /api/v1/patients/` - Create patient
- `GET /api/v1/patients/{id}` - Get patient
- `PUT /api/v1/patients/{id}` - Update patient
- `DELETE /api/v1/patients/{id}` - Delete patient

### Assessments
- `POST /api/v1/assessments/` - Create assessment
- `GET /api/v1/assessments/patient/{id}` - Patient assessments
- `POST /api/v1/assessments/interactive` - Interactive assessment
- `GET /api/v1/assessments/tasks/{type}` - Assessment tasks

### Reminders
- `POST /api/v1/reminders/` - Create reminder
- `GET /api/v1/reminders/patient/{id}` - Patient reminders
- `GET /api/v1/reminders/due` - Due reminders
- `PUT /api/v1/reminders/{id}` - Update reminder
- `POST /api/v1/reminders/{id}/complete` - Complete reminder

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://faker_user:faker_pass@localhost:5432/faker_db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT secret key | Change in production |
| `ENVIRONMENT` | Environment mode | `development` |

### Gemma 3n Configuration

```python
GEMMA_MODEL = "gemma-3-27b-it"
MAX_TOKENS = 1000
TEMPERATURE = 0.7
```

## Database Schema

### Core Models

- **Patient**: Patient profiles and medical information
- **Conversation**: AI conversation history with multimodal support
- **Assessment**: Cognitive assessment results and scoring
- **Reminder**: Smart reminders with recurrence patterns
- **Memory**: Patient memory storage and associations
- **Caregiver**: Caregiver profiles and access control
- **Alert**: Caregiver notifications and alerts

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app/
isort app/
```

### Database Migrations

```bash
# Auto-generated on startup
# Manual migrations with Alembic if needed
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Production Deployment

### Docker Setup

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

1. Set production environment variables
2. Use PostgreSQL and Redis instances
3. Configure proper CORS origins
4. Set up SSL/TLS termination
5. Configure logging and monitoring

## Security

- API key management through environment variables
- CORS configuration for allowed origins
- Input validation with Pydantic models
- SQL injection prevention with SQLAlchemy
- Rate limiting (implement with Redis)

## Monitoring

- Health check endpoints
- Structured logging
- Database connection monitoring
- Gemma API availability checks

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review logs for error details
3. Verify environment configuration
4. Test Gemma API connectivity
