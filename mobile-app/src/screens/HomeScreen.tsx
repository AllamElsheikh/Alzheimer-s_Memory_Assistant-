import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, Avatar, Title, Paragraph } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';

import { GemmaService } from '../services/GemmaService';
import { PatientService } from '../services/PatientService';
import { theme } from '../theme/theme';

const { width } = Dimensions.get('window');

interface HomeScreenProps {
  navigation: any;
}

export default function HomeScreen({ navigation }: HomeScreenProps) {
  const [greeting, setGreeting] = useState('');
  const [patientName, setPatientName] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeHome();
  }, []);

  const initializeHome = async () => {
    try {
      // Get patient info
      const patient = await PatientService.getCurrentPatient();
      if (patient) {
        setPatientName(patient.name);
      }

      // Generate personalized greeting
      const gemmaService = new GemmaService();
      const currentHour = new Date().getHours();
      let timeGreeting = '';
      
      if (currentHour < 12) {
        timeGreeting = 'صباح الخير';
      } else if (currentHour < 17) {
        timeGreeting = 'مساء الخير';
      } else {
        timeGreeting = 'مساء النور';
      }

      const greetingText = await gemmaService.generateGreeting(patient?.name || '', timeGreeting);
      setGreeting(greetingText);

      // Speak greeting
      Speech.speak(greetingText, {
        language: 'ar',
        rate: 0.8,
        pitch: 1.0,
      });

    } catch (error) {
      console.error('Error initializing home:', error);
      setGreeting('أهلاً وسهلاً! كيف حالك اليوم؟');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'conversation':
        navigation.navigate('Conversation');
        break;
      case 'photos':
        navigation.navigate('Photos');
        break;
      case 'reminders':
        navigation.navigate('Reminders');
        break;
      case 'assessment':
        navigation.navigate('Assessment');
        break;
      case 'emergency':
        handleEmergency();
        break;
    }
  };

  const handleEmergency = () => {
    Alert.alert(
      'طوارئ',
      'هل تحتاج مساعدة عاجلة؟',
      [
        { text: 'إلغاء', style: 'cancel' },
        { text: 'اتصال بالطوارئ', onPress: () => {/* Call emergency */ }},
        { text: 'اتصال بالعائلة', onPress: () => {/* Call family */ }},
      ]
    );
  };

  const speakText = (text: string) => {
    Speech.speak(text, {
      language: 'ar',
      rate: 0.8,
      pitch: 1.0,
    });
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Animatable.View animation="pulse" iterationCount="infinite">
            <Avatar.Icon size={80} icon="brain" style={{ backgroundColor: theme.colors.primary }} />
          </Animatable.View>
          <Text style={styles.loadingText}>جاري التحميل...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Welcome Card */}
        <Animatable.View animation="fadeInDown" duration={1000}>
          <Card style={styles.welcomeCard}>
            <LinearGradient
              colors={[theme.colors.primary, theme.colors.secondary]}
              style={styles.welcomeGradient}
            >
              <Card.Content>
                <View style={styles.welcomeContent}>
                  <Avatar.Icon 
                    size={60} 
                    icon="account-heart" 
                    style={styles.welcomeAvatar}
                  />
                  <View style={styles.welcomeText}>
                    <Title style={styles.welcomeTitle}>
                      مرحباً {patientName || 'عزيزي'}
                    </Title>
                    <Paragraph style={styles.welcomeSubtitle}>
                      {greeting}
                    </Paragraph>
                  </View>
                  <TouchableOpacity 
                    onPress={() => speakText(greeting)}
                    style={styles.speakButton}
                  >
                    <Ionicons name="volume-high" size={24} color="white" />
                  </TouchableOpacity>
                </View>
              </Card.Content>
            </LinearGradient>
          </Card>
        </Animatable.View>

        {/* Quick Actions */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={300}>
          <Text style={styles.sectionTitle}>الأنشطة الرئيسية</Text>
          <View style={styles.actionsGrid}>
            <TouchableOpacity 
              style={[styles.actionCard, { backgroundColor: '#4CAF50' }]}
              onPress={() => handleQuickAction('conversation')}
            >
              <Ionicons name="chatbubbles" size={40} color="white" />
              <Text style={styles.actionText}>محادثة</Text>
              <Text style={styles.actionSubtext}>تكلم مع فاكر</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.actionCard, { backgroundColor: '#2196F3' }]}
              onPress={() => handleQuickAction('photos')}
            >
              <Ionicons name="camera" size={40} color="white" />
              <Text style={styles.actionText}>الصور</Text>
              <Text style={styles.actionSubtext}>شاهد الذكريات</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.actionCard, { backgroundColor: '#FF9800' }]}
              onPress={() => handleQuickAction('reminders')}
            >
              <Ionicons name="notifications" size={40} color="white" />
              <Text style={styles.actionText}>التذكيرات</Text>
              <Text style={styles.actionSubtext}>المواعيد والأدوية</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.actionCard, { backgroundColor: '#9C27B0' }]}
              onPress={() => handleQuickAction('assessment')}
            >
              <Ionicons name="medical" size={40} color="white" />
              <Text style={styles.actionText}>التقييم</Text>
              <Text style={styles.actionSubtext}>تمارين الذاكرة</Text>
            </TouchableOpacity>
          </View>
        </Animatable.View>

        {/* Emergency Button */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={600}>
          <TouchableOpacity 
            style={styles.emergencyButton}
            onPress={() => handleQuickAction('emergency')}
          >
            <Ionicons name="call" size={30} color="white" />
            <Text style={styles.emergencyText}>طوارئ</Text>
          </TouchableOpacity>
        </Animatable.View>

        {/* Daily Tips */}
        <Animatable.View animation="fadeInUp" duration={1000} delay={900}>
          <Card style={styles.tipsCard}>
            <Card.Content>
              <Title style={styles.tipsTitle}>نصيحة اليوم</Title>
              <Paragraph style={styles.tipsText}>
                تذكر أن تشرب الماء بانتظام وتتناول وجباتك في مواعيدها. 
                النشاط البدني البسيط مثل المشي مفيد جداً للذاكرة.
              </Paragraph>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 20,
    fontSize: 18,
    color: theme.colors.primary,
    fontFamily: 'Cairo-Regular',
  },
  scrollContent: {
    padding: 16,
  },
  welcomeCard: {
    marginBottom: 20,
    elevation: 4,
    borderRadius: 12,
  },
  welcomeGradient: {
    borderRadius: 12,
  },
  welcomeContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  welcomeAvatar: {
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  welcomeText: {
    flex: 1,
    marginLeft: 16,
  },
  welcomeTitle: {
    color: 'white',
    fontSize: 20,
    fontFamily: 'Cairo-Bold',
  },
  welcomeSubtitle: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 14,
    fontFamily: 'Cairo-Regular',
  },
  speakButton: {
    padding: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  actionCard: {
    width: (width - 48) / 2,
    height: 120,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
    elevation: 3,
  },
  actionText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 8,
    fontFamily: 'Cairo-Bold',
  },
  actionSubtext: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: 12,
    textAlign: 'center',
    fontFamily: 'Cairo-Regular',
  },
  emergencyButton: {
    backgroundColor: '#F44336',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
    elevation: 4,
  },
  emergencyText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 12,
    fontFamily: 'Cairo-Bold',
  },
  tipsCard: {
    elevation: 2,
    borderRadius: 12,
  },
  tipsTitle: {
    color: theme.colors.primary,
    fontSize: 16,
    fontFamily: 'Cairo-Bold',
  },
  tipsText: {
    fontSize: 14,
    lineHeight: 22,
    fontFamily: 'Cairo-Regular',
  },
});
