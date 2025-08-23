import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, FAB, Chip } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
// import * as Notifications from 'expo-notifications'; // Disabled for Expo Go compatibility
import * as Speech from 'expo-speech';
import * as Animatable from 'react-native-animatable';

import { ReminderService, Reminder } from '../services/ReminderService';
import { theme } from '../theme/theme';

export default function RemindersScreen() {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [dueReminders, setDueReminders] = useState<Reminder[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadReminders();
    const interval = setInterval(loadDueReminders, 60000); // Check every minute
    return () => clearInterval(interval);
  }, []);

  const loadReminders = async () => {
    try {
      setIsLoading(true);
      const [allReminders, due] = await Promise.all([
        ReminderService.getPatientReminders(1, true), // upcoming only
        ReminderService.getDueReminders(1, 2), // next 2 hours
      ]);
      
      setReminders(allReminders);
      setDueReminders(due);
    } catch (error) {
      console.error('Error loading reminders:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadDueReminders = async () => {
    try {
      const due = await ReminderService.getDueReminders(1, 1);
      setDueReminders(due);
    } catch (error) {
      console.error('Error loading due reminders:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadReminders();
    setRefreshing(false);
  };

  const completeReminder = async (reminderId: number) => {
    try {
      await ReminderService.completeReminder(reminderId);
      await loadReminders();
      
      Alert.alert('تم!', 'تم تسجيل إكمال التذكير بنجاح');
      Speech.speak('أحسنت! تم تسجيل إكمال المهمة', { language: 'ar' });
    } catch (error) {
      console.error('Error completing reminder:', error);
      Alert.alert('خطأ', 'حدث خطأ في تسجيل إكمال التذكير');
    }
  };

  const speakReminder = (reminder: Reminder) => {
    const text = `تذكير: ${reminder.title}. ${reminder.description || ''}`;
    Speech.speak(text, { language: 'ar', rate: 0.8 });
  };

  const getReminderIcon = (type: string) => {
    switch (type) {
      case 'medication': return 'medical';
      case 'appointment': return 'calendar';
      case 'activity': return 'fitness';
      case 'social': return 'people';
      default: return 'notifications';
    }
  };

  const getReminderColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return '#F44336';
      case 'high': return '#FF9800';
      case 'medium': return '#2196F3';
      case 'low': return '#4CAF50';
      default: return '#2196F3';
    }
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ar-EG', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return 'اليوم';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'غداً';
    } else {
      return date.toLocaleDateString('ar-EG');
    }
  };

  const renderReminder = (reminder: Reminder, isDue: boolean = false) => (
    <Animatable.View
      key={reminder.id}
      animation="fadeInUp"
      duration={600}
    >
      <Card style={[
        styles.reminderCard,
        isDue && styles.dueReminderCard
      ]}>
        <Card.Content>
          <View style={styles.reminderHeader}>
            <View style={styles.reminderInfo}>
              <Ionicons
                name={getReminderIcon(reminder.reminder_type)}
                size={24}
                color={getReminderColor(reminder.priority)}
              />
              <View style={styles.reminderText}>
                <Text style={styles.reminderTitle}>{reminder.title}</Text>
                {reminder.description && (
                  <Text style={styles.reminderDescription}>
                    {reminder.description}
                  </Text>
                )}
              </View>
            </View>
            <TouchableOpacity
              onPress={() => speakReminder(reminder)}
              style={styles.speakButton}
            >
              <Ionicons name="volume-high" size={20} color={theme.colors.primary} />
            </TouchableOpacity>
          </View>

          <View style={styles.reminderDetails}>
            <View style={styles.timeInfo}>
              <Ionicons name="time" size={16} color="#666" />
              <Text style={styles.timeText}>
                {formatDate(reminder.scheduled_time)} - {formatTime(reminder.scheduled_time)}
              </Text>
            </View>
            
            <View style={styles.reminderTags}>
              <Chip
                style={[styles.priorityChip, { backgroundColor: getReminderColor(reminder.priority) }]}
                textStyle={styles.chipText}
              >
                {reminder.priority === 'urgent' ? 'عاجل' :
                 reminder.priority === 'high' ? 'مهم' :
                 reminder.priority === 'medium' ? 'متوسط' : 'عادي'}
              </Chip>
              
              {reminder.is_recurring && (
                <Chip style={styles.recurringChip} textStyle={styles.chipText}>
                  متكرر
                </Chip>
              )}
            </View>
          </View>

          <View style={styles.reminderActions}>
            <Button
              mode="contained"
              onPress={() => completeReminder(reminder.id)}
              style={styles.completeButton}
              labelStyle={styles.buttonLabel}
              icon="check"
            >
              تم
            </Button>
            
            {isDue && (
              <Button
                mode="outlined"
                onPress={() => {
                  // Snooze for 15 minutes
                  Alert.alert('تأجيل', 'سيتم تذكيرك مرة أخرى خلال 15 دقيقة');
                }}
                style={styles.snoozeButton}
                labelStyle={styles.buttonLabel}
              >
                تأجيل
              </Button>
            )}
          </View>
        </Card.Content>
      </Card>
    </Animatable.View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Due Reminders */}
        {dueReminders.length > 0 && (
          <Animatable.View animation="fadeInDown" duration={1000}>
            <View style={styles.sectionHeader}>
              <Ionicons name="alarm" size={24} color="#F44336" />
              <Text style={[styles.sectionTitle, { color: '#F44336' }]}>
                تذكيرات مستحقة الآن
              </Text>
            </View>
            {dueReminders.map(reminder => renderReminder(reminder, true))}
          </Animatable.View>
        )}

        {/* Upcoming Reminders */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={300}>
          <View style={styles.sectionHeader}>
            <Ionicons name="calendar-outline" size={24} color={theme.colors.primary} />
            <Text style={styles.sectionTitle}>التذكيرات القادمة</Text>
          </View>
          
          {reminders.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Ionicons name="calendar-clear" size={64} color="#ccc" />
                <Text style={styles.emptyText}>لا توجد تذكيرات قادمة</Text>
                <Text style={styles.emptySubtext}>
                  يمكنك إضافة تذكيرات جديدة باستخدام الزر أدناه
                </Text>
              </Card.Content>
            </Card>
          ) : (
            reminders.map(reminder => renderReminder(reminder))
          )}
        </Animatable.View>

        {/* Quick Add Suggestions */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={600}>
          <Text style={styles.sectionTitle}>إضافة سريعة</Text>
          <View style={styles.quickAddGrid}>
            <TouchableOpacity
              style={[styles.quickAddCard, { backgroundColor: '#4CAF50' }]}
              onPress={() => {/* Add medication reminder */}}
            >
              <Ionicons name="medical" size={32} color="white" />
              <Text style={styles.quickAddText}>دواء</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.quickAddCard, { backgroundColor: '#2196F3' }]}
              onPress={() => {/* Add appointment reminder */}}
            >
              <Ionicons name="calendar" size={32} color="white" />
              <Text style={styles.quickAddText}>موعد</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.quickAddCard, { backgroundColor: '#FF9800' }]}
              onPress={() => {/* Add meal reminder */}}
            >
              <Ionicons name="restaurant" size={32} color="white" />
              <Text style={styles.quickAddText}>وجبة</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.quickAddCard, { backgroundColor: '#9C27B0' }]}
              onPress={() => {/* Add activity reminder */}}
            >
              <Ionicons name="fitness" size={32} color="white" />
              <Text style={styles.quickAddText}>نشاط</Text>
            </TouchableOpacity>
          </View>
        </Animatable.View>
      </ScrollView>

      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => {
          Alert.alert('إضافة تذكير', 'سيتم إضافة نموذج إنشاء التذكيرات قريباً');
        }}
      />
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
    paddingBottom: 80,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    marginTop: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  reminderCard: {
    marginBottom: 12,
    elevation: 2,
    borderRadius: 12,
  },
  dueReminderCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#F44336',
    elevation: 4,
  },
  reminderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  reminderInfo: {
    flexDirection: 'row',
    flex: 1,
  },
  reminderText: {
    marginLeft: 12,
    flex: 1,
  },
  reminderTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    fontFamily: 'Cairo-Bold',
  },
  reminderDescription: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
    fontFamily: 'Cairo-Regular',
  },
  speakButton: {
    padding: 4,
  },
  reminderDetails: {
    marginBottom: 16,
  },
  timeInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  timeText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#666',
    fontFamily: 'Cairo-Regular',
  },
  reminderTags: {
    flexDirection: 'row',
    gap: 8,
  },
  priorityChip: {
    height: 28,
  },
  recurringChip: {
    height: 28,
    backgroundColor: '#E0E0E0',
  },
  chipText: {
    fontSize: 12,
    color: 'white',
    fontFamily: 'Cairo-Regular',
  },
  reminderActions: {
    flexDirection: 'row',
    gap: 12,
  },
  completeButton: {
    flex: 1,
    backgroundColor: '#4CAF50',
  },
  snoozeButton: {
    flex: 1,
  },
  buttonLabel: {
    fontFamily: 'Cairo-Bold',
    fontSize: 14,
  },
  emptyCard: {
    elevation: 2,
    borderRadius: 12,
  },
  emptyContent: {
    alignItems: 'center',
    padding: 32,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginTop: 16,
    fontFamily: 'Cairo-Bold',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginTop: 8,
    fontFamily: 'Cairo-Regular',
  },
  quickAddGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12,
  },
  quickAddCard: {
    width: '48%',
    aspectRatio: 1.5,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 3,
  },
  quickAddText: {
    color: 'white',
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 8,
    fontFamily: 'Cairo-Bold',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.primary,
  },
});
