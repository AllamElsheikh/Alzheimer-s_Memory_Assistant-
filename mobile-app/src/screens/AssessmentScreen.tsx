import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Card, Button, Title, Paragraph, ProgressBar } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import * as Speech from 'expo-speech';
import * as Animatable from 'react-native-animatable';

import { GemmaService } from '../services/GemmaService';
import { theme } from '../theme/theme';

interface AssessmentTask {
  id: string;
  type: string;
  question: string;
  expectedResponse?: string;
  userResponse?: string;
  score?: number;
  completed: boolean;
}

interface AssessmentResult {
  scores: { [key: string]: number };
  severity_level: string;
  recommendations: string[];
}

export default function AssessmentScreen() {
  const [currentTask, setCurrentTask] = useState<AssessmentTask | null>(null);
  const [tasks, setTasks] = useState<AssessmentTask[]>([]);
  const [taskIndex, setTaskIndex] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState<AssessmentResult | null>(null);
  const [assessmentStarted, setAssessmentStarted] = useState(false);
  const gemmaService = new GemmaService();

  useEffect(() => {
    if (assessmentStarted && tasks.length > 0) {
      setCurrentTask(tasks[taskIndex]);
    }
  }, [taskIndex, tasks, assessmentStarted]);

  const startAssessment = async (type: string) => {
    setIsLoading(true);
    try {
      // Generate assessment tasks
      const assessmentTasks: AssessmentTask[] = [
        {
          id: '1',
          type: 'memory_recall',
          question: 'احفظ هذه الكلمات الثلاث: تفاحة، سيارة، كتاب. سأسألك عنها بعد قليل.',
          completed: false,
        },
        {
          id: '2',
          type: 'orientation',
          question: 'ما هو اليوم والتاريخ اليوم؟',
          completed: false,
        },
        {
          id: '3',
          type: 'attention',
          question: 'اعد من 100 إلى 93 بالعكس (100، 99، 98...)',
          completed: false,
        },
        {
          id: '4',
          type: 'language',
          question: 'اذكر أكبر عدد من أسماء الحيوانات في دقيقة واحدة',
          completed: false,
        },
        {
          id: '5',
          type: 'memory_recall_check',
          question: 'الآن، ما هي الكلمات الثلاث التي طلبت منك حفظها في البداية؟',
          expectedResponse: 'تفاحة، سيارة، كتاب',
          completed: false,
        },
      ];

      setTasks(assessmentTasks);
      setTaskIndex(0);
      setAssessmentStarted(true);
      setAssessmentResult(null);

      // Speak first task
      Speech.speak(assessmentTasks[0].question, { language: 'ar', rate: 0.8 });

    } catch (error) {
      console.error('Error starting assessment:', error);
      Alert.alert('خطأ', 'حدث خطأ في بدء التقييم');
    } finally {
      setIsLoading(false);
    }
  };

  const submitResponse = async () => {
    if (!currentTask || !userInput.trim()) return;

    setIsLoading(true);
    try {
      // Submit response to Gemma for analysis
      const analysis = await gemmaService.submitAssessmentResponse(
        currentTask.type,
        userInput.trim()
      );

      // Update current task
      const updatedTask = {
        ...currentTask,
        userResponse: userInput.trim(),
        score: analysis?.score || 0,
        completed: true,
      };

      // Update tasks array
      const updatedTasks = [...tasks];
      updatedTasks[taskIndex] = updatedTask;
      setTasks(updatedTasks);

      // Move to next task or finish assessment
      if (taskIndex < tasks.length - 1) {
        setTaskIndex(taskIndex + 1);
        setUserInput('');
        
        // Speak next task
        setTimeout(() => {
          Speech.speak(tasks[taskIndex + 1].question, { language: 'ar', rate: 0.8 });
        }, 1000);
      } else {
        // Assessment completed
        await completeAssessment(updatedTasks);
      }

    } catch (error) {
      console.error('Error submitting response:', error);
      Alert.alert('خطأ', 'حدث خطأ في تسجيل الإجابة');
    } finally {
      setIsLoading(false);
    }
  };

  const completeAssessment = async (completedTasks: AssessmentTask[]) => {
    try {
      // Get comprehensive assessment from Gemma
      const result = await gemmaService.getCognitiveAssessment('comprehensive');
      
      if (result) {
        setAssessmentResult(result);
        
        // Speak results summary
        const summary = `تم إكمال التقييم. المستوى العام: ${result.severity_level}`;
        Speech.speak(summary, { language: 'ar', rate: 0.8 });
      }

    } catch (error) {
      console.error('Error completing assessment:', error);
    }
  };

  const resetAssessment = () => {
    setAssessmentStarted(false);
    setTasks([]);
    setTaskIndex(0);
    setCurrentTask(null);
    setUserInput('');
    setAssessmentResult(null);
  };

  const speakText = (text: string) => {
    Speech.speak(text, { language: 'ar', rate: 0.8 });
  };

  const getProgressPercentage = () => {
    if (tasks.length === 0) return 0;
    return (taskIndex / tasks.length) * 100;
  };

  const getSeverityColor = (level: string) => {
    switch (level) {
      case 'normal': return '#4CAF50';
      case 'mild': return '#FF9800';
      case 'moderate': return '#F44336';
      case 'severe': return '#9C27B0';
      default: return '#2196F3';
    }
  };

  const getSeverityText = (level: string) => {
    switch (level) {
      case 'normal': return 'طبيعي';
      case 'mild': return 'خفيف';
      case 'moderate': return 'متوسط';
      case 'severe': return 'شديد';
      default: return 'غير محدد';
    }
  };

  if (!assessmentStarted) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <Animatable.View animation="fadeInDown" duration={1000}>
            <Card style={styles.welcomeCard}>
              <Card.Content style={styles.welcomeContent}>
                <Ionicons name="medical" size={64} color={theme.colors.primary} />
                <Title style={styles.welcomeTitle}>التقييم المعرفي</Title>
                <Paragraph style={styles.welcomeText}>
                  سيساعدك هذا التقييم على متابعة حالتك المعرفية من خلال مجموعة من التمارين البسيطة
                </Paragraph>
              </Card.Content>
            </Card>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" duration={1000} delay={300}>
            <Text style={styles.sectionTitle}>أنواع التقييم</Text>
            
            <TouchableOpacity
              style={[styles.assessmentCard, { backgroundColor: '#4CAF50' }]}
              onPress={() => startAssessment('comprehensive')}
            >
              <Ionicons name="medical" size={40} color="white" />
              <View style={styles.assessmentInfo}>
                <Text style={styles.assessmentTitle}>تقييم شامل</Text>
                <Text style={styles.assessmentDescription}>
                  تقييم كامل للذاكرة والانتباه واللغة (10-15 دقيقة)
                </Text>
              </View>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.assessmentCard, { backgroundColor: '#2196F3' }]}
              onPress={() => startAssessment('memory')}
            >
              <Ionicons name="library" size={40} color="white" />
              <View style={styles.assessmentInfo}>
                <Text style={styles.assessmentTitle}>تقييم الذاكرة</Text>
                <Text style={styles.assessmentDescription}>
                  تركيز على اختبارات الذاكرة قصيرة وطويلة المدى (5-7 دقائق)
                </Text>
              </View>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.assessmentCard, { backgroundColor: '#FF9800' }]}
              onPress={() => startAssessment('attention')}
            >
              <Ionicons name="eye" size={40} color="white" />
              <View style={styles.assessmentInfo}>
                <Text style={styles.assessmentTitle}>تقييم الانتباه</Text>
                <Text style={styles.assessmentDescription}>
                  اختبارات التركيز والانتباه والمعالجة المعرفية (3-5 دقائق)
                </Text>
              </View>
            </TouchableOpacity>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" duration={1000} delay={600}>
            <Card style={styles.tipsCard}>
              <Card.Content>
                <Title style={styles.tipsTitle}>نصائح مهمة</Title>
                <View style={styles.tipsList}>
                  <View style={styles.tipItem}>
                    <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                    <Text style={styles.tipText}>اختر مكان هادئ ومريح</Text>
                  </View>
                  <View style={styles.tipItem}>
                    <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                    <Text style={styles.tipText}>خذ وقتك في الإجابة</Text>
                  </View>
                  <View style={styles.tipItem}>
                    <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                    <Text style={styles.tipText}>لا تقلق من الأخطاء</Text>
                  </View>
                </View>
              </Card.Content>
            </Card>
          </Animatable.View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  if (assessmentResult) {
    return (
      <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <Animatable.View animation="fadeInDown" duration={1000}>
            <Card style={styles.resultCard}>
              <Card.Content>
                <View style={styles.resultHeader}>
                  <Ionicons name="checkmark-circle" size={48} color="#4CAF50" />
                  <Title style={styles.resultTitle}>تم إكمال التقييم</Title>
                </View>

                <View style={styles.severityContainer}>
                  <Text style={styles.severityLabel}>المستوى العام:</Text>
                  <View style={[
                    styles.severityBadge,
                    { backgroundColor: getSeverityColor(assessmentResult.severity_level) }
                  ]}>
                    <Text style={styles.severityText}>
                      {getSeverityText(assessmentResult.severity_level)}
                    </Text>
                  </View>
                </View>

                <View style={styles.scoresContainer}>
                  <Text style={styles.scoresTitle}>النتائج التفصيلية:</Text>
                  {Object.entries(assessmentResult.scores).map(([key, value]) => (
                    <View key={key} style={styles.scoreItem}>
                      <Text style={styles.scoreLabel}>
                        {key === 'memory_short_term' ? 'الذاكرة قصيرة المدى' :
                         key === 'memory_long_term' ? 'الذاكرة طويلة المدى' :
                         key === 'attention' ? 'الانتباه والتركيز' :
                         key === 'language' ? 'المهارات اللغوية' :
                         key === 'orientation' ? 'التوجه الزمني والمكاني' : key}
                      </Text>
                      <View style={styles.scoreBar}>
                        <ProgressBar
                          progress={value / 10}
                          color={value >= 7 ? '#4CAF50' : value >= 5 ? '#FF9800' : '#F44336'}
                          style={styles.progressBar}
                        />
                        <Text style={styles.scoreValue}>{value.toFixed(1)}/10</Text>
                      </View>
                    </View>
                  ))}
                </View>
              </Card.Content>
            </Card>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" duration={1000} delay={300}>
            <Card style={styles.recommendationsCard}>
              <Card.Content>
                <Title style={styles.recommendationsTitle}>التوصيات</Title>
                {assessmentResult.recommendations.map((rec, index) => (
                  <View key={index} style={styles.recommendationItem}>
                    <Ionicons name="bulb" size={16} color="#FF9800" />
                    <Text style={styles.recommendationText}>{rec}</Text>
                  </View>
                ))}
              </Card.Content>
            </Card>
          </Animatable.View>

          <View style={styles.resultActions}>
            <Button
              mode="contained"
              onPress={resetAssessment}
              style={styles.resetButton}
              labelStyle={styles.buttonLabel}
              icon="refresh"
            >
              تقييم جديد
            </Button>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.assessmentContainer}>
        {/* Progress */}
        <View style={styles.progressContainer}>
          <Text style={styles.progressText}>
            السؤال {taskIndex + 1} من {tasks.length}
          </Text>
          <ProgressBar
            progress={getProgressPercentage() / 100}
            color={theme.colors.primary}
            style={styles.progressBar}
          />
        </View>

        {/* Current Task */}
        {currentTask && (
          <Animatable.View animation="fadeIn" duration={500} key={currentTask.id}>
            <Card style={styles.taskCard}>
              <Card.Content>
                <View style={styles.taskHeader}>
                  <Title style={styles.taskTitle}>
                    {currentTask.type === 'memory_recall' ? 'اختبار الذاكرة' :
                     currentTask.type === 'orientation' ? 'التوجه الزمني' :
                     currentTask.type === 'attention' ? 'اختبار الانتباه' :
                     currentTask.type === 'language' ? 'اختبار اللغة' :
                     currentTask.type === 'memory_recall_check' ? 'مراجعة الذاكرة' : 'اختبار'}
                  </Title>
                  <TouchableOpacity
                    onPress={() => speakText(currentTask.question)}
                    style={styles.speakButton}
                  >
                    <Ionicons name="volume-high" size={24} color={theme.colors.primary} />
                  </TouchableOpacity>
                </View>

                <Paragraph style={styles.taskQuestion}>
                  {currentTask.question}
                </Paragraph>

                <TextInput
                  style={styles.responseInput}
                  value={userInput}
                  onChangeText={setUserInput}
                  placeholder="اكتب إجابتك هنا..."
                  placeholderTextColor="#999"
                  multiline
                  textAlign="right"
                />

                <Button
                  mode="contained"
                  onPress={submitResponse}
                  disabled={!userInput.trim() || isLoading}
                  loading={isLoading}
                  style={styles.submitButton}
                  labelStyle={styles.buttonLabel}
                >
                  {taskIndex === tasks.length - 1 ? 'إنهاء التقييم' : 'السؤال التالي'}
                </Button>
              </Card.Content>
            </Card>
          </Animatable.View>
        )}

        {/* Cancel Button */}
        <Button
          mode="outlined"
          onPress={() => {
            Alert.alert(
              'إلغاء التقييم',
              'هل تريد إلغاء التقييم الحالي؟',
              [
                { text: 'متابعة', style: 'cancel' },
                { text: 'إلغاء', onPress: resetAssessment },
              ]
            );
          }}
          style={styles.cancelButton}
          labelStyle={styles.buttonLabel}
        >
          إلغاء التقييم
        </Button>
      </View>
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
  welcomeCard: {
    marginBottom: 20,
    elevation: 4,
    borderRadius: 12,
  },
  welcomeContent: {
    alignItems: 'center',
    padding: 20,
  },
  welcomeTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginTop: 16,
  },
  welcomeText: {
    textAlign: 'center',
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
  assessmentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    elevation: 3,
  },
  assessmentInfo: {
    marginLeft: 16,
    flex: 1,
  },
  assessmentTitle: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    fontFamily: 'Cairo-Bold',
  },
  assessmentDescription: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: 14,
    marginTop: 4,
    fontFamily: 'Cairo-Regular',
  },
  tipsCard: {
    elevation: 2,
    borderRadius: 12,
    marginTop: 16,
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
  assessmentContainer: {
    flex: 1,
    padding: 16,
  },
  progressContainer: {
    marginBottom: 20,
  },
  progressText: {
    textAlign: 'center',
    fontSize: 16,
    marginBottom: 8,
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  taskCard: {
    elevation: 4,
    borderRadius: 12,
    marginBottom: 20,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  taskTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
  },
  speakButton: {
    padding: 8,
  },
  taskQuestion: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 20,
    fontFamily: 'Cairo-Regular',
  },
  responseInput: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    minHeight: 100,
    marginBottom: 20,
    fontFamily: 'Cairo-Regular',
  },
  submitButton: {
    backgroundColor: theme.colors.primary,
  },
  cancelButton: {
    marginTop: 16,
  },
  buttonLabel: {
    fontFamily: 'Cairo-Bold',
    fontSize: 16,
  },
  resultCard: {
    elevation: 4,
    borderRadius: 12,
    marginBottom: 16,
  },
  resultHeader: {
    alignItems: 'center',
    marginBottom: 20,
  },
  resultTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginTop: 8,
  },
  severityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  severityLabel: {
    fontSize: 16,
    marginRight: 12,
    fontFamily: 'Cairo-Regular',
  },
  severityBadge: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  severityText: {
    color: 'white',
    fontWeight: 'bold',
    fontFamily: 'Cairo-Bold',
  },
  scoresContainer: {
    marginBottom: 16,
  },
  scoresTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 12,
    fontFamily: 'Cairo-Bold',
  },
  scoreItem: {
    marginBottom: 12,
  },
  scoreLabel: {
    fontSize: 14,
    marginBottom: 4,
    fontFamily: 'Cairo-Regular',
  },
  scoreBar: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreValue: {
    marginLeft: 12,
    fontSize: 14,
    fontWeight: 'bold',
    minWidth: 40,
    fontFamily: 'Cairo-Bold',
  },
  recommendationsCard: {
    elevation: 2,
    borderRadius: 12,
    marginBottom: 16,
  },
  recommendationsTitle: {
    color: theme.colors.primary,
    fontFamily: 'Cairo-Bold',
    marginBottom: 12,
  },
  recommendationItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  recommendationText: {
    marginLeft: 8,
    fontSize: 14,
    flex: 1,
    fontFamily: 'Cairo-Regular',
  },
  resultActions: {
    alignItems: 'center',
  },
  resetButton: {
    backgroundColor: theme.colors.primary,
    minWidth: 200,
  },
});
