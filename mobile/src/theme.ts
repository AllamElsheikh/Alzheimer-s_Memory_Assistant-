import { DefaultTheme } from 'react-native-paper';
import { Platform } from 'react-native';

// Color palette optimized for elderly users and Alzheimer's patients
// - High contrast colors
// - Soothing tones
// - Consistent color coding for different functions
export const colors = {
  primary: '#1E88E5', // Blue - Primary actions
  primaryDark: '#1565C0',
  primaryLight: '#BBDEFB',
  
  secondary: '#26A69A', // Teal - Secondary actions
  secondaryDark: '#00796B',
  secondaryLight: '#B2DFDB',
  
  accent: '#FF8A65', // Coral - Accents and highlights
  accentDark: '#E64A19',
  accentLight: '#FFCCBC',
  
  success: '#66BB6A', // Green - Success/completion
  error: '#F44336',   // Red - Errors/warnings
  warning: '#FFA726', // Orange - Warnings/alerts
  
  background: '#FFFFFF',
  surface: '#F5F5F5',
  card: '#FFFFFF',
  
  text: '#212121',     // Very dark gray - Primary text
  textSecondary: '#424242', // Dark gray - Secondary text
  textDisabled: '#757575', // Medium gray - Disabled text
  
  border: '#E0E0E0',
  divider: '#EEEEEE',
  
  // Memory categories
  family: '#8E24AA',    // Purple for family memories
  places: '#00897B',    // Teal for places
  activities: '#7CB342', // Green for activities
  cultural: '#FB8C00',  // Orange for cultural memories
};

// Typography optimized for elderly users
// - Larger font sizes
// - Clear, readable fonts
// - Consistent hierarchy
export const typography = {
  fontFamily: {
    regular: 'cairo-regular',
    medium: 'cairo-semibold',
    bold: 'cairo-bold',
  },
  fontSize: {
    xs: 14,
    sm: 16,
    md: 18,
    lg: 22,
    xl: 26,
    xxl: 32,
  },
  lineHeight: {
    xs: 20,
    sm: 24,
    md: 28,
    lg: 32,
    xl: 38,
    xxl: 46,
  },
};

// Spacing scale
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Border radius scale
export const borderRadius = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  round: 9999,
};

// Shadows
export const shadows = {
  small: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.2,
      shadowRadius: 2,
    },
    android: {
      elevation: 2,
    },
    default: {},
  }),
  medium: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.25,
      shadowRadius: 3.84,
    },
    android: {
      elevation: 4,
    },
    default: {},
  }),
  large: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.3,
      shadowRadius: 4.65,
    },
    android: {
      elevation: 8,
    },
    default: {},
  }),
};

// React Native Paper theme
export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: colors.primary,
    accent: colors.accent,
    background: colors.background,
    surface: colors.surface,
    text: colors.text,
    disabled: colors.textDisabled,
    placeholder: colors.textSecondary,
    backdrop: 'rgba(0, 0, 0, 0.5)',
    notification: colors.error,
  },
  fonts: {
    regular: {
      fontFamily: typography.fontFamily.regular,
    },
    medium: {
      fontFamily: typography.fontFamily.medium,
    },
    light: {
      fontFamily: typography.fontFamily.regular,
    },
    thin: {
      fontFamily: typography.fontFamily.regular,
    },
  },
  roundness: borderRadius.md,
}; 