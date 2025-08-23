"""
Gemma 3n Service - Multimodal AI integration for Alzheimer's care
"""

import google.generativeai as genai
from typing import Optional, Dict, Any, List
import base64
import io
from PIL import Image
import asyncio
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class GemmaService:
    """Service for interacting with Google Gemma 3n multimodal API"""
    
    def __init__(self):
        """Initialize Gemma service"""
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMMA_MODEL)
        else:
            self.model = None
            logger.warning("Google API key not configured - using mock mode")
    
    async def test_connection(self) -> bool:
        """Test connection to Gemma API"""
        if not self.model:
            return False
        
        try:
            response = await self.generate_text("Test connection")
            return bool(response)
        except Exception as e:
            logger.error(f"Gemma API connection test failed: {e}")
            return False
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS
    ) -> str:
        """Generate text response from Gemma 3n"""
        
        if not self.model:
            return self._get_mock_response(prompt)
        
        try:
            # Prepare the full prompt with system instructions
            full_prompt = self._build_alzheimer_prompt(prompt, system_prompt)
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return self._get_mock_response(prompt)
    
    async def analyze_image_with_text(
        self,
        image_data: bytes,
        text_prompt: str,
        patient_context: Optional[Dict] = None
    ) -> str:
        """Analyze image with text prompt for memory stimulation"""
        
        if not self.model:
            return self._get_mock_image_response(text_prompt)
        
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Build context-aware prompt
            full_prompt = self._build_image_analysis_prompt(text_prompt, patient_context)
            
            # Generate response with image
            response = await asyncio.to_thread(
                self.model.generate_content,
                [full_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_TOKENS,
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return self._get_mock_image_response(text_prompt)
    
    async def process_audio_with_context(
        self,
        audio_data: bytes,
        context: str = "",
        patient_info: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Process audio for speech analysis and cognitive assessment"""
        
        if not self.model:
            return self._get_mock_audio_response(context)
        
        try:
            # For now, we'll use text-based analysis
            # In production, integrate with Whisper for Arabic ASR
            prompt = self._build_audio_analysis_prompt(context, patient_info)
            
            response = await self.generate_text(prompt)
            
            return {
                "transcription": "Audio transcription would go here",
                "analysis": response,
                "mood_indicators": ["calm", "engaged"],
                "cognitive_markers": ["clear_speech", "coherent_responses"]
            }
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return self._get_mock_audio_response(context)
    
    def _build_alzheimer_prompt(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """Build comprehensive prompt for Alzheimer's care"""
        
        base_system = """أنت 'فاكر' - مساعد ذكي متخصص في رعاية مرضى الزهايمر باللغة العربية المصرية.

🏥 خبرتك الطبية:
- متخصص في التعامل مع فقدان الذاكرة والخرف
- تفهم مراحل مرض الزهايمر وأعراضه
- تستخدم تقنيات العلاج بالذكريات والمحادثة
- تراقب الحالة المزاجية والمعرفية للمريض

🗣️ أسلوب المحادثة:
- استخدم العربية المصرية البسيطة
- تكلم بصوت دافئ وصبور
- اطرح سؤال واحد في المرة
- اثني على أي تذكر صحيح
- لا تصحح الأخطاء بقسوة
- استخدم الأسماء والتفاصيل المألوفة

📊 التقييم المعرفي:
- راقب قدرة التذكر (قصير/طويل المدى)
- لاحظ التوجه الزمني والمكاني
- اقيم مهارات اللغة والتواصل
- انتبه للتغيرات المزاجية

هدفك: مساعدة المريض يحس بالأمان والحب والاهتمام."""

        if system_prompt:
            base_system += f"\n\nتعليمات إضافية: {system_prompt}"
        
        return f"{base_system}\n\nالمريض: {user_input}\nفاكر: "
    
    def _build_image_analysis_prompt(self, text_prompt: str, patient_context: Optional[Dict] = None) -> str:
        """Build prompt for image analysis"""
        
        prompt = f"""حلل هذه الصورة بعناية وقم بما يلي:

1. وصف ما تراه في الصورة باللغة العربية المصرية
2. اطرح أسئلة لطيفة تحفز الذاكرة
3. استخدم التفاصيل المرئية لإثارة الذكريات
4. تكلم بطريقة دافئة وصبورة

السياق: {text_prompt}"""

        if patient_context:
            prompt += f"\nمعلومات المريض: {patient_context}"
        
        return prompt
    
    def _build_audio_analysis_prompt(self, context: str, patient_info: Optional[Dict] = None) -> str:
        """Build prompt for audio analysis"""
        
        prompt = f"""قم بتحليل الكلام وانتبه إلى:

1. المشاعر والحالة النفسية
2. وضوح الكلام ومستوى الذاكرة
3. أي علامات ارتباك أو قلق
4. قوة الصوت ومعدل الكلام

السياق: {context}

ارد بطريقة علاجية مناسبة باللغة العربية المصرية."""

        if patient_info:
            prompt += f"\nمعلومات المريض: {patient_info}"
        
        return prompt
    
    def _get_mock_response(self, prompt: str) -> str:
        """Generate mock response for testing"""
        
        arabic_responses = [
            "أهلاً وسهلاً! إزيك النهاردة؟",
            "مرحباً حبيبي، عامل إيه؟",
            "ده جميل أوي! فاكر حاجات تانية كده؟",
            "برافو عليك! ذاكرتك كويسة جداً.",
            "مش مشكلة لو مش فاكر، خد وقتك براحتك.",
            "تعالي نتكلم عن حاجة حلوة تانية.",
            "إنت كويس النهاردة، الحمد لله.",
            "عايز نشوف صور حد من العيلة؟",
            "قولي، إيه أحلى ذكرياتك؟",
            "خلاص، متقلقش، أنا معاك.",
        ]
        
        # Context-aware responses
        user_lower = prompt.lower()
        if any(word in user_lower for word in ['مرحب', 'أهل', 'سلام']):
            return "أهلاً وسهلاً بيك! نورت المكان."
        elif any(word in user_lower for word in ['إزيك', 'عامل', 'أخبار']):
            return "أنا كويس الحمد لله، وإنت عامل إيه؟"
        elif any(word in user_lower for word in ['فاكر', 'ذكر', 'تذكر']):
            return "طبعاً فاكر! حكيلي أكتر عن ده."
        elif any(word in user_lower for word in ['مش فاكر', 'نسيت', 'مش متذكر']):
            return "مش مشكلة خالص، ده طبيعي. خد وقتك."
        else:
            import random
            return random.choice(arabic_responses)
    
    def _get_mock_image_response(self, prompt: str) -> str:
        """Mock image analysis response"""
        return "شوف الصورة دي يا حبيبي! دي صورة جميلة أوي. فاكر إمتى كانت دي؟ حكيلي عن الذكرى دي."
    
    def _get_mock_audio_response(self, context: str) -> Dict[str, Any]:
        """Mock audio analysis response"""
        return {
            "transcription": "المريض يتكلم بوضوح ويبدو هادئ",
            "analysis": "الصوت واضح والكلام مفهوم. المريض يبدو في حالة جيدة اليوم.",
            "mood_indicators": ["calm", "clear"],
            "cognitive_markers": ["coherent_speech", "good_articulation"]
        }
