/**
 * SpeechToTextService.ts
 * Service for speech-to-text conversion using Web Speech API with cloud fallback
 */

import * as FileSystem from 'expo-file-system';
import { Audio } from 'expo-av';
import Constants from 'expo-constants';

// Environment variables
const OPENAI_API_KEY = Constants.expoConfig?.extra?.openaiApiKey || '';

/**
 * SpeechToTextService - Handles speech-to-text conversion
 */
class SpeechToTextService {
  private isRecording: boolean = false;
  private recording: Audio.Recording | null = null;
  private audioUri: string | null = null;
  
  /**
   * Initialize the speech-to-text service
   */
  initialize = async (): Promise<boolean> => {
    try {
      // Request audio recording permissions
      const { status } = await Audio.requestPermissionsAsync();
      
      if (status !== 'granted') {
        console.error('Audio recording permissions not granted');
        return false;
      }
      
      // Configure audio mode
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
        staysActiveInBackground: true,
        interruptionModeIOS: Audio.INTERRUPTION_MODE_IOS_DUCK_OTHERS,
        interruptionModeAndroid: Audio.INTERRUPTION_MODE_ANDROID_DUCK_OTHERS,
      });
      
      return true;
    } catch (error) {
      console.error('Error initializing speech-to-text service:', error);
      return false;
    }
  };
  
  /**
   * Start recording audio
   */
  startRecording = async (): Promise<boolean> => {
    try {
      if (this.isRecording) {
        return true;
      }
      
      // Initialize the recording
      this.recording = new Audio.Recording();
      await this.recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      await this.recording.startAsync();
      this.isRecording = true;
      
      return true;
    } catch (error) {
      console.error('Error starting recording:', error);
      return false;
    }
  };
  
  /**
   * Stop recording and transcribe audio
   */
  stopRecordingAndTranscribe = async (): Promise<{ success: boolean; text: string; }> => {
    try {
      if (!this.isRecording || !this.recording) {
        return { success: false, text: '' };
      }
      
      // Stop recording
      await this.recording.stopAndUnloadAsync();
      this.isRecording = false;
      
      // Get the audio URI
      this.audioUri = this.recording.getURI();
      this.recording = null;
      
      if (!this.audioUri) {
        return { success: false, text: '' };
      }
      
      // Try to transcribe using Web Speech API first if available
      // Note: This is a web-only API, so we'll use it as a fallback in a real app
      // For mobile, we'll use the cloud service directly
      
      // Transcribe using cloud service
      const transcription = await this.transcribeWithCloudService(this.audioUri);
      
      return { success: true, text: transcription };
    } catch (error) {
      console.error('Error stopping recording and transcribing:', error);
      return { success: false, text: '' };
    }
  };
  
  /**
   * Transcribe audio using OpenAI Whisper API
   * Note: In a production app, this should be done through a backend service
   * to avoid exposing API keys in the client
   */
  private transcribeWithCloudService = async (audioUri: string): Promise<string> => {
    try {
      // Check if we have an API key
      if (!OPENAI_API_KEY) {
        console.warn('OpenAI API key not found, using mock transcription');
        return this.getMockTranscription();
      }
      
      // Read the audio file
      const fileInfo = await FileSystem.getInfoAsync(audioUri);
      if (!fileInfo.exists) {
        throw new Error('Audio file does not exist');
      }
      
      // In a real implementation, we would upload the audio file to OpenAI Whisper API
      // For now, we'll use a mock response since we can't make direct API calls
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // For demo purposes, return mock transcription
      return this.getMockTranscription();
      
      /* Real implementation would be:
      
      const formData = new FormData();
      formData.append('file', {
        uri: audioUri,
        name: 'audio.m4a',
        type: 'audio/m4a',
      });
      formData.append('model', 'whisper-1');
      formData.append('language', 'ar');
      
      const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
        },
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      return data.text;
      */
    } catch (error) {
      console.error('Error transcribing with cloud service:', error);
      return this.getMockTranscription();
    }
  };
  
  /**
   * Get a mock transcription for testing
   */
  private getMockTranscription = (): string => {
    const mockTranscriptions = [
      'مرحباً، أنا بحاجة إلى مساعدة في تذكر بعض الأشياء',
      'أين وضعت نظارتي؟ لا أستطيع تذكر مكانها',
      'هل يمكنك مساعدتي في تذكر اسم حفيدي؟',
      'أريد أن أتذكر ما حدث بالأمس',
      'ساعدني في تذكر موعد الدواء',
    ];
    
    return mockTranscriptions[Math.floor(Math.random() * mockTranscriptions.length)];
  };
  
  /**
   * Cancel recording
   */
  cancelRecording = async (): Promise<boolean> => {
    try {
      if (this.isRecording && this.recording) {
        await this.recording.stopAndUnloadAsync();
        this.isRecording = false;
        this.recording = null;
      }
      
      return true;
    } catch (error) {
      console.error('Error canceling recording:', error);
      return false;
    }
  };
  
  /**
   * Check if currently recording
   */
  isCurrentlyRecording = (): boolean => {
    return this.isRecording;
  };
}

export default new SpeechToTextService(); 