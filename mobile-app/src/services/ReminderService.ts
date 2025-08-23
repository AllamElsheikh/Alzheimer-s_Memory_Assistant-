import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = 'http://10.0.2.2:8000/api/v1'; // Android emulator localhost

export interface Reminder {
  id: number;
  patient_id: number;
  title: string;
  description?: string;
  reminder_type: string;
  scheduled_time: string;
  is_recurring: boolean;
  recurrence_pattern?: string;
  is_completed: boolean;
  priority: string;
  created_at: string;
}

export interface ReminderCreate {
  patient_id: number;
  title: string;
  description?: string;
  reminder_type: string;
  scheduled_time: string;
  is_recurring?: boolean;
  recurrence_pattern?: string;
  priority?: string;
}

export class ReminderService {
  static async getPatientReminders(patientId: number, upcomingOnly: boolean = false): Promise<Reminder[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/patients/${patientId}/reminders`);
      return response.data;
    } catch (error) {
      console.error('Error getting patient reminders:', error);
      return [];
    }
  }

  static async getDueReminders(patientId?: number, hoursAhead: number = 1): Promise<Reminder[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/reminders/due`);
      return response.data;
    } catch (error) {
      console.error('Error getting due reminders:', error);
      return [];
    }
  }

  static async createReminder(reminderData: ReminderCreate): Promise<Reminder | null> {
    try {
      const response = await axios.post(`${API_BASE_URL}/reminders/`, reminderData);
      return response.data;
    } catch (error) {
      console.error('Error creating reminder:', error);
      return null;
    }
  }

  static async completeReminder(reminderId: number): Promise<boolean> {
    try {
      await axios.post(`${API_BASE_URL}/reminders/${reminderId}/complete`);
      return true;
    } catch (error) {
      console.error('Error completing reminder:', error);
      return false;
    }
  }

  static async updateReminder(reminderId: number, updates: Partial<ReminderCreate>): Promise<Reminder | null> {
    try {
      const response = await axios.put(`${API_BASE_URL}/reminders/${reminderId}`, updates);
      return response.data;
    } catch (error) {
      console.error('Error updating reminder:', error);
      return null;
    }
  }

  static async deleteReminder(reminderId: number): Promise<boolean> {
    try {
      await axios.delete(`${API_BASE_URL}/reminders/${reminderId}`);
      return true;
    } catch (error) {
      console.error('Error deleting reminder:', error);
      return false;
    }
  }
}
