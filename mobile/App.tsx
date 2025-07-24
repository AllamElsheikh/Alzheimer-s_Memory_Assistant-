import React, { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Provider as PaperProvider } from 'react-native-paper';
import * as Font from 'expo-font';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import ConversationScreen from './src/screens/ConversationScreen';
import MemoryPromptScreen from './src/screens/MemoryPromptScreen';
import PhotoAnalysisScreen from './src/screens/PhotoAnalysisScreen';
import ReminderScreen from './src/screens/ReminderScreen';

// Theme and Services
import { theme } from './src/theme';
import LocalizationService from './src/services/LocalizationService';

// LocalizationService automatically handles RTL setup

const Stack = createNativeStackNavigator();

export default function App() {
  const [fontsLoaded, setFontsLoaded] = React.useState(false);

  useEffect(() => {
    async function loadFonts() {
      await Font.loadAsync({
        'cairo-bold': require('./assets/fonts/Cairo-Bold.ttf'),
        'cairo-regular': require('./assets/fonts/Cairo-Regular.ttf'),
        'cairo-semibold': require('./assets/fonts/Cairo-SemiBold.ttf'),
      });
      setFontsLoaded(true);
    }
    
    loadFonts();
  }, []);

  if (!fontsLoaded) {
    return null; // Show nothing until fonts are loaded
  }

  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <NavigationContainer>
          <Stack.Navigator 
            initialRouteName="Home"
            screenOptions={{
              headerShown: false,
              animation: 'fade',
            }}
          >
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Conversation" component={ConversationScreen} />
            <Stack.Screen name="MemoryPrompt" component={MemoryPromptScreen} />
            <Stack.Screen name="PhotoAnalysis" component={PhotoAnalysisScreen} />
            <Stack.Screen name="Reminder" component={ReminderScreen} />
          </Stack.Navigator>
          <StatusBar style="auto" />
        </NavigationContainer>
      </PaperProvider>
    </SafeAreaProvider>
  );
} 