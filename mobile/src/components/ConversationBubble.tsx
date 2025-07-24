import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';
import * as Speech from 'expo-speech';

interface ConversationBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
  onPress?: () => void;
}

/**
 * ConversationBubble - A component for displaying chat messages
 * Features:
 * - Different styles for user and assistant messages
 * - Text-to-speech on press
 * - RTL support for Arabic
 * - Large, readable text
 */
const ConversationBubble: React.FC<ConversationBubbleProps> = ({
  message,
  isUser,
  timestamp,
  onPress,
}) => {
  const handlePress = () => {
    // Speak the message when pressed
    Speech.speak(message, { language: 'ar' });
    
    if (onPress) {
      onPress();
    }
  };

  return (
    <Pressable
      onPress={handlePress}
      style={[
        styles.container,
        isUser ? styles.userContainer : styles.assistantContainer,
      ]}
      accessibilityRole="button"
      accessibilityLabel={isUser ? "Your message" : "Assistant message"}
      accessibilityHint="Press to hear this message spoken aloud"
    >
      <View style={styles.bubbleContent}>
        <Text style={[
          styles.messageText,
          isUser ? styles.userText : styles.assistantText,
        ]}>
          {message}
        </Text>
        
        {timestamp && (
          <Text style={styles.timestamp}>
            {timestamp}
          </Text>
        )}
      </View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    maxWidth: '85%',
    marginVertical: spacing.sm,
    borderRadius: borderRadius.lg,
    ...shadows.small,
  },
  userContainer: {
    alignSelf: 'flex-end',
    backgroundColor: colors.primaryLight,
    marginLeft: spacing.xl,
    marginRight: spacing.sm,
    borderBottomRightRadius: borderRadius.xs,
  },
  assistantContainer: {
    alignSelf: 'flex-start',
    backgroundColor: colors.surface,
    marginRight: spacing.xl,
    marginLeft: spacing.sm,
    borderBottomLeftRadius: borderRadius.xs,
  },
  bubbleContent: {
    padding: spacing.md,
  },
  messageText: {
    fontSize: typography.fontSize.md,
    lineHeight: typography.lineHeight.md,
    fontFamily: typography.fontFamily.regular,
  },
  userText: {
    color: colors.text,
    textAlign: 'right',
  },
  assistantText: {
    color: colors.text,
  },
  timestamp: {
    fontSize: typography.fontSize.xs,
    color: colors.textSecondary,
    marginTop: spacing.xs,
    textAlign: 'right',
  },
});

export default ConversationBubble; 