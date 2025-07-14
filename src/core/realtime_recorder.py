import pyaudio
import wave
import threading
import time
from typing import Optional, Callable

class RealTimeRecorder:
    """Real-time audio recording for voice interactions"""
    
    def __init__(self, 
                 sample_rate: int = 16000,
                 chunk_size: int = 1024,
                 format: int = pyaudio.paInt16,
                 channels: int = 1):
        """Initialize the real-time recorder"""
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.recording_thread = None
        self.frames = []
        
        # Callbacks
        self.on_recording_start: Optional[Callable] = None
        self.on_recording_stop: Optional[Callable] = None
        self.on_recording_data: Optional[Callable] = None
    
    def start_recording(self) -> bool:
        """Start recording audio"""
        if self.recording:
            return False
        
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.recording = True
            self.frames = []
            self.recording_thread = threading.Thread(target=self._recording_loop)
            self.recording_thread.start()
            
            if self.on_recording_start:
                self.on_recording_start()
            
            return True
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False
    
    def stop_recording(self) -> Optional[str]:
        """Stop recording and save to file"""
        if not self.recording:
            return None
        
        self.recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        
        # Save recording to file
        if self.frames:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            try:
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.format))
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(b''.join(self.frames))
                
                if self.on_recording_stop:
                    self.on_recording_stop(filename)
                
                return filename
                
            except Exception as e:
                print(f"Error saving recording: {e}")
                return None
        
        return None
    
    def _recording_loop(self):
        """Main recording loop"""
        while self.recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.frames.append(data)
                
                if self.on_recording_data:
                    self.on_recording_data(data)
                    
            except Exception as e:
                print(f"Error in recording loop: {e}")
                break
    
    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.recording
    
    def get_duration(self) -> float:
        """Get current recording duration in seconds"""
        if not self.frames:
            return 0.0
        
        total_frames = len(self.frames) * self.chunk_size
        return total_frames / self.sample_rate
    
    def cleanup(self):
        """Clean up resources"""
        if self.recording:
            self.stop_recording()
        
        if hasattr(self, 'audio'):
            self.audio.terminate()

# Voice Activity Detection (simple volume-based)
class SimpleVAD:
    """Simple Voice Activity Detection based on volume threshold"""
    
    def __init__(self, threshold: float = 0.01, min_duration: float = 0.5):
        """Initialize VAD"""
        self.threshold = threshold
        self.min_duration = min_duration
        self.is_speaking = False
        self.silence_start = None
        self.speech_start = None
    
    def process_audio_chunk(self, audio_data: bytes) -> str:
        """
        Process audio chunk and return VAD status
        Returns: 'speech', 'silence', or 'unknown'
        """
        import numpy as np
        
        # Convert bytes to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Calculate RMS (volume)
        rms = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))
        normalized_rms = rms / 32768.0  # Normalize to 0-1
        
        current_time = time.time()
        
        if normalized_rms > self.threshold:
            # Speech detected
            if not self.is_speaking:
                self.speech_start = current_time
                self.is_speaking = True
                self.silence_start = None
            return 'speech'
        else:
            # Silence detected
            if self.is_speaking:
                if self.silence_start is None:
                    self.silence_start = current_time
                elif current_time - self.silence_start > self.min_duration:
                    # End of speech detected
                    self.is_speaking = False
                    return 'end_speech'
            return 'silence'
        
        return 'unknown'

# Example usage
if __name__ == "__main__":
    recorder = RealTimeRecorder()
    vad = SimpleVAD()
    
    def on_start():
        print("Recording started...")
    
    def on_stop(filename):
        print(f"Recording stopped. Saved as: {filename}")
    
    def on_data(data):
        status = vad.process_audio_chunk(data)
        if status == 'end_speech':
            print("End of speech detected")
    
    recorder.on_recording_start = on_start
    recorder.on_recording_stop = on_stop
    recorder.on_recording_data = on_data
    
    print("Press Enter to start recording, Enter again to stop...")
    input()
    recorder.start_recording()
    input()
    filename = recorder.stop_recording()
    recorder.cleanup()
    
    print(f"Recording saved as: {filename}")
