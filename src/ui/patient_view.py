import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import soundfile as sf
import os
import random
from PIL import Image
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

        # Right Frame for Prompts
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)

        self.prompt_label = ctk.CTkLabel(self.right_frame, text="Memory Prompts", font=ctk.CTkFont(size=20, weight="bold"))
        self.prompt_label.pack(pady=10)

        self.prompt_image_label = ctk.CTkLabel(self.right_frame, text="")
        self.prompt_image_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.show_prompt_button = ctk.CTkButton(self.right_frame, text="Show me a memory", command=self.show_memory_prompt)
        self.show_prompt_button.pack(pady=20, padx=20)

    def on_record_press(self):
        """Handles the record button press event by simulating audio recording and transcribing it."""
        self.status_label.configure(text="... جاري الاستماع (Listening)")
        self.update_idletasks() # Force UI update

        audio_path = "dummy_audio.wav"
        samplerate = 16000
        data = np.random.randn(samplerate * 3).astype(np.float32)
        sf.write(audio_path, data, samplerate)

        self.status_label.configure(text="... جاري معالجة الصوت (Processing)")
        self.update_idletasks()

        try:
            # Use actual ASR service instead of hardcoded text
            transcribed_text = self.asr_service.transcribe_audio_file(audio_path)
            if not transcribed_text:
                transcribed_text = "مرحباً، كيف حالك اليوم؟"  # Fallback for demo
            
            self.add_message("أنت", transcribed_text)
            
            # Add to context manager
            self.context_manager.add_context('user_input', transcribed_text)

            # Get AI response
            self.status_label.configure(text="... فاكر؟ بيفكر (Faker? is thinking)")
            self.update_idletasks()
            
            # Get relevant context for better responses
            relevant_context = self.context_manager.retrieve_relevant_context(transcribed_text)
            
            # Enhance prompt with context
            enhanced_prompt = self._enhance_prompt_with_context(transcribed_text, relevant_context)
            
            ai_response = self.gemma_integration.generate_response(enhanced_prompt)
            self.add_message("فاكر؟", ai_response)
            
            # Add AI response to context
            self.context_manager.add_context('ai_response', ai_response)
            
            # Speak the AI response
            self.tts_service.speak_async(ai_response)

        except Exception as e:
            self.status_label.configure(text="!حدث خطأ")
            print(f"An error occurred: {e}")
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
        """Enhanced memory prompt system with context tracking"""
        prompts = self.prompt_manager.get_prompts()
        if not prompts:
            self.add_message("فاكر؟", "لم يتم إضافة أي تذكيرات بعد. يمكن للعائلة إضافة صور وذكريات من لوحة المراقب.")
            return

        prompt = random.choice(prompts)
        prompt_text = prompt.get('text')
        image_path = prompt.get('image_path')
        audio_path = prompt.get('audio_path')

        if prompt_text:
            # Enhance prompt with Egyptian Arabic warmth
            enhanced_text = f"تعالي نتكلم عن ده: {prompt_text}. فاكر حاجة عن الصورة دي؟"
            self.add_message("فاكر؟", enhanced_text)
            
            # Track memory prompt activity
            self.context_manager.add_context('memory_prompt', prompt_text)
            
            # Speak the prompt
            self.tts_service.speak_async(enhanced_text)

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                # Resize image to fit better
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
                self.prompt_image_label.configure(image=ctk_img)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.prompt_image_label.configure(image=None)
        else:
            self.prompt_image_label.configure(image=None)

        if audio_path and os.path.exists(audio_path):
            # TODO: Implement actual audio playback
            self.add_message("فاكر؟", f"(تشغيل ملف صوتي: {os.path.basename(audio_path)})")
            print(f"Audio prompt would play: {audio_path}")
    
    def end_session(self):
        """End the current session and save context"""
        if self.session_active:
            self.context_manager.save_context_to_memory()
            self.session_active = False
            
            # Generate session report
            report = self.context_manager.get_session_report()
            print(f"Session ended. Report: {report}")
