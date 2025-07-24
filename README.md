# فاكر؟ (Faker?) - Alzheimer's Memory Assistant

An Arabic-language memory assistant application designed to help Alzheimer's patients and their caregivers. The application uses AI to provide personalized memory stimulation, conversation, and reminders.

## Project Structure

The project consists of two main parts:

1. **Python Backend** - AI core services including:
   - Google Gemma 3n for conversation
   - Whisper ASR for speech recognition
   - TTS for speech synthesis
   - Memory Engine for context management
   - Cognitive Assessment tools

2. **React Native Mobile App** - Patient-facing interface with:
   - Voice-first conversation interface
   - Memory prompts and exercises
   - Photo analysis for memory stimulation
   - Medication and activity reminders
   - Accessible UI designed for elderly users

## Mobile App Features

The React Native mobile application provides:

- **Accessible Design**: Large buttons, high contrast, and voice feedback
- **Voice Conversation**: Natural language interaction in Arabic
- **Memory Exercises**: Interactive prompts for family, places, and cultural memories
- **Photo Analysis**: AI analysis of photos to stimulate memories
- **Reminder System**: Medication and activity reminders with notifications
- **RTL Support**: Full Arabic language and right-to-left text support

## Getting Started

### Prerequisites

- Node.js 14+
- npm or yarn
- Expo CLI
- Android Studio or Xcode for mobile development

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Alzheimer-s_Memory_Assistant-.git
   cd Alzheimer-s_Memory_Assistant-
   ```

2. Install dependencies for the mobile app:
   ```
   cd mobile
   npm install
   ```

3. Set up environment variables:
   ```
   cp env.example .env
   ```
   Edit the `.env` file to add your API keys.

4. Start the development server:
   ```
   npm start
   ```

## Environment Variables

The mobile app requires the following environment variables:

- `GEMMA_API_KEY`: Google Gemma API key for AI conversation
- `OPENAI_API_KEY`: OpenAI API key for speech-to-text (optional)

## Development

See the documentation in each directory for specific development guidelines:

- [Mobile App Documentation](mobile/README.md)
- [API Integration](mobile/API_INTEGRATION.md)
- [Environment Variables and Services](mobile/ENV_AND_SERVICES.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemma for providing the AI model
- Expo for the React Native development framework
- All contributors and supporters of this project