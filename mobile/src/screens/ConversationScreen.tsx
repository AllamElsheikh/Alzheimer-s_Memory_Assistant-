import React, { useState, useEffect, useRef } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  TextInput, 
  TouchableOpacity, 
  KeyboardAvoidingView, 
  Platform,
  ActivityIndicator,
  Image,
  Alert
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';

import ConversationBubble from '../components/ConversationBubble';
import AccessibleButton from '../components/AccessibleButton';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';
import GemmaService from '../services/GemmaService';
import SpeechToTextService from '../services/SpeechToTextService';

// Message type definition
interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
}

/**
 * ConversationScreen - Voice-first conversation interface for elderly users
 * Features:
 * - Voice input and output
 * - Text chat with large, readable bubbles
 * - Automatic text-to-speech for AI responses
 * - Visual indicators for recording state
 */
const ConversationScreen: React.FC = () => {
  const navigation = useNavigation();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'أهلاً بك! أنا فاكر، مساعدك الشخصي. كيف يمكنني مساعدتك اليوم؟',
      isUser: false,
      timestamp: new Date().toLocaleTimeString('ar-EG'),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (flatListRef.current && messages.length > 0) {
      setTimeout(() => {
        flatListRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  }, [messages]);

  // Speak the initial greeting
  useEffect(() => {
    if (messages.length > 0 && !messages[0].isUser) {
      Speech.speak(messages[0].text, { language: 'ar' });
    }
  }, []);

  // Handle sending a text message
  const handleSendMessage = async () => {
    if (inputText.trim() === '') return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date().toLocaleTimeString('ar-EG'),
    };
    
    const userText = inputText;
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputText('');
    setIsProcessing(true);
    
    try {
      // Get response from GemmaService
      const response = await GemmaService.sendTextMessage(userText);
      
      setMessages(prevMessages => [...prevMessages, response]);
      setIsProcessing(false);
      
      // Speak the AI response
      Speech.speak(response.text, { language: 'ar' });
    } catch (error) {
      console.error('Failed to get AI response', error);
      setIsProcessing(false);
      
      // Add error message
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'عذراً، حدثت مشكلة في الاتصال. يرجى المحاولة مرة أخرى.',
        isUser: false,
        timestamp: new Date().toLocaleTimeString('ar-EG'),
      };
      
      setMessages(prevMessages => [...prevMessages, errorMessage]);
      
      // Speak the error message
      Speech.speak(errorMessage.text, { language: 'ar' });
    }
  };

    // Initialize SpeechToTextService
  useEffect(() => {
    const initSpeechService = async () => {
      await SpeechToTextService.initialize();
    };
    
    initSpeechService();
  }, []);

  // Start voice recording
  const startRecording = async () => {
    try {
      const success = await SpeechToTextService.startRecording();
      if (!success) {
        Alert.alert('خطأ', 'فشل في بدء التسجيل. يرجى المحاولة مرة أخرى.');
        return;
      }
      
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording', error);
      Alert.alert('خطأ', 'فشل في بدء التسجيل. يرجى المحاولة مرة أخرى.');
    }
  };
  
  // Stop voice recording and process audio
  const stopRecording = async () => {
    setIsRecording(false);
    setIsProcessing(true);
    
    try {
      // Use SpeechToTextService to get transcription
      const result = await SpeechToTextService.stopRecordingAndTranscribe();
      
      if (!result.success) {
        throw new Error('Transcription failed');
      }
      
      const transcribedText = result.text;
      
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        text: transcribedText,
        isUser: true,
        timestamp: new Date().toLocaleTimeString('ar-EG'),
      };
      
      setMessages(prevMessages => [...prevMessages, userMessage]);
      
      // Get AI response using GemmaService
      try {
        const response = await GemmaService.sendTextMessage(transcribedText);
        
        setMessages(prevMessages => [...prevMessages, response]);
        setIsProcessing(false);
        
        // Speak the AI response
        Speech.speak(response.text, { language: 'ar' });
      } catch (error) {
        console.error('Failed to get AI response', error);
        setIsProcessing(false);
        Alert.alert('خطأ', 'فشل في الحصول على رد. يرجى المحاولة مرة أخرى.');
      }
    } catch (error) {
      console.error('Failed to process voice recording', error);
      setIsProcessing(false);
      Alert.alert('خطأ', 'فشل في معالجة التسجيل الصوتي. يرجى المحاولة مرة أخرى.');
    }
  };

  // Simulate AI responses (in a real app, this would come from your API)
  const getAIResponse = (userInput: string): string => {
    const responses = [
      'يمكن أن تكون نظاراتك على الطاولة في غرفة المعيشة. هل تريد مني أن أساعدك في البحث عنها؟',
      'أتذكر أنك وضعت نظاراتك في غرفة النوم بجانب السرير. هل تريد أن أذكرك بأماكن أخرى قد تكون فيها؟',
      'لا تقلق، يحدث هذا كثيراً. دعنا نفكر معاً أين يمكن أن تكون نظاراتك. هل تتذكر آخر مرة استخدمتها؟',
      'ربما تكون نظاراتك في المطبخ. هل تريد أن أساعدك في تذكر الأماكن التي تضع فيها أغراضك عادةً؟',
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            onPress={() => navigation.goBack()}
            style={styles.backButton}
            accessibilityLabel="العودة للصفحة الرئيسية"
            accessibilityRole="button"
          >
            <Ionicons name="arrow-back" size={28} color={colors.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>المحادثة</Text>
          <View style={styles.headerRight} />
        </View>
        
        {/* Messages List */}
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <ConversationBubble
              message={item.text}
              isUser={item.isUser}
              timestamp={item.timestamp}
            />
          )}
          contentContainerStyle={styles.messageList}
        />
        
        {/* Processing Indicator */}
        {isProcessing && (
          <View style={styles.processingContainer}>
            <ActivityIndicator size="large" color={colors.primary} />
            <Text style={styles.processingText}>جاري التفكير...</Text>
          </View>
        )}
        
        {/* Input Area */}
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          keyboardVerticalOffset={100}
          style={styles.inputContainer}
        >
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.textInput}
              value={inputText}
              onChangeText={setInputText}
              placeholder="اكتب رسالتك هنا..."
              placeholderTextColor={colors.textSecondary}
              multiline
              maxLength={500}
              textAlign="right"
              accessibilityLabel="حقل إدخال النص"
              accessibilityHint="اكتب رسالتك هنا"
            />
            
            <TouchableOpacity
              onPress={handleSendMessage}
              disabled={inputText.trim() === '' || isProcessing}
              style={[
                styles.sendButton,
                (inputText.trim() === '' || isProcessing) && styles.disabledButton
              ]}
              accessibilityLabel="إرسال الرسالة"
              accessibilityRole="button"
            >
              <Ionicons name="send" size={24} color={colors.background} />
            </TouchableOpacity>
          </View>
          
          {/* Voice Recording Button */}
          <TouchableOpacity
            onPress={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
            style={[
              styles.recordButton,
              isRecording && styles.recordingActive,
              isProcessing && styles.disabledButton
            ]}
            accessibilityLabel={isRecording ? "إيقاف التسجيل" : "تسجيل صوتي"}
            accessibilityRole="button"
          >
            <Ionicons
              name={isRecording ? "stop-circle" : "mic"}
              size={28}
              color={colors.background}
            />
            <Text style={styles.recordButtonText}>
              {isRecording ? "إيقاف" : "تحدث"}
            </Text>
          </TouchableOpacity>
        </KeyboardAvoidingView>
      </View>
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
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    backgroundColor: colors.background,
    ...shadows.small,
  },
  backButton: {
    padding: spacing.sm,
  },
  headerTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.lg,
    color: colors.text,
  },
  headerRight: {
    width: 44,
  },
  messageList: {
    flexGrow: 1,
    padding: spacing.md,
  },
  processingContainer: {
    position: 'absolute',
    bottom: 100,
    alignSelf: 'center',
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    ...shadows.medium,
  },
  processingText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginLeft: spacing.sm,
  },
  inputContainer: {
    padding: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    backgroundColor: colors.background,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  textInput: {
    flex: 1,
    minHeight: 50,
    maxHeight: 100,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    fontFamily: typography.fontFamily.regular,
    fontSize: typography.fontSize.md,
    color: colors.text,
    textAlignVertical: 'center',
    marginRight: spacing.sm,
  },
  sendButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.small,
  },
  disabledButton: {
    backgroundColor: colors.textDisabled,
    opacity: 0.7,
  },
  recordButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.secondary,
    borderRadius: borderRadius.lg,
    paddingVertical: spacing.sm,
    marginTop: spacing.md,
    ...shadows.small,
  },
  recordingActive: {
    backgroundColor: colors.error,
  },
  recordButtonText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.md,
    color: colors.background,
    marginLeft: spacing.sm,
  },
});

export default ConversationScreen; 