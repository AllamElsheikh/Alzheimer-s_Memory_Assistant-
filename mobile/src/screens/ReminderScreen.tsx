import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Modal,
  TextInput,
  Platform,
  Alert,
  ScrollView,
  Switch,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import DateTimePicker from '@react-native-community/datetimepicker';

import AccessibleButton from '../components/AccessibleButton';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';
import ReminderService, { Reminder, ReminderType, ReminderFrequency } from '../services/ReminderService';

const typeLabels: Record<ReminderType, string> = {
  medication: 'دواء',
  activity: 'نشاط',
  appointment: 'موعد',
  other: 'أخرى',
};

const frequencyLabels: Record<ReminderFrequency, string> = {
  once: 'مرة واحدة',
  daily: 'يومي',
  weekly: 'أسبوعي',
  monthly: 'شهري',
  custom: 'مخصص',
};

const ReminderScreen: React.FC = () => {
  const navigation = useNavigation();
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingReminder, setEditingReminder] = useState<Reminder | null>(null);
  const [form, setForm] = useState({
    title: '',
    description: '',
    type: ReminderType.MEDICATION,
    time: '08:00',
    frequency: ReminderFrequency.DAILY,
    isActive: true,
  });
  const [showTimePicker, setShowTimePicker] = useState(false);

  useEffect(() => {
    loadReminders();
    ReminderService.initialize();
  }, []);

  const loadReminders = async () => {
    setLoading(true);
    const data = await ReminderService.getReminders();
    setReminders(data);
    setLoading(false);
  };

  const resetForm = () => {
    setForm({
      title: '',
      description: '',
      type: ReminderType.MEDICATION,
      time: '08:00',
      frequency: ReminderFrequency.DAILY,
      isActive: true,
    });
    setEditingReminder(null);
  };

  const openAddModal = () => {
    resetForm();
    setModalVisible(true);
    Speech.speak('إضافة تذكير جديد', { language: 'ar' });
  };

  const openEditModal = (reminder: Reminder) => {
    setForm({
      title: reminder.title,
      description: reminder.description || '',
      type: reminder.type,
      time: reminder.time,
      frequency: reminder.frequency,
      isActive: reminder.isActive,
    });
    setEditingReminder(reminder);
    setModalVisible(true);
    Speech.speak('تعديل التذكير', { language: 'ar' });
  };

  const handleSave = async () => {
    if (!form.title.trim()) {
      Alert.alert('خطأ', 'يرجى إدخال عنوان التذكير');
      return;
    }
    try {
      if (editingReminder) {
        await ReminderService.updateReminder({
          ...editingReminder,
          ...form,
        });
      } else {
        await ReminderService.addReminder({
          ...form,
        } as any);
      }
      setModalVisible(false);
      loadReminders();
      Speech.speak('تم حفظ التذكير', { language: 'ar' });
    } catch (error) {
      Alert.alert('خطأ', 'حدث خطأ أثناء حفظ التذكير');
    }
  };

  const handleDelete = async (reminder: Reminder) => {
    Alert.alert('حذف التذكير', 'هل أنت متأكد من حذف هذا التذكير؟', [
      { text: 'إلغاء', style: 'cancel' },
      {
        text: 'حذف',
        style: 'destructive',
        onPress: async () => {
          await ReminderService.deleteReminder(reminder.id);
          loadReminders();
          Speech.speak('تم حذف التذكير', { language: 'ar' });
        },
      },
    ]);
  };

  const handleToggleActive = async (reminder: Reminder) => {
    await ReminderService.toggleReminderActive(reminder.id);
    loadReminders();
  };

  const handleTimeChange = (event: any, selectedDate?: Date) => {
    setShowTimePicker(false);
    if (selectedDate) {
      const hours = selectedDate.getHours().toString().padStart(2, '0');
      const minutes = selectedDate.getMinutes().toString().padStart(2, '0');
      setForm({ ...form, time: `${hours}:${minutes}` });
    }
  };

  const renderReminder = ({ item }: { item: Reminder }) => (
    <View style={styles.reminderCard}>
      <View style={styles.reminderInfo}>
        <Text style={styles.reminderTitle}>{item.title}</Text>
        <Text style={styles.reminderDesc}>{item.description}</Text>
        <Text style={styles.reminderMeta}>
          {typeLabels[item.type]} | {frequencyLabels[item.frequency]} | {item.time}
        </Text>
      </View>
      <View style={styles.reminderActions}>
        <Switch
          value={item.isActive}
          onValueChange={() => handleToggleActive(item)}
          accessibilityLabel={item.isActive ? 'تعطيل التذكير' : 'تفعيل التذكير'}
        />
        <TouchableOpacity onPress={() => openEditModal(item)} style={styles.actionBtn}>
          <Ionicons name="create" size={22} color={colors.primary} />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => handleDelete(item)} style={styles.actionBtn}>
          <Ionicons name="trash" size={22} color={colors.error} />
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton} accessibilityLabel="العودة للصفحة الرئيسية" accessibilityRole="button">
            <Ionicons name="arrow-back" size={28} color={colors.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>التذكيرات</Text>
          <View style={styles.headerRight} />
        </View>
        {/* List */}
        <FlatList
          data={reminders}
          keyExtractor={item => item.id}
          renderItem={renderReminder}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={!loading && <Text style={styles.emptyText}>لا توجد تذكيرات بعد</Text>}
          refreshing={loading}
          onRefresh={loadReminders}
        />
        {/* Add Button */}
        <AccessibleButton
          text="إضافة تذكير جديد"
          icon={<Ionicons name="add-circle" size={28} color={colors.background} />}
          onPress={openAddModal}
          variant="primary"
          size="large"
          fullWidth
          style={styles.addButton}
        />
        {/* Modal */}
        <Modal visible={modalVisible} animationType="slide" transparent>
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <ScrollView contentContainerStyle={styles.modalScroll}>
                <Text style={styles.modalTitle}>{editingReminder ? 'تعديل التذكير' : 'إضافة تذكير جديد'}</Text>
                <TextInput
                  style={styles.input}
                  placeholder="عنوان التذكير"
                  value={form.title}
                  onChangeText={text => setForm({ ...form, title: text })}
                  accessibilityLabel="عنوان التذكير"
                />
                <TextInput
                  style={styles.input}
                  placeholder="وصف (اختياري)"
                  value={form.description}
                  onChangeText={text => setForm({ ...form, description: text })}
                  accessibilityLabel="وصف التذكير"
                />
                <View style={styles.row}>
                  <Text style={styles.label}>النوع:</Text>
                  <TouchableOpacity onPress={() => setForm({ ...form, type: ReminderType.MEDICATION })} style={[styles.typeBtn, form.type === ReminderType.MEDICATION && styles.typeBtnActive]}><Text style={styles.typeBtnText}>دواء</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, type: ReminderType.ACTIVITY })} style={[styles.typeBtn, form.type === ReminderType.ACTIVITY && styles.typeBtnActive]}><Text style={styles.typeBtnText}>نشاط</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, type: ReminderType.APPOINTMENT })} style={[styles.typeBtn, form.type === ReminderType.APPOINTMENT && styles.typeBtnActive]}><Text style={styles.typeBtnText}>موعد</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, type: ReminderType.OTHER })} style={[styles.typeBtn, form.type === ReminderType.OTHER && styles.typeBtnActive]}><Text style={styles.typeBtnText}>أخرى</Text></TouchableOpacity>
                </View>
                <View style={styles.row}>
                  <Text style={styles.label}>التكرار:</Text>
                  <TouchableOpacity onPress={() => setForm({ ...form, frequency: ReminderFrequency.ONCE })} style={[styles.typeBtn, form.frequency === ReminderFrequency.ONCE && styles.typeBtnActive]}><Text style={styles.typeBtnText}>مرة واحدة</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, frequency: ReminderFrequency.DAILY })} style={[styles.typeBtn, form.frequency === ReminderFrequency.DAILY && styles.typeBtnActive]}><Text style={styles.typeBtnText}>يومي</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, frequency: ReminderFrequency.WEEKLY })} style={[styles.typeBtn, form.frequency === ReminderFrequency.WEEKLY && styles.typeBtnActive]}><Text style={styles.typeBtnText}>أسبوعي</Text></TouchableOpacity>
                  <TouchableOpacity onPress={() => setForm({ ...form, frequency: ReminderFrequency.MONTHLY })} style={[styles.typeBtn, form.frequency === ReminderFrequency.MONTHLY && styles.typeBtnActive]}><Text style={styles.typeBtnText}>شهري</Text></TouchableOpacity>
                </View>
                <View style={styles.row}>
                  <Text style={styles.label}>الوقت:</Text>
                  <TouchableOpacity onPress={() => setShowTimePicker(true)} style={styles.timeBtn}>
                    <Ionicons name="time" size={20} color={colors.primary} />
                    <Text style={styles.timeBtnText}>{form.time}</Text>
                  </TouchableOpacity>
                </View>
                <View style={styles.row}>
                  <Text style={styles.label}>مفعل:</Text>
                  <Switch value={form.isActive} onValueChange={v => setForm({ ...form, isActive: v })} />
                </View>
                <View style={styles.modalActions}>
                  <AccessibleButton text="حفظ" onPress={handleSave} variant="primary" size="large" style={styles.modalActionBtn} />
                  <AccessibleButton text="إلغاء" onPress={() => setModalVisible(false)} variant="outline" size="large" style={styles.modalActionBtn} />
                </View>
                {showTimePicker && (
                  <DateTimePicker
                    value={new Date(0, 0, 0, parseInt(form.time.split(':')[0]), parseInt(form.time.split(':')[1]))}
                    mode="time"
                    is24Hour
                    display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                    onChange={handleTimeChange}
                  />
                )}
              </ScrollView>
            </View>
          </View>
        </Modal>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  container: { flex: 1 },
  header: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    paddingHorizontal: spacing.md, paddingVertical: spacing.md,
    borderBottomWidth: 1, borderBottomColor: colors.border, backgroundColor: colors.background, ...shadows.small,
  },
  backButton: { padding: spacing.sm },
  headerTitle: { fontFamily: typography.fontFamily.bold, fontSize: typography.fontSize.lg, color: colors.text, textAlign: 'center' },
  headerRight: { width: 44 },
  listContent: { padding: spacing.md },
  emptyText: { textAlign: 'center', color: colors.textSecondary, fontFamily: typography.fontFamily.medium, fontSize: typography.fontSize.md, marginTop: spacing.xl },
  addButton: { margin: spacing.md },
  reminderCard: { backgroundColor: colors.surface, borderRadius: borderRadius.lg, padding: spacing.md, marginBottom: spacing.md, flexDirection: 'row', alignItems: 'center', ...shadows.small },
  reminderInfo: { flex: 1 },
  reminderTitle: { fontFamily: typography.fontFamily.bold, fontSize: typography.fontSize.lg, color: colors.primary },
  reminderDesc: { fontFamily: typography.fontFamily.regular, fontSize: typography.fontSize.md, color: colors.text, marginVertical: spacing.xs },
  reminderMeta: { fontFamily: typography.fontFamily.medium, fontSize: typography.fontSize.sm, color: colors.textSecondary },
  reminderActions: { flexDirection: 'row', alignItems: 'center', marginLeft: spacing.md },
  actionBtn: { marginLeft: spacing.sm },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { backgroundColor: colors.background, borderRadius: borderRadius.lg, width: '90%', maxHeight: '90%', padding: spacing.lg, ...shadows.large },
  modalScroll: { paddingBottom: spacing.xl },
  modalTitle: { fontFamily: typography.fontFamily.bold, fontSize: typography.fontSize.xl, color: colors.primary, textAlign: 'center', marginBottom: spacing.lg },
  input: { backgroundColor: colors.surface, borderRadius: borderRadius.md, padding: spacing.md, fontFamily: typography.fontFamily.regular, fontSize: typography.fontSize.md, color: colors.text, marginBottom: spacing.md },
  row: { flexDirection: 'row', alignItems: 'center', marginBottom: spacing.md, flexWrap: 'wrap' },
  label: { fontFamily: typography.fontFamily.medium, fontSize: typography.fontSize.md, color: colors.text, marginRight: spacing.sm },
  typeBtn: { backgroundColor: colors.surface, borderRadius: borderRadius.md, paddingVertical: spacing.xs, paddingHorizontal: spacing.md, marginRight: spacing.sm, marginBottom: spacing.xs },
  typeBtnActive: { backgroundColor: colors.primaryLight },
  typeBtnText: { fontFamily: typography.fontFamily.medium, fontSize: typography.fontSize.sm, color: colors.text },
  timeBtn: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface, borderRadius: borderRadius.md, paddingVertical: spacing.xs, paddingHorizontal: spacing.md, marginLeft: spacing.sm },
  timeBtnText: { fontFamily: typography.fontFamily.medium, fontSize: typography.fontSize.md, color: colors.primary, marginLeft: spacing.xs },
  modalActions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: spacing.lg },
  modalActionBtn: { flex: 1, marginHorizontal: spacing.sm },
});

export default ReminderScreen; 