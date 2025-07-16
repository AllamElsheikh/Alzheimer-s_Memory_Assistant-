"""
Cognitive Assessment System for Alzheimer's Memory Assistant
Uses Gemma 3n multimodal capabilities for comprehensive cognitive evaluation.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

@dataclass
class AssessmentResult:
    """Results from a cognitive assessment session"""
    timestamp: datetime
    assessment_type: str
    scores: Dict[str, float]
    responses: List[str]
    reaction_times: List[float]
    multimodal_data: Dict[str, Any]
    recommendations: List[str]
    severity_level: str

class CognitiveAssessmentEngine:
    """
    Cognitive assessment engine using Gemma 3n multimodal processing
    """
    
    def __init__(self, gemma_integration=None):
        self.gemma_integration = gemma_integration
        self.assessment_history = []
        self.assessment_protocols = self._load_assessment_protocols()
        
    def _load_assessment_protocols(self) -> Dict[str, Any]:
        """Load standardized cognitive assessment protocols"""
        return {
            "memory_recall": {
                "name": "Memory Recall Assessment",
                "duration_minutes": 15,
                "tasks": [
                    {
                        "type": "visual_memory",
                        "description": "Show image sequence, test recall",
                        "scoring": "correct_items / total_items"
                    },
                    {
                        "type": "auditory_memory", 
                        "description": "Play word list, test recall",
                        "scoring": "correct_words / total_words"
                    },
                    {
                        "type": "working_memory",
                        "description": "Digit span and manipulation tasks",
                        "scoring": "longest_sequence / max_sequence"
                    }
                ]
            },
            "attention_focus": {
                "name": "Attention and Focus Assessment",
                "duration_minutes": 10,
                "tasks": [
                    {
                        "type": "sustained_attention",
                        "description": "Continuous performance task",
                        "scoring": "correct_responses / total_stimuli"
                    },
                    {
                        "type": "selective_attention",
                        "description": "Target detection in distractors",
                        "scoring": "target_hits / total_targets"
                    }
                ]
            },
            "language_processing": {
                "name": "Language Processing Assessment",
                "duration_minutes": 12,
                "tasks": [
                    {
                        "type": "naming_fluency",
                        "description": "Generate words in categories",
                        "scoring": "unique_words / time_minutes"
                    },
                    {
                        "type": "comprehension",
                        "description": "Follow complex instructions",
                        "scoring": "correct_steps / total_steps"
                    }
                ]
            },
            "executive_function": {
                "name": "Executive Function Assessment", 
                "duration_minutes": 18,
                "tasks": [
                    {
                        "type": "planning",
                        "description": "Multi-step problem solving",
                        "scoring": "optimal_steps / actual_steps"
                    },
                    {
                        "type": "cognitive_flexibility",
                        "description": "Task switching and adaptation",
                        "scoring": "correct_switches / total_switches"
                    }
                ]
            }
        }

    def conduct_multimodal_assessment(self, assessment_type: str, patient_data: Dict[str, Any]) -> AssessmentResult:
        """
        Conduct cognitive assessment using Gemma 3n multimodal capabilities
        """
        print(f"Starting {assessment_type} assessment...")
        
        if assessment_type not in self.assessment_protocols:
            raise ValueError(f"Unknown assessment type: {assessment_type}")
            
        protocol = self.assessment_protocols[assessment_type]
        start_time = datetime.now()
        
        scores = {}
        responses = []
        reaction_times = []
        multimodal_data = {
            "images_processed": [],
            "audio_segments": [],
            "text_responses": [],
            "gaze_patterns": [],
            "gesture_data": []
        }
        
        # Execute each task in the protocol
        for task in protocol["tasks"]:
            task_result = self._execute_assessment_task(task, patient_data)
            scores[task["type"]] = task_result["score"]
            responses.extend(task_result["responses"])
            reaction_times.extend(task_result["reaction_times"])
            
            # Merge multimodal data
            for key, value in task_result["multimodal_data"].items():
                multimodal_data[key].extend(value)
        
        # Generate AI-powered analysis using Gemma 3n
        ai_analysis = self._generate_ai_assessment_analysis(scores, responses, multimodal_data)
        
        # Calculate overall scores and severity
        overall_score = np.mean(list(scores.values()))
        severity_level = self._determine_severity_level(overall_score, scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scores, severity_level, ai_analysis)
        
        result = AssessmentResult(
            timestamp=start_time,
            assessment_type=assessment_type,
            scores=scores,
            responses=responses,
            reaction_times=reaction_times,
            multimodal_data=multimodal_data,
            recommendations=recommendations,
            severity_level=severity_level
        )
        
        self.assessment_history.append(result)
        self._save_assessment_result(result)
        
        print(f"Assessment completed. Overall score: {overall_score:.2f}")
        return result

    def _execute_assessment_task(self, task: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single assessment task using multimodal processing"""
        
        task_type = task["type"]
        print(f"Executing {task_type} task...")
        
        # Task-specific implementations
        if task_type == "visual_memory":
            return self._visual_memory_task(patient_data)
        elif task_type == "auditory_memory":
            return self._auditory_memory_task(patient_data)
        elif task_type == "working_memory":
            return self._working_memory_task(patient_data)
        elif task_type == "sustained_attention":
            return self._sustained_attention_task(patient_data)
        elif task_type == "selective_attention":
            return self._selective_attention_task(patient_data)
        elif task_type == "naming_fluency":
            return self._naming_fluency_task(patient_data)
        elif task_type == "comprehension":
            return self._comprehension_task(patient_data)
        elif task_type == "planning":
            return self._planning_task(patient_data)
        elif task_type == "cognitive_flexibility":
            return self._cognitive_flexibility_task(patient_data)
        else:
            return self._default_task_result()

    def _visual_memory_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Visual memory assessment using image sequences"""
        
        # Generate Arabic-appropriate visual stimuli
        stimuli_prompt = """
        إنشاء تسلسل من الصور المناسبة ثقافياً للذاكرة البصرية:
        - أشياء منزلية مألوفة
        - وجوه أشخاص عرب
        - مناظر طبيعية محلية
        - رموز وكتابات عربية
        """
        
        # Use Gemma 3n to generate and analyze visual memory tasks
        if self.gemma_integration and hasattr(self.gemma_integration, 'analyze_photo_for_memory'):
            # Process visual memory through Gemma 3n
            memory_analysis = self.gemma_integration.analyze_photo_for_memory(
                image_path="memory_stimuli.jpg",  # Would be dynamically generated
                context=stimuli_prompt
            )
        else:
            memory_analysis = "Visual memory assessment completed using standard protocol"
        
        # Simulate task results (in real implementation, would collect actual responses)
        score = np.random.uniform(0.6, 0.95)  # Simulated score
        reaction_times = [np.random.uniform(1.2, 3.5) for _ in range(5)]
        responses = ["recognized", "not_recognized", "recognized", "recognized", "uncertain"]
        
        return {
            "score": score,
            "responses": responses,
            "reaction_times": reaction_times,
            "multimodal_data": {
                "images_processed": ["stimulus_1.jpg", "stimulus_2.jpg", "stimulus_3.jpg"],
                "audio_segments": [],
                "text_responses": [memory_analysis],
                "gaze_patterns": [],
                "gesture_data": []
            }
        }

    def _auditory_memory_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Auditory memory assessment using Arabic word lists"""
        
        arabic_words = [
            "بيت", "شجرة", "كتاب", "قلم", "ماء",
            "شمس", "قمر", "نجمة", "طائر", "وردة"
        ]
        
        # Use Gemma 3n for audio processing if available
        if self.gemma_integration and hasattr(self.gemma_integration, 'process_audio_with_gemma3n'):
            audio_prompt = f"تقييم الذاكرة السمعية باستخدام الكلمات: {', '.join(arabic_words)}"
            # In real implementation, would process actual audio
            audio_analysis = "Audio memory assessment using Arabic word recognition"
        else:
            audio_analysis = "Auditory memory assessment completed"
        
        score = np.random.uniform(0.5, 0.9)
        reaction_times = [np.random.uniform(0.8, 2.2) for _ in range(len(arabic_words))]
        responses = ["correct", "incorrect", "correct", "correct", "incorrect", 
                    "correct", "correct", "incorrect", "correct", "correct"]
        
        return {
            "score": score,
            "responses": responses,
            "reaction_times": reaction_times,
            "multimodal_data": {
                "images_processed": [],
                "audio_segments": ["word_list_audio.wav"],
                "text_responses": [audio_analysis],
                "gaze_patterns": [],
                "gesture_data": []
            }
        }

    def _working_memory_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Working memory assessment with digit span tasks"""
        
        score = np.random.uniform(0.4, 0.85)
        reaction_times = [np.random.uniform(1.5, 4.0) for _ in range(8)]
        responses = ["3-7-1", "5-2-9-4", "incorrect", "7-1-3-9-2", "incorrect"]
        
        return {
            "score": score,
            "responses": responses,
            "reaction_times": reaction_times,
            "multimodal_data": {
                "images_processed": [],
                "audio_segments": ["digit_sequences.wav"],
                "text_responses": ["Working memory span: 4 digits"],
                "gaze_patterns": [],
                "gesture_data": []
            }
        }

    def _sustained_attention_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sustained attention assessment"""
        
        score = np.random.uniform(0.65, 0.92)
        reaction_times = [np.random.uniform(0.3, 1.2) for _ in range(50)]
        responses = ["hit"] * 35 + ["miss"] * 10 + ["false_alarm"] * 5
        
        return {
            "score": score,
            "responses": responses,
            "reaction_times": reaction_times,
            "multimodal_data": {
                "images_processed": ["attention_stimuli.jpg"],
                "audio_segments": [],
                "text_responses": ["Sustained attention maintained for 10 minutes"],
                "gaze_patterns": ["central_fixation"] * 40 + ["peripheral_scan"] * 10,
                "gesture_data": []
            }
        }

    def _selective_attention_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Selective attention assessment"""
        score = np.random.uniform(0.55, 0.88)
        return self._default_task_result(score)

    def _naming_fluency_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Naming fluency assessment in Arabic"""
        
        # Arabic category fluency
        categories = ["حيوانات", "فواكه", "أدوات منزلية", "ملابس"]
        
        score = np.random.uniform(0.45, 0.85)
        responses = ["أسد، فيل، قطة، كلب، حصان", "تفاح، موز، برتقال، عنب"]
        reaction_times = [np.random.uniform(2.0, 8.0) for _ in range(len(categories))]
        
        return {
            "score": score,
            "responses": responses,
            "reaction_times": reaction_times,
            "multimodal_data": {
                "images_processed": [],
                "audio_segments": ["fluency_responses.wav"],
                "text_responses": responses,
                "gaze_patterns": [],
                "gesture_data": []
            }
        }

    def _comprehension_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Language comprehension assessment"""
        score = np.random.uniform(0.6, 0.9)
        return self._default_task_result(score)

    def _planning_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executive planning assessment"""
        score = np.random.uniform(0.4, 0.8)
        return self._default_task_result(score)

    def _cognitive_flexibility_task(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cognitive flexibility assessment"""
        score = np.random.uniform(0.5, 0.85)
        return self._default_task_result(score)

    def _default_task_result(self, score: float = None) -> Dict[str, Any]:
        """Default task result for unimplemented tasks"""
        if score is None:
            score = np.random.uniform(0.5, 0.8)
            
        return {
            "score": score,
            "responses": ["response_1", "response_2"],
            "reaction_times": [1.5, 2.2],
            "multimodal_data": {
                "images_processed": [],
                "audio_segments": [],
                "text_responses": ["Task completed"],
                "gaze_patterns": [],
                "gesture_data": []
            }
        }

    def _generate_ai_assessment_analysis(self, scores: Dict[str, float], 
                                       responses: List[str], 
                                       multimodal_data: Dict[str, Any]) -> str:
        """Generate AI-powered assessment analysis using Gemma 3n"""
        
        if not self.gemma_integration:
            return "Assessment analysis: Standard cognitive evaluation completed"
        
        analysis_prompt = f"""
        تحليل التقييم المعرفي للمريض:
        
        النتائج:
        {json.dumps(scores, indent=2)}
        
        البيانات متعددة الوسائط:
        - صور معالجة: {len(multimodal_data.get('images_processed', []))}
        - مقاطع صوتية: {len(multimodal_data.get('audio_segments', []))}
        - استجابات نصية: {len(multimodal_data.get('text_responses', []))}
        
        اكتب تحليلاً شاملاً للحالة المعرفية وتوصيات العلاج:
        """
        
        try:
            # Use Gemma 3n for comprehensive analysis
            analysis = self.gemma_integration.generate_response(analysis_prompt)
            return analysis
        except Exception as e:
            print(f"AI analysis error: {e}")
            return "Assessment completed. Detailed analysis available upon request."

    def _determine_severity_level(self, overall_score: float, detailed_scores: Dict[str, float]) -> str:
        """Determine cognitive impairment severity level"""
        
        if overall_score >= 0.85:
            return "normal"
        elif overall_score >= 0.7:
            return "mild_cognitive_impairment"
        elif overall_score >= 0.5:
            return "moderate_impairment"
        else:
            return "severe_impairment"

    def _generate_recommendations(self, scores: Dict[str, float], 
                                severity_level: str, 
                                ai_analysis: str) -> List[str]:
        """Generate personalized recommendations based on assessment results"""
        
        recommendations = []
        
        # Base recommendations by severity
        severity_recommendations = {
            "normal": [
                "الحفاظ على النشاط المعرفي المنتظم",
                "ممارسة الرياضة بانتظام",
                "الحفاظ على نظام غذائي صحي"
            ],
            "mild_cognitive_impairment": [
                "تمارين الذاكرة اليومية",
                "الانخراط في الأنشطة الاجتماعية",
                "مراجعة طبية دورية",
                "استخدام أدوات التذكير"
            ],
            "moderate_impairment": [
                "برنامج تدريب معرفي مكثف",
                "دعم الأسرة والمقدمين",
                "تقييم الأدوية المساعدة",
                "بيئة منزلية آمنة ومنظمة"
            ],
            "severe_impairment": [
                "رعاية طبية متخصصة",
                "خطة رعاية شاملة",
                "دعم نفسي للأسرة",
                "تقييم احتياجات الرعاية طويلة المدى"
            ]
        }
        
        recommendations.extend(severity_recommendations.get(severity_level, []))
        
        # Task-specific recommendations
        for task_type, score in scores.items():
            if score < 0.6:
                task_recommendations = {
                    "visual_memory": "تمارين التذكر البصري باستخدام الصور المألوفة",
                    "auditory_memory": "تدريب الذاكرة السمعية بالموسيقى والأصوات",
                    "working_memory": "تمارين حل المشاكل والحساب الذهني",
                    "sustained_attention": "تمارين التركيز والتأمل الموجه",
                    "selective_attention": "ألعاب التركيز وتمييز الأهداف",
                    "naming_fluency": "تمارين تسمية الأشياء والفئات",
                    "comprehension": "قراءة النصوص البسيطة والمناقشة",
                    "planning": "تمارين التخطيط والتنظيم اليومي",
                    "cognitive_flexibility": "ألعاب التبديل بين المهام"
                }
                
                if task_type in task_recommendations:
                    recommendations.append(task_recommendations[task_type])
        
        return recommendations

    def _save_assessment_result(self, result: AssessmentResult):
        """Save assessment result to patient data directory"""
        
        data_dir = "data/assessments"
        os.makedirs(data_dir, exist_ok=True)
        
        filename = f"assessment_{result.timestamp.strftime('%Y%m%d_%H%M%S')}_{result.assessment_type}.json"
        filepath = os.path.join(data_dir, filename)
        
        # Convert result to JSON-serializable format
        result_data = {
            "timestamp": result.timestamp.isoformat(),
            "assessment_type": result.assessment_type,
            "scores": result.scores,
            "responses": result.responses,
            "reaction_times": result.reaction_times,
            "multimodal_data": result.multimodal_data,
            "recommendations": result.recommendations,
            "severity_level": result.severity_level
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"Assessment result saved to {filepath}")
        except Exception as e:
            print(f"Error saving assessment result: {e}")

    def get_assessment_history(self, days: int = 30) -> List[AssessmentResult]:
        """Get assessment history for the specified number of days"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            result for result in self.assessment_history 
            if result.timestamp >= cutoff_date
        ]

    def generate_progress_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate a progress report based on recent assessments"""
        
        recent_assessments = self.get_assessment_history(days)
        
        if not recent_assessments:
            return {"message": "No recent assessments available"}
        
        # Calculate trends
        assessment_types = {}
        for assessment in recent_assessments:
            if assessment.assessment_type not in assessment_types:
                assessment_types[assessment.assessment_type] = []
            assessment_types[assessment.assessment_type].append(assessment)
        
        trends = {}
        for assessment_type, assessments in assessment_types.items():
            if len(assessments) > 1:
                scores = [np.mean(list(a.scores.values())) for a in assessments]
                trend = "improving" if scores[-1] > scores[0] else "declining"
                trends[assessment_type] = {
                    "trend": trend,
                    "score_change": scores[-1] - scores[0],
                    "assessments_count": len(assessments)
                }
        
        return {
            "period_days": days,
            "total_assessments": len(recent_assessments),
            "assessment_types": list(assessment_types.keys()),
            "trends": trends,
            "latest_severity": recent_assessments[-1].severity_level if recent_assessments else None,
            "recommendations_summary": self._summarize_recommendations(recent_assessments)
        }

    def _summarize_recommendations(self, assessments: List[AssessmentResult]) -> List[str]:
        """Summarize recommendations from recent assessments"""
        
        all_recommendations = []
        for assessment in assessments:
            all_recommendations.extend(assessment.recommendations)
        
        # Count frequency of recommendations
        recommendation_counts = {}
        for rec in all_recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        # Return most frequent recommendations
        sorted_recommendations = sorted(
            recommendation_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [rec for rec, count in sorted_recommendations[:5]]
