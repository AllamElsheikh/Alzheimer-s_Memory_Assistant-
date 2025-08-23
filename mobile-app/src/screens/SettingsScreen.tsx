import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Switch,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, Title, List, Divider } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as SecureStore from 'expo-secure-store';
// import * as Notifications from 'expo-notifications'; // Disabled for Expo Go compatibility

import { theme } from '../theme/theme';

export default function SettingsScreen({ navigation }: any) {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [voiceGuidanceEnabled, setVoiceGuidanceEnabled] = useState(true);
  const [highContrastMode, setHighContrastMode] = useState(false);
  const [largeTextMode, setLargeTextMode] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const notifications = await SecureStore.getItemAsync('notifications_enabled');
      const voiceGuidance = await SecureStore.getItemAsync('voice_guidance_enabled');
      const highContrast = await SecureStore.getItemAsync('high_contrast_mode');
      const largeText = await SecureStore.getItemAsync('large_text_mode');

      setNotificationsEnabled(notifications !== 'false');
      setVoiceGuidanceEnabled(voiceGuidance !== 'false');
      setHighContrastMode(highContrast === 'true');
      setLargeTextMode(largeText === 'true');
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const saveSetting = async (key: string, value: boolean) => {
    try {
      await SecureStore.setItemAsync(key, value.toString());
    } catch (error) {
      console.error('Error saving setting:', error);
    }
  };

  const toggleNotifications = async (value: boolean) => {
    setNotificationsEnabled(value);
    await saveSetting('notifications_enabled', value);
    
    if (value) {
      // Notifications disabled for Expo Go compatibility
      Alert.alert('تنبيه', 'الإشعارات غير متاحة في Expo Go. استخدم تطبيق مخصص للحصول على الإشعارات الكاملة.');
      setNotificationsEnabled(false);
      await saveSetting('notifications_enabled', false);
    }
  };

  const toggleVoiceGuidance = async (value: boolean) => {
    setVoiceGuidanceEnabled(value);
    await saveSetting('voice_guidance_enabled', value);
  };

  const toggleHighContrast = async (value: boolean) => {
    setHighContrastMode(value);
    await saveSetting('high_contrast_mode', value);
    Alert.alert('إعادة تشغيل', 'يتطلب إعادة تشغيل التطبيق لتطبيق التغييرات');
  };

  const toggleLargeText = async (value: boolean) => {
    setLargeTextMode(value);
    await saveSetting('large_text_mode', value);
    Alert.alert('إعادة تشغيل', 'يتطلب إعادة تشغيل التطبيق لتطبيق التغييرات');
  };

  const clearData = () => {
    Alert.alert(
      'مسح البيانات',
      'هل تريد مسح جميع البيانات المحفوظة؟ لا يمكن التراجع عن هذا الإجراء.',
      [
        { text: 'إلغاء', style: 'cancel' },
        {
          text: 'مسح',
          style: 'destructive',
          onPress: async () => {
            try {
              await SecureStore.deleteItemAsync('current_session_id');
              await SecureStore.deleteItemAsync('current_patient_id');
              Alert.alert('تم', 'تم مسح البيانات بنجاح');
            } catch (error) {
              Alert.alert('خطأ', 'حدث خطأ في مسح البيانات');
            }
          },
        },
      ]
    );
  };

  const showAbout = () => {
    Alert.alert(
      'حول فاكر',
      'فاكر - مساعد الذاكرة\nالإصدار 1.0.0\n\nتطبيق ذكي لمساعدة مرضى الزهايمر وعائلاتهم\nمدعوم بتقنية Gemma 3n المتقدمة',
      [{ text: 'موافق' }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* App Settings */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>إعدادات التطبيق</Title>
            
            <List.Item
              title="الإشعارات"
              description="تلقي تذكيرات المواعيد والأدوية"
              left={() => <Ionicons name="notifications" size={24} color={theme.colors.primary} />}
              right={() => (
                <Switch
                  value={notificationsEnabled}
                  onValueChange={toggleNotifications}
                  trackColor={{ false: '#767577', true: theme.colors.primary }}
                />
              )}
            />
            
            <Divider />
            
            <List.Item
              title="الإرشاد الصوتي"
              description="تشغيل الردود والتعليمات صوتياً"
              left={() => <Ionicons name="volume-high" size={24} color={theme.colors.primary} />}
              right={() => (
                <Switch
                  value={voiceGuidanceEnabled}
                  onValueChange={toggleVoiceGuidance}
                  trackColor={{ false: '#767577', true: theme.colors.primary }}
                />
              )}
            />
          </Card.Content>
        </Card>

        {/* Accessibility Settings */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>إعدادات إمكانية الوصول</Title>
            
            <List.Item
              title="التباين العالي"
              description="ألوان أكثر وضوحاً للنص والخلفية"
              left={() => <Ionicons name="contrast" size={24} color={theme.colors.primary} />}
              right={() => (
                <Switch
                  value={highContrastMode}
                  onValueChange={toggleHighContrast}
                  trackColor={{ false: '#767577', true: theme.colors.primary }}
                />
              )}
            />
            
            <Divider />
            
            <List.Item
              title="النص الكبير"
              description="حجم خط أكبر لسهولة القراءة"
              left={() => <Ionicons name="text" size={24} color={theme.colors.primary} />}
              right={() => (
                <Switch
                  value={largeTextMode}
                  onValueChange={toggleLargeText}
                  trackColor={{ false: '#767577', true: theme.colors.primary }}
                />
              )}
            />
          </Card.Content>
        </Card>

        {/* Patient Profile */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>الملف الشخصي</Title>
            
            <TouchableOpacity
              style={styles.settingItem}
              onPress={() => navigation.navigate('PatientProfile')}
            >
              <Ionicons name="person" size={24} color={theme.colors.primary} />
              <View style={styles.settingText}>
                <Text style={styles.settingTitle}>معلومات المريض</Text>
                <Text style={styles.settingDescription}>تحديث البيانات الشخصية والطبية</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#666" />
            </TouchableOpacity>
          </Card.Content>
        </Card>

        {/* Data & Privacy */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>البيانات والخصوصية</Title>
            
            <TouchableOpacity style={styles.settingItem} onPress={clearData}>
              <Ionicons name="trash" size={24} color="#F44336" />
              <View style={styles.settingText}>
                <Text style={[styles.settingTitle, { color: '#F44336' }]}>مسح البيانات</Text>
                <Text style={styles.settingDescription}>حذف جميع البيانات المحفوظة</Text>
              </View>
            </TouchableOpacity>
          </Card.Content>
        </Card>

        {/* Support & Info */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>الدعم والمعلومات</Title>
            
            <TouchableOpacity style={styles.settingItem} onPress={showAbout}>
              <Ionicons name="information-circle" size={24} color={theme.colors.primary} />
              <View style={styles.settingText}>
                <Text style={styles.settingTitle}>حول التطبيق</Text>
                <Text style={styles.settingDescription}>معلومات الإصدار والمطور</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#666" />
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.settingItem}
              onPress={() => Alert.alert('الدعم الفني', 'للدعم الفني، يرجى التواصل مع فريق التطوير')}
            >
              <Ionicons name="help-circle" size={24} color={theme.colors.primary} />
              <View style={styles.settingText}>
                <Text style={styles.settingTitle}>الدعم الفني</Text>
                <Text style={styles.settingDescription}>المساعدة والأسئلة الشائعة</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#666" />
            </TouchableOpacity>
          </Card.Content>
        </Card>

        {/* Emergency Contacts */}
        <Card style={styles.settingsCard}>
          <Card.Content>
            <Title style={styles.cardTitle}>جهات الاتصال الطارئة</Title>
            
            <Button
              mode="contained"
              onPress={() => Alert.alert('الطوارئ', 'سيتم إضافة إدارة جهات الاتصال الطارئة قريباً')}
              style={styles.emergencyButton}
              labelStyle={styles.buttonLabel}
              icon="phone"
            >
              إدارة جهات الاتصال
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
  settingsCard: {
    marginBottom: 16,
    elevation: 2,
    borderRadius: 12,
  },
  cardTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginBottom: 8,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  settingText: {
    flex: 1,
    marginLeft: 16,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    fontFamily: 'Cairo-Bold',
  },
  settingDescription: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
    fontFamily: 'Cairo-Regular',
  },
  emergencyButton: {
    backgroundColor: '#F44336',
    marginTop: 8,
  },
  buttonLabel: {
    fontFamily: 'Cairo-Bold',
    fontSize: 14,
  },
});
