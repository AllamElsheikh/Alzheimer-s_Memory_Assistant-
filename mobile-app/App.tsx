import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { Provider as PaperProvider } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AppRegistry } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import ConversationScreen from './src/screens/ConversationScreen';
import PhotoAnalysisScreen from './src/screens/PhotoAnalysisScreen';
import RemindersScreen from './src/screens/RemindersScreen';
import AssessmentScreen from './src/screens/AssessmentScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import PatientProfileScreen from './src/screens/PatientProfileScreen';

// Services
import { NotificationService } from './src/services/NotificationService';
import { theme } from './src/theme/theme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Conversation') {
            iconName = focused ? 'chatbubbles' : 'chatbubbles-outline';
          } else if (route.name === 'Photos') {
            iconName = focused ? 'camera' : 'camera-outline';
          } else if (route.name === 'Reminders') {
            iconName = focused ? 'notifications' : 'notifications-outline';
          } else if (route.name === 'Assessment') {
            iconName = focused ? 'medical' : 'medical-outline';
          } else {
            iconName = 'ellipse';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          paddingBottom: 5,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
        headerStyle: {
          backgroundColor: theme.colors.primary,
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ 
          title: 'الرئيسية',
          headerTitle: 'فاكر - مساعد الذاكرة'
        }}
      />
      <Tab.Screen 
        name="Conversation" 
        component={ConversationScreen}
        options={{ 
          title: 'المحادثة',
          headerTitle: 'محادثة مع فاكر'
        }}
      />
      <Tab.Screen 
        name="Photos" 
        component={PhotoAnalysisScreen}
        options={{ 
          title: 'الصور',
          headerTitle: 'تحليل الصور'
        }}
      />
      <Tab.Screen 
        name="Reminders" 
        component={RemindersScreen}
        options={{ 
          title: 'التذكيرات',
          headerTitle: 'التذكيرات والمواعيد'
        }}
      />
      <Tab.Screen 
        name="Assessment" 
        component={AssessmentScreen}
        options={{ 
          title: 'التقييم',
          headerTitle: 'التقييم المعرفي'
        }}
      />
    </Tab.Navigator>
  );
}

function App() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        // Initialize notification service
        await NotificationService.initialize();

        // Request permissions
        await NotificationService.requestPermissions();

      } catch (e) {
        console.warn('Error during app initialization:', e);
      } finally {
        setIsReady(true);
      }
    }

    prepare();
  }, []);

  if (!isReady) {
    return null; // Show splash screen
  }

  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <NavigationContainer>
          <Stack.Navigator>
            <Stack.Screen 
              name="MainTabs" 
              component={MainTabs}
              options={{ headerShown: false }}
            />
            <Stack.Screen 
              name="Settings" 
              component={SettingsScreen}
              options={{ 
                title: 'الإعدادات',
                headerStyle: { backgroundColor: theme.colors.primary },
                headerTintColor: '#fff'
              }}
            />
            <Stack.Screen 
              name="PatientProfile" 
              component={PatientProfileScreen}
              options={{ 
                title: 'ملف المريض',
                headerStyle: { backgroundColor: theme.colors.primary },
                headerTintColor: '#fff'
              }}
            />
          </Stack.Navigator>
        </NavigationContainer>
        <StatusBar style="light" />
      </PaperProvider>
    </SafeAreaProvider>
  );
}

// Register the main component
AppRegistry.registerComponent('main', () => App);

export default App;