import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, Title, Avatar } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';

import { PatientService, Patient } from '../services/PatientService';
import { theme } from '../theme/theme';

export default function PatientProfileScreen({ navigation }: any) {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    diagnosis_stage: 'early',
    cultural_background: 'egyptian',
  });

  useEffect(() => {
    loadPatientData();
  }, []);

  const loadPatientData = async () => {
    try {
      const currentPatient = await PatientService.getCurrentPatient();
      if (currentPatient) {
        setPatient(currentPatient);
        setFormData({
          name: currentPatient.name,
          age: currentPatient.age?.toString() || '',
          diagnosis_stage: currentPatient.diagnosis_stage || 'early',
          cultural_background: currentPatient.cultural_background || 'egyptian',
        });
      }
    } catch (error) {
      console.error('Error loading patient data:', error);
    }
  };

  const savePatientData = async () => {
    if (!formData.name.trim()) {
      Alert.alert('خطأ', 'يرجى إدخال الاسم');
      return;
    }

    setIsLoading(true);
    try {
      const updateData = {
        name: formData.name.trim(),
        age: formData.age ? parseInt(formData.age) : undefined,
        diagnosis_stage: formData.diagnosis_stage,
        cultural_background: formData.cultural_background,
      };

      if (patient) {
        // Update existing patient
        const updatedPatient = await PatientService.updatePatient(patient.id, updateData);
        if (updatedPatient) {
          setPatient(updatedPatient);
          setIsEditing(false);
          Alert.alert('تم', 'تم حفظ البيانات بنجاح');
        }
      } else {
        // Create new patient
        const newPatient = await PatientService.createPatient({
          ...updateData,
          language_preference: 'ar',
        });
        if (newPatient) {
          setPatient(newPatient);
          setIsEditing(false);
          Alert.alert('تم', 'تم إنشاء الملف الشخصي بنجاح');
        }
      }
    } catch (error) {
      console.error('Error saving patient data:', error);
      Alert.alert('خطأ', 'حدث خطأ في حفظ البيانات');
    } finally {
      setIsLoading(false);
    }
  };

  const getStageText = (stage: string) => {
    switch (stage) {
      case 'early': return 'مبكرة';
      case 'moderate': return 'متوسطة';
      case 'severe': return 'متقدمة';
      default: return 'غير محدد';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Profile Header */}
        <Card style={styles.headerCard}>
          <Card.Content style={styles.headerContent}>
            <Avatar.Icon 
              size={80} 
              icon="account" 
              style={{ backgroundColor: theme.colors.primary }}
            />
            <View style={styles.headerText}>
              <Title style={styles.headerTitle}>
                {patient?.name || 'ملف شخصي جديد'}
              </Title>
              <Text style={styles.headerSubtitle}>
                {patient ? 'عضو منذ ' + new Date(patient.created_at).toLocaleDateString('ar-EG') : 'مرحباً بك'}
              </Text>
            </View>
          </Card.Content>
        </Card>

        {/* Profile Form */}
        <Card style={styles.formCard}>
          <Card.Content>
            <View style={styles.formHeader}>
              <Title style={styles.formTitle}>المعلومات الشخصية</Title>
              {!isEditing && (
                <Button
                  mode="outlined"
                  onPress={() => setIsEditing(true)}
                  icon="pencil"
                  compact
                >
                  تعديل
                </Button>
              )}
            </View>

            <View style={styles.formField}>
              <Text style={styles.fieldLabel}>الاسم *</Text>
              <TextInput
                style={[styles.textInput, !isEditing && styles.disabledInput]}
                value={formData.name}
                onChangeText={(text) => setFormData({ ...formData, name: text })}
                placeholder="أدخل الاسم الكامل"
                editable={isEditing}
                textAlign="right"
              />
            </View>

            <View style={styles.formField}>
              <Text style={styles.fieldLabel}>العمر</Text>
              <TextInput
                style={[styles.textInput, !isEditing && styles.disabledInput]}
                value={formData.age}
                onChangeText={(text) => setFormData({ ...formData, age: text })}
                placeholder="أدخل العمر"
                keyboardType="numeric"
                editable={isEditing}
                textAlign="right"
              />
            </View>

            <View style={styles.formField}>
              <Text style={styles.fieldLabel}>مرحلة التشخيص</Text>
              <View style={styles.stageContainer}>
                {['early', 'moderate', 'severe'].map((stage) => (
                  <Button
                    key={stage}
                    mode={formData.diagnosis_stage === stage ? 'contained' : 'outlined'}
                    onPress={() => isEditing && setFormData({ ...formData, diagnosis_stage: stage })}
                    style={styles.stageButton}
                    compact
                    disabled={!isEditing}
                  >
                    {getStageText(stage)}
                  </Button>
                ))}
              </View>
            </View>

            <View style={styles.formField}>
              <Text style={styles.fieldLabel}>الخلفية الثقافية</Text>
              <View style={styles.cultureContainer}>
                {[
                  { key: 'egyptian', label: 'مصرية' },
                  { key: 'gulf', label: 'خليجية' },
                  { key: 'levantine', label: 'شامية' },
                  { key: 'maghrebi', label: 'مغاربية' },
                ].map((culture) => (
                  <Button
                    key={culture.key}
                    mode={formData.cultural_background === culture.key ? 'contained' : 'outlined'}
                    onPress={() => isEditing && setFormData({ ...formData, cultural_background: culture.key })}
                    style={styles.cultureButton}
                    compact
                    disabled={!isEditing}
                  >
                    {culture.label}
                  </Button>
                ))}
              </View>
            </View>

            {isEditing && (
              <View style={styles.formActions}>
                <Button
                  mode="contained"
                  onPress={savePatientData}
                  loading={isLoading}
                  disabled={isLoading}
                  style={styles.saveButton}
                  labelStyle={styles.buttonLabel}
                  icon="check"
                >
                  حفظ
                </Button>
                <Button
                  mode="outlined"
                  onPress={() => {
                    setIsEditing(false);
                    loadPatientData(); // Reset form
                  }}
                  style={styles.cancelButton}
                  labelStyle={styles.buttonLabel}
                >
                  إلغاء
                </Button>
              </View>
            )}
          </Card.Content>
        </Card>

        {/* Medical Information */}
        <Card style={styles.medicalCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>المعلومات الطبية</Title>
            
            <View style={styles.medicalItem}>
              <Ionicons name="medical" size={24} color={theme.colors.primary} />
              <View style={styles.medicalText}>
                <Text style={styles.medicalLabel}>مرحلة التشخيص</Text>
                <Text style={styles.medicalValue}>
                  {getStageText(formData.diagnosis_stage)}
                </Text>
              </View>
            </View>

            <View style={styles.medicalItem}>
              <Ionicons name="calendar" size={24} color={theme.colors.primary} />
              <View style={styles.medicalText}>
                <Text style={styles.medicalLabel}>تاريخ التسجيل</Text>
                <Text style={styles.medicalValue}>
                  {patient ? new Date(patient.created_at).toLocaleDateString('ar-EG') : 'غير محدد'}
                </Text>
              </View>
            </View>

            <View style={styles.medicalItem}>
              <Ionicons name="language" size={24} color={theme.colors.primary} />
              <View style={styles.medicalText}>
                <Text style={styles.medicalLabel}>اللغة المفضلة</Text>
                <Text style={styles.medicalValue}>العربية</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>إجراءات سريعة</Title>
            
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Assessment')}
              style={styles.actionButton}
              labelStyle={styles.buttonLabel}
              icon="brain"
            >
              إجراء تقييم معرفي
            </Button>

            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Conversation')}
              style={styles.actionButton}
              labelStyle={styles.buttonLabel}
              icon="chat"
            >
              بدء محادثة مع فاكر
            </Button>

            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Reminders')}
              style={styles.actionButton}
              labelStyle={styles.buttonLabel}
              icon="notifications"
            >
              إدارة التذكيرات
            </Button>
          </Card.Content>
        </Card>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    padding: 16,
  },
  headerCard: {
    marginBottom: 16,
    elevation: 4,
    borderRadius: 12,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
  },
  headerText: {
    marginLeft: 16,
    flex: 1,
  },
  headerTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  headerSubtitle: {
    color: '#666',
    fontSize: 14,
    fontFamily: 'Cairo-Regular',
  },
  formCard: {
    marginBottom: 16,
    elevation: 2,
    borderRadius: 12,
  },
  formHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  formTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  formField: {
    marginBottom: 16,
  },
  fieldLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#333',
    fontFamily: 'Cairo-Bold',
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: 'white',
    fontFamily: 'Cairo-Regular',
  },
  disabledInput: {
    backgroundColor: '#f5f5f5',
    color: '#666',
  },
  stageContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  stageButton: {
    flex: 1,
  },
  cultureContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  cultureButton: {
    minWidth: '45%',
  },
  formActions: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 16,
  },
  saveButton: {
    flex: 1,
    backgroundColor: theme.colors.primary,
  },
  cancelButton: {
    flex: 1,
  },
  buttonLabel: {
    fontFamily: 'Cairo-Bold',
    fontSize: 14,
  },
  medicalCard: {
    marginBottom: 16,
    elevation: 2,
    borderRadius: 12,
  },
  cardTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginBottom: 16,
  },
  medicalItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  medicalText: {
    marginLeft: 16,
    flex: 1,
  },
  medicalLabel: {
    fontSize: 14,
    color: '#666',
    fontFamily: 'Cairo-Regular',
  },
  medicalValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    fontFamily: 'Cairo-Bold',
  },
  actionsCard: {
    elevation: 2,
    borderRadius: 12,
  },
  actionButton: {
    marginBottom: 8,
  },
});
