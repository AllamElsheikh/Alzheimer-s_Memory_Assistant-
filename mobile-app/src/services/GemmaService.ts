import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = 'http://10.0.2.2:8000/api/v1'; // Android emulator localhost

export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  audioPath?: string;
  imagePath?: string;
}

export interface ConversationResponse {
  id: number;
  content: string;
  response: string;
  mood_score?: number;
  cognitive_score?: number;
  timestamp: string;
}

export interface MultimodalResponse {
  id: number;
  response: string;
  session_id: string;
  timestamp: string;
}

export class GemmaService {
  private sessionId: string | null = null;
  private patientId: number | null = null;

  constructor() {
    this.initializeSession();
  }

  private async initializeSession() {
    try {
      // Get or create session ID
      this.sessionId = await SecureStore.getItemAsync('current_session_id');
      if (!this.sessionId) {
        this.sessionId = this.generateSessionId();
        await SecureStore.setItemAsync('current_session_id', this.sessionId);
      }

      // Get patient ID
      const patientIdStr = await SecureStore.getItemAsync('current_patient_id');
      this.patientId = patientIdStr ? parseInt(patientIdStr) : 1; // Default patient ID
    } catch (error) {
      console.error('Error initializing session:', error);
      this.sessionId = this.generateSessionId();
      this.patientId = 1;
    }
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  async sendTextMessage(userText: string): Promise<Message> {
    try {
      await this.initializeSession();

      const response = await axios.post(`${API_BASE_URL}/conversations`, {
        patient_id: this.patientId,
        content: userText,
        session_id: this.sessionId
      });

      const data: ConversationResponse = response.data;

      return {
        id: data.id.toString(),
        text: data.response,
        isUser: false,
        timestamp: new Date(data.timestamp),
      };

    } catch (error) {
      console.error('Error sending text message:', error);
      return this.getFallbackResponse(userText);
    }
  }

  async sendMultimodalMessage(
    textPrompt: string,
    imageUri?: string,
    audioUri?: string
  ): Promise<Message> {
    try {
      await this.initializeSession();

      const formData = new FormData();
      formData.append('patient_id', this.patientId?.toString() || '1');
      formData.append('text_prompt', textPrompt);
      formData.append('session_id', this.sessionId || '');

      if (imageUri) {
        formData.append('image', {
          uri: imageUri,
          type: 'image/jpeg',
          name: 'image.jpg',
        } as any);
      }

      if (audioUri) {
        formData.append('audio', {
          uri: audioUri,
          type: 'audio/wav',
          name: 'audio.wav',
        } as any);
      }

      const response = await axios.post(
        `${API_BASE_URL}/conversations/multimodal`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const data: MultimodalResponse = response.data;

      return {
        id: data.id.toString(),
        text: data.response,
        isUser: false,
        timestamp: new Date(data.timestamp),
        imagePath: imageUri,
        audioPath: audioUri,
      };

    } catch (error) {
      console.error('Error sending multimodal message:', error);
      return this.getFallbackResponse(textPrompt);
    }
  }

  async generateGreeting(patientName: string, timeGreeting: string): Promise<string> {
    try {
      const greetingPrompt = `Generate a warm, personalized Arabic greeting for ${patientName}. Time: ${timeGreeting}. Keep it short and caring.`;
      
      const response = await this.sendTextMessage(greetingPrompt);
      return response.text;
    } catch (error) {
      console.error('Error generating greeting:', error);
      return `${timeGreeting} ${patientName}! كيف حالك اليوم؟`;
    }
  }

  async analyzePhoto(imageUri: string, context: string = ''): Promise<string> {
    try {
      const analysisPrompt = context || 'حلل هذه الصورة وساعدني أتذكر الذكريات المرتبطة بها';
      const response = await this.sendMultimodalMessage(analysisPrompt, imageUri);
      return response.text;
    } catch (error) {
      console.error('Error analyzing photo:', error);
      return 'عذراً، لم أستطع تحليل الصورة. حاول مرة أخرى.';
    }
  }

  async processVoiceMessage(audioUri: string, context: string = ''): Promise<Message> {
    try {
      const voicePrompt = context || 'استمع لهذه الرسالة الصوتية وارد عليها';
      return await this.sendMultimodalMessage(voicePrompt, undefined, audioUri);
    } catch (error) {
      console.error('Error processing voice message:', error);
      return this.getFallbackResponse('رسالة صوتية');
    }
  }

  async getCognitiveAssessment(assessmentType: string): Promise<any> {
    try {
      const response = await axios.post(`${API_BASE_URL}/assessments`, {
        patient_id: this.patientId,
        type: assessmentType
      });

      return response.data;
    } catch (error) {
      console.error('Error getting cognitive assessment:', error);
      return null;
    }
  }

  async submitAssessmentResponse(taskType: string, userResponse: string): Promise<any> {
    try {
      const response = await axios.post(`${API_BASE_URL}/assessments`, {
        patient_id: this.patientId,
        type: taskType,
        data: { user_response: userResponse }
      });

      return response.data;
    } catch (error) {
      console.error('Error submitting assessment response:', error);
      return null;
    }
  }

  private getFallbackResponse(userText: string): Message {
    const fallbackResponses = [
      'أهلاً وسهلاً! كيف يمكنني مساعدتك اليوم؟',
      'مرحباً حبيبي، أنا هنا معاك.',
      'تكلم براحتك، أنا بسمعك.',
      'إيه اللي عايز تحكيلي عنه؟',
      'أنا موجود عشان أساعدك، متقلقش.',
      'خد وقتك وحكيلي اللي في بالك.',
    ];

    // Simple context-aware fallback
    let response = fallbackResponses[0];
    const lowerText = userText.toLowerCase();
    
    if (lowerText.includes('مرحب') || lowerText.includes('أهل') || lowerText.includes('سلام')) {
      response = 'أهلاً وسهلاً بيك! نورت المكان.';
    } else if (lowerText.includes('إزيك') || lowerText.includes('عامل') || lowerText.includes('أخبار')) {
      response = 'أنا كويس الحمد لله، وإنت عامل إيه؟';
    } else if (lowerText.includes('تعبان') || lowerText.includes('مش كويس')) {
      response = 'متقلقش، هتبقى كويس إن شاء الله. عايز تحكيلي إيه اللي تعبك؟';
    } else {
      response = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
    }

    return {
      id: Date.now().toString(),
      text: response,
      isUser: false,
      timestamp: new Date(),
    };
  }

  async getConversationHistory(limit: number = 20): Promise<Message[]> {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/conversations?patient_id=${this.patientId}&session_id=${this.sessionId}`
      );

      return response.data.map((conv: any) => ({
        id: conv.id.toString(),
        text: conv.response,
        isUser: false,
        timestamp: new Date(conv.timestamp),
      }));
    } catch (error) {
      console.error('Error getting conversation history:', error);
      return [];
    }
  }

  async clearSession() {
    try {
      await SecureStore.deleteItemAsync('current_session_id');
      this.sessionId = this.generateSessionId();
      await SecureStore.setItemAsync('current_session_id', this.sessionId);
    } catch (error) {
      console.error('Error clearing session:', error);
    }
  }
}
