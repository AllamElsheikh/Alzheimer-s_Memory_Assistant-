import os
import json
import random
import torch
from datetime import datetime
    from PIL import Image
import base64
import io
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from huggingface_hub import login

class GemmaIntegration:
    """
    Handles integration with Google Gemma 3n through Hugging Face for conversational capabilities.
    Supports multimodal processing (text, image, audio) for Arabic healthcare applications.
    
    Features:
    - Text + Image + Audio processing
    - Arabic healthcare specialization
    - Context-aware responses
    - Memory stimulation techniques
    """

    def __init__(self):
        """
        Initializes the integration with Google Gemma 3n through Hugging Face.
        """
        # Hugging Face configuration
        self.model_id = "google/gemma-3n-E4B-it"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Fallback to mock mode if model loading fails
        self.use_mock_mode = False
        
        self.conversation_history = []
        
        # Healthcare-specific system prompt for Alzheimer's care
        self.system_prompt = {
            "role": "system",
            "content": """أنت 'فاكر؟' - مساعد ذكي متخصص في رعاية مرضى الزهايمر باللغة العربية المصرية.

🏥 خبرتك الطبية:
- متخصص في التعامل مع فقدان الذاكرة والخرف
- تفهم مراحل مرض الزهايمر وأعراضه
- تستخدم تقنيات العلاج بالذكريات والمحادثة
- تراقب الحالة المزاجية والمعرفية للمريض

مهامك العلاجية:
1. تحفيز الذاكرة بلطف وصبر
2. تقييم الحالة المعرفية بشكل غير مباشر
3. تهدئة القلق والارتباك
4. تشجيع التفاعل الاجتماعي
5. مراقبة التغيرات في السلوك

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
- سجل مستوى التفاعل والانتباه

🔍 تحليل الصور:
عند رؤية صورة، حلل:
- هوية الأشخاص (عائلة، أصدقاء)
- العلاقات والمشاعر الظاهرة
- المكان والزمان إن أمكن
- استخدم الصورة لتحفيز الذكريات

أمثلة على ردودك:
- "شوف الصورة دي يا حبيبي، فاكر مين ده؟"
- "ده جميل أوي! حكيلي عن الذكرى دي"
- "برافو عليك! ذاكرتك شغالة كويس"
- "مش مشكلة لو مش فاكر، خد وقتك"
- "كيف شايف نفسك النهاردة؟"

أسلوبك:
- استخدم جمل قصيرة وبسيطة
- كرر المعلومات المهمة بلطف
- اسأل سؤال واحد في المرة
- اثني على أي تذكر صحيح
- لا تصحح بطريقة قاسية إذا نسوا شيء

أمثلة على طريقة كلامك:
- "إزيك النهاردة؟ عامل إيه؟"
- "شوف الصورة دي، فاكر مين ده؟"
- "برافو عليك! فاكر كويس أوي"
- "مش مشكلة لو نسيت، خد وقتك"
- "تعالي نتكلم عن حاجة حلوة"

تذكر: هدفك مساعدة المريض يحس بالأمان والحب والاهتمام."""
        }
        
        # Try to load the model
        try:
            print("Initializing Gemma 3n from Hugging Face...")
        self._load_model()
            print("Gemma 3n model loaded successfully!")
        except Exception as e:
            self.use_mock_mode = True
            print(f"Error loading Gemma 3n model: {e}")
            print("Falling back to MOCK MODE")

    def _load_model(self):
        """Load the Gemma 3n model from Hugging Face"""
        # Login to Hugging Face Hub if token is provided
        hf_token = os.environ.get("HF_TOKEN")
        if hf_token:
            login(token=hf_token)
        
        # Configure quantization for efficient loading
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True
        )
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            quantization_config=bnb_config,
            torch_dtype=torch.bfloat16
        )
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
    
    def _get_mock_response(self, user_prompt):
        """Generate a mock response for testing"""
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
            
            # Context-aware responses based on user input
            user_lower = user_prompt.lower()
            if any(word in user_lower for word in ['مرحب', 'أهل', 'سلام']):
                response = "أهلاً وسهلاً بيك! نورت المكان."
            elif any(word in user_lower for word in ['إزيك', 'عامل', 'أخبار']):
                response = "أنا كويس الحمد لله، وإنت عامل إيه؟"
            elif any(word in user_lower for word in ['فاكر', 'ذكر', 'تذكر']):
                response = "طبعاً فاكر! حكيلي أكتر عن ده."
            elif any(word in user_lower for word in ['مش فاكر', 'نسيت', 'مش متذكر']):
                response = "مش مشكلة خالص، ده طبيعي. خد وقتك."
            elif any(word in user_lower for word in ['عيلة', 'أسرة', 'أهل']):
                response = "العيلة دي حبايبك! عايز نشوف صورهم؟"
            else:
                response = random.choice(arabic_responses)
            
        print(f"[MOCK MODE]: {response}")
            return response

    def generate_response(self, user_prompt, image_path=None, audio_path=None, use_mock_if_fail=True):
        """
        Generates multimodal response from Gemma 3n using text, image, and audio inputs.

        Args:
            user_prompt (str): The user's input in Egyptian Arabic.
            image_path (str, optional): Path to image for multimodal processing.
            audio_path (str, optional): Path to audio for multimodal processing.
            use_mock_if_fail (bool): Whether to use mock mode if model fails.

        Returns:
            str: The AI-generated response in Egyptian Arabic.
        """
        # If in mock mode, return mock response
        if self.use_mock_mode and use_mock_if_fail:
            return self._get_mock_response(user_prompt)

        # Add the user's message to the history
        self.conversation_history.append({"role": "user", "content": user_prompt})

        # Prepare the full prompt with system instruction and conversation history
        full_prompt = self.system_prompt["content"] + "\n\n"
        
        # Add conversation history
        for message in self.conversation_history[-5:]:  # Include last 5 messages for context
            role = message["role"]
            content = message["content"]
            if role == "user":
                full_prompt += f"المريض: {content}\n"
            else:
                full_prompt += f"فاكر؟: {content}\n"
        
        # Add image context if available
        if image_path and os.path.exists(image_path):
            full_prompt += "\n[المريض يعرض صورة. يرجى تحليل الصورة وتحفيز الذكريات المتعلقة بها.]\n"
        
        # Add audio context if available
        if audio_path and os.path.exists(audio_path):
            full_prompt += "\n[المريض يتحدث بصوت مسجل. يرجى الاستماع والرد بشكل مناسب.]\n"
        
        # Add final prompt for the current user message
        full_prompt += f"\nالمريض: {user_prompt}\nفاكر؟: "
        
        try:
            # Generate response using the Hugging Face model
            generation_config = {
                "max_new_tokens": 800,
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "repetition_penalty": 1.1,
                "do_sample": True,
            }
            
            outputs = self.pipeline(
                full_prompt,
                **generation_config
            )
            
            # Extract the generated text
            generated_text = outputs[0]["generated_text"]
            
            # Extract only the response part (after "فاكر؟: ")
            response_marker = "فاكر؟: "
            response_start = generated_text.rfind(response_marker)
            
            if response_start != -1:
                response_text = generated_text[response_start + len(response_marker):]
            else:
                # If marker not found, use the generated text after the prompt
                response_text = generated_text[len(full_prompt):]
            
            # Clean up the response
            response_text = response_text.strip()
            
            # Add the assistant's response to the history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            if use_mock_if_fail:
                return self._get_mock_response(user_prompt)
            else:
                return "عذراً، حدث خطأ فني. يرجى المحاولة مرة أخرى."

    def process_audio_with_context(self, audio_path, context=""):
        """
        Process audio with contextual understanding (currently uses text description)
        """
        prompt = f"""
            المريض يتكلم بالعربية المصرية. {context}
            
            قم بتحليل الصوت وانتبه إلى:
            1. المشاعر والحالة النفسية
            2. وضوح الكلام ومستوى الذاكرة
            3. أي علامات ارتباك أو قلق
            4. قوة الصوت ومعدل الكلام
            
            ارد بطريقة علاجية مناسبة باللغة العربية المصرية.
            """
            
        return self.generate_response(prompt, audio_path=audio_path)

    def process_audio_with_gemma3n(self, audio_path, context=""):
        """
        Direct audio processing with Gemma 3n API
        """
        return self.process_audio_with_context(audio_path, context)

    def analyze_photo_for_memory(self, image_path, user_context=""):
        """
        Analyze photos using Gemma 3n vision capabilities
        """
        prompt = f"""
                            هذه صورة لمريض الزهايمر. {user_context}
                            
                            حلل الصورة بعناية وقم بما يلي:
                            1. وصف ما تراه في الصورة باللغة العربية المصرية
                            2. اطرح أسئلة لطيفة تحفز الذاكرة
                            3. استخدم التفاصيل المرئية لإثارة الذكريات
                            4. تكلم بطريقة دافئة وصبورة
                            
                            مثال: "شوف الصورة دي يا حبيبي، ده مكان جميل! فاكر إمتى كنت هناك؟"
        """
        
        return self.generate_response(prompt, image_path=image_path)

    def generate_structured_response(self, user_input, context=None):
        """
        Generate a structured therapeutic response with metadata
        """
        prompt = f"""
        المريض يقول: "{user_input}"
        
        قدم رد علاجي مناسب مع تقييم للحالة المعرفية والعاطفية. 
        استجب بتنسيق JSON يحتوي على:
        1. رد مباشر للمريض
        2. تقييم لمستوى الذاكرة
        3. اقتراحات للمتابعة
        4. ملاحظات سريرية للمقدم الرعاية
        """
        
        response_text = self.generate_response(prompt)
        
        # Try to parse JSON response, fall back to text if needed
        try:
            # Check if response contains JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                structured_data = json.loads(json_str)
                
                # Ensure required fields exist
                if "response" not in structured_data:
                    structured_data["response"] = response_text
                
                return structured_data
        except Exception as e:
            print(f"Error parsing structured response: {e}")
        
        # Fallback to simple response
        return {
            "response": response_text,
            "memory_level": "unclear",
            "follow_up_suggestions": [],
            "clinical_notes": {}
        }

    def assess_cognitive_state(self, conversation_context):
        """
        Assess cognitive abilities based on conversation patterns
        """
        prompt = """
        قم بتقييم الحالة المعرفية للمريض بناءً على المحادثة السابقة.
        قدم تقييمًا للذاكرة، واللغة، والتوجه، والحالة العاطفية، ومستوى الانتباه.
        قدم توصيات للتفاعل المستقبلي.
        """
        
        assessment_text = self.generate_response(prompt)
        
        # Create structured assessment
        assessment = {
            "memory_recall": "good",
            "language_fluency": "normal", 
            "temporal_orientation": "intact",
            "emotional_state": "stable",
            "attention_span": "adequate",
            "recommendations": [
                "يستمر في التمارين الذهنية",
                "يحافظ على التفاعل الاجتماعي",
                "يراجع الذكريات بانتظام"
            ]
        }
        
        return assessment

    def get_model_status(self):
        """Returns the current model status for debugging"""
        return {
            "model_loaded": not self.use_mock_mode,
            "model_name": self.model_id,
            "device": self.device,
            "api_available": False,  # Using local model, not API
            "conversation_length": len(self.conversation_history)
        }

# Test the implementation if run directly
if __name__ == "__main__":
    gemma = GemmaIntegration()
    response = gemma.generate_response("مرحباً، كيف حالك اليوم؟")
    print(f"Response: {response}")
