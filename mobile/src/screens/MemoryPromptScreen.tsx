import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  Image, 
  TouchableOpacity, 
  ScrollView,
  ActivityIndicator,
  Dimensions
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import { LinearGradient } from 'expo-linear-gradient';

import AccessibleButton from '../components/AccessibleButton';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';

// Memory prompt categories
const MEMORY_CATEGORIES = [
  {
    id: 'family',
    title: 'العائلة',
    icon: 'people',
    color: colors.family,
  },
  {
    id: 'places',
    title: 'الأماكن',
    icon: 'location',
    color: colors.places,
  },
  {
    id: 'activities',
    title: 'الأنشطة',
    icon: 'bicycle',
    color: colors.activities,
  },
  {
    id: 'cultural',
    title: 'الثقافة',
    icon: 'book',
    color: colors.cultural,
  },
];

// Mock memory prompts
const MEMORY_PROMPTS = {
  family: [
    {
      id: 'f1',
      question: 'من هو الشخص في هذه الصورة؟',
      imagePath: require('../../assets/images/family-placeholder.jpg'),
      hint: 'هذا أحد أفراد عائلتك المقربين',
      correctAnswer: 'ابنك محمد',
    },
    {
      id: 'f2',
      question: 'متى كان آخر عيد ميلاد احتفلت به مع العائلة؟',
      imagePath: require('../../assets/images/birthday-placeholder.jpg'),
      hint: 'كان في الصيف الماضي',
      correctAnswer: 'عيد ميلاد حفيدتك ليلى',
    },
  ],
  places: [
    {
      id: 'p1',
      question: 'هل تتذكر هذا المكان؟ أين هو؟',
      imagePath: require('../../assets/images/place-placeholder.jpg'),
      hint: 'مكان تزوره كثيراً للاسترخاء',
      correctAnswer: 'حديقة الأزهر في القاهرة',
    },
  ],
  activities: [
    {
      id: 'a1',
      question: 'ما هي الهواية التي كنت تمارسها في هذه الصورة؟',
      imagePath: require('../../assets/images/activity-placeholder.jpg'),
      hint: 'نشاط يتعلق بالطبيعة والهواء الطلق',
      correctAnswer: 'البستنة وزراعة الورود',
    },
  ],
  cultural: [
    {
      id: 'c1',
      question: 'ما اسم هذه الأكلة المصرية الشهيرة؟',
      imagePath: require('../../assets/images/food-placeholder.jpg'),
      hint: 'طبق شعبي يؤكل في الإفطار',
      correctAnswer: 'الفول المدمس',
    },
  ],
};

interface MemoryPrompt {
  id: string;
  question: string;
  imagePath: any;
  hint: string;
  correctAnswer: string;
}

/**
 * MemoryPromptScreen - Interactive memory exercises for Alzheimer's patients
 * Features:
 * - Categorized memory prompts
 * - Visual and text-based prompts
 * - Hints and guidance
 * - Voice-enabled interaction
 */
const MemoryPromptScreen: React.FC = () => {
  const navigation = useNavigation();
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [currentPrompt, setCurrentPrompt] = useState<MemoryPrompt | null>(null);
  const [showHint, setShowHint] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Select a random prompt from the selected category
  const selectRandomPrompt = (category: string) => {
    setIsLoading(true);
    setShowHint(false);
    setShowAnswer(false);
    
    // Simulate loading delay
    setTimeout(() => {
      const prompts = MEMORY_PROMPTS[category as keyof typeof MEMORY_PROMPTS];
      const randomPrompt = prompts[Math.floor(Math.random() * prompts.length)];
      setCurrentPrompt(randomPrompt);
      setIsLoading(false);
      
      // Speak the question
      Speech.speak(randomPrompt.question, { language: 'ar' });
    }, 1000);
  };

  // Handle category selection
  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId);
    selectRandomPrompt(categoryId);
  };

  // Show hint
  const handleShowHint = () => {
    setShowHint(true);
    if (currentPrompt) {
      Speech.speak(currentPrompt.hint, { language: 'ar' });
    }
  };

  // Show answer
  const handleShowAnswer = () => {
    setShowAnswer(true);
    if (currentPrompt) {
      Speech.speak(currentPrompt.correctAnswer, { language: 'ar' });
    }
  };

  // Get next prompt
  const handleNextPrompt = () => {
    if (selectedCategory) {
      selectRandomPrompt(selectedCategory);
    }
  };

  // Go back to categories
  const handleBackToCategories = () => {
    setSelectedCategory(null);
    setCurrentPrompt(null);
    setShowHint(false);
    setShowAnswer(false);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            onPress={() => selectedCategory ? handleBackToCategories() : navigation.goBack()}
            style={styles.backButton}
            accessibilityLabel={selectedCategory ? "العودة للفئات" : "العودة للصفحة الرئيسية"}
            accessibilityRole="button"
          >
            <Ionicons name="arrow-back" size={28} color={colors.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>
            {selectedCategory ? MEMORY_CATEGORIES.find(c => c.id === selectedCategory)?.title : "تمارين الذاكرة"}
          </Text>
          <View style={styles.headerRight} />
        </View>

        {/* Content */}
        <ScrollView 
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {!selectedCategory ? (
            // Category Selection
            <View style={styles.categoriesContainer}>
              <Text style={styles.instructionText}>
                اختر فئة للبدء في تمارين الذاكرة
              </Text>
              
              <View style={styles.categoriesGrid}>
                {MEMORY_CATEGORIES.map((category) => (
                  <TouchableOpacity
                    key={category.id}
                    style={styles.categoryCard}
                    onPress={() => handleCategorySelect(category.id)}
                    accessibilityLabel={`فئة ${category.title}`}
                    accessibilityRole="button"
                  >
                    <LinearGradient
                      colors={[category.color, `${category.color}99`]}
                      style={styles.categoryGradient}
                      start={{ x: 0, y: 0 }}
                      end={{ x: 1, y: 1 }}
                    >
                      <Ionicons name={category.icon} size={36} color={colors.background} />
                      <Text style={styles.categoryTitle}>{category.title}</Text>
                    </LinearGradient>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          ) : (
            // Memory Prompt
            <View style={styles.promptContainer}>
              {isLoading ? (
                <View style={styles.loadingContainer}>
                  <ActivityIndicator size="large" color={colors.primary} />
                  <Text style={styles.loadingText}>جاري تحميل السؤال...</Text>
                </View>
              ) : currentPrompt ? (
                <>
                  <View style={styles.promptCard}>
                    <Text style={styles.questionText}>{currentPrompt.question}</Text>
                    
                    <Image
                      source={currentPrompt.imagePath}
                      style={styles.promptImage}
                      accessibilityLabel="صورة للتذكر"
                    />
                    
                    {showHint && (
                      <View style={styles.hintContainer}>
                        <Text style={styles.hintLabel}>تلميح:</Text>
                        <Text style={styles.hintText}>{currentPrompt.hint}</Text>
                      </View>
                    )}
                    
                    {showAnswer && (
                      <View style={styles.answerContainer}>
                        <Text style={styles.answerLabel}>الإجابة:</Text>
                        <Text style={styles.answerText}>{currentPrompt.correctAnswer}</Text>
                      </View>
                    )}
                  </View>
                  
                  <View style={styles.actionsContainer}>
                    {!showHint && (
                      <AccessibleButton
                        text="أعطني تلميح"
                        icon={<Ionicons name="help-circle" size={24} color={colors.background} />}
                        onPress={handleShowHint}
                        variant="secondary"
                        size="medium"
                        style={styles.actionButton}
                      />
                    )}
                    
                    {!showAnswer && (
                      <AccessibleButton
                        text="أظهر الإجابة"
                        icon={<Ionicons name="eye" size={24} color={colors.background} />}
                        onPress={handleShowAnswer}
                        variant="primary"
                        size="medium"
                        style={styles.actionButton}
                      />
                    )}
                    
                    <AccessibleButton
                      text="سؤال آخر"
                      icon={<Ionicons name="refresh" size={24} color={colors.background} />}
                      onPress={handleNextPrompt}
                      variant={showAnswer ? "primary" : "outline"}
                      size="medium"
                      style={styles.actionButton}
                    />
                  </View>
                </>
              ) : null}
            </View>
          )}
        </ScrollView>
      </View>
    </SafeAreaView>
  );
};

const { width } = Dimensions.get('window');
const cardWidth = (width - (spacing.lg * 3)) / 2;

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },
  container: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    backgroundColor: colors.background,
    ...shadows.small,
  },
  backButton: {
    padding: spacing.sm,
  },
  headerTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.lg,
    color: colors.text,
    textAlign: 'center',
  },
  headerRight: {
    width: 44,
  },
  content: {
    flexGrow: 1,
    padding: spacing.md,
  },
  categoriesContainer: {
    flex: 1,
    alignItems: 'center',
  },
  instructionText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.lg,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    width: '100%',
  },
  categoryCard: {
    width: cardWidth,
    height: cardWidth,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.md,
    overflow: 'hidden',
    ...shadows.medium,
  },
  categoryGradient: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.md,
  },
  categoryTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.lg,
    color: colors.background,
    marginTop: spacing.sm,
    textAlign: 'center',
  },
  promptContainer: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xl,
  },
  loadingText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginTop: spacing.md,
  },
  promptCard: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    ...shadows.medium,
  },
  questionText: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.xl,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  promptImage: {
    width: '100%',
    height: 200,
    borderRadius: borderRadius.md,
    marginBottom: spacing.lg,
    resizeMode: 'cover',
  },
  hintContainer: {
    backgroundColor: colors.primaryLight,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  hintLabel: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginBottom: spacing.xs,
  },
  hintText: {
    fontFamily: typography.fontFamily.regular,
    fontSize: typography.fontSize.md,
    color: colors.text,
  },
  answerContainer: {
    backgroundColor: colors.secondaryLight,
    borderRadius: borderRadius.md,
    padding: spacing.md,
  },
  answerLabel: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.md,
    color: colors.secondary,
    marginBottom: spacing.xs,
  },
  answerText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.lg,
    color: colors.text,
  },
  actionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: spacing.lg,
  },
  actionButton: {
    margin: spacing.sm,
    minWidth: 150,
  },
});

export default MemoryPromptScreen; 