import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
// Audio recording temporarily disabled for Expo Go compatibility
// import { Audio } from 'expo-audio';
import * as Haptics from 'expo-haptics';
import * as Animatable from 'react-native-animatable';

import { GemmaService, Message } from '../services/GemmaService';
import { theme } from '../theme/theme';

export default function ConversationScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [recording, setRecording] = useState<any | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);
  const gemmaService = useRef(new GemmaService()).current;

  useEffect(() => {
    initializeConversation();
    return () => {
      if (recording) {
        recording.stopAndUnloadAsync();
      }
    };
  }, []);

  const initializeConversation = async () => {
    // Load conversation history
    try {
      const history = await gemmaService.getConversationHistory(10);
      setMessages(history);
    } catch (error) {
      console.error('Error loading conversation history:', error);
    }

    // Send welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      text: 'أهلاً وسهلاً! أنا فاكر، مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟',
      isUser: false,
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);

    // Speak welcome message
    Speech.speak(welcomeMessage.text, {
      language: 'ar',
      rate: 0.8,
      pitch: 1.0,
    });
  };

  const sendMessage = async (text?: string) => {
    const messageText = text || inputText.trim();
    if (!messageText) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await gemmaService.sendTextMessage(messageText);
      setMessages(prev => [...prev, response]);

      // Speak response
      Speech.speak(response.text, {
        language: 'ar',
        rate: 0.8,
        pitch: 1.0,
      });

      // Haptic feedback
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

    } catch (error) {
      console.error('Error sending message:', error);
      Alert.alert('خطأ', 'حدث خطأ في إرسال الرسالة. حاول مرة أخرى.');
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      // Audio recording disabled for Expo Go compatibility
      Alert.alert(
        'تسجيل صوتي', 
        'التسجيل الصوتي غير متاح في Expo Go. استخدم النص بدلاً من ذلك.',
        [{ text: 'حسناً', style: 'default' }]
      );
    } catch (error) {
      console.error('Error starting recording:', error);
      Alert.alert('خطأ', 'لم نتمكن من بدء التسجيل');
    }
  };

  const stopRecording = async () => {
    // Audio recording disabled for Expo Go compatibility
    setIsRecording(false);
    Alert.alert(
      'تسجيل صوتي', 
      'التسجيل الصوتي غير متاح في Expo Go. استخدم النص بدلاً من ذلك.',
      [{ text: 'حسناً', style: 'default' }]
    );
  };

  const clearConversation = () => {
    Alert.alert(
      'مسح المحادثة',
      'هل تريد مسح جميع الرسائل؟',
      [
        { text: 'إلغاء', style: 'cancel' },
        { 
          text: 'مسح', 
          style: 'destructive',
          onPress: () => {
            setMessages([]);
            gemmaService.clearSession();
          }
        },
      ]
    );
  };

  const renderMessage = (message: Message, index: number) => {
    const isUser = message.isUser;
    const animationDelay = index * 100;

    return (
      <Animatable.View
        key={message.id}
        animation="fadeInUp"
        delay={animationDelay}
        style={[
          styles.messageContainer,
          isUser ? styles.userMessage : styles.botMessage,
        ]}
      >
        <View style={[
          styles.messageBubble,
          isUser ? styles.userBubble : styles.botBubble,
        ]}>
          <Text style={[
            styles.messageText,
            isUser ? styles.userText : styles.botText,
          ]}>
            {message.text}
          </Text>
          <Text style={[
            styles.messageTime,
            isUser ? styles.userTime : styles.botTime,
          ]}>
            {message.timestamp.toLocaleTimeString('ar-EG', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </Text>
        </View>
        {!isUser && (
          <TouchableOpacity
            style={styles.speakButton}
            onPress={() => Speech.speak(message.text, { language: 'ar', rate: 0.8 })}
          >
            <Ionicons name="volume-high" size={16} color={theme.colors.primary} />
          </TouchableOpacity>
        )}
      </Animatable.View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>محادثة مع فاكر</Text>
          <TouchableOpacity onPress={clearConversation} style={styles.clearButton}>
            <Ionicons name="trash-outline" size={24} color="white" />
          </TouchableOpacity>
        </View>

        {/* Messages */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={styles.messagesContent}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.map((message, index) => renderMessage(message, index))}
          
          {isLoading && (
            <Animatable.View 
              animation="pulse" 
              iterationCount="infinite"
              style={styles.loadingContainer}
            >
              <View style={styles.loadingBubble}>
                <Text style={styles.loadingText}>فاكر يكتب...</Text>
              </View>
            </Animatable.View>
          )}
        </ScrollView>

        {/* Input Area */}
        <View style={styles.inputContainer}>
          <View style={styles.inputRow}>
            <TextInput
              style={styles.textInput}
              value={inputText}
              onChangeText={setInputText}
              placeholder="اكتب رسالتك هنا..."
              placeholderTextColor="#999"
              multiline
              maxLength={500}
              textAlign="right"
            />
            <TouchableOpacity
              style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
              onPress={() => sendMessage()}
              disabled={!inputText.trim() || isLoading}
            >
              <Ionicons name="send" size={24} color="white" />
            </TouchableOpacity>
          </View>

          {/* Voice Recording */}
          <View style={styles.voiceContainer}>
            <TouchableOpacity
              style={[
                styles.recordButton,
                isRecording && styles.recordButtonActive,
              ]}
              onPressIn={startRecording}
              onPressOut={stopRecording}
              disabled={isLoading}
            >
              <Ionicons 
                name={isRecording ? "stop" : "mic"} 
                size={32} 
                color="white" 
              />
            </TouchableOpacity>
            <Text style={styles.recordHint}>
              {isRecording ? 'اترك الزر لإنهاء التسجيل' : 'اضغط واستمر للتسجيل الصوتي'}
            </Text>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: theme.colors.primary,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: 'Cairo-Bold',
  },
  clearButton: {
    padding: 8,
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
  },
  messageContainer: {
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  userMessage: {
    justifyContent: 'flex-end',
  },
  botMessage: {
    justifyContent: 'flex-start',
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
  },
  userBubble: {
    backgroundColor: theme.colors.primary,
    borderBottomRightRadius: 4,
  },
  botBubble: {
    backgroundColor: 'white',
    borderBottomLeftRadius: 4,
    elevation: 2,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
    fontFamily: 'Cairo-Regular',
  },
  userText: {
    color: 'white',
  },
  botText: {
    color: '#333',
  },
  messageTime: {
    fontSize: 12,
    marginTop: 4,
  },
  userTime: {
    color: 'rgba(255,255,255,0.7)',
  },
  botTime: {
    color: '#666',
  },
  speakButton: {
    marginLeft: 8,
    padding: 4,
  },
  loadingContainer: {
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  loadingBubble: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 16,
    borderBottomLeftRadius: 4,
    elevation: 2,
  },
  loadingText: {
    color: '#666',
    fontStyle: 'italic',
    fontFamily: 'Cairo-Regular',
  },
  inputContainer: {
    backgroundColor: 'white',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    marginBottom: 12,
  },
  textInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginRight: 12,
    maxHeight: 100,
    fontSize: 16,
    fontFamily: 'Cairo-Regular',
  },
  sendButton: {
    backgroundColor: theme.colors.primary,
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#ccc',
  },
  voiceContainer: {
    alignItems: 'center',
  },
  recordButton: {
    backgroundColor: '#F44336',
    width: 64,
    height: 64,
    borderRadius: 32,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 4,
  },
  recordButtonActive: {
    backgroundColor: '#D32F2F',
    transform: [{ scale: 1.1 }],
  },
  recordHint: {
    marginTop: 8,
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    fontFamily: 'Cairo-Regular',
  },
});
