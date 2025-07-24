/**
 * ReminderService.ts
 * Service to manage medication and activity reminders
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Reminder types
export enum ReminderType {
  MEDICATION = 'medication',
  ACTIVITY = 'activity',
  APPOINTMENT = 'appointment',
  OTHER = 'other',
}

// Reminder frequency
export enum ReminderFrequency {
  ONCE = 'once',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  CUSTOM = 'custom',
}

// Reminder interface
export interface Reminder {
  id: string;
  title: string;
  description?: string;
  type: ReminderType;
  time: string; // HH:MM format
  date?: string; // YYYY-MM-DD format (for non-recurring)
  frequency: ReminderFrequency;
  daysOfWeek?: number[]; // 0-6 for Sunday-Saturday (for weekly)
  daysOfMonth?: number[]; // 1-31 (for monthly)
  customDates?: string[]; // YYYY-MM-DD format (for custom)
  isActive: boolean;
  notificationId?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * ReminderService - Manages medication and activity reminders
 */
class ReminderService {
  private STORAGE_KEY = '@faker_reminders';
  
  /**
   * Initialize the reminder service
   */
  initialize = async (): Promise<void> => {
    // Request notification permissions
    await this.requestNotificationPermissions();
    
    // Configure notification behavior
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      }),
    });
  };
  
  /**
   * Request notification permissions
   */
  requestNotificationPermissions = async (): Promise<boolean> => {
    if (Platform.OS === 'android') {
      // Android permissions are granted by default
      return true;
    }
    
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    
    return finalStatus === 'granted';
  };
  
  /**
   * Get all reminders
   */
  getReminders = async (): Promise<Reminder[]> => {
    try {
      const remindersJson = await AsyncStorage.getItem(this.STORAGE_KEY);
      return remindersJson ? JSON.parse(remindersJson) : [];
    } catch (error) {
      console.error('Error getting reminders:', error);
      return [];
    }
  };
  
  /**
   * Get reminders by type
   */
  getRemindersByType = async (type: ReminderType): Promise<Reminder[]> => {
    const reminders = await this.getReminders();
    return reminders.filter(reminder => reminder.type === type);
  };
  
  /**
   * Get reminders for today
   */
  getTodayReminders = async (): Promise<Reminder[]> => {
    const reminders = await this.getReminders();
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
    const dayOfWeek = today.getDay(); // 0-6
    const dayOfMonth = today.getDate(); // 1-31
    
    return reminders.filter(reminder => {
      if (!reminder.isActive) return false;
      
      // Check for one-time reminders for today
      if (reminder.frequency === ReminderFrequency.ONCE && reminder.date === todayStr) {
        return true;
      }
      
      // Check for daily reminders
      if (reminder.frequency === ReminderFrequency.DAILY) {
        return true;
      }
      
      // Check for weekly reminders
      if (reminder.frequency === ReminderFrequency.WEEKLY && 
          reminder.daysOfWeek && 
          reminder.daysOfWeek.includes(dayOfWeek)) {
        return true;
      }
      
      // Check for monthly reminders
      if (reminder.frequency === ReminderFrequency.MONTHLY && 
          reminder.daysOfMonth && 
          reminder.daysOfMonth.includes(dayOfMonth)) {
        return true;
      }
      
      // Check for custom reminders
      if (reminder.frequency === ReminderFrequency.CUSTOM && 
          reminder.customDates && 
          reminder.customDates.includes(todayStr)) {
        return true;
      }
      
      return false;
    });
  };
  
  /**
   * Add a new reminder
   */
  addReminder = async (reminder: Omit<Reminder, 'id' | 'createdAt' | 'updatedAt'>): Promise<Reminder> => {
    try {
      const reminders = await this.getReminders();
      
      const newReminder: Reminder = {
        ...reminder,
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      
      // Schedule the notification
      if (newReminder.isActive) {
        const notificationId = await this.scheduleNotification(newReminder);
        newReminder.notificationId = notificationId;
      }
      
      // Save to storage
      await AsyncStorage.setItem(this.STORAGE_KEY, JSON.stringify([...reminders, newReminder]));
      
      return newReminder;
    } catch (error) {
      console.error('Error adding reminder:', error);
      throw error;
    }
  };
  
  /**
   * Update an existing reminder
   */
  updateReminder = async (updatedReminder: Reminder): Promise<Reminder> => {
    try {
      const reminders = await this.getReminders();
      const reminderIndex = reminders.findIndex(r => r.id === updatedReminder.id);
      
      if (reminderIndex === -1) {
        throw new Error('Reminder not found');
      }
      
      // Cancel existing notification if present
      if (reminders[reminderIndex].notificationId) {
        await Notifications.cancelScheduledNotificationAsync(reminders[reminderIndex].notificationId);
      }
      
      // Schedule new notification if active
      if (updatedReminder.isActive) {
        const notificationId = await this.scheduleNotification(updatedReminder);
        updatedReminder.notificationId = notificationId;
      } else {
        updatedReminder.notificationId = undefined;
      }
      
      updatedReminder.updatedAt = new Date().toISOString();
      
      // Update in storage
      reminders[reminderIndex] = updatedReminder;
      await AsyncStorage.setItem(this.STORAGE_KEY, JSON.stringify(reminders));
      
      return updatedReminder;
    } catch (error) {
      console.error('Error updating reminder:', error);
      throw error;
    }
  };
  
  /**
   * Delete a reminder
   */
  deleteReminder = async (id: string): Promise<void> => {
    try {
      const reminders = await this.getReminders();
      const reminderToDelete = reminders.find(r => r.id === id);
      
      if (!reminderToDelete) {
        throw new Error('Reminder not found');
      }
      
      // Cancel notification if exists
      if (reminderToDelete.notificationId) {
        await Notifications.cancelScheduledNotificationAsync(reminderToDelete.notificationId);
      }
      
      // Remove from storage
      const updatedReminders = reminders.filter(r => r.id !== id);
      await AsyncStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedReminders));
    } catch (error) {
      console.error('Error deleting reminder:', error);
      throw error;
    }
  };
  
  /**
   * Toggle reminder active status
   */
  toggleReminderActive = async (id: string): Promise<Reminder> => {
    try {
      const reminders = await this.getReminders();
      const reminderIndex = reminders.findIndex(r => r.id === id);
      
      if (reminderIndex === -1) {
        throw new Error('Reminder not found');
      }
      
      const reminder = reminders[reminderIndex];
      reminder.isActive = !reminder.isActive;
      reminder.updatedAt = new Date().toISOString();
      
      // Handle notification
      if (reminder.isActive) {
        // Schedule new notification
        const notificationId = await this.scheduleNotification(reminder);
        reminder.notificationId = notificationId;
      } else if (reminder.notificationId) {
        // Cancel existing notification
        await Notifications.cancelScheduledNotificationAsync(reminder.notificationId);
        reminder.notificationId = undefined;
      }
      
      // Update in storage
      reminders[reminderIndex] = reminder;
      await AsyncStorage.setItem(this.STORAGE_KEY, JSON.stringify(reminders));
      
      return reminder;
    } catch (error) {
      console.error('Error toggling reminder:', error);
      throw error;
    }
  };
  
  /**
   * Schedule a notification for a reminder
   */
  private scheduleNotification = async (reminder: Reminder): Promise<string> => {
    try {
      // For simplicity, we'll just schedule the next occurrence
      const trigger = this.calculateNextTrigger(reminder);
      
      if (!trigger) {
        console.warn('No valid trigger time for reminder:', reminder.title);
        return '';
      }
      
      // Create notification content
      const content = {
        title: reminder.title,
        body: reminder.description || '',
        sound: true,
        priority: Notifications.AndroidNotificationPriority.HIGH,
        data: { reminderType: reminder.type, reminderId: reminder.id },
      };
      
      // Schedule the notification
      const notificationId = await Notifications.scheduleNotificationAsync({
        content,
        trigger,
      });
      
      return notificationId;
    } catch (error) {
      console.error('Error scheduling notification:', error);
      return '';
    }
  };
  
  /**
   * Calculate the next trigger time for a reminder
   */
  private calculateNextTrigger = (reminder: Reminder): Notifications.NotificationTriggerInput | null => {
    try {
      const [hours, minutes] = reminder.time.split(':').map(Number);
      const now = new Date();
      
      // For one-time reminders
      if (reminder.frequency === ReminderFrequency.ONCE && reminder.date) {
        const reminderDate = new Date(reminder.date);
        reminderDate.setHours(hours, minutes, 0);
        
        // If the date is in the past, don't schedule
        if (reminderDate <= now) {
          return null;
        }
        
        return {
          date: reminderDate,
        };
      }
      
      // For daily reminders
      if (reminder.frequency === ReminderFrequency.DAILY) {
        const triggerDate = new Date();
        triggerDate.setHours(hours, minutes, 0);
        
        // If the time is already past for today, schedule for tomorrow
        if (triggerDate <= now) {
          triggerDate.setDate(triggerDate.getDate() + 1);
        }
        
        return {
          hour: hours,
          minute: minutes,
          repeats: true,
        };
      }
      
      // For weekly reminders
      if (reminder.frequency === ReminderFrequency.WEEKLY && reminder.daysOfWeek && reminder.daysOfWeek.length > 0) {
        const currentDay = now.getDay();
        const currentTime = now.getHours() * 60 + now.getMinutes();
        const reminderTime = hours * 60 + minutes;
        
        // Find the next occurrence
        let daysToAdd = 0;
        let foundNextDay = false;
        
        // Check if today is a reminder day and the time hasn't passed
        if (reminder.daysOfWeek.includes(currentDay) && reminderTime > currentTime) {
          foundNextDay = true;
        } else {
          // Find the next day in the week
          for (let i = 1; i <= 7; i++) {
            const nextDay = (currentDay + i) % 7;
            if (reminder.daysOfWeek.includes(nextDay)) {
              daysToAdd = i;
              foundNextDay = true;
              break;
            }
          }
        }
        
        if (!foundNextDay) {
          return null;
        }
        
        const triggerDate = new Date();
        triggerDate.setDate(triggerDate.getDate() + daysToAdd);
        triggerDate.setHours(hours, minutes, 0);
        
        return {
          date: triggerDate,
        };
      }
      
      // For monthly reminders
      if (reminder.frequency === ReminderFrequency.MONTHLY && reminder.daysOfMonth && reminder.daysOfMonth.length > 0) {
        const currentDate = now.getDate();
        const currentMonth = now.getMonth();
        const currentYear = now.getFullYear();
        const currentTime = now.getHours() * 60 + now.getMinutes();
        const reminderTime = hours * 60 + minutes;
        
        // Find the next occurrence
        let targetDate = 0;
        let monthsToAdd = 0;
        
        // Check if there's a day later this month
        const laterDaysThisMonth = reminder.daysOfMonth
          .filter(day => day > currentDate || (day === currentDate && reminderTime > currentTime))
          .sort((a, b) => a - b);
        
        if (laterDaysThisMonth.length > 0) {
          targetDate = laterDaysThisMonth[0];
        } else {
          // Move to next month
          monthsToAdd = 1;
          targetDate = reminder.daysOfMonth.sort((a, b) => a - b)[0];
        }
        
        const triggerDate = new Date(currentYear, currentMonth + monthsToAdd, targetDate, hours, minutes);
        
        return {
          date: triggerDate,
        };
      }
      
      // For custom reminders
      if (reminder.frequency === ReminderFrequency.CUSTOM && reminder.customDates && reminder.customDates.length > 0) {
        // Find the next date
        const futureDates = reminder.customDates
          .map(dateStr => {
            const date = new Date(dateStr);
            date.setHours(hours, minutes, 0);
            return date;
          })
          .filter(date => date > now)
          .sort((a, b) => a.getTime() - b.getTime());
        
        if (futureDates.length === 0) {
          return null;
        }
        
        return {
          date: futureDates[0],
        };
      }
      
      return null;
    } catch (error) {
      console.error('Error calculating trigger:', error);
      return null;
    }
  };
}

export default new ReminderService(); 