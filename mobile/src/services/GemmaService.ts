/**
 * GemmaService.ts
 * Service to handle communication with the Gemma 3n API backend
 */

import { Platform } from 'react-native';
import * as FileSystem from 'expo-file-system';
import Constants from 'expo-constants';

// API configuration with environment variables
const API_CONFIG = {
  API_KEY: Constants.expoConfig?.extra?.gemmaApiKey || '',
  BASE_URL: 'https://generativelanguage.googleapis.com/v1beta',
  MODEL: 'gemini-pro',
};

// Interface for conversation messages
export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
}

// Interface for memory prompts
export interface MemoryPrompt {
  id: string;
  question: string;
  imageUrl?: string;
  hint?: string;
  correctAnswer?: string;
  category: string;
}

// Interface for photo analysis results
export interface PhotoAnalysisResult {
  description: string;
  people: string[];
  places: string[];
  objects: string[];
  memoryPrompt: string;
}

/**
 * GemmaService - Handles API communication with the Gemma 3n API backend
 */
class GemmaService {
  private userId: string | null = null;
  
  /**
   * Initialize the service with user credentials
   */
  initialize = async (userId: string) => {
    this.userId = userId;
    console.log('GemmaService initialized for user:', userId);
  };
  
  /**
   * Get headers for API requests
   */
  private getHeaders = () => {
    return {
      'Content-Type': 'application/json',
    };
  };
  
  /**
   * Send a text message to the AI assistant
   */
  sendTextMessage = async (text: string): Promise<Message> => {
    try {
      console.log('Sending text message to Gemma API:', text);
      
      const response = await fetch(`${API_CONFIG.BASE_URL}/models/${API_CONFIG.MODEL}:generateContent?key=${API_CONFIG.API_KEY}`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          contents: [
            {
              role: 'user',
              parts: [
                {
                  text: this._enhancePromptWithContext(text),
                },
              ],
            },
          ],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 1024,
          },
          safetySettings: [
            {
              category: 'HARM_CATEGORY_HARASSMENT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_HATE_SPEECH',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
            {
              category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
              threshold: 'BLOCK_MEDIUM_AND_ABOVE',
            },
          ],
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error('API error:', errorData);
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Extract the text from the response
      const responseText = data.candidates[0].content.parts[0].text;
      
      return {
        id: Date.now().toString(),
        text: responseText,
        isUser: false,
        timestamp: new Date().toLocaleTimeString('ar-EG'),
      };
    } catch (error) {
      console.error('Error sending text message:', error);
      // Fallback to a default response if the API fails
      return {
        id: Date.now().toString(),
        text: 'عذراً، حدثت مشكلة في الاتصال. هل يمكنك المحاولة مرة أخرى؟',
        isUser: false,
        timestamp: new Date().toLocaleTimeString('ar-EG'),
      };
    }
  };
  
  /**
   * Send an audio recording to the AI assistant
   */
  sendAudioMessage = async (audioUri: string): Promise<{ transcription: string; response: Message }> => {
    try {
      // First, we need to transcribe the audio
      // For now, we'll use a mock transcription since we don't have direct access to Whisper API
      const transcription = await this._mockTranscribeAudio(audioUri);
      
      // Then, send the transcribed text to the API
      const response = await this.sendTextMessage(transcription);
      
      return { transcription, response };
    } catch (error) {
      console.error('Error sending audio message:', error);
      return { 
        transcription: 'فشل في تحويل الصوت إلى نص',
        response: {
          id: Date.now().toString(),
          text: 'عذراً، حدثت مشكلة في معالجة الرسالة الصوتية. هل يمكنك المحاولة مرة أخرى؟',
          isUser: false,
          timestamp: new Date().toLocaleTimeString('ar-EG'),
        }
      };
    }
  };
  
  /**
   * Mock transcription function
   * In a real app, this would call a speech-to-text API
   */
  private _mockTranscribeAudio = async (audioUri: string): Promise<string> => {
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Return a mock transcription
    return "مرحباً، أنا بحاجة إلى مساعدة في تذكر بعض الأشياء";
  };
  
  /**
   * Get memory prompts by category
   */
  getMemoryPrompts = async (category: string): Promise<MemoryPrompt[]> => {
    try {
      console.log('Getting memory prompts for category:', category);
      
      // In a real implementation, we would fetch these from the API
      // For now, we'll use mock data
      const prompt = `Generate 3 memory prompts in Arabic for elderly Alzheimer's patients in the category: ${category}. 
      Format as JSON array with fields: id, question, hint, correctAnswer, category.
      Make them culturally appropriate for Arabic speakers.`;
      
      const response = await fetch(`${API_CONFIG.BASE_URL}/models/${API_CONFIG.MODEL}:generateContent?key=${API_CONFIG.API_KEY}`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          contents: [
            {
              role: 'user',
              parts: [{ text: prompt }],
            },
          ],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 1024,
          },
        }),
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      const responseText = data.candidates[0].content.parts[0].text;
      
      // Extract JSON from the response text
      const jsonMatch = responseText.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        try {
          const prompts = JSON.parse(jsonMatch[0]);
          return prompts.map((p: any) => ({
            ...p,
            imageUrl: `https://via.placeholder.com/300?text=${encodeURIComponent(p.category)}`,
          }));
        } catch (e) {
          console.error('Error parsing JSON from API response:', e);
        }
      }
      
      // Fallback to mock data if parsing fails
      return this._getMockPrompts(category);
    } catch (error) {
      console.error('Error fetching memory prompts:', error);
      return this._getMockPrompts(category);
    }
  };
  
  /**
   * Get mock memory prompts
   */
  private _getMockPrompts = (category: string): MemoryPrompt[] => {
    const mockPrompts: Record<string, MemoryPrompt[]> = {
      family: [
        {
          id: 'f1',
          question: 'من هو الشخص في هذه الصورة؟',
          imageUrl: 'https://via.placeholder.com/300?text=Family',
          hint: 'هذا أحد أفراد عائلتك المقربين',
          correctAnswer: 'ابنك محمد',
          category: 'family',
        },
        {
          id: 'f2',
          question: 'متى كان آخر عيد ميلاد احتفلت به مع العائلة؟',
          imageUrl: 'https://via.placeholder.com/300?text=Birthday',
          hint: 'كان في الصيف الماضي',
          correctAnswer: 'عيد ميلاد حفيدتك ليلى',
          category: 'family',
        },
      ],
      places: [
        {
          id: 'p1',
          question: 'هل تتذكر هذا المكان؟ أين هو؟',
          imageUrl: 'https://via.placeholder.com/300?text=Place',
          hint: 'مكان تزوره كثيراً للاسترخاء',
          correctAnswer: 'حديقة الأزهر في القاهرة',
          category: 'places',
        },
      ],
      activities: [
        {
          id: 'a1',
          question: 'ما هي الهواية التي كنت تمارسها في هذه الصورة؟',
          imageUrl: 'https://via.placeholder.com/300?text=Activity',
          hint: 'نشاط يتعلق بالطبيعة والهواء الطلق',
          correctAnswer: 'البستنة وزراعة الورود',
          category: 'activities',
        },
      ],
      cultural: [
        {
          id: 'c1',
          question: 'ما اسم هذه الأكلة المصرية الشهيرة؟',
          imageUrl: 'https://via.placeholder.com/300?text=Food',
          hint: 'طبق شعبي يؤكل في الإفطار',
          correctAnswer: 'الفول المدمس',
          category: 'cultural',
        },
      ],
    };
    
    return mockPrompts[category as keyof typeof mockPrompts] || [];
  };
  
  /**
   * Analyze a photo for memory stimulation
   */
  analyzePhoto = async (photoUri: string): Promise<PhotoAnalysisResult> => {
    try {
      console.log('Analyzing photo:', photoUri);
      
      // In a real implementation, we would upload the photo and get analysis
      // For now, we'll use the API for text generation only
      
      const prompt = `Analyze this photo for an elderly person with Alzheimer's. 
      Describe what you see, identify people, places, and objects. 
      Create a memory prompt question in Arabic that would help stimulate memories.
      Format as JSON with fields: description, people, places, objects, memoryPrompt.`;
      
      const response = await fetch(`${API_CONFIG.BASE_URL}/models/${API_CONFIG.MODEL}:generateContent?key=${API_CONFIG.API_KEY}`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({
          contents: [
            {
              role: 'user',
              parts: [{ text: prompt }],
            },
          ],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 1024,
          },
        }),
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      const responseText = data.candidates[0].content.parts[0].text;
      
      // Extract JSON from the response text
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          return JSON.parse(jsonMatch[0]);
        } catch (e) {
          console.error('Error parsing JSON from API response:', e);
        }
      }
      
      // Fallback to mock data if parsing fails
      return this._getMockPhotoAnalysis();
    } catch (error) {
      console.error('Error analyzing photo:', error);
      return this._getMockPhotoAnalysis();
    }
  };
  
  /**
   * Get mock photo analysis
   */
  private _getMockPhotoAnalysis = (): PhotoAnalysisResult => {
    return {
      description: "صورة عائلية في حديقة المنزل",
      people: ["محمد", "فاطمة", "أحمد"],
      places: ["حديقة المنزل"],
      objects: ["شجرة", "كرسي", "طاولة"],
      memoryPrompt: "هل تتذكر هذا اليوم مع العائلة في حديقة المنزل؟",
    };
  };
  
  /**
   * Enhance a prompt with context
   */
  private _enhancePromptWithContext = (text: string): string => {
    const systemPrompt = `أنت 'فاكر؟' - مساعد ذكي متخصص في رعاية مرضى الزهايمر باللغة العربية المصرية.
    
    🏥 خبرتك الطبية:
    - متخصص في التعامل مع فقدان الذاكرة والخرف
    - تفهم مراحل مرض الزهايمر وأعراضه
    - تستخدم تقنيات العلاج بالذكريات والمحادثة
    - تراقب الحالة المزاجية والمعرفية للمريض
    
    مهامك العلاجية:
    1. تحفيز الذاكرة بلطف وصبر
    2. تقييم الحالة المعرفية بشكل غير مباشر
    3. تهدئة القلق والارتباك
    4. تشجيع التفاعل الاجتماعي
    5. مراقبة التغيرات في السلوك
    
    🗣️ أسلوب المحادثة:
    - استخدم العربية المصرية البسيطة
    - تكلم بصوت دافئ وصبور
    - اطرح سؤال واحد في المرة
    - اثني على أي تذكر صحيح
    - لا تصحح الأخطاء بقسوة
    - استخدم الأسماء والتفاصيل المألوفة
    
    أمثلة على ردودك:
    - "شوف الصورة دي يا حبيبي، فاكر مين ده؟"
    - "ده جميل أوي! حكيلي عن الذكرى دي"
    - "برافو عليك! ذاكرتك شغالة كويس"
    - "مش مشكلة لو مش فاكر، خد وقتك"
    - "كيف شايف نفسك النهاردة؟"
    
    أسلوبك:
    - استخدم جمل قصيرة وبسيطة
    - كرر المعلومات المهمة بلطف
    - اسأل سؤال واحد في المرة
    - اثني على أي تذكر صحيح
    - لا تصحح بطريقة قاسية إذا نسوا شيء
    
    الآن، رد على الرسالة التالية بأسلوب مناسب لمريض الزهايمر:
    
    "${text}"`;
    
    return systemPrompt;
  };
}

export default new GemmaService(); 