import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = 'http://10.0.2.2:8000/api/v1'; // Android emulator localhost

export interface Patient {
  id: number;
  name: string;
  age?: number;
  diagnosis_stage?: string;
  language_preference: string;
  cultural_background?: string;
  created_at: string;
  updated_at?: string;
}

export interface PatientCreate {
  name: string;
  age?: number;
  diagnosis_stage?: string;
  language_preference?: string;
  cultural_background?: string;
  emergency_contacts?: any;
  medication_schedule?: any;
}

export class PatientService {
  static async getCurrentPatient(): Promise<Patient | null> {
    try {
      const patientIdStr = await SecureStore.getItemAsync('current_patient_id');
      if (!patientIdStr) {
        return null;
      }

      const patientId = parseInt(patientIdStr);
      const response = await axios.get(`${API_BASE_URL}/patients/${patientId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting current patient:', error);
      return null;
    }
  }

  static async createPatient(patientData: PatientCreate): Promise<Patient | null> {
    try {
      const response = await axios.post(`${API_BASE_URL}/patients/`, patientData);
      const patient = response.data;
      
      // Store as current patient
      await SecureStore.setItemAsync('current_patient_id', patient.id.toString());
      
      return patient;
    } catch (error) {
      console.error('Error creating patient:', error);
      return null;
    }
  }

  static async updatePatient(patientId: number, updates: Partial<PatientCreate>): Promise<Patient | null> {
    try {
      const response = await axios.put(`${API_BASE_URL}/patients/${patientId}`, updates);
      return response.data;
    } catch (error) {
      console.error('Error updating patient:', error);
      return null;
    }
  }

  static async setCurrentPatient(patientId: number): Promise<void> {
    try {
      await SecureStore.setItemAsync('current_patient_id', patientId.toString());
    } catch (error) {
      console.error('Error setting current patient:', error);
    }
  }

  static async getAllPatients(): Promise<Patient[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/patients/`);
      return response.data;
    } catch (error) {
      console.error('Error getting all patients:', error);
      return [];
    }
  }
}
