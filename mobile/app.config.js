// Environment variables configuration for Expo
import 'dotenv/config';

export default {
  name: "فاكر؟",
  slug: "faker-memory-assistant",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/icon.png",
  userInterfaceStyle: "light",
  splash: {
    image: "./assets/splash.png",
    resizeMode: "contain",
    backgroundColor: "#1E88E5"
  },
  assetBundlePatterns: [
    "**/*"
  ],
  ios: {
    supportsTablet: true,
    bundleIdentifier: "com.fakerapp.memoryassistant",
    buildNumber: "1.0.0",
    infoPlist: {
      NSCameraUsageDescription: "This app uses the camera to analyze photos for memory assistance.",
      NSPhotoLibraryUsageDescription: "This app uses photos for memory assistance and stimulation.",
      NSMicrophoneUsageDescription: "This app uses the microphone for voice conversations.",
      UIBackgroundModes: ["audio"]
    }
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#1E88E5"
    },
    package: "com.fakerapp.memoryassistant",
    versionCode: 1,
    permissions: [
      "CAMERA",
      "READ_EXTERNAL_STORAGE",
      "WRITE_EXTERNAL_STORAGE",
      "RECORD_AUDIO",
      "VIBRATE"
    ]
  },
  web: {
    favicon: "./assets/favicon.png"
  },
  plugins: [
    [
      "expo-notifications",
      {
        icon: "./assets/notification-icon.png",
        color: "#1E88E5"
      }
    ],
    "expo-localization"
  ],
  extra: {
    // Environment variables
    gemmaApiKey: process.env.GEMMA_API_KEY || 'AIzaSyD7M1y4CkI9ODgbeL-7qE2O9W6m5BdxQkE', // Fallback to the provided key for development
    openaiApiKey: process.env.OPENAI_API_KEY || '',
    eas: {
      projectId: "faker-memory-assistant"
    }
  }
}; 