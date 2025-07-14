import whisper
import torch

class ASRService:
    """
    Handles Automatic Speech Recognition (ASR) using OpenAI's Whisper model.
    """

    def __init__(self, model_size="base"):
        """
        Initializes the ASRService, loading the Whisper model.

        Args:
            model_size (str): The size of the Whisper model to use (e.g., 'tiny', 'base', 'small').
        """
        self.model = None
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()

    def load_model(self):
        """
        Downloads and loads the Whisper model.
        """
        try:
            print(f"Loading Whisper model ({self.model_size})...")
            self.model = whisper.load_model(self.model_size, device=self.device)
            print(f"Whisper model loaded successfully on {self.device}.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None

    def transcribe_audio_file(self, audio_path: str) -> str:
        """
        Transcribes the given audio file into text.

        Args:
            audio_path (str): The path to the audio file (e.g., .wav, .mp3).

        Returns:
            str: The transcribed text, or an empty string if transcription fails.
        """
        if not self.model:
            print("ASR model is not available.")
            return ""

        try:
            print(f"Transcribing audio file: {audio_path}")
            # Specify the language as Arabic for better accuracy
            result = self.model.transcribe(audio_path, language="ar")
            transcribed_text = result['text']
            print(f"Transcription result: {transcribed_text}")
            return transcribed_text
        except Exception as e:
            print(f"Error during audio transcription: {e}")
            return ""

# Example usage (for testing purposes):
if __name__ == '__main__':
    # This part will only run when the script is executed directly
    # You would need a sample audio file named 'test_audio.wav' for this to work.
    asr = ASRService(model_size="base")
    
    # Create a dummy audio file for testing if you don't have one.
    # NOTE: This requires 'soundfile' and 'numpy' to be installed: pip install soundfile numpy
    try:
        import soundfile as sf
        import numpy as np
        samplerate = 16000 # Whisper expects 16kHz
        duration = 5 # seconds
        frequency = 440 # Hz
        t = np.linspace(0., duration, int(samplerate * duration), endpoint=False)
        amplitude = np.iinfo(np.int16).max * 0.5
        data = amplitude * np.sin(2. * np.pi * frequency * t)
        dummy_audio_path = "test_audio.wav"
        sf.write(dummy_audio_path, data.astype(np.int16), samplerate)
        print(f"Created dummy audio file at {dummy_audio_path}")

        transcription = asr.transcribe_audio_file(dummy_audio_path)
        if transcription:
            print(f"\nFinal Transcription: {transcription}")
        else:
            print("\nCould not transcribe the audio.")

    except ImportError:
        print("\nPlease install 'soundfile' and 'numpy' to run the example.")
    except Exception as e:
        print(f"An error occurred during the example run: {e}")
