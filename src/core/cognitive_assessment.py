import os
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

@dataclass
class AssessmentResult:
    """Data class to store cognitive assessment results"""
    assessment_type: str
    timestamp: datetime
    scores: Dict[str, float]
    severity_level: str
    recommendations: List[str]
    raw_data: Dict[str, Any]

class CognitiveAssessmentEngine:
    """
    Engine for cognitive assessment of Alzheimer's patients using Gemma 3n.
    Provides tools to evaluate memory, attention, language processing, and executive function.
    """
    
    def __init__(self, gemma_integration):
        """Initialize the cognitive assessment engine"""
        self.gemma_integration = gemma_integration
        self.assessment_history = []
        self.current_assessment = None
        
        # Define assessment types and their tasks
        self.assessment_types = {
            "memory_recall": {
                "name": "تقييم الذاكرة",
                "tasks": ["short_term_recall", "long_term_recall", "recognition", "association"],
                "prompt_template": "سأسألك بعض الأسئلة لتقييم الذاكرة. {task_instruction}"
            },
            "attention_focus": {
                "name": "تقييم التركيز",
                "tasks": ["sustained_attention", "divided_attention", "selective_attention"],
                "prompt_template": "سأطلب منك القيام ببعض المهام لتقييم التركيز. {task_instruction}"
            },
            "language_processing": {
                "name": "تقييم اللغة",
                "tasks": ["naming", "comprehension", "fluency", "reading"],
                "prompt_template": "سأطلب منك القيام ببعض المهام اللغوية. {task_instruction}"
            },
            "executive_function": {
                "name": "تقييم الوظائف التنفيذية",
                "tasks": ["planning", "problem_solving", "flexibility", "inhibition"],
                "prompt_template": "سأطلب منك القيام ببعض المهام لتقييم قدراتك على التخطيط وحل المشكلات. {task_instruction}"
            }
        }
        
    def conduct_assessment(self, assessment_type: str, patient_data: Dict) -> AssessmentResult:
        """
        Conduct a cognitive assessment of the specified type
        
        Args:
            assessment_type: Type of assessment to conduct
            patient_data: Patient information for context
            
        Returns:
            AssessmentResult object with scores and recommendations
        """
        if assessment_type not in self.assessment_types:
            raise ValueError(f"Unknown assessment type: {assessment_type}")
        
        assessment_info = self.assessment_types[assessment_type]
        tasks = assessment_info["tasks"]
        
        # Track task scores
        task_scores = {}
        raw_data = {
            "patient_id": patient_data.get("patient_id", "unknown"),
            "assessment_type": assessment_type,
            "timestamp": datetime.now().isoformat(),
            "tasks": {}
        }
        
        # Conduct each task in the assessment
        for task in tasks:
            task_instruction = self._get_task_instruction(assessment_type, task)
            prompt = assessment_info["prompt_template"].format(task_instruction=task_instruction)
            
            # Generate response using Gemma
            response = self.gemma_integration.generate_response(prompt)
            
            # Analyze response to calculate score
            score = self._analyze_task_response(assessment_type, task, response)
            task_scores[task] = score
            
            # Store raw data
            raw_data["tasks"][task] = {
                "instruction": task_instruction,
                "response": response,
                "score": score
            }
        
        # Calculate overall score and severity
        overall_score = sum(task_scores.values()) / len(task_scores)
        severity_level = self._determine_severity(overall_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(assessment_type, task_scores, severity_level)
        
        # Create and return result
        result = AssessmentResult(
            assessment_type=assessment_type,
            timestamp=datetime.now(),
            scores=task_scores,
            severity_level=severity_level,
            recommendations=recommendations,
            raw_data=raw_data
        )
        
        # Store in history
        self.assessment_history.append(result)
        
        return result
    
    def conduct_multimodal_assessment(self, assessment_type: str, patient_data: Dict) -> AssessmentResult:
        """
        Conduct a multimodal cognitive assessment using text, image, and audio inputs
        
        Args:
            assessment_type: Type of assessment to conduct
            patient_data: Patient information for context
            
        Returns:
            AssessmentResult object with scores and recommendations
        """
        # For now, this is a placeholder that calls the text-based assessment
        # In a real implementation, this would use multimodal inputs
        return self.conduct_assessment(assessment_type, patient_data)
    
    def get_assessment_history(self, patient_id: str) -> List[Dict]:
        """Get assessment history for a specific patient"""
        history = []
        for result in self.assessment_history:
            if result.raw_data.get("patient_id") == patient_id:
                history.append({
                    "assessment_type": result.assessment_type,
                    "timestamp": result.timestamp.isoformat(),
                    "severity_level": result.severity_level,
                    "overall_score": sum(result.scores.values()) / len(result.scores)
                })
        return history
    
    def track_progress(self, patient_id: str, assessment_type: str) -> Dict:
        """Track patient progress over time for a specific assessment type"""
        history = self.get_assessment_history(patient_id)
        filtered_history = [item for item in history if item["assessment_type"] == assessment_type]
        
        if not filtered_history:
            return {"status": "no_data"}
        
        # Sort by timestamp
        filtered_history.sort(key=lambda x: x["timestamp"])
        
        # Calculate trend
        scores = [item["overall_score"] for item in filtered_history]
        if len(scores) > 1:
            trend = scores[-1] - scores[0]
        else:
            trend = 0
        
        return {
            "assessment_type": assessment_type,
            "data_points": len(filtered_history),
            "first_assessment": filtered_history[0]["timestamp"],
            "latest_assessment": filtered_history[-1]["timestamp"],
            "latest_score": scores[-1],
            "trend": trend,
            "trend_direction": "improving" if trend > 0 else "declining" if trend < 0 else "stable"
        }
    
    def _get_task_instruction(self, assessment_type: str, task: str) -> str:
        """Get instruction for a specific task"""
        # These would be more sophisticated in a real implementation
        instructions = {
            "memory_recall": {
                "short_term_recall": "سأذكر لك 5 كلمات، وأريدك أن تكررها بعد دقيقة واحدة: بيت، قلم، شجرة، ساعة، كتاب.",
                "long_term_recall": "هل تتذكر أين كنت تعيش قبل 10 سنوات؟ صف المكان.",
                "recognition": "سأذكر لك 3 أشياء، ثم سأسألك عنها لاحقًا: مفتاح، نظارة، محفظة.",
                "association": "ما هي العلاقة بين الشمس والقمر؟"
            },
            "attention_focus": {
                "sustained_attention": "عد تنازليًا من 100 إلى 80.",
                "divided_attention": "اذكر أيام الأسبوع بالترتيب العكسي.",
                "selective_attention": "اذكر كل الحيوانات التي تبدأ بحرف الألف."
            },
            "language_processing": {
                "naming": "سمِّ 5 أنواع من الفواكه.",
                "comprehension": "ما معنى المثل: 'العقل السليم في الجسم السليم'؟",
                "fluency": "اذكر أكبر عدد ممكن من الكلمات التي تبدأ بحرف الميم في دقيقة واحدة.",
                "reading": "اقرأ هذه الجملة: 'الشمس تشرق من الشرق وتغرب في الغرب.'"
            },
            "executive_function": {
                "planning": "صف خطوات تحضير كوب من الشاي.",
                "problem_solving": "لديك 8 تفاحات وتريد توزيعها على 4 أشخاص بالتساوي. كم تفاحة سيحصل كل شخص؟",
                "flexibility": "اذكر 3 استخدامات مختلفة لقلم رصاص.",
                "inhibition": "عندما أقول 'أحمر'، قل 'أزرق'، وعندما أقول 'أزرق'، قل 'أحمر'."
            }
        }
        
        return instructions.get(assessment_type, {}).get(task, "قم بالمهمة المطلوبة.")
    
    def _analyze_task_response(self, assessment_type: str, task: str, response: str) -> float:
        """
        Analyze task response to calculate score
        
        In a real implementation, this would use Gemma 3n to analyze the response
        For now, we'll use a simple random score for demonstration
        """
        # This is a placeholder - in a real implementation, this would use Gemma 3n
        # to analyze the response and calculate a score based on accuracy, completeness, etc.
        
        # Use Gemma to analyze the response
        analysis_prompt = f"""
        قم بتحليل استجابة المريض للمهمة التالية:
        
        نوع التقييم: {assessment_type}
        المهمة: {task}
        استجابة المريض: "{response}"
        
        قيم الاستجابة على مقياس من 0 إلى 10 بناءً على:
        - الدقة
        - الاكتمال
        - السرعة
        - الملاءمة
        
        قدم تقييمًا رقميًا نهائيًا من 0 إلى 1 (حيث 1 هو الأفضل).
        """
        
        try:
            analysis_response = self.gemma_integration.generate_response(analysis_prompt)
            
            # Try to extract a score from the response
            # This is a simple heuristic - in a real implementation, you'd want to structure the response
            score_candidates = []
            for line in analysis_response.split('\n'):
                if "تقييم" in line and ":" in line:
                    try:
                        score_text = line.split(":")[-1].strip()
                        score = float(score_text)
                        if 0 <= score <= 1:
                            score_candidates.append(score)
                        elif 0 <= score <= 10:
                            score_candidates.append(score / 10)
                    except ValueError:
                        pass
            
            if score_candidates:
                return sum(score_candidates) / len(score_candidates)
            
            # Fallback to random score
            return random.uniform(0.3, 0.9)
            
        except Exception as e:
            print(f"Error analyzing task response: {e}")
            return random.uniform(0.3, 0.9)
    
    def _determine_severity(self, overall_score: float) -> str:
        """Determine severity level based on overall score"""
        if overall_score >= 0.8:
            return "mild"
        elif overall_score >= 0.5:
            return "moderate"
        else:
            return "severe"
    
    def _generate_recommendations(self, assessment_type: str, task_scores: Dict[str, float], severity_level: str) -> List[str]:
        """Generate recommendations based on assessment results"""
        # This would be more sophisticated in a real implementation
        recommendations = []
        
        # General recommendation based on severity
        if severity_level == "mild":
            recommendations.append("استمر في التمارين المعرفية اليومية للحفاظ على القدرات الحالية.")
        elif severity_level == "moderate":
            recommendations.append("زيادة التمارين المعرفية مع التركيز على المهارات الأكثر ضعفًا.")
            recommendations.append("النظر في برنامج إعادة تأهيل معرفي منظم.")
        else:  # severe
            recommendations.append("التركيز على الروتين اليومي والتمارين البسيطة.")
            recommendations.append("زيادة الدعم والإشراف في الأنشطة اليومية.")
        
        # Specific recommendations based on assessment type
        if assessment_type == "memory_recall":
            recommendations.append("استخدام تقنيات المساعدة على التذكر مثل القوائم والملاحظات.")
        elif assessment_type == "attention_focus":
            recommendations.append("ممارسة تمارين التركيز في بيئة هادئة بدون مشتتات.")
        elif assessment_type == "language_processing":
            recommendations.append("المشاركة في محادثات منتظمة وقراءة مواد متنوعة.")
        elif assessment_type == "executive_function":
            recommendations.append("تقسيم المهام المعقدة إلى خطوات بسيطة وواضحة.")
        
        # Add specific recommendations based on task scores
        lowest_score_task = min(task_scores.items(), key=lambda x: x[1])
        if lowest_score_task[1] < 0.5:
            task_name = lowest_score_task[0]
            if task_name == "short_term_recall":
                recommendations.append("تمارين يومية لتحسين الذاكرة قصيرة المدى.")
            elif task_name == "sustained_attention":
                recommendations.append("تمارين التركيز المستمر لفترات متزايدة تدريجيًا.")
            elif task_name == "naming":
                recommendations.append("تمارين تسمية الأشياء والصور بشكل يومي.")
            elif task_name == "planning":
                recommendations.append("ممارسة التخطيط للمهام البسيطة بشكل يومي.")
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # This would typically use the actual GemmaIntegration
    from ..ai.gemma_integration import GemmaIntegration
    
    # For testing
    gemma = GemmaIntegration()
    assessment_engine = CognitiveAssessmentEngine(gemma)
    
    # Sample assessment
    patient_data = {"patient_id": "12345", "age": 72, "condition": "mild_cognitive_impairment"}
    result = assessment_engine.conduct_assessment("memory_recall", patient_data)
    
    print(f"Assessment type: {result.assessment_type}")
    print(f"Severity level: {result.severity_level}")
    print(f"Scores: {result.scores}")
    print(f"Recommendations:")
    for rec in result.recommendations:
        print(f"- {rec}")
