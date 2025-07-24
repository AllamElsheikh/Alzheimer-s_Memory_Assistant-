/**
 * LocalizationService.ts
 * Service to handle Arabic translations and RTL support
 */

import * as Localization from 'expo-localization';
import { I18n } from 'i18n-js';
import { I18nManager } from 'react-native';

// Arabic translations
const translations = {
  ar: {
    // Common
    app_name: 'فاكر؟',
    back: 'رجوع',
    save: 'حفظ',
    cancel: 'إلغاء',
    delete: 'حذف',
    edit: 'تعديل',
    loading: 'جاري التحميل...',
    error: 'خطأ',
    success: 'نجاح',
    
    // Home Screen
    welcome_message: 'أهلاً بك في تطبيق فاكر. كيف يمكنني مساعدتك اليوم؟',
    chat_button: 'دردشة معي',
    memory_button: 'تمارين الذاكرة',
    photo_button: 'تحليل الصور',
    reminder_button: 'التذكيرات',
    footer_text: 'تطبيق فاكر؟ - مساعد ذكي لمرضى الزهايمر',
    
    // Conversation Screen
    conversation_title: 'المحادثة',
    message_input: 'اكتب رسالتك هنا...',
    send_button: 'إرسال',
    record_button: 'تحدث',
    stop_recording: 'إيقاف',
    thinking: 'جاري التفكير...',
    
    // Memory Prompt Screen
    memory_prompt_title: 'تمارين الذاكرة',
    select_category: 'اختر فئة للبدء في تمارين الذاكرة',
    family_category: 'العائلة',
    places_category: 'الأماكن',
    activities_category: 'الأنشطة',
    cultural_category: 'الثقافة',
    loading_prompt: 'جاري تحميل السؤال...',
    hint_button: 'أعطني تلميح',
    hint_label: 'تلميح:',
    show_answer: 'أظهر الإجابة',
    answer_label: 'الإجابة:',
    next_prompt: 'سؤال آخر',
    
    // Photo Analysis Screen
    photo_analysis_title: 'تحليل الصور',
    photo_instruction: 'اختر صورة لتحليلها ومساعدتك على تذكر الأشخاص والأماكن',
    take_photo: 'التقاط صورة',
    choose_gallery: 'اختيار من المعرض',
    photo_tips_title: 'نصائح للصور:',
    photo_tip_1: '• اختر صوراً واضحة للوجوه والأماكن',
    photo_tip_2: '• يفضل اختيار صور ذات ذكريات مهمة',
    photo_tip_3: '• صور العائلة والأصدقاء مفيدة للذاكرة',
    analyzing_photo: 'جاري تحليل الصورة...',
    analyze_button: 'تحليل الصورة',
    choose_another: 'اختيار صورة أخرى',
    analysis_result: 'تحليل الصورة:',
    people_label: 'الأشخاص:',
    places_label: 'الأماكن:',
    objects_label: 'الأشياء:',
    memory_prompt_label: 'سؤال للذاكرة:',
    new_photo: 'صورة جديدة',
    read_question: 'قراءة السؤال',
    
    // Reminder Screen
    reminders_title: 'التذكيرات',
    no_reminders: 'لا توجد تذكيرات بعد',
    add_reminder: 'إضافة تذكير جديد',
    edit_reminder: 'تعديل التذكير',
    reminder_title_placeholder: 'عنوان التذكير',
    reminder_desc_placeholder: 'وصف (اختياري)',
    type_label: 'النوع:',
    medication_type: 'دواء',
    activity_type: 'نشاط',
    appointment_type: 'موعد',
    other_type: 'أخرى',
    frequency_label: 'التكرار:',
    once_frequency: 'مرة واحدة',
    daily_frequency: 'يومي',
    weekly_frequency: 'أسبوعي',
    monthly_frequency: 'شهري',
    custom_frequency: 'مخصص',
    time_label: 'الوقت:',
    active_label: 'مفعل:',
    delete_reminder_title: 'حذف التذكير',
    delete_reminder_message: 'هل أنت متأكد من حذف هذا التذكير؟',
    reminder_saved: 'تم حفظ التذكير',
    reminder_deleted: 'تم حذف التذكير',
    reminder_error: 'حدث خطأ أثناء حفظ التذكير',
    reminder_title_required: 'يرجى إدخال عنوان التذكير',
  },
};

// Create i18n instance
const i18n = new I18n(translations);

/**
 * LocalizationService - Handles translations and RTL support
 */
class LocalizationService {
  constructor() {
    // Set default locale to Arabic
    i18n.locale = 'ar';
    i18n.enableFallback = true;
    
    // Force RTL layout for Arabic
    I18nManager.forceRTL(true);
    I18nManager.allowRTL(true);
  }
  
  /**
   * Get a translated string
   */
  t = (key: string, params?: object): string => {
    return i18n.t(key, params);
  };
  
  /**
   * Check if the current locale is RTL
   */
  isRTL = (): boolean => {
    return I18nManager.isRTL;
  };
  
  /**
   * Get the current locale
   */
  getLocale = (): string => {
    return i18n.locale;
  };
}

export default new LocalizationService(); 