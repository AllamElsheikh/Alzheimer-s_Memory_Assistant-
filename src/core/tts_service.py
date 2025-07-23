import os
import threading
import pyttsx3
import tempfile
import time
from typing import Optional, List, Dict, Any

class TTSService:
    """
    Text-to-Speech service optimized for Arabic language.
    Provides high-quality voice synthesis with emotional variations.
    """
    
    def __init__(self, voice_name: str = "Arabic", rate: int = 150, volume: float = 0.8):
        """
        Initialize the TTS service with Arabic voice support.
        
        Args:
            voice_name: Name of the voice to use (default: Arabic)
            rate: Speaking rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        # Initialize pyttsx3 engine
        self.engine = pyttsx3.init()
        
        # Configure voice
        self.voice_name = voice_name
        self.set_voice(voice_name)
        
        # Set properties
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Arabic language optimization
        self.arabic_optimizations = {
            'elongate_vowels': True,  # Elongate vowels for better pronunciation
            'pause_after_sentences': True,  # Add natural pauses
            'emphasize_questions': True,  # Emphasize question intonation
            'dialect': 'egyptian'  # Egyptian Arabic dialect
        }
        
        # Emotional tone settings
        self.emotional_tones = {
            'neutral': {'rate': 150, 'volume': 0.8, 'pitch': 1.0},
            'happy': {'rate': 170, 'volume': 0.9, 'pitch': 1.1},
            'sad': {'rate': 130, 'volume': 0.7, 'pitch': 0.9},
            'calm': {'rate': 140, 'volume': 0.75, 'pitch': 0.95},
            'excited': {'rate': 180, 'volume': 0.95, 'pitch': 1.15},
            'elderly_friendly': {'rate': 130, 'volume': 0.85, 'pitch': 0.95}
        }
        
        # Default emotional tone
        self.current_tone = 'neutral'
        
        # Thread for asynchronous speaking
        self.speak_thread = None
        self.is_speaking = False
        self.stop_speaking = False
        
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices"""
        voices = []
        for voice in self.engine.getProperty('voices'):
            voices.append({
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages,
                'gender': voice.gender,
                'age': voice.age
            })
        return voices
        
    def set_voice(self, voice_name: str) -> bool:
        """
        Set the voice by name.
        
        Args:
            voice_name: Name of the voice to use
            
        Returns:
            bool: True if voice was found and set, False otherwise
        """
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                self.voice_name = voice.name
                print(f"{voice_name} voice found: {voice.name}")
                return True
                
        # If specific voice not found, try to find any Arabic voice
        if voice_name.lower() == "arabic":
            for voice in voices:
                if "arabic" in voice.name.lower() or "ar" in voice.languages:
                    self.engine.setProperty('voice', voice.id)
                    self.voice_name = voice.name
                    print(f"Arabic voice found: {voice.name}")
                    return True
                    
        print(f"Voice '{voice_name}' not found. Using default voice.")
        return False
        
    def set_emotional_tone(self, tone: str) -> bool:
        """
        Set emotional tone for speech.
        
        Args:
            tone: Emotional tone (neutral, happy, sad, calm, excited, elderly_friendly)
            
        Returns:
            bool: True if tone was set, False if tone is not recognized
        """
        if tone in self.emotional_tones:
            settings = self.emotional_tones[tone]
            self.engine.setProperty('rate', settings['rate'])
            self.engine.setProperty('volume', settings['volume'])
            
            # Some TTS engines support pitch adjustment
            try:
                self.engine.setProperty('pitch', settings['pitch'])
            except:
                pass
                
            self.current_tone = tone
            return True
        return False
        
    def optimize_arabic_text(self, text: str) -> str:
        """
        Optimize Arabic text for better pronunciation.
        
        Args:
            text: Arabic text to optimize
            
        Returns:
            str: Optimized text
        """
        # Handle Arabic text direction
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            text = bidi_text
        except ImportError:
            pass  # Libraries not available
            
        # Apply optimizations based on settings
        if self.arabic_optimizations['elongate_vowels']:
            # Elongate certain vowels for emphasis
            vowel_map = {
                'ا': 'اا',  # Elongate alif
                'و': 'وو',  # Elongate waw
                'ي': 'يي'   # Elongate ya
            }
            for vowel, elongated in vowel_map.items():
                text = text.replace(vowel + ' ', elongated + ' ')
                
        if self.arabic_optimizations['pause_after_sentences']:
            # Add pauses after sentence endings
            for punct in ['.', '؟', '!', '،']:
                text = text.replace(punct, punct + ' <break time="500ms"/> ')
                
        if self.arabic_optimizations['emphasize_questions']:
            # Add emphasis to questions
            text = text.replace('؟', ' <emphasis level="strong"> ؟ </emphasis>')
            
        return text
        
    def speak(self, text: str, tone: Optional[str] = None) -> bool:
        """
        Speak text synchronously.
        
        Args:
            text: Text to speak
            tone: Optional emotional tone
            
        Returns:
            bool: True if speech completed, False if error occurred
        """
        if tone:
            self.set_emotional_tone(tone)
            
        try:
            # Optimize Arabic text
            optimized_text = self.optimize_arabic_text(text)
            
            # Speak the text
            self.engine.say(optimized_text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
            return False
            
    def speak_async(self, text: str, tone: Optional[str] = None) -> bool:
        """
        Speak text asynchronously in a separate thread.
        
        Args:
            text: Text to speak
            tone: Optional emotional tone
            
        Returns:
            bool: True if speech started, False if already speaking
        """
        if self.is_speaking:
            return False
            
        if tone:
            self.set_emotional_tone(tone)
            
        # Start speaking in a separate thread
        self.stop_speaking = False
        self.is_speaking = True
        self.speak_thread = threading.Thread(target=self._speak_thread, args=(text,))
        self.speak_thread.start()
        return True
        
    def _speak_thread(self, text: str):
        """Thread function for asynchronous speaking"""
        try:
            # Optimize Arabic text
            optimized_text = self.optimize_arabic_text(text)
            
            # Create a temporary callback to check for stop flag
            def on_word(name, location, length):
                return not self.stop_speaking
                
            # Connect callback
            self.engine.connect('started-word', on_word)
            
            # Speak the text
            self.engine.say(optimized_text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Error in TTS thread: {e}")
        finally:
            self.is_speaking = False
            
    def stop(self) -> bool:
        """
        Stop current speech.
        
        Returns:
            bool: True if speech was stopped, False if not speaking
        """
        if not self.is_speaking:
            return False
            
        self.stop_speaking = True
        
        # Wait for thread to finish
        if self.speak_thread and self.speak_thread.is_alive():
            self.speak_thread.join(timeout=1.0)
            
        return True
        
    def save_to_file(self, text: str, file_path: str, tone: Optional[str] = None) -> bool:
        """
        Save speech to audio file.
        
        Args:
            text: Text to speak
            file_path: Path to save audio file
            tone: Optional emotional tone
            
        Returns:
            bool: True if file was saved, False if error occurred
        """
        if tone:
            self.set_emotional_tone(tone)
            
        try:
            # Optimize Arabic text
            optimized_text = self.optimize_arabic_text(text)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # Save to file
            self.engine.save_to_file(optimized_text, file_path)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error saving TTS to file: {e}")
            return False
            
    def cleanup(self):
        """Clean up resources"""
        if self.is_speaking:
            self.stop()
        
        # Some engines need explicit cleanup
        try:
            self.engine.stop()
        except:
            pass

# Example usage
if __name__ == "__main__":
    tts = TTSService()
    
    print("Available voices:")
    voices = tts.get_available_voices()
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice['name']} ({voice['languages']})")
    
    # Test different emotional tones
    arabic_text = "مرحباً! كيف حالك اليوم؟ أنا هنا لمساعدتك على تذكر الأشياء المهمة."
    
    print("\nTesting different emotional tones:")
    for tone in ['neutral', 'happy', 'sad', 'calm', 'excited', 'elderly_friendly']:
        print(f"\nSpeaking with {tone} tone:")
        tts.speak(arabic_text, tone)
        time.sleep(1)
    
    # Save to file
    print("\nSaving speech to file...")
    tts.save_to_file(arabic_text, "test_speech.wav", "elderly_friendly")
    print("Speech saved to test_speech.wav")
    
    tts.cleanup()
