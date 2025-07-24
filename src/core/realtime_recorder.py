import os
import wave
import time
import numpy as np
import threading
import pyaudio
import audioop
from datetime import datetime
from typing import Optional, Callable, Dict, Any

class RealtimeRecorder:
    """
    Real-time audio recorder with voice activity detection optimized for Arabic speech.
    Provides continuous recording with automatic silence detection.
    """
    
    def __init__(self, 
                 output_dir='data/audio/recordings',
                 format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 chunk=1024,
                 silence_threshold=1000,
                 silence_duration=1.5,
                 max_duration=30.0):
        """
        Initialize the real-time recorder.
        
        Args:
            output_dir: Directory to save recordings
            format: Audio format (default: 16-bit PCM)
            channels: Number of audio channels (default: mono)
            rate: Sample rate in Hz (default: 16kHz for Whisper compatibility)
            chunk: Buffer size in frames
            silence_threshold: Threshold for silence detection
            silence_duration: Duration of silence to end recording (seconds)
            max_duration: Maximum recording duration (seconds)
        """
        self.output_dir = output_dir
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.max_duration = max_duration
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Recording state
        self.is_recording = False
        self.stop_recording = False
        self.recording_thread = None
        self.current_file = None
        self.on_recording_complete = None
        
        # Voice activity detection parameters
        self.vad_enabled = True
        self.vad_energy_history = []
        self.vad_history_size = 10
        self.vad_energy_threshold = 300  # Adjusted for Arabic speech patterns
        self.vad_speech_detected = False
        self.vad_silence_counter = 0
        self.vad_speech_counter = 0
        
        # Arabic speech optimization
        self.arabic_speech_params = {
            'energy_boost': 1.2,  # Boost for softer consonants in Arabic
            'min_utterance_ms': 500,  # Minimum utterance length in ms
            'trailing_silence_ms': 800  # Keep trailing silence for natural speech
        }
        
    def start_recording(self, callback: Optional[Callable[[str], None]] = None):
        """
        Start recording audio in a separate thread.
        
        Args:
            callback: Function to call when recording is complete with path to audio file
        """
        if self.is_recording:
            print("Already recording")
            return None
            
        self.stop_recording = False
        self.is_recording = True
        self.on_recording_complete = callback
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = os.path.join(self.output_dir, f"recording_{timestamp}.wav")
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        
        return self.current_file
        
    def stop_recording(self):
        """Stop the current recording"""
        if not self.is_recording:
            return False
        
        self.stop_recording = True
        if self.recording_thread:
            self.recording_thread.join()
        
        return True
        
    def _record_audio(self):
        """Record audio with voice activity detection"""
        try:
            # Open audio stream
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            print(f"🎤 Recording started... (Output: {self.current_file})")
            
            frames = []
            silent_chunks = 0
            active_chunks = 0
            start_time = time.time()
            recording_started = False
            
            # Calculate parameters in chunks
            silence_chunks = int(self.silence_duration * self.rate / self.chunk)
            min_utterance_chunks = int(self.arabic_speech_params['min_utterance_ms'] * self.rate / (self.chunk * 1000))
            trailing_silence_chunks = int(self.arabic_speech_params['trailing_silence_ms'] * self.rate / (self.chunk * 1000))
            
            # Record until stopped or silence detected
            while not self.stop_recording:
                # Read audio chunk
                data = stream.read(self.chunk, exception_on_overflow=False)
                
                # Voice activity detection
                if self.vad_enabled:
                    # Calculate audio energy
                    energy = audioop.rms(data, 2) * self.arabic_speech_params['energy_boost']
                    
                    # Detect speech
                    is_speech = energy > self.silence_threshold
                    
                    # Update speech detection state
                    if is_speech:
                        silent_chunks = 0
                        active_chunks += 1
                        recording_started = True
                    else:
                        silent_chunks += 1
                        
                    # Add frames if recording has started
                    if recording_started:
                        frames.append(data)
        
                    # Check if we should stop recording due to silence
                    elapsed_time = time.time() - start_time
                    if (recording_started and 
                        active_chunks > min_utterance_chunks and 
                        silent_chunks > silence_chunks and 
                        elapsed_time > 2.0):
                        # Add trailing silence for natural speech ending
                        for _ in range(min(trailing_silence_chunks, silence_chunks)):
                            frames.append(data)
                        break
                        
                    # Check for maximum duration
                    if elapsed_time > self.max_duration:
                        break
                else:
                    # Simple recording without VAD
                    frames.append(data)
                    
                    # Check for maximum duration
                    if time.time() - start_time > self.max_duration:
                        break
            
            # Close stream
            stream.stop_stream()
            stream.close()
            
            # Save recording if we have frames
            if frames:
                self._save_recording(frames)
                print(f"🎤 Recording saved: {self.current_file}")
                
                # Call callback with file path
                if self.on_recording_complete:
                    self.on_recording_complete(self.current_file)
            else:
                print("No audio recorded")
                self.current_file = None
                
            except Exception as e:
            print(f"Error during recording: {e}")
            self.current_file = None
        finally:
            self.is_recording = False
            
    def _save_recording(self, frames):
        """Save recorded frames to WAV file"""
        try:
            wf = wave.open(self.current_file, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            return True
        except Exception as e:
                print(f"Error saving recording: {e}")
            return False
            
    def adjust_silence_threshold(self, threshold):
        """Adjust the silence threshold"""
        self.silence_threshold = threshold
        
    def optimize_for_arabic(self, speaker_type="adult"):
        """
        Optimize recording parameters for Arabic speech patterns
        
        Args:
            speaker_type: Type of speaker (adult, elderly, child)
        """
        if speaker_type == "elderly":
            # Elderly speakers often have softer speech
            self.silence_threshold = 800
            self.arabic_speech_params['energy_boost'] = 1.5
            self.arabic_speech_params['min_utterance_ms'] = 700
            self.arabic_speech_params['trailing_silence_ms'] = 1000
        elif speaker_type == "child":
            # Children have higher pitched voices
            self.silence_threshold = 1200
            self.arabic_speech_params['energy_boost'] = 1.0
            self.arabic_speech_params['min_utterance_ms'] = 400
            self.arabic_speech_params['trailing_silence_ms'] = 600
        else:
            # Default adult settings
            self.silence_threshold = 1000
            self.arabic_speech_params['energy_boost'] = 1.2
            self.arabic_speech_params['min_utterance_ms'] = 500
            self.arabic_speech_params['trailing_silence_ms'] = 800
            
    def get_available_devices(self):
        """Get list of available audio input devices"""
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxInputChannels'],
                    'sample_rate': device_info['defaultSampleRate']
                })
        return devices
        
    def set_input_device(self, device_index):
        """Set the input device by index"""
        if device_index >= 0 and device_index < self.audio.get_device_count():
            # Store device index for next recording
            self.device_index = device_index
            return True
        return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.is_recording:
            self.stop_recording()
            self.audio.terminate()

# Example usage
if __name__ == "__main__":
    recorder = RealtimeRecorder()
    
    def on_recording_done(file_path):
        print(f"Recording complete: {file_path}")
        
    print("Available audio input devices:")
    devices = recorder.get_available_devices()
    for device in devices:
        print(f"Index: {device['index']}, Name: {device['name']}")
        
    print("\nOptimizing for Arabic elderly speech...")
    recorder.optimize_for_arabic("elderly")
    
    print("\nPress Enter to start recording (max 10 seconds)...")
    input()
    
    file_path = recorder.start_recording(on_recording_done)
    
    print("Recording... Press Enter to stop")
    input()
    
    recorder.stop_recording()
    recorder.cleanup()
