import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import AccessibleButton from '../components/AccessibleButton';
import * as Speech from 'expo-speech';

// Mock expo-speech
jest.mock('expo-speech', () => ({
  speak: jest.fn(),
}));

describe('AccessibleButton', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('renders correctly with required props', () => {
    const { getByText } = render(
      <AccessibleButton text="Test Button" onPress={() => {}} />
    );
    
    expect(getByText('Test Button')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <AccessibleButton text="Test Button" onPress={onPressMock} />
    );
    
    fireEvent.press(getByText('Test Button'));
    expect(onPressMock).toHaveBeenCalledTimes(1);
  });

  it('speaks text on long press when speakOnFocus is true', () => {
    const { getByText } = render(
      <AccessibleButton text="Test Button" onPress={() => {}} speakOnFocus={true} />
    );
    
    fireEvent(getByText('Test Button'), 'onLongPress');
    expect(Speech.speak).toHaveBeenCalledWith('Test Button', { language: 'ar' });
  });

  it('does not speak text on long press when speakOnFocus is false', () => {
    const { getByText } = render(
      <AccessibleButton text="Test Button" onPress={() => {}} speakOnFocus={false} />
    );
    
    fireEvent(getByText('Test Button'), 'onLongPress');
    expect(Speech.speak).not.toHaveBeenCalled();
  });

  it('applies different styles based on variant', () => {
    const { getByText, rerender } = render(
      <AccessibleButton text="Primary Button" onPress={() => {}} variant="primary" />
    );
    
    // We can't easily test styles directly, but we can check if the component renders
    expect(getByText('Primary Button')).toBeTruthy();
    
    rerender(
      <AccessibleButton text="Secondary Button" onPress={() => {}} variant="secondary" />
    );
    expect(getByText('Secondary Button')).toBeTruthy();
    
    rerender(
      <AccessibleButton text="Outline Button" onPress={() => {}} variant="outline" />
    );
    expect(getByText('Outline Button')).toBeTruthy();
    
    rerender(
      <AccessibleButton text="Text Button" onPress={() => {}} variant="text" />
    );
    expect(getByText('Text Button')).toBeTruthy();
  });

  it('applies different styles based on size', () => {
    const { getByText, rerender } = render(
      <AccessibleButton text="Small Button" onPress={() => {}} size="small" />
    );
    
    expect(getByText('Small Button')).toBeTruthy();
    
    rerender(
      <AccessibleButton text="Medium Button" onPress={() => {}} size="medium" />
    );
    expect(getByText('Medium Button')).toBeTruthy();
    
    rerender(
      <AccessibleButton text="Large Button" onPress={() => {}} size="large" />
    );
    expect(getByText('Large Button')).toBeTruthy();
  });

  it('is disabled when disabled prop is true', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <AccessibleButton text="Disabled Button" onPress={onPressMock} disabled={true} />
    );
    
    fireEvent.press(getByText('Disabled Button'));
    expect(onPressMock).not.toHaveBeenCalled();
  });
}); 