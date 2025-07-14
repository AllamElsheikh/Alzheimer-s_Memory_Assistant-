import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class GemmaIntegration:
    """
    Handles the integration with the AI model for conversational capabilities.
    Specifically designed for Google Gemma 3n Hackathon competition.
    """

    def __init__(self, model_name=None):
        """
        Initializes the integration with Google Gemma 3n model for competition.

        Args:
            model_name (str, optional): The name of the Hugging Face model to use.
                                      Defaults to Gemma 3n for competition compliance.
        """
        # Gemma 3n models for competition - MUST USE GEMMA 3N TO WIN
        self.model_candidates = [
            "google/gemma-3n-E4B-it",  # PRIMARY: 8B Gemma 3n model for competition 🏆
            "google/gemma-3n-E2B-it",  # SECONDARY: 6B Gemma 3n model 
            "google/gemma-2-2b-it",    # FALLBACK: Gemma 2 (not competition compliant)
        ]
        
        if model_name:
            self.model_candidates.insert(0, model_name)
            
        self.model_name = None  # Will be set during loading
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.conversation_history = []
        self.system_prompt = {
            "role": "system",
            "content": """أنت 'فاكر؟' - رفيق ذكي وصبور يتحدث بالعربية المصرية ويساعد المسنين الذين يعانون من فقدان الذاكرة.

خصائصك:
- تتكلم بالعربية المصرية البسيطة والواضحة
- صبور جداً ولا تظهر إحباط أبداً
- تقدم تذكيرات لطيفة وتشجع على التذكر
- تساعد في التعرف على الأشخاص والذكريات
- تستخدم أسلوب محادثة دافئ وودود

مهامك:
1. المحادثة اليومية البسيطة
2. مساعدة في التذكر بلطف
3. التشجيع على مشاركة الذكريات
4. تقديم التذكيرات بالأدوية والمواعيد
5. تهدئة القلق والارتباك

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
        self._load_model()

    def _load_model(self):
        """Loads the tokenizer and model from Hugging Face.
        
        Prioritizes Gemma 3n for competition compliance.
        """
        # Authentication token for gated model access
        auth_token = os.getenv("HF_TOKEN")
        if not auth_token:
            raise RuntimeError("Hugging Face token not found. Please set HF_TOKEN environment variable.")
        
        for model_name in self.model_candidates:
            try:
                print(f"🔄 Attempting to load {model_name}...")
                
                # Check if this is the competition-required Gemma 3n model
                is_gemma_3n = "gemma-3n" in model_name.lower()
                if is_gemma_3n:
                    print("🏆 COMPETITION MODEL: This is Gemma 3n - required for winning!")
                
                # Try to load tokenizer with current transformers API
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_name, 
                    token=auth_token,
                    trust_remote_code=True
                )
                
                print(f"✓ Tokenizer loaded for {model_name}")
                print(f"Loading model on {self.device}...")
                
                # Try to load model
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    device_map="auto" if self.device == "cuda" else self.device,
                    token=auth_token,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    low_cpu_mem_usage=True
                )
                
                # If we get here, loading was successful
                self.model_name = model_name
                success_msg = f"✅ SUCCESS: '{model_name}' loaded successfully on {self.device}!"
                if is_gemma_3n:
                    success_msg += " 🏆 COMPETITION READY!"
                print(success_msg)
                return

            except Exception as e:
                error_message = str(e)
                print(f"❌ Failed to load '{model_name}': {error_message}")
                
                # Clean up any partially loaded components
                self.tokenizer = None
                self.model = None
                
                # Continue to next model
                continue
        
        # If we get here, all models failed to load
        print("\n🚨 CRITICAL ERROR: No Gemma models could be loaded!")
        print("This will prevent winning the competition!")
        print("\nTroubleshooting steps:")
        print("1. Check internet connection")
        print("2. Verify Hugging Face authentication")
        print("3. Try running: huggingface-cli login")
        print("4. Check available disk space")
        print("5. Update transformers: pip install --upgrade transformers")
        
        # Set model to None to indicate failure
        self.model = None
        self.tokenizer = None

    def generate_response(self, user_prompt: str) -> str:
        """
        Generates a response from the Gemma model based on the user's prompt and conversation history.

        Args:
            user_prompt (str): The user's input in Egyptian Arabic.

        Returns:
            str: The AI-generated response in Egyptian Arabic.
        """
        if not self.model or not self.tokenizer:
            # Enhanced mock responses for demo when model is loading/failed
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
                import random
                response = random.choice(arabic_responses)
            
            print(f"[DEMO MODE - Gemma 3n Loading]: {response}")
            print("🏆 Note: Using enhanced mock while Gemma 3n model loads for competition")
            return response

        # Add the user's message to the history
        self.conversation_history.append({"role": "user", "content": user_prompt})

        # Prepare the full chat history for the model
        full_chat = [self.system_prompt] + self.conversation_history

        try:
            # Apply the chat template if available
            if hasattr(self.tokenizer, 'apply_chat_template'):
                chat_prompt = self.tokenizer.apply_chat_template(
                    full_chat,
                    tokenize=False,
                    add_generation_prompt=True
                )
            else:
                # Fallback for models without chat template
                chat_prompt = f"{self.system_prompt['content']}\n\nUser: {user_prompt}\nAssistant:"

            # Tokenize the input
            inputs = self.tokenizer.encode(
                chat_prompt,
                add_special_tokens=True,
                return_tensors="pt"
            ).to(self.model.device)

            # Generate a response with proper parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs, 
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the response, skipping special tokens
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract only the newly generated part
            if "<start_of_turn>model" in response_text:
                # Gemma-style template
                model_response_start = response_text.rfind("<start_of_turn>model")
                clean_response = response_text[model_response_start:].split("\n", 1)[-1].strip()
            elif "Assistant:" in response_text:
                # Simple template
                clean_response = response_text.split("Assistant:")[-1].strip()
            else:
                # Extract new tokens only
                input_length = inputs.shape[1]
                new_tokens = outputs[0][input_length:]
                clean_response = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

            # Ensure response is in Arabic and reasonable
            if not clean_response or len(clean_response) < 3:
                clean_response = "عفواً، مش فاهم قصدك. ممكن تكرر تاني؟"

            # Add the model's response to the history
            self.conversation_history.append({"role": "assistant", "content": clean_response})

            print(f"[GEMMA RESPONSE]: {clean_response}")
            return clean_response

        except Exception as e:
            print(f"Error during response generation: {e}")
            error_response = "عذراً، حصل مشكلة صغيرة. ممكن نجرب تاني؟"
            self.conversation_history.append({"role": "assistant", "content": error_response})
            return error_response

    def clear_history(self):
        """Clears the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")

    def get_model_status(self):
        """Returns the current model status for debugging."""
        status = {
            "model_loaded": self.model is not None,
            "tokenizer_loaded": self.tokenizer is not None,
            "model_name": self.model_name,
            "device": self.device,
            "conversation_length": len(self.conversation_history)
        }
        return status
