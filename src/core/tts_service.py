import pyttsx3
import os
from typing import Optional

class TTSService:
    """Text-to-Speech service for Arabic voice output"""
    
    def __init__(self):
        """Initialize TTS engine"""
        self.engine = None
        self.is_initialized = False
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine with Arabic support"""
        try:
            self.engine = pyttsx3.init()
            self.is_initialized = True
            
            # Configure for Arabic
            voices = self.engine.getProperty('voices')
            arabic_voice = None
            
            # Look for Arabic voice
            for voice in voices:
                if 'arabic' in voice.name.lower() or 'ar' in voice.id.lower():
                    arabic_voice = voice
                    break
            
            if arabic_voice:
                self.engine.setProperty('voice', arabic_voice.id)
                print(f"Arabic voice found: {arabic_voice.name}")
            else:
                print("No specific Arabic voice found, using default")
            
            # Set speech rate and volume
            self.engine.setProperty('rate', 150)  # Slower for elderly users
            self.engine.setProperty('volume', 0.9)
            
        except Exception as e:
            print(f"Failed to initialize TTS engine: {e}")
            self.is_initialized = False
    
    def speak(self, text: str, save_to_file: Optional[str] = None) -> bool:
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert to speech
            save_to_file (str, optional): Path to save audio file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_initialized or not self.engine:
            print("TTS engine not initialized")
            return False
        
        try:
            if save_to_file:
                self.engine.save_to_file(text, save_to_file)
            else:
                self.engine.say(text)
            
            self.engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"Error in TTS: {e}")
            return False
    
    def speak_async(self, text: str) -> bool:
        """
        Convert text to speech asynchronously (non-blocking)
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.is_initialized or not self.engine:
            return False
        
        try:
            self.engine.say(text)
            # Don't wait for completion
            return True
        except Exception as e:
            print(f"Error in async TTS: {e}")
            return False
    
    def stop(self):
        """Stop current speech"""
        if self.is_initialized and self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                print(f"Error stopping TTS: {e}")
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        if self.is_initialized and self.engine:
            try:
                self.engine.setProperty('rate', rate)
            except Exception as e:
                print(f"Error setting rate: {e}")
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        if self.is_initialized and self.engine:
            try:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            except Exception as e:
                print(f"Error setting volume: {e}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if not self.is_initialized or not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str) -> bool:
        """Set specific voice by ID"""
        if not self.is_initialized or not self.engine:
            return False
        
        try:
            self.engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    tts = TTSService()
    
    # Test Arabic text
    arabic_text = "مرحباً، أنا فاكر، مساعدك الذكي للذاكرة"
    english_text = "Hello, I am Faker, your intelligent memory assistant"
    
    print("Available voices:")
    for voice_id, voice_name in tts.get_available_voices():
        print(f"  {voice_id}: {voice_name}")
    
    print(f"Speaking Arabic: {arabic_text}")
    tts.speak(arabic_text)
    
    print(f"Speaking English: {english_text}")
    tts.speak(english_text)
