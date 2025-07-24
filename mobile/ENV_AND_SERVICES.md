# Environment Variables and Services

This document explains how environment variables and the speech-to-text service are implemented in the فاكر؟ (Faker?) Memory Assistant app.

## Environment Variables

The app uses environment variables to securely manage API keys and other sensitive information.

### Setup

1. **app.config.js**: This file loads environment variables and makes them available to the app:

```javascript
// Environment variables configuration for Expo
import 'dotenv/config';

export default {
  // ... app configuration ...
  extra: {
    // Environment variables
    gemmaApiKey: process.env.GEMMA_API_KEY || 'AIzaSyD7M1y4CkI9ODgbeL-7qE2O9W6m5BdxQkE', // Fallback to the provided key for development
    openaiApiKey: process.env.OPENAI_API_KEY || '',
    // ...
  }
};
```

2. **env.example**: This file provides a template for the `.env` file:

```
# Environment Variables for فاكر؟ (Faker?) Memory Assistant
# Copy this file to .env and fill in your API keys

# Google Gemma API Key
GEMMA_API_KEY=your_gemma_api_key_here

# OpenAI API Key (for speech-to-text)
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Accessing Environment Variables**: Environment variables are accessed using `expo-constants`:

```javascript
import Constants from 'expo-constants';

const API_KEY = Constants.expoConfig?.extra?.gemmaApiKey || '';
```

### Security Considerations

- The `.env` file should never be committed to version control
- For production builds, environment variables should be set in the CI/CD pipeline
- For Expo EAS builds, use the `--env-file` option or the EAS secret management system

## Speech-to-Text Service

The app includes a dedicated service for speech-to-text conversion, which can be integrated with cloud services.

### SpeechToTextService

This service handles:
- Audio recording permissions
- Recording management
- Transcription of audio to text

```javascript
class SpeechToTextService {
  // Initialize the service and request permissions
  initialize = async (): Promise<boolean> => { ... }
  
  // Start recording audio
  startRecording = async (): Promise<boolean> => { ... }
  
  // Stop recording and transcribe audio
  stopRecordingAndTranscribe = async (): Promise<{ success: boolean; text: string; }> => { ... }
  
  // Transcribe audio using cloud service
  private transcribeWithCloudService = async (audioUri: string): Promise<string> => { ... }
}
```

### Integration with OpenAI Whisper API

The service is designed to work with the OpenAI Whisper API for Arabic speech recognition:

```javascript
const transcribeWithCloudService = async (audioUri: string): Promise<string> => {
  // Create form data with audio file
  const formData = new FormData();
  formData.append('file', {
    uri: audioUri,
    name: 'audio.m4a',
    type: 'audio/m4a',
  });
  formData.append('model', 'whisper-1');
  formData.append('language', 'ar');
  
  // Make API request
  const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
    },
    body: formData,
  });
  
  // Process response
  const data = await response.json();
  return data.text;
};
```

### Fallback Mechanism

If the API key is not available or the API call fails, the service falls back to mock transcriptions:

```javascript
private getMockTranscription = (): string => {
  const mockTranscriptions = [
    'مرحباً، أنا بحاجة إلى مساعدة في تذكر بعض الأشياء',
    'أين وضعت نظارتي؟ لا أستطيع تذكر مكانها',
    // ...
  ];
  
  return mockTranscriptions[Math.floor(Math.random() * mockTranscriptions.length)];
};
```

## Usage in the App

The ConversationScreen uses both the environment variables (via GemmaService) and the SpeechToTextService:

```javascript
// Initialize services
useEffect(() => {
  const initSpeechService = async () => {
    await SpeechToTextService.initialize();
  };
  
  initSpeechService();
}, []);

// Handle voice recording
const stopRecording = async () => {
  // Get transcription
  const result = await SpeechToTextService.stopRecordingAndTranscribe();
  
  // Get AI response using GemmaService
  const response = await GemmaService.sendTextMessage(result.text);
  
  // Display and speak response
  // ...
};
```

## Future Improvements

1. **Backend Proxy**: Move API calls to a backend service to avoid exposing API keys in the client
2. **Streaming Transcription**: Implement real-time transcription for a more responsive experience
3. **Offline Support**: Add offline speech recognition for basic commands
4. **Multiple Languages**: Support multiple Arabic dialects for better accessibility 