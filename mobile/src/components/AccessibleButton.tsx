import React from 'react';
import { StyleSheet, TouchableOpacity, Text, ViewStyle, TextStyle, View } from 'react-native';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';
import * as Speech from 'expo-speech';
import { LinearGradient } from 'expo-linear-gradient';

interface AccessibleButtonProps {
  onPress: () => void;
  text: string;
  icon?: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  disabled?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  speakOnFocus?: boolean;
}

/**
 * AccessibleButton - A highly accessible button component optimized for elderly users
 * Features:
 * - Large touch targets
 * - High contrast colors
 * - Optional text-to-speech on focus
 * - Clear visual feedback
 * - Support for icons
 */
const AccessibleButton: React.FC<AccessibleButtonProps> = ({
  onPress,
  text,
  icon,
  variant = 'primary',
  size = 'medium',
  fullWidth = false,
  disabled = false,
  style,
  textStyle,
  speakOnFocus = true,
}) => {
  // Handle long press - speak the button text
  const handleLongPress = () => {
    if (speakOnFocus && !disabled) {
      Speech.speak(text, { language: 'ar' });
    }
  };

  // Get button styles based on variant and size
  const getButtonStyles = (): ViewStyle => {
    let variantStyle: ViewStyle = {};
    
    // Size styles
    const sizeStyles = {
      small: {
        paddingVertical: spacing.sm,
        paddingHorizontal: spacing.md,
        minHeight: 44, // Minimum touch target size
      },
      medium: {
        paddingVertical: spacing.md,
        paddingHorizontal: spacing.lg,
        minHeight: 56,
      },
      large: {
        paddingVertical: spacing.lg,
        paddingHorizontal: spacing.xl,
        minHeight: 72,
      },
    };
    
    // Variant styles
    switch (variant) {
      case 'primary':
        variantStyle = {
          backgroundColor: disabled ? colors.textDisabled : colors.primary,
          ...shadows.medium,
        };
        break;
      case 'secondary':
        variantStyle = {
          backgroundColor: disabled ? colors.textDisabled : colors.secondary,
          ...shadows.medium,
        };
        break;
      case 'outline':
        variantStyle = {
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderColor: disabled ? colors.textDisabled : colors.primary,
        };
        break;
      case 'text':
        variantStyle = {
          backgroundColor: 'transparent',
        };
        break;
    }
    
    return {
      ...sizeStyles[size],
      ...variantStyle,
      opacity: disabled ? 0.7 : 1,
      width: fullWidth ? '100%' : undefined,
    };
  };

  // Get text styles based on variant and size
  const getTextStyles = (): TextStyle => {
    const baseTextStyle: TextStyle = {
      fontFamily: typography.fontFamily.medium,
      textAlign: 'center',
    };
    
    // Size styles
    const sizeStyles = {
      small: {
        fontSize: typography.fontSize.md,
      },
      medium: {
        fontSize: typography.fontSize.lg,
      },
      large: {
        fontSize: typography.fontSize.xl,
      },
    };
    
    // Color based on variant
    let textColor = colors.text;
    switch (variant) {
      case 'primary':
      case 'secondary':
        textColor = colors.background;
        break;
      case 'outline':
      case 'text':
        textColor = disabled ? colors.textDisabled : colors.primary;
        break;
    }
    
    return {
      ...baseTextStyle,
      ...sizeStyles[size],
      color: textColor,
    };
  };

  // Render gradient background for primary and secondary buttons
  const renderBackground = () => {
    if (variant === 'primary') {
      return (
        <LinearGradient
          colors={[colors.primary, colors.primaryDark]}
          style={StyleSheet.absoluteFill}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        />
      );
    }
    
    if (variant === 'secondary') {
      return (
        <LinearGradient
          colors={[colors.secondary, colors.secondaryDark]}
          style={StyleSheet.absoluteFill}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        />
      );
    }
    
    return null;
  };

  return (
    <TouchableOpacity
      onPress={disabled ? undefined : onPress}
      onLongPress={handleLongPress}
      activeOpacity={0.7}
      disabled={disabled}
      style={[
        styles.button,
        getButtonStyles(),
        style,
      ]}
      accessibilityRole="button"
      accessibilityLabel={text}
      accessibilityHint={`Press to ${text.toLowerCase()}`}
      accessibilityState={{ disabled }}
    >
      {(variant === 'primary' || variant === 'secondary') && !disabled && renderBackground()}
      
      <View style={styles.contentContainer}>
        {icon && <View style={styles.iconContainer}>{icon}</View>}
        <Text style={[getTextStyles(), textStyle]}>{text}</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: borderRadius.lg,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  contentContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconContainer: {
    marginRight: spacing.sm,
  },
});

export default AccessibleButton; 