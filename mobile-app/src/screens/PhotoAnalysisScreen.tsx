import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, Title, Paragraph } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import * as Speech from 'expo-speech';
import * as Animatable from 'react-native-animatable';

import { GemmaService } from '../services/GemmaService';
import { theme } from '../theme/theme';

const { width } = Dimensions.get('window');

interface PhotoAnalysis {
  id: string;
  imageUri: string;
  analysis: string;
  timestamp: Date;
}

export default function PhotoAnalysisScreen() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<string>('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [recentAnalyses, setRecentAnalyses] = useState<PhotoAnalysis[]>([]);
  const gemmaService = new GemmaService();

  useEffect(() => {
    requestPermissions();
  }, []);

  const requestPermissions = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('تنبيه', 'نحتاج إذن الوصول للصور لتحليل الذكريات');
    }
  };

  const pickImage = async (source: 'camera' | 'library') => {
    try {
      let result;
      
      if (source === 'camera') {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('تنبيه', 'نحتاج إذن الكاميرا لالتقاط الصور');
          return;
        }
        result = await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });
      } else {
        result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });
      }

      if (!result.canceled && result.assets[0]) {
        setSelectedImage(result.assets[0].uri);
        setAnalysis('');
      }
    } catch (error) {
      console.error('Error picking image:', error);
      Alert.alert('خطأ', 'حدث خطأ في اختيار الصورة');
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setIsAnalyzing(true);
    try {
      const analysisResult = await gemmaService.analyzePhoto(
        selectedImage,
        'حلل هذه الصورة وساعدني أتذكر الذكريات والتفاصيل المرتبطة بها. تكلم بطريقة دافئة ومحفزة للذاكرة.'
      );

      setAnalysis(analysisResult);

      // Add to recent analyses
      const newAnalysis: PhotoAnalysis = {
        id: Date.now().toString(),
        imageUri: selectedImage,
        analysis: analysisResult,
        timestamp: new Date(),
      };
      setRecentAnalyses(prev => [newAnalysis, ...prev.slice(0, 4)]);

      // Speak the analysis
      Speech.speak(analysisResult, {
        language: 'ar',
        rate: 0.8,
        pitch: 1.0,
      });

    } catch (error) {
      console.error('Error analyzing image:', error);
      Alert.alert('خطأ', 'حدث خطأ في تحليل الصورة. حاول مرة أخرى.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const speakAnalysis = (text: string) => {
    Speech.speak(text, {
      language: 'ar',
      rate: 0.8,
      pitch: 1.0,
    });
  };

  const clearImage = () => {
    setSelectedImage(null);
    setAnalysis('');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Image Selection */}
        <Animatable.View animation="fadeInDown" duration={1000}>
          <Card style={styles.selectionCard}>
            <Card.Content>
              <Title style={styles.cardTitle}>اختر صورة للتحليل</Title>
              <View style={styles.buttonRow}>
                <Button
                  mode="contained"
                  onPress={() => pickImage('camera')}
                  style={[styles.actionButton, { backgroundColor: '#4CAF50' }]}
                  labelStyle={styles.buttonLabel}
                  icon="camera"
                >
                  التقط صورة
                </Button>
                <Button
                  mode="contained"
                  onPress={() => pickImage('library')}
                  style={[styles.actionButton, { backgroundColor: '#2196F3' }]}
                  labelStyle={styles.buttonLabel}
                  icon="image"
                >
                  اختر من المعرض
                </Button>
              </View>
            </Card.Content>
          </Card>
        </Animatable.View>

        {/* Selected Image */}
        {selectedImage && (
          <Animatable.View animation="fadeInUp" duration={1000}>
            <Card style={styles.imageCard}>
              <Card.Content>
                <Image source={{ uri: selectedImage }} style={styles.selectedImage} />
                <View style={styles.imageActions}>
                  <Button
                    mode="contained"
                    onPress={analyzeImage}
                    loading={isAnalyzing}
                    disabled={isAnalyzing}
                    style={styles.analyzeButton}
                    labelStyle={styles.buttonLabel}
                    icon="brain"
                  >
                    {isAnalyzing ? 'جاري التحليل...' : 'حلل الصورة'}
                  </Button>
                  <TouchableOpacity onPress={clearImage} style={styles.clearImageButton}>
                    <Ionicons name="close-circle" size={32} color="#F44336" />
                  </TouchableOpacity>
                </View>
              </Card.Content>
            </Card>
          </Animatable.View>
        )}

        {/* Analysis Result */}
        {analysis && (
          <Animatable.View animation="fadeInUp" duration={1000} delay={300}>
            <Card style={styles.analysisCard}>
              <Card.Content>
                <View style={styles.analysisHeader}>
                  <Title style={styles.analysisTitle}>تحليل الصورة</Title>
                  <TouchableOpacity 
                    onPress={() => speakAnalysis(analysis)}
                    style={styles.speakButton}
                  >
                    <Ionicons name="volume-high" size={24} color={theme.colors.primary} />
                  </TouchableOpacity>
                </View>
                <Paragraph style={styles.analysisText}>{analysis}</Paragraph>
              </Card.Content>
            </Card>
          </Animatable.View>
        )}

        {/* Recent Analyses */}
        {recentAnalyses.length > 0 && (
          <Animatable.View animation="fadeInUp" duration={1000} delay={600}>
            <Text style={styles.sectionTitle}>التحليلات الأخيرة</Text>
            {recentAnalyses.map((item, index) => (
              <Card key={item.id} style={styles.recentCard}>
                <Card.Content>
                  <View style={styles.recentItem}>
                    <Image source={{ uri: item.imageUri }} style={styles.recentImage} />
                    <View style={styles.recentContent}>
                      <Text style={styles.recentTime}>
                        {item.timestamp.toLocaleDateString('ar-EG')} - {item.timestamp.toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })}
                      </Text>
                      <Text style={styles.recentAnalysis} numberOfLines={3}>
                        {item.analysis}
                      </Text>
                      <TouchableOpacity 
                        onPress={() => speakAnalysis(item.analysis)}
                        style={styles.recentSpeakButton}
                      >
                        <Ionicons name="play-circle" size={20} color={theme.colors.primary} />
                        <Text style={styles.recentSpeakText}>استمع</Text>
                      </TouchableOpacity>
                    </View>
                  </View>
                </Card.Content>
              </Card>
            ))}
          </Animatable.View>
        )}

        {/* Tips */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={900}>
          <Card style={styles.tipsCard}>
            <Card.Content>
              <Title style={styles.tipsTitle}>نصائح لتحليل أفضل</Title>
              <View style={styles.tipsList}>
                <View style={styles.tipItem}>
                  <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                  <Text style={styles.tipText}>استخدم صور واضحة وجيدة الإضاءة</Text>
                </View>
                <View style={styles.tipItem}>
                  <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                  <Text style={styles.tipText}>الصور العائلية والذكريات الشخصية أفضل</Text>
                </View>
                <View style={styles.tipItem}>
                  <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                  <Text style={styles.tipText}>يمكن تحليل صور الأماكن والأحداث المهمة</Text>
                </View>
              </View>
            </Card.Content>
          </Card>
        </Animatable.View>
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
  selectionCard: {
    marginBottom: 16,
    elevation: 4,
    borderRadius: 12,
  },
  cardTitle: {
    textAlign: 'center',
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginBottom: 16,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 8,
  },
  buttonLabel: {
    fontFamily: 'Cairo-Bold',
    fontSize: 14,
  },
  imageCard: {
    marginBottom: 16,
    elevation: 4,
    borderRadius: 12,
  },
  selectedImage: {
    width: '100%',
    height: 250,
    borderRadius: 8,
    marginBottom: 16,
  },
  imageActions: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  analyzeButton: {
    flex: 1,
    marginRight: 16,
    backgroundColor: theme.colors.primary,
  },
  clearImageButton: {
    padding: 4,
  },
  analysisCard: {
    marginBottom: 16,
    elevation: 4,
    borderRadius: 12,
  },
  analysisHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  analysisTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  speakButton: {
    padding: 8,
  },
  analysisText: {
    fontSize: 16,
    lineHeight: 24,
    fontFamily: 'Cairo-Regular',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  recentCard: {
    marginBottom: 12,
    elevation: 2,
    borderRadius: 8,
  },
  recentItem: {
    flexDirection: 'row',
  },
  recentImage: {
    width: 80,
    height: 80,
    borderRadius: 8,
    marginRight: 12,
  },
  recentContent: {
    flex: 1,
  },
  recentTime: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
    fontFamily: 'Cairo-Regular',
  },
  recentAnalysis: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 8,
    fontFamily: 'Cairo-Regular',
  },
  recentSpeakButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  recentSpeakText: {
    marginLeft: 4,
    color: theme.colors.primary,
    fontSize: 12,
    fontFamily: 'Cairo-Regular',
  },
  tipsCard: {
    elevation: 2,
    borderRadius: 12,
    marginTop: 8,
  },
  tipsTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginBottom: 12,
  },
  tipsList: {
    gap: 8,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  tipText: {
    marginLeft: 8,
    fontSize: 14,
    fontFamily: 'Cairo-Regular',
  },
});
