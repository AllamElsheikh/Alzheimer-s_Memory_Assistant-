import { DefaultTheme } from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#1976D2',
    secondary: '#03DAC6',
    accent: '#FF9800',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    error: '#F44336',
    text: '#212121',
    onSurface: '#000000',
    disabled: '#BDBDBD',
    placeholder: '#757575',
    backdrop: 'rgba(0, 0, 0, 0.5)',
  },
  fonts: {
    ...DefaultTheme.fonts,
    regular: {
      fontFamily: 'Cairo-Regular',
      fontWeight: 'normal' as const,
    },
    medium: {
      fontFamily: 'Cairo-Bold',
      fontWeight: '500' as const,
    },
    light: {
      fontFamily: 'Cairo-Regular',
      fontWeight: '300' as const,
    },
    thin: {
      fontFamily: 'Cairo-Regular',
      fontWeight: '100' as const,
    },
  },
};
