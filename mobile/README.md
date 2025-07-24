# فاكر؟ (Faker?) - Mobile App for Alzheimer's Patients

A React Native mobile application designed specifically for Arabic-speaking Alzheimer's patients, with a focus on accessibility, memory stimulation, and ease of use.

## Features

### 🎯 Key Features

- **Voice-First Interface**: Optimized for elderly users with speech input and output in Arabic
- **Memory Exercises**: Categorized memory prompts with images, hints, and guidance
- **Accessible Design**: Large buttons, high contrast, and intuitive navigation
- **Real-time Conversation**: Natural dialogue with the AI assistant
- **Photo Analysis**: Upload and analyze photos to stimulate memories
- **Medication Reminders**: Customizable medication and activity reminders
- **RTL Support**: Full right-to-left support for Arabic language

### 🧠 Memory Stimulation

The app includes several memory exercise categories:
- Family memories
- Places and locations
- Activities and hobbies
- Cultural references

### 🔊 Voice Accessibility

- Text-to-speech for all content
- Speech recognition for hands-free interaction
- Voice guidance throughout the app
- Long-press to hear button descriptions

## Technical Details

### 📱 Technology Stack

- **Framework**: React Native with Expo
- **UI Components**: Custom accessible components
- **State Management**: React Context API and Hooks
- **Navigation**: React Navigation
- **Accessibility**: Full support for screen readers and voice control
- **Animations**: React Native Reanimated for smooth transitions
- **Localization**: i18n-js for Arabic language support
- **API Integration**: Google Gemma API for AI conversation
- **Speech-to-Text**: OpenAI Whisper API (optional)

### 📐 Design Principles

- **Large Touch Targets**: All interactive elements are at least 44px × 44px
- **High Contrast**: 4.5:1 minimum contrast ratio for text
- **Consistent Layout**: Predictable navigation and UI patterns
- **Error Prevention**: Confirmation dialogs and clear feedback
- **Voice Guidance**: Audio cues and spoken instructions

## Installation

### Prerequisites

- Node.js 14+
- npm or yarn
- Expo CLI
- Android Studio or Xcode for mobile development

### Setup

1. Clone the repository and navigate to the mobile directory:
   ```bash
   git clone https://github.com/yourusername/Alzheimer-s_Memory_Assistant-.git
   cd Alzheimer-s_Memory_Assistant-/mobile
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   npm run setup-env
   ```
   Then edit the `.env` file to add your API keys.

4. Initialize git hooks (optional):
   ```bash
   npm run init-husky
   ```

5. Start the development server:
   ```bash
   npm start
   ```

6. Run on a device or emulator:
   ```bash
   npm run android
   # or
   npm run ios
   ```

## Environment Variables

The app requires the following environment variables:

- `GEMMA_API_KEY`: Google Gemma API key for AI conversation
- `OPENAI_API_KEY`: OpenAI API key for speech-to-text (optional)

You can check if your environment is set up correctly with:

```bash
npm run check-env
```

## Project Structure

```
mobile/
├── assets/            # Images, fonts, and other static assets
├── scripts/           # Utility scripts
├── src/
│   ├── components/    # Reusable UI components
│   ├── screens/       # Screen components
│   ├── services/      # API and business logic
│   ├── theme.ts       # Global styling and theming
│   └── types/         # TypeScript type definitions
├── App.tsx            # Main application entry point
└── app.config.js      # Expo configuration with environment variables
```

## Development

### Code Style

The project uses ESLint and Prettier for code formatting:

```bash
npm run lint        # Check for linting issues
npm run lint:fix    # Fix linting issues
npm run format      # Format code with Prettier
```

### Git Hooks

The project uses Husky for git hooks:

- **pre-commit**: Runs lint-staged to format and lint changed files
- **pre-push**: Runs linting and environment checks

### Testing

Run tests with:

```bash
npm test
npm run test:watch  # Watch mode
```

## Usage

1. Launch the app
2. Choose from the main menu options:
   - Chat with the assistant
   - Memory exercises
   - Photo analysis
   - Medication reminders
3. Follow the voice prompts for guidance

## Documentation

- [API Integration](./API_INTEGRATION.md) - Details about the Gemma API integration
- [Environment Variables and Services](./ENV_AND_SERVICES.md) - Information about environment variables and services

## Contributing

Contributions are welcome! Please read our [contributing guidelines](../CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details. 