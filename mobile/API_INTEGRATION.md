# Gemma API Integration

This document explains how the فاكر؟ (Faker?) Memory Assistant app integrates with the Google Gemma API.

## API Configuration

The app uses the Google Gemini Pro API with the following configuration:

```javascript
const API_CONFIG = {
  API_KEY: 'AIzaSyD7M1y4CkI9ODgbeL-7qE2O9W6m5BdxQkE',
  BASE_URL: 'https://generativelanguage.googleapis.com/v1beta',
  MODEL: 'gemini-pro',
};
```

## Integration Points

The app integrates with the Gemma API at three main points:

### 1. Conversation

When the user sends a text or voice message, the app sends a request to the Gemma API with a carefully crafted prompt that includes:

- System instructions for responding to Alzheimer's patients in Egyptian Arabic
- Guidelines for tone, simplicity, and patience
- The user's message

```javascript
sendTextMessage = async (text: string): Promise<Message> => {
  // API call with enhanced prompt
  const response = await fetch(`${API_CONFIG.BASE_URL}/models/${API_CONFIG.MODEL}:generateContent?key=${API_CONFIG.API_KEY}`, {
    method: 'POST',
    headers: this.getHeaders(),
    body: JSON.stringify({
      contents: [{
        role: 'user',
        parts: [{ text: this._enhancePromptWithContext(text) }],
      }],
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 1024,
      },
      // Safety settings...
    }),
  });
  
  // Process response...
}
```

### 2. Memory Prompts

For memory exercises, the app requests culturally appropriate prompts in Arabic:

```javascript
getMemoryPrompts = async (category: string): Promise<MemoryPrompt[]> => {
  const prompt = `Generate 3 memory prompts in Arabic for elderly Alzheimer's patients in the category: ${category}. 
  Format as JSON array with fields: id, question, hint, correctAnswer, category.
  Make them culturally appropriate for Arabic speakers.`;
  
  // API call...
  // Parse JSON from response...
}
```

### 3. Photo Analysis

When analyzing photos for memory stimulation:

```javascript
analyzePhoto = async (photoUri: string): Promise<PhotoAnalysisResult> => {
  const prompt = `Analyze this photo for an elderly person with Alzheimer's. 
  Describe what you see, identify people, places, and objects. 
  Create a memory prompt question in Arabic that would help stimulate memories.
  Format as JSON with fields: description, people, places, objects, memoryPrompt.`;
  
  // API call...
  // Parse JSON from response...
}
```

## Prompt Engineering

The app uses careful prompt engineering to ensure the Gemma API responds appropriately for Alzheimer's patients:

### System Prompt

```
أنت 'فاكر؟' - مساعد ذكي متخصص في رعاية مرضى الزهايمر باللغة العربية المصرية.

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
```

## Error Handling

The app includes fallback mechanisms for API failures:

1. **Network Errors**: If the API call fails, the app displays a friendly error message in Arabic
2. **Parsing Errors**: If JSON parsing fails, the app falls back to mock data
3. **Rate Limiting**: The app handles API rate limiting with appropriate error messages

## Security

The API key is stored in the app configuration. In a production environment, this should be:

1. Stored securely using environment variables
2. Accessed through a backend proxy to avoid exposing the key
3. Restricted to specific domains/apps in the Google Cloud Console

## Future Improvements

1. **Streaming Responses**: Implement streaming for more responsive conversations
2. **Image Upload**: Add direct image upload to the API when Gemini Vision becomes available
3. **Voice Processing**: Integrate with a speech-to-text API for better voice recognition
4. **Caching**: Implement response caching to reduce API calls
5. **User Profiles**: Personalize prompts based on user profiles and history 