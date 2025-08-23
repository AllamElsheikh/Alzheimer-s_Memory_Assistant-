"""
Cognitive Assessments API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.services.database import get_db
from app.services.gemma_service import GemmaService
from app.models.database import Assessment, Patient
from sqlalchemy import select

router = APIRouter()

class AssessmentRequest(BaseModel):
    patient_id: int
    assessment_type: str  # memory, attention, language, executive, comprehensive
    administered_by: str = "AI"

class AssessmentResponse(BaseModel):
    id: int
    patient_id: int
    assessment_type: str
    scores: Dict[str, Any]
    severity_level: str
    recommendations: List[str]
    timestamp: datetime

class CognitiveTask(BaseModel):
    task_type: str
    question: str
    expected_response: Optional[str] = None
    scoring_criteria: Dict[str, Any]

@router.post("/", response_model=AssessmentResponse)
async def create_assessment(
    request: AssessmentRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create and administer a cognitive assessment"""
    
    # Verify patient exists
    patient_result = await db.execute(select(Patient).where(Patient.id == request.patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Generate assessment using Gemma service
    gemma_service = GemmaService()
    assessment_data = await _generate_assessment(
        gemma_service, 
        request.assessment_type, 
        patient
    )
    
    # Create assessment record
    assessment = Assessment(
        patient_id=request.patient_id,
        assessment_type=request.assessment_type,
        scores=assessment_data["scores"],
        severity_level=assessment_data["severity_level"],
        recommendations=assessment_data["recommendations"],
        raw_data=assessment_data["raw_data"],
        administered_by=request.administered_by
    )
    
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    
    return AssessmentResponse(
        id=assessment.id,
        patient_id=assessment.patient_id,
        assessment_type=assessment.assessment_type,
        scores=assessment.scores,
        severity_level=assessment.severity_level,
        recommendations=assessment.recommendations,
        timestamp=assessment.timestamp
    )

@router.get("/patient/{patient_id}")
async def get_patient_assessments(
    patient_id: int,
    assessment_type: Optional[str] = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get assessments for a specific patient"""
    
    query = select(Assessment).where(Assessment.patient_id == patient_id)
    
    if assessment_type:
        query = query.where(Assessment.assessment_type == assessment_type)
    
    query = query.order_by(Assessment.timestamp.desc()).limit(limit)
    
    result = await db.execute(query)
    assessments = result.scalars().all()
    
    return [
        {
            "id": assessment.id,
            "assessment_type": assessment.assessment_type,
            "scores": assessment.scores,
            "severity_level": assessment.severity_level,
            "recommendations": assessment.recommendations,
            "timestamp": assessment.timestamp
        }
        for assessment in assessments
    ]

@router.get("/tasks/{assessment_type}")
async def get_assessment_tasks(assessment_type: str):
    """Get cognitive tasks for a specific assessment type"""
    
    tasks = _get_cognitive_tasks(assessment_type)
    return {"assessment_type": assessment_type, "tasks": tasks}

@router.post("/interactive")
async def interactive_assessment(
    patient_id: int,
    task_type: str,
    user_response: str,
    db: AsyncSession = Depends(get_db)
):
    """Process interactive assessment response"""
    
    # Verify patient exists
    patient_result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = patient_result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    gemma_service = GemmaService()
    
    # Analyze response using Gemma
    analysis_prompt = f"""
    تحليل استجابة المريض في تقييم معرفي:
    
    نوع المهمة: {task_type}
    استجابة المريض: {user_response}
    معلومات المريض: الاسم {patient.name}, العمر {patient.age}, المرحلة {patient.diagnosis_stage}
    
    قم بتحليل الاستجابة وتقييم:
    1. مستوى الذاكرة
    2. وضوح التفكير
    3. القدرة اللغوية
    4. التوجه الزمني والمكاني
    5. اقتراحات للتحسين
    
    أعط تقييماً باللغة العربية مع درجة من 1-10.
    """
    
    analysis = await gemma_service.generate_text(analysis_prompt)
    
    return {
        "task_type": task_type,
        "user_response": user_response,
        "analysis": analysis,
        "next_task": _get_next_task(task_type),
        "timestamp": datetime.now()
    }

async def _generate_assessment(gemma_service: GemmaService, assessment_type: str, patient: Patient) -> Dict[str, Any]:
    """Generate assessment using Gemma service"""
    
    assessment_prompt = f"""
    إجراء تقييم معرفي شامل للمريض:
    
    الاسم: {patient.name}
    العمر: {patient.age}
    مرحلة المرض: {patient.diagnosis_stage}
    نوع التقييم: {assessment_type}
    
    قم بتقييم المجالات التالية وأعط درجة من 1-10:
    1. الذاكرة قصيرة المدى
    2. الذاكرة طويلة المدى  
    3. التوجه الزمني والمكاني
    4. القدرة اللغوية
    5. الانتباه والتركيز
    6. الوظائف التنفيذية
    7. المهارات الحركية
    8. الحالة المزاجية
    
    أعط تقييماً شاملاً مع توصيات علاجية باللغة العربية.
    """
    
    assessment_text = await gemma_service.generate_text(assessment_prompt)
    
    # Parse assessment (simplified for demo)
    scores = {
        "memory_short_term": 7.5,
        "memory_long_term": 6.8,
        "orientation": 8.2,
        "language": 7.9,
        "attention": 6.5,
        "executive": 7.1,
        "motor_skills": 8.0,
        "mood": 7.3,
        "overall": 7.4
    }
    
    # Determine severity level
    overall_score = scores["overall"]
    if overall_score >= 8.0:
        severity_level = "normal"
    elif overall_score >= 6.0:
        severity_level = "mild"
    elif overall_score >= 4.0:
        severity_level = "moderate"
    else:
        severity_level = "severe"
    
    recommendations = [
        "تمارين الذاكرة اليومية",
        "أنشطة التحفيز المعرفي",
        "التفاعل الاجتماعي المنتظم",
        "متابعة طبية دورية",
        "استخدام التذكيرات البصرية"
    ]
    
    return {
        "scores": scores,
        "severity_level": severity_level,
        "recommendations": recommendations,
        "raw_data": {
            "assessment_text": assessment_text,
            "assessment_type": assessment_type,
            "patient_info": {
                "name": patient.name,
                "age": patient.age,
                "stage": patient.diagnosis_stage
            }
        }
    }

def _get_cognitive_tasks(assessment_type: str) -> List[CognitiveTask]:
    """Get cognitive tasks for assessment type"""
    
    tasks_map = {
        "memory": [
            CognitiveTask(
                task_type="word_recall",
                question="احفظ هذه الكلمات الثلاث: تفاحة، سيارة، كتاب. سأسألك عنها بعد قليل.",
                scoring_criteria={"max_score": 3, "time_limit": 300}
            ),
            CognitiveTask(
                task_type="story_recall",
                question="احكيلي عن ذكرى جميلة من طفولتك.",
                scoring_criteria={"coherence": 5, "detail": 5}
            )
        ],
        "attention": [
            CognitiveTask(
                task_type="digit_span",
                question="اسمع الأرقام دي وأعيدها: 3-7-2-9",
                scoring_criteria={"max_digits": 7, "accuracy": True}
            )
        ],
        "language": [
            CognitiveTask(
                task_type="naming",
                question="إيه اسم الحاجة دي؟ (صورة قلم)",
                scoring_criteria={"accuracy": True, "fluency": 5}
            )
        ]
    }
    
    return tasks_map.get(assessment_type, [])

def _get_next_task(current_task: str) -> Optional[str]:
    """Get next task in assessment sequence"""
    
    task_sequence = {
        "word_recall": "story_recall",
        "story_recall": "digit_span",
        "digit_span": "naming",
        "naming": None
    }
    
    return task_sequence.get(current_task)
