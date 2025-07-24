import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  Image, 
  TouchableOpacity, 
  ScrollView,
  ActivityIndicator,
  Alert
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import * as Speech from 'expo-speech';

import AccessibleButton from '../components/AccessibleButton';
import { colors, typography, spacing, borderRadius, shadows } from '../theme';
import GemmaService, { PhotoAnalysisResult } from '../services/GemmaService';

/**
 * PhotoAnalysisScreen - Screen for analyzing photos to stimulate memories
 * Features:
 * - Photo selection from gallery or camera
 * - AI-powered photo analysis
 * - Person recognition
 * - Memory prompts based on photo content
 * - Voice guidance
 */
const PhotoAnalysisScreen: React.FC = () => {
  const navigation = useNavigation();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<PhotoAnalysisResult | null>(null);
  
  // Request camera and photo library permissions
  const requestPermissions = async () => {
    const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
    const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (cameraStatus !== 'granted' || libraryStatus !== 'granted') {
      Alert.alert(
        'الأذونات مطلوبة',
        'نحتاج إلى إذن للوصول إلى الكاميرا ومكتبة الصور.',
        [{ text: 'حسناً' }]
      );
      return false;
    }
    
    return true;
  };
  
  // Take a photo with the camera
  const takePhoto = async () => {
    const hasPermissions = await requestPermissions();
    if (!hasPermissions) return;
    
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });
      
      if (!result.canceled && result.assets && result.assets.length > 0) {
        setSelectedImage(result.assets[0].uri);
        setAnalysisResult(null);
      }
    } catch (error) {
      console.error('Error taking photo:', error);
      Alert.alert('خطأ', 'حدث خطأ أثناء التقاط الصورة. يرجى المحاولة مرة أخرى.');
    }
  };
  
  // Select a photo from the gallery
  const selectPhoto = async () => {
    const hasPermissions = await requestPermissions();
    if (!hasPermissions) return;
    
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });
      
      if (!result.canceled && result.assets && result.assets.length > 0) {
        setSelectedImage(result.assets[0].uri);
        setAnalysisResult(null);
      }
    } catch (error) {
      console.error('Error selecting photo:', error);
      Alert.alert('خطأ', 'حدث خطأ أثناء اختيار الصورة. يرجى المحاولة مرة أخرى.');
    }
  };
  
  // Analyze the selected photo
  const analyzePhoto = async () => {
    if (!selectedImage) return;
    
    setIsAnalyzing(true);
    
    try {
      const result = await GemmaService.analyzePhoto(selectedImage);
      setAnalysisResult(result);
      
      // Speak the memory prompt
      Speech.speak(result.memoryPrompt, { language: 'ar' });
    } catch (error) {
      console.error('Error analyzing photo:', error);
      Alert.alert('خطأ', 'حدث خطأ أثناء تحليل الصورة. يرجى المحاولة مرة أخرى.');
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  // Reset the analysis and select a new photo
  const handleReset = () => {
    setSelectedImage(null);
    setAnalysisResult(null);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            onPress={() => navigation.goBack()}
            style={styles.backButton}
            accessibilityLabel="العودة للصفحة الرئيسية"
            accessibilityRole="button"
          >
            <Ionicons name="arrow-back" size={28} color={colors.primary} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>تحليل الصور</Text>
          <View style={styles.headerRight} />
        </View>
        
        <ScrollView 
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {!selectedImage ? (
            // Photo Selection View
            <View style={styles.photoSelectionContainer}>
              <Text style={styles.instructionText}>
                اختر صورة لتحليلها ومساعدتك على تذكر الأشخاص والأماكن
              </Text>
              
              <View style={styles.photoOptionsContainer}>
                <AccessibleButton
                  text="التقاط صورة"
                  icon={<Ionicons name="camera" size={24} color={colors.background} />}
                  onPress={takePhoto}
                  variant="primary"
                  size="large"
                  style={styles.photoButton}
                />
                
                <AccessibleButton
                  text="اختيار من المعرض"
                  icon={<Ionicons name="images" size={24} color={colors.background} />}
                  onPress={selectPhoto}
                  variant="secondary"
                  size="large"
                  style={styles.photoButton}
                />
              </View>
              
              <View style={styles.photoTipsContainer}>
                <Text style={styles.tipsTitle}>نصائح للصور:</Text>
                <Text style={styles.tipText}>• اختر صوراً واضحة للوجوه والأماكن</Text>
                <Text style={styles.tipText}>• يفضل اختيار صور ذات ذكريات مهمة</Text>
                <Text style={styles.tipText}>• صور العائلة والأصدقاء مفيدة للذاكرة</Text>
              </View>
            </View>
          ) : (
            // Photo Analysis View
            <View style={styles.analysisContainer}>
              {/* Selected Photo */}
              <View style={styles.selectedPhotoContainer}>
                <Image 
                  source={{ uri: selectedImage }} 
                  style={styles.selectedPhoto}
                  accessibilityLabel="الصورة المختارة للتحليل"
                />
              </View>
              
              {isAnalyzing ? (
                // Loading Indicator
                <View style={styles.loadingContainer}>
                  <ActivityIndicator size="large" color={colors.primary} />
                  <Text style={styles.loadingText}>جاري تحليل الصورة...</Text>
                </View>
              ) : analysisResult ? (
                // Analysis Results
                <View style={styles.resultsContainer}>
                  <Text style={styles.resultTitle}>تحليل الصورة:</Text>
                  
                  <Text style={styles.resultDescription}>
                    {analysisResult.description}
                  </Text>
                  
                  {analysisResult.people.length > 0 && (
                    <View style={styles.resultSection}>
                      <Text style={styles.resultSectionTitle}>الأشخاص:</Text>
                      <View style={styles.tagsContainer}>
                        {analysisResult.people.map((person, index) => (
                          <View key={`person-${index}`} style={styles.tag}>
                            <Text style={styles.tagText}>{person}</Text>
                          </View>
                        ))}
                      </View>
                    </View>
                  )}
                  
                  {analysisResult.places.length > 0 && (
                    <View style={styles.resultSection}>
                      <Text style={styles.resultSectionTitle}>الأماكن:</Text>
                      <View style={styles.tagsContainer}>
                        {analysisResult.places.map((place, index) => (
                          <View key={`place-${index}`} style={[styles.tag, styles.placeTag]}>
                            <Text style={styles.tagText}>{place}</Text>
                          </View>
                        ))}
                      </View>
                    </View>
                  )}
                  
                  {analysisResult.objects.length > 0 && (
                    <View style={styles.resultSection}>
                      <Text style={styles.resultSectionTitle}>الأشياء:</Text>
                      <View style={styles.tagsContainer}>
                        {analysisResult.objects.map((object, index) => (
                          <View key={`object-${index}`} style={[styles.tag, styles.objectTag]}>
                            <Text style={styles.tagText}>{object}</Text>
                          </View>
                        ))}
                      </View>
                    </View>
                  )}
                  
                  <View style={styles.memoryPromptContainer}>
                    <Text style={styles.memoryPromptTitle}>سؤال للذاكرة:</Text>
                    <Text style={styles.memoryPromptText}>
                      {analysisResult.memoryPrompt}
                    </Text>
                  </View>
                  
                  <View style={styles.actionsContainer}>
                    <AccessibleButton
                      text="صورة جديدة"
                      icon={<Ionicons name="refresh" size={24} color={colors.background} />}
                      onPress={handleReset}
                      variant="primary"
                      size="medium"
                      style={styles.actionButton}
                    />
                    
                    <AccessibleButton
                      text="قراءة السؤال"
                      icon={<Ionicons name="volume-high" size={24} color={colors.background} />}
                      onPress={() => Speech.speak(analysisResult.memoryPrompt, { language: 'ar' })}
                      variant="secondary"
                      size="medium"
                      style={styles.actionButton}
                    />
                  </View>
                </View>
              ) : (
                // Analyze Button
                <View style={styles.analyzeButtonContainer}>
                  <AccessibleButton
                    text="تحليل الصورة"
                    icon={<Ionicons name="search" size={24} color={colors.background} />}
                    onPress={analyzePhoto}
                    variant="primary"
                    size="large"
                    fullWidth
                  />
                  
                  <AccessibleButton
                    text="اختيار صورة أخرى"
                    icon={<Ionicons name="images" size={24} color={colors.primary} />}
                    onPress={handleReset}
                    variant="outline"
                    size="medium"
                    style={styles.cancelButton}
                  />
                </View>
              )}
            </View>
          )}
        </ScrollView>
      </View>
    </SafeAreaView>
  );
};

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
  photoSelectionContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xl,
  },
  instructionText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.lg,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.xl,
    paddingHorizontal: spacing.md,
  },
  photoOptionsContainer: {
    width: '100%',
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  photoButton: {
    marginBottom: spacing.md,
    width: '80%',
  },
  photoTipsContainer: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    width: '90%',
    ...shadows.small,
  },
  tipsTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginBottom: spacing.sm,
  },
  tipText: {
    fontFamily: typography.fontFamily.regular,
    fontSize: typography.fontSize.md,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  analysisContainer: {
    flex: 1,
  },
  selectedPhotoContainer: {
    width: '100%',
    aspectRatio: 4/3,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    marginBottom: spacing.md,
    ...shadows.medium,
  },
  selectedPhoto: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  loadingText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginTop: spacing.md,
  },
  analyzeButtonContainer: {
    alignItems: 'center',
    marginTop: spacing.lg,
  },
  cancelButton: {
    marginTop: spacing.md,
  },
  resultsContainer: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    ...shadows.medium,
  },
  resultTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.lg,
    color: colors.text,
    marginBottom: spacing.md,
  },
  resultDescription: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.md,
    color: colors.text,
    marginBottom: spacing.lg,
    textAlign: 'right',
  },
  resultSection: {
    marginBottom: spacing.md,
  },
  resultSectionTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.md,
    color: colors.textSecondary,
    marginBottom: spacing.sm,
  },
  tagsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  tag: {
    backgroundColor: colors.primaryLight,
    borderRadius: borderRadius.round,
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
    margin: spacing.xs,
  },
  placeTag: {
    backgroundColor: colors.secondaryLight,
  },
  objectTag: {
    backgroundColor: colors.accentLight,
  },
  tagText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.sm,
    color: colors.text,
  },
  memoryPromptContainer: {
    backgroundColor: colors.primaryLight,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginTop: spacing.md,
    marginBottom: spacing.lg,
  },
  memoryPromptTitle: {
    fontFamily: typography.fontFamily.bold,
    fontSize: typography.fontSize.md,
    color: colors.primary,
    marginBottom: spacing.sm,
  },
  memoryPromptText: {
    fontFamily: typography.fontFamily.medium,
    fontSize: typography.fontSize.lg,
    color: colors.text,
    textAlign: 'right',
  },
  actionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: spacing.md,
  },
  actionButton: {
    minWidth: 140,
  },
});

export default PhotoAnalysisScreen; 