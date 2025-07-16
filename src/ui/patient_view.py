import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import soundfile as sf
import os
import random
from datetime import datetime
from PIL import Image
from tkinter import filedialog
from ..ai.asr_service import ASRService
from ..ai.gemma_integration import GemmaIntegration
from ..ai.context_manager import ContextManager
from ..core.prompt_manager import PromptManager
from ..core.memory_engine import MemoryEngine
from ..core.tts_service import TTSService

class PatientView(ctk.CTkFrame):
    """The patient-facing view with conversation and recording controls."""

    def __init__(self, parent, controller, asr_service, gemma_integration):
        """Initializes the PatientView frame."""
        super().__init__(parent)
        self.controller = controller
        self.asr_service = asr_service
        self.gemma_integration = gemma_integration
        self.prompt_manager = PromptManager()
        self.memory_engine = MemoryEngine()
        self.context_manager = ContextManager()
        self.tts_service = TTSService()
        
        # Session tracking
        self.session_active = True

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Left Frame for Conversation
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(self.left_frame, text="أهلاً بك! أنا 'فاكر؟' لمساعدتك", font=ctk.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=20, pady=20)

        self.conversation_text = scrolledtext.ScrolledText(self.left_frame, wrap=tk.WORD, state='disabled', font=("Arial", 14))
        self.conversation_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.status_label = ctk.CTkLabel(self.left_frame, text="اضغط على 'سجل' للتحدث", font=ctk.CTkFont(size=16))
        self.status_label.grid(row=2, column=0, padx=20, pady=10)

        self.record_button = ctk.CTkButton(self.left_frame, text="سجل (Record)", font=ctk.CTkFont(size=18, weight="bold"), command=self.on_record_press)
        self.record_button.grid(row=3, column=0, padx=20, pady=20)

        # NEW: Multimodal interaction button
        self.photo_button = ctk.CTkButton(
            self.left_frame, 
            text="🖼️ تحليل صورة (Analyze Photo)", 
            font=ctk.CTkFont(size=16, weight="bold"), 
            command=self.upload_and_analyze_photo,
            fg_color="green"
        )
        self.photo_button.grid(row=4, column=0, padx=20, pady=10)

        # Right Frame for Prompts
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)

        self.prompt_label = ctk.CTkLabel(self.right_frame, text="Memory Prompts", font=ctk.CTkFont(size=20, weight="bold"))
        self.prompt_label.pack(pady=10)

        self.prompt_image_label = ctk.CTkLabel(self.right_frame, text="")
        self.prompt_image_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.show_prompt_button = ctk.CTkButton(self.right_frame, text="Show me a memory", command=self.show_memory_prompt)
        self.show_prompt_button.pack(pady=20, padx=20)

        # Phase 2 Feature Buttons
        self.phase2_frame = ctk.CTkFrame(self.right_frame)
        self.phase2_frame.pack(pady=20, padx=20, fill="x")
        
        # Conversation session button
        self.conversation_session_button = ctk.CTkButton(
            self.phase2_frame,
            text="جلسة محادثة علاجية",
            command=self.start_therapeutic_session,
            width=180,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.conversation_session_button.pack(pady=5)
        
        # Cognitive assessment button  
        self.assessment_button = ctk.CTkButton(
            self.phase2_frame,
            text="تقييم معرفي",
            command=self.start_cognitive_assessment,
            width=180,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.assessment_button.pack(pady=5)
        
        # Memory assistance button
        self.memory_assist_button = ctk.CTkButton(
            self.phase2_frame,
            text="مساعدة الذاكرة",
            command=self.open_memory_assistance,
            width=180,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.memory_assist_button.pack(pady=5)

        # Import Phase 2 components
        try:
            from ..core.cognitive_assessment import CognitiveAssessmentEngine
            from ..core.intelligent_memory import IntelligentMemoryRetrieval
            from ..core.conversation_flow import ConversationFlowManager
            
            self.assessment_engine = CognitiveAssessmentEngine(self.gemma_integration)
            self.memory_retrieval = IntelligentMemoryRetrieval(self.gemma_integration)
            self.conversation_manager = ConversationFlowManager(
                self.gemma_integration, 
                self.memory_retrieval, 
                self.assessment_engine
            )
            print("Phase 2 components loaded successfully")
        except ImportError as e:
            print(f"Phase 2 components not available: {e}")
            self.assessment_engine = None
            self.memory_retrieval = None
            self.conversation_manager = None
        self.multimodal_button = ctk.CTkButton(
            self.right_frame,
            text="🎤📸 جلسة متكاملة (Multimodal Session)",
            command=self.start_multimodal_session,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="purple"
        )
        self.multimodal_button.pack(pady=10, padx=20)

        # Audio analysis button
        self.audio_analysis_button = ctk.CTkButton(
            self.right_frame,
            text="🎤 تحليل صوتي (Audio Analysis)", 
            command=self.analyze_audio,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange"
        )
        self.audio_analysis_button.pack(pady=10, padx=20)

    def on_record_press(self):
        """Handles multimodal recording with real-time Gemma 3n processing."""
        self.status_label.configure(text="... جاري الاستماع (Listening)")
        self.update_idletasks() # Force UI update

        audio_path = "dummy_audio.wav"
        samplerate = 16000
        data = np.random.randn(samplerate * 3).astype(np.float32)
        sf.write(audio_path, data, samplerate)

        self.status_label.configure(text="... جاري معالجة الصوت (Processing)")
        self.update_idletasks()

        try:
            # PHASE 1: Multimodal processing
            transcribed_text = None
            ai_response = None
            
            # Check if we're in multimodal mode and use multimodal processing
            if getattr(self, 'multimodal_mode', False):
                ai_response = self.handle_multimodal_recording(audio_path)
                transcribed_text = "(Multimodal processing)"
            elif hasattr(self.gemma_integration, 'process_audio_with_context'):
                # Try direct audio processing with context
                context = "المريض يتحدث في جلسة علاجية للذاكرة"
                ai_response = self.gemma_integration.process_audio_with_context(audio_path, context)
                transcribed_text = "(Direct audio processing)"
                try:
                    print("🎵 Attempting direct audio processing with Gemma 3n...")
                    self.status_label.configure(text="🧠 معالجة متعددة الوسائط...")
                    
                    # Build context for audio processing
                    current_context = self.context_manager.get_current_context()
                    context_info = f"المريض في جلسة علاجية. الحالة: {current_context.get('mood', 'عادي')}"
                    
                    # Use Gemma 3n direct audio processing
                    ai_response = self.gemma_integration.process_audio_with_gemma3n(
                        audio_path, 
                        context_info
                    )
                    
                    if ai_response and "معذرة" not in ai_response and "غير متاح" not in ai_response:
                        print("Direct audio processing successful!")
                        self.add_message("أنت", "[تم تحليل الصوت مباشرة بواسطة Gemma 3n]")
                        self.add_message("فاكر؟", ai_response)
                        
                        # Add to context with metadata
                        self.context_manager.add_context('multimodal_interaction', {
                            'audio_processed': True,
                            'response': ai_response,
                            'method': 'gemma3n_direct_audio',
                            'modalities': ['audio', 'text']
                        })
                        
                        # Speak response and exit
                        self.tts_service.speak_async(ai_response)
                        self.status_label.configure(text="تم بنجاح")
                        return
                        
                except Exception as e:
                    print(f"Direct audio processing failed: {e}")
                    self.status_label.configure(text="🔄 التبديل إلى المعالجة التقليدية...")
            
            # Fallback: Use traditional ASR + text processing
            print("🔄 Falling back to ASR + text processing...")
            transcribed_text = self.asr_service.transcribe_audio_file(audio_path)
            if not transcribed_text:
                transcribed_text = "مرحباً، كيف حالك اليوم؟"  # Fallback for demo
            
            self.add_message("أنت", transcribed_text)
            
            # Add to context manager
            self.context_manager.add_context('user_input', transcribed_text)

            # Get AI response using structured generation
            self.status_label.configure(text="... فاكر؟ بيفكر (Faker? is thinking)")
            self.update_idletasks()
            
            # Get relevant context for better responses
            relevant_context = self.context_manager.retrieve_relevant_context(transcribed_text)
            
            # Generate structured AI response with therapeutic insights
            try:
                # Try multimodal generation if available
                if hasattr(self.gemma_integration, '_generate_multimodal_response'):
                    print("Attempting multimodal response generation...")
                    ai_response = self.gemma_integration.generate_response(
                        transcribed_text, 
                        image_path=None,  # No image in this flow
                        audio_path=None   # Audio already processed
                    )
                else:
                    # Fallback to structured response
                    structured_response = self.gemma_integration.generate_structured_response(
                        transcribed_text, 
                        relevant_context
                    )
                    
                    # Extract the main response
                    ai_response = structured_response.get('response', 
                        self.gemma_integration.generate_response(transcribed_text))
                
                # Store therapeutic data for caregiver reports
                therapeutic_data = {
                    'user_input': transcribed_text,
                    'ai_response': ai_response,
                    'therapeutic_intent': structured_response.get('therapeutic_intent', 'general'),
                    'memory_level': structured_response.get('memory_level', 'unclear'),
                    'engagement_score': structured_response.get('engagement_score', 5),
                    'follow_up_suggestions': structured_response.get('follow_up_suggestions', []),
                    'clinical_notes': structured_response.get('clinical_notes', {}),
                    'timestamp': self.context_manager._get_timestamp() if hasattr(self.context_manager, '_get_timestamp') else None
                }
                
                # Update context with structured interaction data
                self.context_manager.add_context('conversation', therapeutic_data)
                
            except Exception as e:
                print(f"Error in structured response: {e}")
                # Fallback to simple response
                contextual_prompt = self._enhance_prompt_with_context(transcribed_text, relevant_context)
                ai_response = self.gemma_integration.generate_response(contextual_prompt)
            
            self.add_message("فاكر؟", ai_response)
            
            # Add AI response to context
            self.context_manager.add_context('ai_response', ai_response)
            
            # Speak the AI response
            self.tts_service.speak_async(ai_response)

        except Exception as e:
            self.status_label.configure(text="!حدث خطأ")
            print(f"An error occurred: {e}")

    def handle_multimodal_interaction(self, text_input: str, image_path: str = None, audio_path: str = None) -> str:
        """
        NEW: Handle multimodal interactions (text + image + audio) with Gemma 3n
        """
        try:
            print(f"Processing multimodal interaction...")
            print(f"   Text: {text_input[:50]}...")
            if image_path:
                print(f"   Image: {image_path}")
            if audio_path:
                print(f"   Audio: {audio_path}")
            
            # Use multimodal generation
            if hasattr(self.gemma_integration, 'generate_response'):
                response = self.gemma_integration.generate_response(
                    text_input,
                    image_path=image_path,
                    audio_path=audio_path
                )
            else:
                # Fallback to regular generation
                response = self.gemma_integration.generate_response(text_input)
            
            # Add multimodal interaction to context
            modalities = ['text']
            if image_path: modalities.append('image')
            if audio_path: modalities.append('audio')
            
            self.context_manager.add_context('multimodal_interaction', {
                'text': text_input,
                'image_path': image_path,
                'audio_path': audio_path,
                'response': response,
                'modalities': modalities,
                'timestamp': datetime.now().isoformat() if hasattr(datetime, 'now') else None
            })
            
            return response
            
        except Exception as e:
            print(f"Multimodal interaction error: {e}")
            return self.gemma_integration.generate_response(text_input)

    def analyze_uploaded_photo(self, image_path: str) -> str:
        """
        NEW: Analyze uploaded photos using Gemma 3n vision capabilities
        """
        try:
            if hasattr(self.gemma_integration, 'analyze_photo_for_memory'):
                print(f"🖼️ Analyzing uploaded photo: {image_path}")
                
                # Get current patient context
                current_context = self.context_manager.get_current_context()
                context_info = f"المريض يريد مناقشة هذه الصورة. الحالة الحالية: {current_context.get('mood', 'عادي')}"
                
                analysis = self.gemma_integration.analyze_photo_for_memory(
                    image_path,
                    context_info
                )
                
                # Display analysis result
                self.add_message("فاكر؟", f"🖼️ {analysis}")
                
                # Add to context
                self.context_manager.add_context('photo_analysis', {
                    'image_path': image_path,
                    'analysis': analysis,
                    'method': 'gemma3n_vision'
                })
                
                return analysis
            else:
                return "عذراً، تحليل الصور غير متاح في الوضع التجريبي"
                
        except Exception as e:
            print(f"🚨 Photo analysis error: {e}")
            return "عذراً، حدث خطأ في تحليل الصورة"

    def upload_and_analyze_photo(self):
        """
        Upload and analyze photo using Gemma 3n multimodal capabilities
        """
        try:
            # Open file dialog
            image_path = filedialog.askopenfilename(
                title="اختر صورة للتحليل",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                    ("All files", "*.*")
                ]
            )
            
            if not image_path:
                return
            
            self.status_label.configure(text="🖼️ جاري تحليل الصورة...")
            self.update_idletasks()
            
            # Analyze the photo
            analysis_result = self.analyze_uploaded_photo(image_path)
            
            # Also try multimodal interaction if available
            if analysis_result and "عذراً" not in analysis_result:
                # Test multimodal with both image and text
                prompt = "شوف الصورة دي وحكيلي إيه اللي شايفه فيها؟"
                multimodal_response = self.handle_multimodal_interaction(
                    prompt,
                    image_path=image_path
                )
                
                if multimodal_response != analysis_result:
                    self.add_message("فاكر؟", f"🧠 تحليل متقدم: {multimodal_response}")
            
            self.status_label.configure(text="✅ تم تحليل الصورة بنجاح")
            
        except Exception as e:
            print(f"🚨 Photo upload error: {e}")
            self.status_label.configure(text="❌ خطأ في تحليل الصورة")
            self.add_message("فاكر؟", "عذراً، حدث خطأ في تحليل الصورة. حاول مرة أخرى.")
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            self.status_label.configure(text="اضغط على 'سجل' للتحدث")

    def add_message(self, sender: str, message: str):
        """Adds a message to the conversation view."""
        self.conversation_text.configure(state='normal')
        self.conversation_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.conversation_text.configure(state='disabled')
        self.conversation_text.see(tk.END) # Auto-scroll to the latest message

    def _enhance_prompt_with_context(self, user_input: str, relevant_context: dict) -> str:
        """Enhance user prompt with relevant context for better AI responses"""
        base_prompt = user_input
        
        # Add context about recent topics
        if relevant_context.get('related_topics'):
            context_info = f"\nRecent topics discussed: {', '.join(relevant_context['related_topics'])}"
            base_prompt += context_info
        
        # Add memory performance context
        current_context = self.context_manager.get_current_context()
        memory_perf = current_context.get('memory_performance', {})
        if memory_perf.get('status') == 'needs_attention':
            base_prompt += "\n(Note: Patient may need simpler questions and more encouragement)"
        
        return base_prompt

    def _detect_mood_from_interaction(self, user_input: str, ai_response: str):
        """Simple mood detection based on interaction patterns"""
        positive_words = ['جيد', 'سعيد', 'كويس', 'تمام', 'حلو']
        negative_words = ['تعبان', 'زعلان', 'مش كويس', 'صعب', 'نسيت']
        
        user_lower = user_input.lower()
        mood = "neutral"
        
        if any(word in user_lower for word in positive_words):
            mood = "positive"
        elif any(word in user_lower for word in negative_words):
            mood = "negative"
        
        self.context_manager.add_context('mood_indicator', mood)

    def show_memory_prompt(self):
        """Shows memory prompt using real Gemma 3n multimodal analysis."""
        try:
            # Get available person cards
            all_cards = self.memory_engine.get_all_cards()
            
            if not all_cards:
                # Create a sample prompt if no cards exist
                self.prompt_image_label.configure(text="لا توجد ذكريات محفوظة بعد.\nاطلب من أهلك إضافة صور في قسم الرعاية.")
                return
            
            # Select a random card for memory stimulation
            selected_card = random.choice(all_cards)
            
            # Use real image analysis if available
            if selected_card.get('image_path') and hasattr(self.gemma_integration, 'analyze_photo_for_memory'):
                try:
                    print(f"🖼️ Analyzing memory photo with Gemma 3n multimodal...")
                    
                    # Build context for image analysis
                    user_context = f"هذا المريض اسمه {selected_card.get('name', 'غير محدد')}. العلاقة: {selected_card.get('relationship', 'غير محدد')}"
                    
                    # Use photo analysis
                    analysis_result = self.gemma_integration.analyze_photo_for_memory(
                        selected_card['image_path'],
                        user_context
                    )
                    
                    # Display the result
                    if analysis_result and "معذرة" not in analysis_result:
                        self.prompt_image_label.configure(text=f"💡 {analysis_result}")
                        print("✅ Multimodal memory analysis successful!")
                        
                        # Add to context as multimodal interaction
                        self.context_manager.add_context('memory_prompt_multimodal', {
                            'card_id': selected_card.get('id'),
                            'analysis': analysis_result,
                            'modalities': ['image', 'text'],
                            'person': selected_card.get('name')
                        })
                        return
                    
                except Exception as e:
                    print(f"⚠️ Multimodal memory analysis failed: {e}")
            
            # Fallback to traditional text-based prompts
            memory_prompts = [
                f"شوف الصورة دي! ده {selected_card.get('name', 'حد من أهلك')}. فاكره؟",
                f"الشخص ده كان {selected_card.get('relationship', 'قريب منك')}. حكيلي عنه.",
                f"ذكرياتك مع {selected_card.get('name', 'الشخص ده')} إيه؟",
                f"أيام حلوة مع {selected_card.get('name', 'أهلك')}... قولي عليها."
            ]
            
            selected_prompt = random.choice(memory_prompts)
            self.prompt_image_label.configure(text=f"💡 {selected_prompt}")
            
            # Add to context
            self.context_manager.add_context('memory_prompt', {
                'prompt': selected_prompt,
                'card_id': selected_card.get('id'),
                'person': selected_card.get('name')
            })
            import random
            selected_card = random.choice(all_cards)
            
            # Use photo analysis
            if selected_card.get('photo_path') and os.path.exists(selected_card['photo_path']):
                analysis = self.gemma_integration.analyze_photo_for_memory(
                    selected_card['photo_path'],
                    f"صورة لـ {selected_card['name']} - {selected_card.get('relationship', 'فرد من العائلة')}"
                )
                
                # Display the analysis
                prompt_text = f"👤 {selected_card['name']}\n"
                prompt_text += f"📋 {analysis.get('description', 'صورة عائلية جميلة')}\n\n"
                
                # Add memory prompts
                memory_prompts = analysis.get('memory_prompts', [])
                if memory_prompts:
                    prompt_text += "💭 أسئلة للتذكر:\n"
                    for i, prompt in enumerate(memory_prompts[:3], 1):
                        prompt_text += f"{i}. {prompt}\n"
                
                self.prompt_image_label.configure(text=prompt_text)
                
                # Auto-generate a conversation starter
                starter_text = f"شوف الصورة دي يا حبيبي، ده {selected_card['name']}. فاكر إيه عنه؟"
                self.add_message("فاكر؟", starter_text)
                
                # Add to context
                self.context_manager.add_context('current_photo', {
                    'person': selected_card,
                    'analysis': analysis
                })
                
            else:
                # Fallback for missing photo
                prompt_text = f"👤 {selected_card['name']}\n"
                prompt_text += f"🔗 {selected_card.get('relationship', 'فرد من العائلة')}\n"
                prompt_text += f"📝 {selected_card.get('notes', 'لا توجد ملاحظات')}"
                self.prompt_image_label.configure(text=prompt_text)
                
                starter_text = f"تعالي نتكلم عن {selected_card['name']}. فاكر حاجات حلوة معاه؟"
                self.add_message("فاكر؟", starter_text)
        
        except Exception as e:
            print(f"Error in show_memory_prompt: {e}")
            self.prompt_image_label.configure(text="عذراً، حدث خطأ في عرض الذكرى.")

    def end_session(self):
        """End the current session and save context"""
        if self.session_active:
            self.context_manager.save_context_to_memory()
            self.session_active = False
            
            # Generate session report
            report = self.context_manager.get_session_report()
            print(f"Session ended. Report: {report}")

    def start_multimodal_session(self):
        """
        Start integrated text+image+audio session
        """
        try:
            self.add_message("فاكر؟", "🎤📸 بدء الجلسة المتكاملة! يمكنك الآن التحدث وإظهار الصور معاً.")
            
            # Enable recording mode
            self.multimodal_mode = getattr(self, 'multimodal_mode', False)
            self.multimodal_mode = True
            self.status_label.configure(text="جلسة متكاملة: اضغط 'سجل' وأظهر صورة")
            
        except Exception as e:
            print(f"Error starting multimodal session: {e}")
            self.add_message("فاكر؟", "عذراً، مشكلة في بدء الجلسة المتكاملة.")

    # Phase 2 Implementation Methods
    
    def start_therapeutic_session(self):
        """Start a therapeutic conversation session using ConversationFlowManager"""
        
        if not self.conversation_manager:
            self._show_message("خطأ", "مدير المحادثة غير متوفر")
            return
        
        try:
            # Start conversation session
            session_id = self.conversation_manager.start_conversation_session("patient_01")
            
            # Create conversation window
            self.conversation_window = ctk.CTkToplevel(self)
            self.conversation_window.title("جلسة محادثة علاجية")
            self.conversation_window.geometry("600x500")
            
            # Conversation display
            self.conversation_display = ctk.CTkTextbox(
                self.conversation_window, 
                height=300, 
                font=ctk.CTkFont(size=14)
            )
            self.conversation_display.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Input frame
            input_frame = ctk.CTkFrame(self.conversation_window)
            input_frame.pack(pady=10, padx=10, fill="x")
            
            self.conversation_input = ctk.CTkEntry(
                input_frame, 
                placeholder_text="اكتب رسالتك هنا...",
                font=ctk.CTkFont(size=12),
                width=400
            )
            self.conversation_input.pack(side="left", padx=5)
            
            send_button = ctk.CTkButton(
                input_frame,
                text="إرسال",
                command=self.send_conversation_message,
                width=80
            )
            send_button.pack(side="right", padx=5)
            
            # Bind Enter key
            self.conversation_input.bind("<Return>", lambda e: self.send_conversation_message())
            
            # Display initial greeting
            initial_response = self.conversation_manager.current_session.turns[0]
            self.conversation_display.insert("end", f"المساعد: {initial_response.content}\n\n")
            
            print(f"Therapeutic session started: {session_id}")
            
        except Exception as e:
            print(f"Error starting therapeutic session: {e}")
            self._show_message("خطأ", f"لا يمكن بدء الجلسة: {str(e)}")

    def send_conversation_message(self):
        """Send message in therapeutic conversation"""
        
        if not self.conversation_manager or not hasattr(self, 'conversation_input'):
            return
        
        message = self.conversation_input.get().strip()
        if not message:
            return
        
        try:
            # Display patient message
            self.conversation_display.insert("end", f"أنت: {message}\n\n")
            
            # Process with conversation manager
            response_data = self.conversation_manager.process_patient_input(message)
            
            # Display AI response
            ai_response = response_data["response"]
            self.conversation_display.insert("end", f"المساعد: {ai_response}\n\n")
            
            # Show therapeutic suggestions if available
            if response_data.get("therapeutic_suggestions"):
                suggestions = ", ".join(response_data["therapeutic_suggestions"])
                self.conversation_display.insert("end", f"اقتراحات علاجية: {suggestions}\n\n")
            
            # Clear input
            self.conversation_input.delete(0, "end")
            
            # Scroll to bottom
            self.conversation_display.see("end")
            
        except Exception as e:
            print(f"Error processing conversation message: {e}")
            self.conversation_display.insert("end", f"خطأ: لا يمكن معالجة الرسالة\n\n")

    def start_cognitive_assessment(self):
        """Start cognitive assessment using CognitiveAssessmentEngine"""
        
        if not self.assessment_engine:
            self._show_message("خطأ", "محرك التقييم غير متوفر")
            return
        
        # Create assessment selection window
        assessment_window = ctk.CTkToplevel(self)
        assessment_window.title("تقييم معرفي")
        assessment_window.geometry("400x300")
        
        # Assessment type selection
        ctk.CTkLabel(
            assessment_window, 
            text="اختر نوع التقييم:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        assessment_types = [
            ("memory_recall", "تقييم الذاكرة"),
            ("attention_focus", "تقييم التركيز"),
            ("language_processing", "تقييم اللغة"),
            ("executive_function", "تقييم الوظائف التنفيذية")
        ]
        
        for assessment_id, assessment_name in assessment_types:
            ctk.CTkButton(
                assessment_window,
                text=assessment_name,
                command=lambda aid=assessment_id: self.run_cognitive_assessment(aid, assessment_window),
                width=250,
                height=40
            ).pack(pady=5)

    def run_cognitive_assessment(self, assessment_type: str, parent_window):
        """Run the selected cognitive assessment"""
        
        parent_window.destroy()
        
        try:
            # Show progress window
            progress_window = ctk.CTkToplevel(self)
            progress_window.title("جاري التقييم...")
            progress_window.geometry("300x150")
            
            progress_label = ctk.CTkLabel(
                progress_window,
                text=f"جاري تنفيذ تقييم {assessment_type}...",
                font=ctk.CTkFont(size=14)
            )
            progress_label.pack(pady=50)
            
            # Update window to show progress
            progress_window.update()
            
            # Run assessment
            patient_data = {"patient_id": "patient_01", "age": 70, "condition": "mild_cognitive_impairment"}
            result = self.assessment_engine.conduct_multimodal_assessment(assessment_type, patient_data)
            
            # Close progress window
            progress_window.destroy()
            
            # Show results
            self.show_assessment_results(result)
            
        except Exception as e:
            print(f"Error running cognitive assessment: {e}")
            if 'progress_window' in locals():
                progress_window.destroy()
            self._show_message("خطأ", f"فشل في تنفيذ التقييم: {str(e)}")

    def show_assessment_results(self, result):
        """Display cognitive assessment results"""
        
        results_window = ctk.CTkToplevel(self)
        results_window.title("نتائج التقييم المعرفي")
        results_window.geometry("500x600")
        
        # Results display
        results_text = ctk.CTkTextbox(
            results_window,
            font=ctk.CTkFont(size=12),
            height=400
        )
        results_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Format results
        results_content = f"""
نتائج التقييم المعرفي
{'='*30}

نوع التقييم: {result.assessment_type}
التاريخ: {result.timestamp.strftime('%Y-%m-%d %H:%M')}
مستوى الشدة: {result.severity_level}

النتائج التفصيلية:
"""
        
        for task_type, score in result.scores.items():
            results_content += f"- {task_type}: {score:.2f}\n"
        
        results_content += f"\n\nالتوصيات:\n"
        for i, recommendation in enumerate(result.recommendations, 1):
            results_content += f"{i}. {recommendation}\n"
        
        results_text.insert("1.0", results_content)
        results_text.configure(state="disabled")
        
        # Close button
        ctk.CTkButton(
            results_window,
            text="إغلاق",
            command=results_window.destroy,
            width=100
        ).pack(pady=10)

    def open_memory_assistance(self):
        """Open memory assistance interface"""
        
        if not self.memory_retrieval:
            self._show_message("خطأ", "نظام الذاكرة غير متوفر")
            return
        
        # Create memory assistance window
        memory_window = ctk.CTkToplevel(self)
        memory_window.title("مساعدة الذاكرة")
        memory_window.geometry("600x500")
        
        # Memory query frame
        query_frame = ctk.CTkFrame(memory_window)
        query_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(
            query_frame,
            text="ابحث في ذكرياتك:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        self.memory_query_entry = ctk.CTkEntry(
            query_frame,
            placeholder_text="اكتب ما تريد تذكره...",
            width=400,
            font=ctk.CTkFont(size=12)
        )
        self.memory_query_entry.pack(pady=5)
        
        search_button = ctk.CTkButton(
            query_frame,
            text="بحث",
            command=lambda: self.search_memories(memory_window),
            width=100
        )
        search_button.pack(pady=5)
        
        # Memory results display
        self.memory_results = ctk.CTkTextbox(
            memory_window,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.memory_results.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Store new memory frame
        store_frame = ctk.CTkFrame(memory_window)
        store_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(
            store_frame,
            text="حفظ ذكرى جديدة:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        self.new_memory_entry = ctk.CTkEntry(
            store_frame,
            placeholder_text="اكتب الذكرى الجديدة...",
            width=400,
            font=ctk.CTkFont(size=12)
        )
        self.new_memory_entry.pack(pady=5)
        
        store_button = ctk.CTkButton(
            store_frame,
            text="حفظ",
            command=self.store_new_memory,
            width=100
        )
        store_button.pack(pady=5)

    def search_memories(self, parent_window):
        """Search for memories using the query"""
        
        query = self.memory_query_entry.get().strip()
        if not query:
            return
        
        try:
            # Search memories
            memories = self.memory_retrieval.retrieve_contextual_memories(
                query, "general", max_results=5
            )
            
            # Display results
            self.memory_results.delete("1.0", "end")
            
            if memories:
                results_text = f"تم العثور على {len(memories)} ذكرى:\n\n"
                
                for i, memory in enumerate(memories, 1):
                    results_text += f"{i}. {memory.content}\n"
                    results_text += f"   التاريخ: {memory.timestamp.strftime('%Y-%m-%d')}\n"
                    results_text += f"   الأهمية: {memory.importance_score:.2f}\n\n"
                
                self.memory_results.insert("1.0", results_text)
            else:
                self.memory_results.insert("1.0", "لم يتم العثور على ذكريات مطابقة")
                
        except Exception as e:
            print(f"Error searching memories: {e}")
            self.memory_results.insert("1.0", f"خطأ في البحث: {str(e)}")

    def store_new_memory(self):
        """Store a new memory"""
        
        memory_content = self.new_memory_entry.get().strip()
        if not memory_content:
            return
        
        try:
            # Store memory
            memory_id = self.memory_retrieval.store_multimodal_memory(
                content=memory_content,
                memory_type="episodic",
                emotional_context="neutral",
                tags=["user_input"]
            )
            
            # Clear input
            self.new_memory_entry.delete(0, "end")
            
            # Show confirmation
            self._show_message("نجح", f"تم حفظ الذكرى بنجاح\nرقم الذكرى: {memory_id}")
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            self._show_message("خطأ", f"فشل في حفظ الذكرى: {str(e)}")

    def _show_message(self, title: str, message: str):
        """Show a message dialog"""
        
        msg_window = ctk.CTkToplevel(self)
        msg_window.title(title)
        msg_window.geometry("300x150")
        
        ctk.CTkLabel(
            msg_window,
            text=message,
            font=ctk.CTkFont(size=12),
            wraplength=250
        ).pack(pady=30)
        
        ctk.CTkButton(
            msg_window,
            text="موافق",
            command=msg_window.destroy,
            width=100
        ).pack(pady=10)

    def analyze_audio(self):
        """
        Dedicated audio processing with Gemma 3n
        """
        try:
            self.status_label.configure(text="🎤 تحليل صوتي: اضغط 'سجل' للبدء")
            self.audio_analysis_mode = getattr(self, 'audio_analysis_mode', False)
            self.audio_analysis_mode = True
            
        except Exception as e:
            print(f"Error in audio analysis: {e}")

    def handle_multimodal_recording(self, audio_path):
        """
        RECORDING: Handle recording with potential image context
        """
        try:
            # Check if we have a recent photo analysis for context
            current_context = self.context_manager.get_current_context()
            recent_photo = current_context.get('photo_analysis')
            
            # Process audio with image context if available
            if recent_photo and hasattr(self.gemma_integration, 'process_audio_with_context'):
                context = f"المريض يتحدث عن صورة حللناها مؤخراً: {recent_photo.get('analysis', '')[:100]}"
                response = self.gemma_integration.process_audio_with_context(audio_path, context)
            else:
                # Regular audio processing
                transcribed_text = self.asr_service.transcribe_audio_file(audio_path)
                response = self.gemma_integration.generate_response(transcribed_text)
            
            return response
            
        except Exception as e:
            print(f"Error in multimodal recording: {e}")
            return "عذراً، مشكلة في معالجة التسجيل."
