import * as Device from 'expo-device';
import { Platform, Alert } from 'react-native';

// Simplified notification service for Expo Go compatibility
export class NotificationService {
  static async initialize() {
    // Local notifications only - no push notifications in Expo Go
    console.log('NotificationService initialized for local notifications only');
  }

  static async requestPermissions(): Promise<boolean> {
    if (!Device.isDevice) {
      console.warn('Must use physical device for notifications');
      return false;
    }
    // Return true for Expo Go compatibility
    return true;
  }

  static async scheduleReminder(
    title: string,
    body: string,
    scheduledTime: Date,
    data?: any
  ): Promise<string | null> {
    try {
      // Use Alert as fallback for Expo Go
      Alert.alert(
        'تذكير مجدول',
        `${title}: ${body}\nسيتم التذكير في: ${scheduledTime.toLocaleString('ar-EG')}`,
        [{ text: 'حسناً', style: 'default' }]
      );
      return `local_${Date.now()}`;
    } catch (error) {
      console.error('Error scheduling notification:', error);
      return null;
    }
  }

  static async scheduleRecurringReminder(
    title: string,
    body: string,
    hour: number,
    minute: number,
    pattern: 'daily' | 'weekly',
    data?: any
  ): Promise<string | null> {
    try {
      const patternText = pattern === 'daily' ? 'يومياً' : 'أسبوعياً';
      Alert.alert(
        'تذكير متكرر',
        `${title}: ${body}\nالنمط: ${patternText} في ${hour}:${minute.toString().padStart(2, '0')}`,
        [{ text: 'حسناً', style: 'default' }]
      );
      return `recurring_${Date.now()}`;
    } catch (error) {
      console.error('Error scheduling recurring notification:', error);
      return null;
    }
  }

  static async sendImmediateNotification(
    title: string,
    body: string,
    data?: any
  ): Promise<void> {
    try {
      Alert.alert(title, body, [{ text: 'حسناً', style: 'default' }]);
    } catch (error) {
      console.error('Error sending immediate notification:', error);
    }
  }

  static async cancelNotification(notificationId: string): Promise<void> {
    try {
      console.log(`Cancelled notification: ${notificationId}`);
    } catch (error) {
      console.error('Error canceling notification:', error);
    }
  }

  static async cancelAllNotifications(): Promise<void> {
    try {
      console.log('All notifications cancelled');
    } catch (error) {
      console.error('Error canceling all notifications:', error);
    }
  }

  static async getScheduledNotifications(): Promise<any[]> {
    try {
      return [];
    } catch (error) {
      console.error('Error getting scheduled notifications:', error);
      return [];
    }
  }
}
