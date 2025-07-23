import os
import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .gemma_integration import GemmaIntegration
from .asr_service import ASRService
from .context_manager import ContextManager
from ..core.tts_service import TTSService

class RealtimeMultimodalSystem:
    """
    Real-time multimodal processing system for Alzheimer's memory assistant.
    Handles simultaneous processing of text, image, and audio inputs.
    """
    
    def __init__(self):
        """Initialize the real-time multimodal system"""
        self.gemma_integration = GemmaIntegration()
        self.asr_service = ASRService()
        self.tts_service = TTSService()
        self.context_manager = ContextManager()
        
        # Processing flags
        self.is_processing = False
        self.session_active = False
        self.current_modalities = set()
        
        # Multimodal buffers
        self.text_buffer = ""
        self.image_path = None
        self.audio_path = None
        
        # Response callbacks
        self.on_response = None
        self.on_error = None
        self.on_status_update = None
        
    def start_session(self):
        """Start a new multimodal session"""
        self.session_active = True
        self.context_manager.clear_context()
        self._update_status("Session started")
        return True
        
    def end_session(self):
        """End the current multimodal session"""
        if self.session_active:
            self.session_active = False
            self.context_manager.save_context_to_memory()
            self._update_status("Session ended")
            return True
        return False
    
    def process_text(self, text: str):
        """Process text input"""
        if not self.session_active:
            self._update_status("No active session")
            return False
            
        self.text_buffer = text
        self.current_modalities.add("text")
        self._update_status("Text received")
        return True
    
    def process_image(self, image_path: str):
        """Process image input"""
        if not self.session_active or not os.path.exists(image_path):
            self._update_status("Invalid image or no active session")
            return False
            
        self.image_path = image_path
        self.current_modalities.add("image")
        self._update_status("Image received")
        return True
    
    def process_audio(self, audio_path: str):
        """Process audio input"""
        if not self.session_active or not os.path.exists(audio_path):
            self._update_status("Invalid audio or no active session")
            return False
            
        self.audio_path = audio_path
        self.current_modalities.add("audio")
        
        # Try to transcribe audio
        try:
            transcribed_text = self.asr_service.transcribe_audio_file(audio_path)
            if transcribed_text:
                self.text_buffer = transcribed_text
                self._update_status(f"Audio transcribed: {transcribed_text[:30]}...")
            else:
                self._update_status("Audio received (transcription failed)")
        except Exception as e:
            print(f"Transcription error: {e}")
            self._update_status("Audio received (transcription error)")
            
        return True
    
    def generate_response(self, callback=None):
        """Generate multimodal response based on current inputs"""
        if not self.session_active:
            self._update_status("No active session")
            return False
            
        if self.is_processing:
            self._update_status("Already processing")
            return False
            
        self.is_processing = True
        self.on_response = callback
        
        # Start processing in a separate thread
        threading.Thread(target=self._process_multimodal).start()
        return True
    
    def _process_multimodal(self):
        """Process multimodal inputs and generate response"""
        try:
            self._update_status("Processing multimodal inputs...")
            
            # Prepare prompt based on available modalities
            prompt = self.text_buffer if self.text_buffer else "تحليل المدخلات"
            
            # Add context information
            current_context = self.context_manager.get_current_context()
            context_info = {
                "modalities": list(self.current_modalities),
                "recent_topics": current_context.get("recent_topics", []),
                "mood_trend": current_context.get("mood_trend", "neutral"),
                "memory_performance": current_context.get("memory_performance", {})
            }
            
            # Generate response using Gemma integration
            response = self.gemma_integration.generate_response(
                prompt,
                image_path=self.image_path,
                audio_path=self.audio_path
            )
            
            # Update context with multimodal interaction
            self.context_manager.add_multimodal_interaction(
                "multimodal_response",
                {
                    "text_input": self.text_buffer,
                    "image_path": self.image_path,
                    "audio_path": self.audio_path,
                    "response": response,
                    "modalities": list(self.current_modalities)
                }
            )
            
            # Speak response if TTS is available
            if hasattr(self, 'tts_service') and self.tts_service:
                self.tts_service.speak_async(response)
            
            # Reset buffers
            self._reset_buffers()
            
            # Call response callback
            if self.on_response:
                self.on_response(response)
                
            self._update_status("Response generated")
            
        except Exception as e:
            print(f"Multimodal processing error: {e}")
            self._update_status(f"Error: {str(e)}")
            if self.on_error:
                self.on_error(str(e))
        finally:
            self.is_processing = False
    
    def _reset_buffers(self):
        """Reset all input buffers"""
        self.text_buffer = ""
        self.image_path = None
        self.audio_path = None
        self.current_modalities.clear()
    
    def _update_status(self, status: str):
        """Update processing status"""
        if self.on_status_update:
            self.on_status_update(status)
        print(f"[MultimodalSystem] {status}")
    
    def get_session_report(self) -> Dict:
        """Get session report for caregivers"""
        if not hasattr(self.context_manager, 'get_session_report'):
            return {"error": "Session reporting not available"}
        return self.context_manager.get_session_report()
    
    def analyze_memory_performance(self) -> Dict:
        """Analyze memory performance from session data"""
        if not hasattr(self.context_manager, '_analyze_memory_performance'):
            return {"status": "no_data"}
        return self.context_manager._analyze_memory_performance()

# Example usage
if __name__ == "__main__":
    # This is just for testing/demonstration
    system = RealtimeMultimodalSystem()
    system.start_session()
    
    # Define a callback
    def on_response_received(response):
        print(f"Response received: {response}")
    
    # Process text
    system.process_text("مرحباً، كيف حالك اليوم؟")
    
    # Generate response
    system.generate_response(callback=on_response_received)
    
    # Wait for processing to complete
    time.sleep(5)
    
    # End session
    system.end_session()
