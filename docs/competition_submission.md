# 🧠 فاكر؟ (Faker?) - Alzheimer's Memory Assistant

## 🏆 Google Gemma 3n Hackathon Submission

### 📋 PROJECT OVERVIEW

**فاكر؟** (pronounced "Faker?", meaning "Do you remember?" in Egyptian Arabic) is an AI memory assistant designed specifically for Arabic-speaking seniors with Alzheimer's disease. It leverages Google's Gemma 3n model to provide culturally appropriate memory support, cognitive assessment, and companionship in Egyptian Arabic.

### 🌍 ADDRESSING A CRITICAL NEED

- **25+ million** Arabic-speaking seniors worldwide
- **2+ million** Alzheimer's cases in the Arab world
- **Zero** existing Arabic AI solutions for memory care
- **Cultural barriers** to traditional memory assistance

### 🚀 TECHNICAL INNOVATIONS

#### 1. Gemma 3n Integration
- Local model integration via Hugging Face
- 4-bit quantization for efficient memory usage
- Optimized prompting for Arabic language
- Graceful fallback to mock mode for testing

#### 2. Multimodal Processing
- Simultaneous handling of text, image, and audio inputs
- Real-time processing with threading
- Context-aware responses
- Session management and reporting

#### 3. Arabic Speech Processing
- Real-time voice recording with voice activity detection
- Arabic speech pattern optimization for elderly users
- Continuous audio capture with automatic silence detection
- Integration with OpenAI Whisper for Arabic transcription

#### 4. Advanced TTS for Arabic
- Enhanced TTS service with emotional tone variations
- Arabic text optimization for better pronunciation
- Asynchronous speech generation
- Elderly-friendly voice settings

#### 5. Intelligent Memory System
- Advanced memory retrieval with associative graph
- Semantic search capabilities using Gemma 3n
- Memory reinforcement based on recall success
- Personalized memory prompts for cognitive stimulation

#### 6. Image Recognition
- Face detection and recognition
- Support for known faces with relationship information
- Arabic memory prompts based on recognized people
- Family photo analysis for memory stimulation

#### 7. Cognitive Assessment
- Comprehensive evaluation of memory, attention, language, and executive function
- Gemma 3n-powered response analysis
- Detailed reporting and recommendations
- Progress tracking over time

### 💡 WHY GEMMA 3N?

Gemma 3n is the perfect foundation for our project because:

1. **Multilingual capabilities** - Essential for Arabic language support
2. **Efficient local deployment** - Ensures privacy and offline operation
3. **Multimodal processing** - Enables our text+image+audio approach
4. **Open model** - Allows customization for Arabic cultural context
5. **Quantization support** - Makes deployment on consumer hardware possible

### 🏥 HEALTHCARE IMPACT

Our solution addresses critical challenges in Alzheimer's care:

1. **Language barrier** - Provides care in the patient's native language
2. **Cultural context** - Incorporates Arabic cultural references and communication patterns
3. **Accessibility** - Voice-first interface for elderly users with limited tech experience
4. **Continuous support** - Available 24/7 unlike human caregivers
5. **Cognitive monitoring** - Tracks memory performance over time

### 👥 TARGET USERS

1. **Primary:** Arabic-speaking elderly with Alzheimer's/dementia
2. **Secondary:** Family caregivers and healthcare providers
3. **Tertiary:** Clinical facilities in Arabic-speaking regions

### 🔍 TECHNICAL ARCHITECTURE

Our system integrates multiple components:

```
1. UI Layer: Patient View, Caregiver View, Report View
2. Core Components: Memory Management, Cognitive Assessment, Reminder System
3. AI Services: Gemma 3n Integration, ASR, TTS, Image Recognition
4. Multimodal System: Real-time processing of text, image, and audio
```

### 📈 FUTURE ROADMAP

1. **Extended language support** - Additional Arabic dialects
2. **Clinical validation** - Partnerships with healthcare providers
3. **Mobile optimization** - Android/iOS applications
4. **IoT integration** - Smart home connectivity
5. **Expanded cognitive exercises** - More memory stimulation activities

### 🎬 DEMO VIDEO

Our demo video showcases:
1. Real-time conversation in Egyptian Arabic
2. Photo recognition and memory prompting
3. Voice interaction with elderly-optimized responses
4. Cognitive assessment capabilities
5. Technical architecture and implementation details

### 👨‍💻 TEAM

**2survivors** - A team dedicated to building AI solutions that preserve human dignity and connection, with expertise in:
- AI/ML Engineering
- Healthcare Technology
- Arabic Language Processing
- User Experience Design

### 🙏 ACKNOWLEDGMENTS

We thank Google for providing the Gemma 3n model and the opportunity to participate in this hackathon. We're committed to advancing AI solutions for underserved communities and believe that technology should be accessible to everyone, regardless of language or cultural background.

---

## 📝 TECHNICAL DETAILS

### Installation

```bash
# Clone repository
git clone https://github.com/2survivors/Alzheimer-s_Memory_Assistant.git
cd Alzheimer-s_Memory_Assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up Hugging Face token for Gemma 3n access
export HF_TOKEN="your_huggingface_token_here"

# Run the application
python src/main.py
```

### System Requirements

- Python 3.8+
- 8GB+ RAM
- CUDA-compatible GPU (recommended)
- Internet connection for initial model download
- Microphone and speakers for voice interaction

### Key Files

- `src/ai/gemma_integration.py` - Gemma 3n integration
- `src/core/intelligent_memory.py` - Memory management system
- `src/core/cognitive_assessment.py` - Cognitive evaluation
- `src/ai/realtime_multimodal_system.py` - Multimodal processing
- `src/core/realtime_recorder.py` - Voice recording
- `src/core/tts_service.py` - Text-to-speech
- `src/core/image_recognition.py` - Image and face recognition

### Libraries Used

- `transformers` - Hugging Face model integration
- `whisper` - Speech recognition
- `pyttsx3` - Text-to-speech
- `face_recognition` - Face detection and recognition
- `customtkinter` - UI framework
- `torch` - Deep learning framework
- `numpy` - Numerical computing
- `pyaudio` - Audio recording and playback

### Model Details

- Model: `google/gemma-3n-E4B-it`
- Quantization: 4-bit
- Deployment: Local via Hugging Face
- Languages: Arabic (primary), English (secondary)
- Context window: 8K tokens
- Response generation: Temperature 0.7, Top-P 0.95 