import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, SafeAreaView } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';

import AccessibleButton from '../components/AccessibleButton';
import { colors, typography, spacing, shadows } from '../theme';
import GemmaService from '../services/GemmaService';
import ReminderService from '../services/ReminderService';

/**
 * HomeScreen - Main entry point of the app with large, accessible buttons
 * Features:
 * - Large, high-contrast buttons
 * - Voice guidance
 * - Simple, uncluttered layout
 * - Visual cues for different functions
 */
const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  
  // Welcome message spoken when screen loads and initialize services
  React.useEffect(() => {
    const welcomeMessage = 'أهلاً بك في تطبيق فاكر. كيف يمكنني مساعدتك اليوم؟';
    Speech.speak(welcomeMessage, { language: 'ar' });
    
    // Initialize services
    const initServices = async () => {
      try {
        // Initialize GemmaService with a default user ID
        // In a real app, this would come from authentication
        await GemmaService.initialize('default-user');
        
        // Initialize ReminderService
        await ReminderService.initialize();
      } catch (error) {
        console.error('Error initializing services:', error);
      }
    };
    
    initServices();
  }, []);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <LinearGradient
        colors={[colors.background, colors.surface]}
        style={styles.container}
      >
        <View style={styles.header}>
          <Image 
            source={require('../../assets/images/logo.png')} 
            style={styles.logo}
            accessibilityLabel="فاكر؟ شعار التطبيق"
          />
          <Text style={styles.title}>فاكر؟</Text>
          <Text style={styles.subtitle}>مساعد الذاكرة الشخصي</Text>
        </View>

        <ScrollView 
          contentContainerStyle={styles.buttonContainer}
          showsVerticalScrollIndicator={false}
        >
          <AccessibleButton
            text="دردشة معي"
            icon={<Ionicons name="chatbubble-ellipses" size={28} color={colors.background} />}
            onPress={() => navigation.navigate('Conversation')}
            variant="primary"
            size="large"
            fullWidth
            speakOnFocus
            style={styles.button}
          />
          
          <AccessibleButton
            text="تمارين الذاكرة"
            icon={<Ionicons name="brain" size={28} color={colors.background} />}
            onPress={() => navigation.navigate('MemoryPrompt')}
            variant="secondary"
            size="large"
            fullWidth
            speakOnFocus
            style={styles.button}
          />
          
          <AccessibleButton
            text="تحليل الصور"
            icon={<Ionicons name="images" size={28} color={colors.background} />}
            onPress={() => navigation.navigate('PhotoAnalysis')}
            variant="primary"
            size="large"
            fullWidth
            speakOnFocus
            style={styles.button}
          />
          
          <AccessibleButton
            text="التذكيرات"
            icon={<Ionicons name="alarm" size={28} color={colors.background} />}
            onPress={() => navigation.navigate('Reminder')}
            variant="secondary"
            size="large"
            fullWidth
            speakOnFocus
            style={styles.button}
          />
        </ScrollView>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            تطبيق فاكر؟ - مساعد ذكي لمرضى الزهايمر
          </Text>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },
  container: {
    flex: 1,
    padding: spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginVertical: spacing.xl,
  },
  logo: {
    width: 120,
    height: 120,
    resizeMode: 'contain',
  },
  title: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.xxl,
    color: colors.primary,
    marginTop: spacing.md,
    textAlign: 'center',
  },
  subtitle: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.lg,
    color: colors.textSecondary,
    marginTop: spacing.xs,
    textAlign: 'center',
  },
  buttonContainer: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  button: {
    marginBottom: spacing.lg,
    ...shadows.medium,
  },
  footer: {
    marginTop: spacing.xl,
    alignItems: 'center',
  },
  footerText: {
    fontFamily: typography.fontFamily.regular,
    fontSize: typography.fontSize.sm,
    color: colors.textSecondary,
    textAlign: 'center',
  },
});

export default HomeScreen; 